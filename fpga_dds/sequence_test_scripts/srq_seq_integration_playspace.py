import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

import sys
sys.path.append('../') # for fpga_dds_sequences.py
import fpga_dds_sequences as ds

# set plotly output
import plotly.io as pio
pio.renderers.default = "browser"

# transition params: pd_setpoints, frequency, Rabi_frequencies, dds_amplitudes
# pulse params: duration, pd_setpoint, phase, frequency, pd_selection, clk_shutter, clk_aom, additional_params, dds_amplitude, dds_wait_for_trigger, dds_digital_out, dds_absolute_phase

# seq = [
#     [ds.SetTransition(ds.Transition(10e6, [0.5], [1e5]))]
#     + ds.XY16(0.005, pulse=ds.PiPulse(centered=True, window=ds.GaussianPulse))
# ]

# seq = [ds.XY16(0.005, pulse=ds.PiPulse(amplitude=1., phase=0., frequency=10e6, centered=True, window=ds.GaussianPulse))
# ]

# seq = [ds.RectangularPulse(1e-3, 1, phase=0., frequency=10e6),
#        ds.Wait(10e-3),
#        ds.RectangularPulse(1e-3, 1)]

# seq = [[ds.SetTransition(ds.Transition(10e6, [0.5], [1e5]))],
#        ds.RectangularPulse(1e-3, 1, phase=0., frequency=10e6),]
#------------------------------------------------------------

# seq = [ds.RectangularPulse(1e-3, 2, phase=0., frequency=10e6),
#        ds.RectangularPulse(1e-3, 2.1, phase=np.pi/2, frequency=11e6),]

seq = [ds.SetTransition(ds.Transition(.5, 10e6, 720)),
        ds.RectangularPulse(1e-3, 2, phase=0.),
        ds.Dark(19e-3),
        [ds.RectangularPulse(1e-3, 4, phase=np.pi/2), ds.RectangularPulse(1e-3, 3, phase=np.pi/2)],]

# seq = [ds.SetTransition(ds.Transition(.5, 10e6, 720)),
#        ds.BlackmanPulse(1e-3, 2, phase=0.),
#        ds.Dark(19e-3),
#        ds.GaussianPulse(1e-3, 3, phase=np.pi/2),]

# seq = [ds.AmplitudeRamp(10e-3, 0, 2, phase=0, frequency=1e6),
#        ds.Dark(2e-3),
#        ds.FrequencyRamp(10e-3, end_frequency=10e6),
#        ds.Dark(2e-3),
#        ds.PhaseRamp(10e-3, start_phase=0, end_phase=2*np.pi),]

# seq = [ds.SetTransition(ds.Transition(.5, 10e6, 720)),
#         ds.PiPulse(phase=0.),
#         ds.Dark(19e-3),
#         ds.Pi2Pulse(phase=np.pi/2),]

# seq = [ds.SetTransition(ds.Transition(.5, 10e6, 720)),
#         ds.PiPulse(phase=np.pi/2),
#         ds.SpinEcho(19e-3, phase=3*np.pi/2),
#         ds.Pi2Pulse(phase=np.pi/2),]

# seq = [
#     [ds.Timestamp(1E-3, 5, 0, 10E6, dds_absolute_phase=True), ds.Timestamp(3, None, None, None)],
#     [ds.Timestamp(1E-3, 4, 0, 10E6, dds_absolute_phase=True), ds.PhaseRamp(3, None, 0, 2*np.pi)]
# ]

# seq = [
#     [ds.Timestamp(1E-3, 5, 0, 10E6, dds_amplitude=.8, dds_absolute_phase=True, additional_params={'cleanup': True})],
#       ds.Timestamp(3),
# ]

# seq = [
#     ds.Timestamp(1E-3, 5, 0, 10E6, dds_absolute_phase=True, additional_params={'cleanup': True}),
#     ds.Timestamp(3),
# ]

# seq = [[],[],[],[], []]

# seq = [
#     ds.Timestamp(1, (i + 1) / 7, None, 10e6, digital_out={i: True, (i - 1) % 7: False})
#     for i in range(7)
# ] + [ds.Timestamp(1, 0, None, 10e6, digital_out={i: False for i in range(7)})]

# associate sequence to a channel
seq = {0: seq}

ds.plot_sequence(seq) # plot sequence with plotly in browser

print('start compilation')
# compiled_str = ds.compile_sequence(seq, output_json=True)
# print(compiled_str)
compiled, durations = ds.compile_sequence(seq, output_json=False)

ds.set_sequence_searchpath('./sequences')
sequencer_mapping = ds.SequencerMapping(additional_params={'cleanup': 'HR Abs. AOM@A02'})
# sequencer_dict = ds.construct_sequencer_sequence(compiled, 'rabi-start', sequencer_mapping=sequencer_mapping) # with additional_params
sequencer_dict = ds.construct_sequencer_sequence(compiled, 'rabi-start') # without additional_params


