import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

import fpga_dds_sequences as ss

# set plotly output
import plotly.io as pio
pio.renderers.default = "browser"


seq = [
    [ss.SetTransition(ss.Transition(10e6, [0.5], [1e5]))]
    + ss.XY16(0.005, pulse=ss.PiPulse(centered=True, window=ss.GaussianPulse))
]

seq = [ss.XY16(0.005, pulse=ss.PiPulse(amplitude=1., phase=0., frequency=10e6, centered=True, window=ss.GaussianPulse))
]

seq = [ss.RectangularPulse(1e-3, 1, phase=0., frequency=10e6),
       ss.Wait(10e-3),
       ss.RectangularPulse(1e-3, 1)]

# seq = [
#     [ss.Timestamp(1E-3, 1, 0, 10E6, absolute_phase=True), ss.Timestamp(3, None, None, None)],
#     [ss.Timestamp(1E-3, 1, 0, 10E6, absolute_phase=True), ss.PhaseRamp(3, None, 0, 2*pi, None, 51)]
# ]

# seq = [[],[],[],[], []]

# seq = [
#     ss.Timestamp(1, (i + 1) / 7, None, 10e6, digital_out={i: True, (i - 1) % 7: False})
#     for i in range(7)
# ] + [ss.Timestamp(1, 0, None, 10e6, digital_out={i: False for i in range(7)})]

# associate sequence to a channel
seq = {0: seq}

ss.plot_sequence(seq)

compiled, durations = ss.compile_sequence(seq, output_json=False)



# obtain time traces, save them and load them again...
time_traces = ss.extract_time_traces(seq)
json_str = ss.timetraces2str(time_traces)

sav_data = {}
sav_data['time_traces'] = json_str
# np.savez_compressed('time_traces.npz', **sav_data)

# loaded_data = dict(np.load('time_traces.npz'))
# time_traces_loaded = ss.str2timetraces(str(loaded_data['time_traces']))
time_traces_loaded = ss.str2timetraces(json_str)




# time_traces = time_traces[0][0] # only first trigger segment of channel 0
# fig,ax = plt.subplots(1, 1)
# ax.plot(time_traces['time'], time_traces['amplitude'])

# time_step = np.min(np.diff(time_traces['time']))

# sampled_time = np.arange(time_traces['time'][0], time_traces['time'][-1], time_step)

# sampled_amplitude = np.empty(sampled_time.size)
# t = 0 # time index in original array
# for i in range(sampled_time.size):
#   if t < time_traces['time'].size-1 and np.abs(sampled_time[i] - time_traces['time'][t+1]) < np.abs(time_traces['time'][t] - sampled_time[i]):
#     t += 1
#   sampled_amplitude[i] = time_traces['amplitude'][t]
#   # if t >= time_traces['time'].size: # end of the original array has been reached; keep values constant now
#   #   sampled_amplitude[i:] = sampled_amplitude[i-1]
#   #   break

# ax.plot(sampled_time, sampled_amplitude)

