import json

from conductor.parameter import ConductorParameter
from current_controller3.devices import _2d
from update.proxy import UpdateProxy


class IsLocked(ConductorParameter, _2d.DeviceProxy):
    autostart = False
    priority = 1

    def initialize(self, config):
        super(IsLocked, self).initialize(config)
        self._update = UpdateProxy('2d')

    def update(self):
        power = self.power
        self.value = bool(power > self._locked_threshold)
        self._update.emit({'power': power})

Parameter = IsLocked
