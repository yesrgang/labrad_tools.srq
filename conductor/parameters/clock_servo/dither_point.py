from conductor.parameter import ConductorParameter
import json
from collections import deque

class Ditherer(object):
    def __init__(self, **kw):
        self.side = None
        for key, value in kw.items():
            setattr(self, key, value)
 
    @property
    def output(self):
        if self.side == 'left':
            return -self.modulation_depth 
        elif self.side == 'right':
            return self.modulation_depth 


class DitherPoint(ConductorParameter):
    """ 
    example_config = {
        'locks': {
            '+9/2': {
                'modulation_depth': 1,
                'control_parameters': ['clock_aom'],
                },
            '-9/2': {
                'modulation_depth': 1,
                'control_parameters': ['clock_aom'],
                },
            },
        }
    """
    locks = {}
    priority = 7
    autostart = True
    value_type = 'list'
    value_log = deque([None, None, None], maxlen=3)
    shot_number_log = deque([None, None, None], maxlen=3)


    def initialize(self, config):
        super(DitherPoint, self).initialize(config)
        for name, settings in self.locks.items():
            self.locks[name] = Ditherer(**settings)

    def _get_lock(self, lock):
        if lock not in self.locks:
            message = 'lock ({}) not defined in {}'.format(lock, self.name)
            raise Exception(message)
        else:
            return self.locks[lock]

    def update(self):
        if self.value is not None:
            name, side = self.value
            
            ditherer = self._get_lock(name)
            ditherer.side = side
            request = {'clock_servo.dithers.{}'.format(name): ditherer.output}
            self.server._set_parameter_values(request)
            
            control_loop = self.server._get_parameter('clock_servo.feedback_point')._get_lock(name)
            output = control_loop.output + ditherer.output
            request = {
                'si21.probe_detuning': control_loop.output + ditherer.output,
                'si21.cleanup_detuning': control_loop.output,
                }
            self.server._set_parameter_values(request)
        
#        if self.server._get_parameter_value('blue_pmt.recorder'):
#            lock, side = self.value
#            print "feeding_back", lock, side
#            shot_number = self.server.experiment.get('shot_number')
#            feedback_point_value = [lock, side, shot_number]
#            request = {'clock_servo.feedback_point': feedback_point_value}
#            self.server._set_parameter_values(request)
#        
        if self.value_log[-2] is not None:
            value = self.value_log[-2]
            lock, side = value
            print "feeding_back", lock, side
            shot_number = self.shot_number_log[-2]
            feedback_point_value = [lock, side, shot_number]
            request = {'clock_servo.feedback_point': feedback_point_value}
            self.server._set_parameter_values(request)
        
        if self.server._get_parameter_value('blue_pmt.recorder'):
            self.value_log.append(self.value)
            self.shot_number_log.append(self.server.experiment.get('shot_number'))


Parameter = DitherPoint

