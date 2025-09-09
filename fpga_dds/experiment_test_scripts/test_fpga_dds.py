import numpy as np
from settings.defaults import parameter_values as pv

import sys
#sys.path.append('../') # for fpga_dds_sequences.py
sys.path.append('C:\\Users\\Ye Lab\\Desktop\\labrad_tools.srq\\fpga_dds') # for fpga_dds_sequences.py
import fpga_dds_sequences as ds
import jsonpickle

sequence_path = 'Q:\\sequences'  # required for building FPGA-DDS sequences
ds.set_sequence_searchpath(sequence_path)


def get_OLPD_SP(ILPD_SP):
    return (0.9405 * ILPD_SP + 0.1645 - 0.167)/1.009
    #return (0.84 * ILPD_SP + 0.06 - 0.08)/1.01

f_0 = -235.610600e6 + 1952.2 + 2.2

delta_p = 1.422e3
delta_s = 1.961e3
f_pump = f_0 - delta_p


T_pi_clean = 34.5e-3
T_pi = 2.82e-3

pv['sequencer.clock-intensity'] = 4.5
pv['sequencer.OLPD-clock-intensity'] = get_OLPD_SP(pv['sequencer.clock-intensity'])

pv['sequencer.clock-intensity-pi'] = 0.08
pv['sequencer.OLPD-clock-intensity-pi'] = get_OLPD_SP(pv['sequencer.clock-intensity-pi'])


detunings = f_pump
pv['si21.cleanup_detuning'] = f_pump
pv['si21.probe_detuning'] = detunings

times = np.linspace(1e-3, 1e-2, 20)
#times = np.linspace(1e-3, 20e-3, 40)
#times0 = np.linspace(1e-6, 2*T_pi , 20)
#times1 = np.linspace(8*T_pi, 10*T_pi , 21)
#times  = np.concatenate([times0, times1])
##times = np.linspace(1e-6, 4 * T_pi , 41)
##times = np.repeat(100*T_pi, 10)
#
#np.random.shuffle(times)
print(times)

### FPGA-DDS programming ###
pv['fpga_dds.verbose'] = 0 # set this to 0 in defaults!

fpga_dds_f0 = 155.52e6
hclk_int_cleanup = pv['sequencer.clock-intensity-pi']
hclk_int_p0 = pv['sequencer.clock-intensity']
hclk_f0 = fpga_dds_f0 + 0.

dds_seqs = []
virtseqs = []
for t in range(times.size):
    #seq = [ds.RectangularPulse(1e-3, 1, phase=0., frequency=f_pump),
    #       ds.Wait(10e-3),
    #       ds.RectangularPulse(1e-3, 1, phase=np.pi)]

    ## Ramsey sequence
    #seq = [ds.Timestamp(1e-3, 2., frequency=f_pump), # run DDS before sequence (ensure that CLK AOM does not cool down!)
    #       ds.Timestamp(6e-3, 2., clk_shutter=False, clk_aom=True, dds_wait_for_trigger=True), # set up sequencer channels
    #       ds.RectangularPulse(10e-3, 2., phase=np.pi),
    #       ds.Dark(5e-3),
    #       ds.RectangularPulse(7.5e-3, 1.)]

    # Rabi pulse
    seq = [ds.Timestamp(1e-3, hclk_int_cleanup, frequency=fpga_dds_f0), # run DDS before sequence (ensure that CLK AOM does not cool down!)
           ds.Timestamp(6e-3, hclk_int_p0, phase=0., frequency=fpga_dds_f0, dds_wait_for_trigger=True), # init
           ds.RectangularPulse(3e-3, hclk_int_p0, phase=0., frequency=fpga_dds_f0, clk_aom=False, clk_shutter=False),

           ds.RectangularPulse(5e-3, 1.2*hclk_int_p0, phase=0., frequency=fpga_dds_f0, clk_aom=True), # dark
           #ds.Dark(19e-3),
           ds.RectangularPulse(times[t], 1.2*hclk_int_p0, phase=np.pi/2, frequency=hclk_f0, pd_selection=False),
           ds.RectangularPulse(6e-3, hclk_int_p0, phase=0., frequency=fpga_dds_f0, clk_aom=True, clk_shutter=False), # dark

           ds.RectangularPulse(3e-3, hclk_int_p0, phase=0., frequency=fpga_dds_f0, clk_aom=False, clk_shutter=False), # end
           ds.RectangularPulse(5e-3, hclk_int_cleanup, phase=0., frequency=fpga_dds_f0, clk_aom=False, clk_shutter=False),]

    #seq = [ds.Timestamp(t, np.pi/2, f_pump, 5, dds_amplitude=.8, additional_params={'cleanup': True}),
    #       ds.Timestamp(30e-3)]
    seq = {0: seq}
    dds_seqs.append(jsonpickle.dumps(seq, keys=True))
    if t == 0:
     ds.plot_sequence(seq)

    # compile DDS sequence for Sequencer
    #seq_mapping = ds.SequencerMapping(additional_params={'trig': 'LR Demod Sweep@C03'})
    #dds_pulses = ds.construct_sequencer_sequence(ds.compile_sequence(seq, False)[0],
    #                                             'rabi-clock-cleanup-CLKOLPD',  # use last timestep for default values
    #                                             sequencer_mapping=seq_mapping)
    dds_pulses = ds.construct_sequencer_sequence(ds.compile_sequence(seq, False)[0],
                                                 'rabi-clock-cleanup-CLKOLPD',  # use last timestep for default values
                                                 dds_trigger_delay=1.05e-6)
    virtseqs.append({'dds_pulses': dds_pulses})

pv['fpga_dds.sequences'] = dds_seqs
pv['sequencer.virtseqs'] = virtseqs
spectroscopy_sequence = 'dds_pulses.virtseq'
#spectroscopy_sequence = 'rabi-clock-x-CLKOLPD'
#spectroscopy_sequence = 'rabi-clock-x'
### END FPGA-DDS programming ###


pv['ad9914_clock_dds.dds_profiles'] = {'0': [f_pump+100, 0., 0.8],
                                       '1': [f_pump+100, 0., 0.8],
                                       '2': [f_pump+100, 0., 0.8],
                                       '3': [f_pump+100, 0., 0.8],
                                       '4': [f_pump+140, 0., 0.3],
                                       '5': [f_pump+150, 0., 0.3],
                                       '6': [f_pump+160, 0., 0.3],
                                       '7': [f_pump+170, 0., 0.3],
                                       }
pv['ad9914_clock_dds.dds_frequency_0'] = detunings # rabi-clock-x
pv['ad9914_clock_dds.dds_frequency_1'] = f_pump # reabi-clock-cleanup
pv['ad9914_clock_dds.dds_frequency_2'] = detunings # rabi-clock-x2
pv['ad9914_clock_dds.dds_phase_0'] = 0.
pv['ad9914_clock_dds.dds_phase_1'] = 0.
pv['ad9914_clock_dds.dds_phase_2'] = 0.
pv['ad9914_clock_dds.dds_prog_modulus_freq'] = detunings
pv['ad9914_clock_dds.program_dds'] = 1.


#pv['sequencer.Trabi-x'] = times
pv['sequencer.Trabi-x'] = T_pi
pv['sequencer.Trabi-x2'] = T_pi
pv['sequencer.Trabi-pi'] = T_pi
pv['sequencer.Trabi-pi2'] = T_pi / 2
pv['sequencer.Trabi-cleanup'] = T_pi_clean
pv['sequencer.Trabi-readout'] = T_pi_clean


pv['sequencer.sequence'] = [
    'blue-mot',
    'red-mot',
    'load-odt',
    'depolarize',
    'evaporate',
    'TenS4',
    'polarize2',
    'load-lattice',

    #'rabi-clock-cleanup-CLKOLPD',
    #'rabi-clock-cleanup',
    #'rabi-clock-x',
    spectroscopy_sequence,
        
    'image-princeton-single',
    'image-princeton-single',

    'image-princeton-single-repump',
    'image-princeton-single-dark2',
    #'image-princeton-single',

    #'image-princeton-single-horizontalcleanup',
    ]
    
pv['sequencer.XCCclk'] = 4.69
pv['sequencer.YCCclk'] = -8.15
pv['sequencer.ZCCclk'] = 0.031

pv['sequencer.T_bm'] = 2.5
pv['sequencer.t-TenS4'] = 0.5e-3 #1.0e-3, #0.5e-3
pv['sequencer.T-pol'] = 2.5e-3 # 100e-6 for polarize3_test, 2.5e-3 for polarize2
pv['sequencer.polarize-int'] = -0.05
pv['sequencer.T_hr-abs'] = 1e-6


_HODT_final = -0.047 #-0.05
pv['sequencer.HODT7'] = _HODT_final #-0.05
pv['sequencer.HODT-decompress'] = _HODT_final #-0.05
pv['sequencer.HODT-compress'] = _HODT_final #-0.05

pv['sequencer.Tevap1'] = 0.1
pv['sequencer.Tevap2'] = 0.1
pv['sequencer.Tevap3'] = 0.1
pv['sequencer.Tevap4'] = 1.0
pv['sequencer.Tevap5'] = 1.5
pv['sequencer.Tevap6'] = 2.0
pv['sequencer.Tevap7'] = 0.5
pv['sequencer.Thold'] = 0.5 # 0.1

pv['sequencer.HODTi'] = -0.5
pv['sequencer.VODTi'] = -0.9 #-0.6
pv['sequencer.VODTf'] = -0.9 #-0.4
pv['sequencer.VODTff'] = -0.9 #-0.3
pv['sequencer.VODT-decompress'] = -0.05
pv['sequencer.VODT-compress'] = -0.3
pv['sequencer.VODT-compress-lat'] = -1.2 #-0.3

pv['lattice_alignment.h1_retro_blocked'] = False
pv['lattice_alignment.h2_retro_blocked'] = False

pv['sequencer.H1-I0'] = 0.015
pv['sequencer.H2-I0'] = 0.008
pv['sequencer.V-I0'] = 0.008
pv['sequencer.H1-I1'] = pv['sequencer.H1-I0'] - 3.5 * 2.5 / 69
pv['sequencer.H1-I2'] = pv['sequencer.H1-I0'] - 3.5 * 10.0 / 69
pv['sequencer.H1-I3'] = pv['sequencer.H1-I0'] - 3.5 * 45.0 / 77.6
pv['sequencer.H1-Imax'] = pv['sequencer.H1-I3']
pv['sequencer.H2-I1'] = pv['sequencer.H2-I0'] - 3.5 * 2.5 / 73
pv['sequencer.H2-I2'] = pv['sequencer.H2-I0'] - 3.5 * 10.0 / 73
pv['sequencer.H2-I3'] = pv['sequencer.H2-I0'] - 3.5 * 45.0 / 85.8
pv['sequencer.H2-Imax'] = pv['sequencer.H2-I3']
pv['sequencer.V-I1'] = pv['sequencer.V-I0'] - 3.0 * 2.5 / 43
pv['sequencer.V-I2'] = pv['sequencer.V-I0'] - 3.0 * 10.0 / 43
pv['sequencer.V-I3'] = pv['sequencer.V-I0'] - 3.0 * 45.0 / 51
pv['sequencer.V-Imax'] = pv['sequencer.V-I3']


#"""
# ps5000a or ps3000a both work
# picoscope is used to measure clock laser psd
#pv['sequencer.pico-timebase'] = 627 # Corresponds to 5us sample spacing. Determines sampling rate for 15-bit operation from (n-2)/125,000,000 s. See page 28 of ps5000a programmers guide or page 15 of ps3000a programmer's guide
# we're not going to use the above parameter value. Instead, we specify the sample duration and calculate the needed timebase in the picoscope server
pv['sequencer.pico-duration'] = 2*50e-3 #50e-3 # 50ms shot duration
pv['sequencer.pico-presamples'] = 20 # samples before trigger
pv['sequencer.pico-postsamples'] = 10000 # samples after trigger
pv['sequencer.pico-model'] = 5000 # picoscope model
pv['sequencer.pico-serialno'] = 'IV953/0134'
#"""
  

if __name__ == '__main__':
    from settings.experiment import Experiment
    import os

    #script_path = os.path.abspath(__file__)
    #settings_dir = os.path.join(os.path.dirname(script_path), 'settings')
    #pv['save_script.names'] = [script_path,
    #                           os.path.join(settings_dir, 'defaults.py'),
    #                           os.path.join(settings_dir, 'experiment.py'),
    #                           ]
    
    my_experiment = Experiment(
        name='scan',
        parameter_values=pv,
        loop=False,
        )
    my_experiment.queue(run_immediately=True)
