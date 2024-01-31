import json

from conductor.parameter import ConductorParameter
from current_controller3.devices import _3d
from update.proxy import UpdateProxy


class IsLocked(ConductorParameter, _3d.DeviceProxy):
    autostart = False
    priority = 1

    def initialize(self, config):
        super(IsLocked, self).initialize(config)
        self._update = UpdateProxy('3d')

    def update(self):
        power = self.power
        self.value = bool(power > self._locked_threshold)
        self._update.emit({'power': power})

Parameter = IsLocked
