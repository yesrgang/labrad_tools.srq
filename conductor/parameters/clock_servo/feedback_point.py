from conductor.parameter import ConductorParameter
from control_loops import PID, PIID
import json
import os
import time
import subprocess
 
class FeedbackPoint(ConductorParameter):
    """ 
    example_config = {
        'locks': {
            '+9/2': {
                'type': 'PID',
                'prop_gain': 1,
                ...
                },
            '-9/2': {
                'type': 'PID',
                'prop_gain': 1,
                ...
                },
            },
        }
    """
    locks = {}
    #priority = 8
    priority = 18
    autostart = False
    value_type = 'list'

    def initialize(self, config):
        super(FeedbackPoint, self).initialize(config)
        self.connect_to_labrad()
        for name, settings in self.locks.items():
            if settings['type'] == 'PID':
                self.locks[name] = PID(**settings)
            if settings['type'] == 'PIID':
                self.locks[name] = PIID(**settings)

    def _get_lock(self, lock):
        if lock not in self.locks:
            message = 'lock ({}) not defined in {}'.format(lock, self.name)
            raise Exception(message)
        else:
            return self.locks[lock]

    def update(self):
        experiment_name = self.server.experiment.get('name')

        #shot_number = self.server.experiment.get('shot_number')
        #if shot_number >= 3: # kuro files may not be updated prior to shot 3
        #    pic_path = self.get_prev_pic_path()
        #    print(pic_path)
        #    print(self.process_pic(pic_path))
        #print('update feedback point!')
        #print('experiment_name', experiment_name)
        #print('shot_number', shot_number)

        print('update feedback point!')
        print('self.value', self.value)

        if (self.value is not None) and (experiment_name is not None):
            name, side, shot = self.value
            control_loop = self._get_lock(name)

            ##Mod for Sr1 data saving convention
            #point_filename = '{}.blue_pmt'.format(shot)
            #point_path = os.path.join(experiment_name, point_filename)

            #request = {'blue_pmt': point_path}
            #response_json = self.cxn.pmt.retrive_records(json.dumps(request))
            #response = json.loads(response_json)
#           # frac = response['blue_pmt']['frac_sum']
#           # tot = response['blue_pmt']['tot_sum']
            #frac = response['blue_pmt']['frac_fit']
            #tot = response['blue_pmt']['tot_fit']

            shot_number = self.server.experiment.get('shot_number')
            print('update feedback point!')
            print(shot_number)
            if shot_number >= 3: # kuro files may not be updated prior to shot 3
                pic_path = self.get_prev_pic_path()
                print(pic_path)
                frac, ntot = self.process_pic(pic_path)

                print('update feedback point!')
                print('eval results for shot {:d}'.format(shot_number))
                print('EF:   {:.3f}'.format(frac))
                print('Ntot: {:.0f}'.format(ntot))

                if ntot > control_loop.tot_cutoff:
                    control_loop.tick(side, frac)
                request = {'clock_servo.control_signals.{}'.format(name): control_loop.output}
                self.server._set_parameter_values(request)

    def get_prev_pic_path(self):
        kuro_path_file = '/srqdata2/data/kuro-tmp-images/destination.txt'
        with open(kuro_path_file, 'r') as f:
            pic_path = f.read()
            pic_path = pic_path[8:].replace('\\', '/') # convert to linux path relative to /srqdata2/data
        return pic_path

    def process_pic(self, pic_path):
        x0 = 572
        y0 = 707

        script_path = '/home/srgang/labrad_tools.srq/conductor/parameters/clock_servo/process_pic.py'
        try:
            ret = subprocess.check_output(['python3.9', script_path, pic_path, '{:d}'.format(x0), '{:d}'.format(y0)]) # should return <excitation_fraction> <total_atom_number>
        except subprocess.CalledProcessError as e:
            print(e.output)
        vals = ret.split()
        return float(vals[0]), float(vals[1]) # [ef, ntot]

Parameter = FeedbackPoint
