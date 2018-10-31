import time

from conductor.parameter import ConductorParameter

class TestParameter(ConductorParameter):
    """ default behavior """

    def activate(self, config):
        super(TestParameter, self).activate(config)

    def update(self):
        print self.value

Parameter = TestParameter
