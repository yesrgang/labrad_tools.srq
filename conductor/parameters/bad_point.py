from conductor.parameter import ConductorParameter


class BadPoint(ConductorParameter):

    def initialize(self, config):
        super(BadPoint, self).initialize(config)

    def get_value(self):
        return bool(self.server.experiment.get('repeat_shot', False))

Parameter = BadPoint
