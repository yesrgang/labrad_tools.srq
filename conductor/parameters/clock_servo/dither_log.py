from conductor.parameter import ConductorParameter
import json
from collections import deque

class DitherLog(ConductorParameter):
    priority = 7
    autostart = False
    value_type = 'list'
    value_log = deque([None, None, None], maxlen=3)
    shot_number_log = deque([None, None, None], maxlen=3)

    def update(self):
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

Parameter = DitherLog

