from conductor.parameter import ConductorParameter
import os
import pathlib
import shutil

class Names(ConductorParameter):
    """ 
    Save script along with measurement data
    """

    priority = 1 # lowest priority executes last
    autostart = False
    value_type = 'list'
    #value_type = 'data'
    
    def initialize(self,config):
	self.connect_to_labrad()

    def update(self):
        if self.value is not None and len(self.value) > 0:
            experiment_name = self.server.experiment.get('name')
            shot_number = self.server.experiment.get('shot_number')

            if experiment_name is not None and shot_number == 0:
                base_path = os.path.join('/', 'srqdata2')
                experiment_path = os.path.join(base_path, 'data', experiment_name)

                script_path_win = pathlib.PureWindowsPath(self.value[0])
                script_path = os.path.join(base_path, *script_path_win.parts[1:])

                save_dir  = os.path.join(experiment_path, 'scripts')
                save_path = os.path.join(save_dir, script_path_win.parts[-1])

                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                shutil.copyfile(script_path, save_path)
                print('saved script {:s} to {:s}'.format(script_path, save_path))


Parameter = Names
