import sys, os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import fpga_dds_sequences as ss
import labrad
import jsonpickle, pprint

from math import pi

#seq = [
#    [ss.SetTransition(ss.Transition(10e6, [0.5], [1e5]))]
#    + ss.XY16(0.005, pulse=ss.PiPulse(centered=True, window=ss.GaussianPulse))
#]

#seq = [
#    [ss.Timestamp(1, 1, 0, 20E6, absolute_phase=True), ss.Timestamp(1, 0, 0, 1)],
#    [ss.Timestamp(1, 1, 0, 20E6, absolute_phase=True), ss.PhaseRamp(1, None, 0, 2*pi, None, 51)]
#]

#seq = [
#    [ss.Timestamp(10, 0.5, 0, 10E6, absolute_phase=True), ss.Timestamp(0, 0, 0, 1)],
#]

#seq = [
#    [ss.Timestamp(10, 0.5, 0, 10E6, absolute_phase=True)],
#]

#seq = [[],[],[],[], []]

seq = [
    ss.Timestamp(1, (i + 1) / 7, None, 10e6, digital_out={i: True, (i - 1) % 7: False})
    for i in range(7)
] + [ss.Timestamp(1, 0, None, 10e6, digital_out={i: False for i in range(7)})]

seq = {0: seq}

#ss.plot_sequence(seq)

# compiled, durations = ss.compile_sequence(seq)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(jsonpickle.loads(compiled))

cxn = labrad.connect()
cxn.yesr13_synthesizer.reset()
cxn.yesr13_synthesizer.write_timestamps(jsonpickle.dumps(seq, keys=True), True, False)
cxn.yesr13_synthesizer.trigger()
