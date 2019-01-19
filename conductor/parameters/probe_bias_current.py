import vxi11
from conductor.parameter import ConductorParameter

class ProbeBiasCurrent(ConductorParameter):
    """ value set by sequencer.sequence """ 
    autostart = False
    priority = 1
    call_in_thread = True

    def initialize(self, config):
        print 'init'
        super(ProbeBiasCurrent, self).initialize(config)
        inst = vxi11.Instrument('192.168.1.14')
        inst.timeout = 0.1
        inst.write('INIT')
        self.inst = inst

    def update(self):
        try:
            response = self.inst.ask('FETCH?')
            self.inst.write('INIT')
            self.value = float(response)
            print self.value
        except:
            print 'fail'
            pass



Parameter = ProbeBiasCurrent
