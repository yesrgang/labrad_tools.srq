import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

import sys
sys.path.append('../') # for fpga_dds_sequences.py
import fpga_dds_sequences as ss

# set plotly output
import plotly.io as pio
pio.renderers.default = "browser"


# seq = [
#     [ss.SetTransition(ss.Transition(10e6, [0.5], [1e5]))]
#     + ss.XY16(0.005, pulse=ss.PiPulse(centered=True, window=ss.GaussianPulse))
# ]

# seq = [ss.XY16(0.005, pulse=ss.PiPulse(amplitude=1., phase=0., frequency=10e6, centered=True, window=ss.GaussianPulse))
# ]

# seq = [ss.RectangularPulse(1e-3, 1, phase=0., frequency=10e6),
#        ss.Wait(10e-3),
#        ss.RectangularPulse(1e-3, 1)]

# seq = [[ss.SetTransition(ss.Transition(10e6, [0.5], [1e5]))],
#        ss.RectangularPulse(1e-3, 1, phase=0., frequency=10e6),]

# seq = [ss.RectangularPulse(1e-3, 1, phase=0., frequency=10e6),
#        ss.RectangularPulse(1e-3, 1, phase=np.pi/2, frequency=11e6),]

# seq = [
#     [ss.Timestamp(1E-3, 0, 10E6, 5, dds_absolute_phase=True), ss.Timestamp(3, None, None, None)],
#     [ss.Timestamp(1E-3, 0, 10E6, 4, dds_absolute_phase=True), ss.PhaseRamp(3, None, 2*np.pi, None)]
# ]

seq = [
    [ss.Timestamp(1E-3, 0, 10E6, 5, dds_amplitude=.8, dds_absolute_phase=True, additional_params={'cleanup': True})],
    ss.Timestamp(3, None, None, None),
]

# seq = [[],[],[],[], []]

# seq = [
#     ss.Timestamp(1, (i + 1) / 7, None, 10e6, digital_out={i: True, (i - 1) % 7: False})
#     for i in range(7)
# ] + [ss.Timestamp(1, 0, None, 10e6, digital_out={i: False for i in range(7)})]

# associate sequence to a channel
seq = {0: seq}

# ss.plot_sequence(seq) # plot sequence with plotly in browser

print('start compilation')
# compiled_str = ss.compile_sequence(seq, output_json=True)
# print(compiled_str)
compiled, durations = ss.compile_sequence(seq, output_json=False)

sequencer_str = ss.construct_sequencer_sequence(compiled, 'rabi-start', sequencer_mapping=ss.SequencerMapping(additional_params={'cleanup': 'HR Abs. AOM@A02'}))
