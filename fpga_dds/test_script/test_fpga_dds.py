import numpy as np
from settings.defaults import parameter_values as pv

import sys
sys.path.append('../') # for fpga_dds_sequences.py
import fpga_dds_sequences as ds
import jsonpickle


def get_OLPD_SP(ILPD_SP):
    return (0.9405 * ILPD_SP + 0.1645 - 0.167)/1.009
    #return (0.84 * ILPD_SP + 0.06 - 0.08)/1.01

#f_0 = -235.610600e6 + 389.6 + 34 + 4.1
#f_0 = -235.610266e6 #  for CLK_INT = 0.2 
f_0 = -235.610600e6 + 824 - 7.4

delta_p = 1.431e3
delta_s = 1.961e3
f_pump = f_0 - delta_p


T_pi_clean = 34.5e-3
T_pi = 2.82e-3

pv['sequencer.clock-intensity'] = 9.8
pv['sequencer.OLPD-clock-intensity'] = get_OLPD_SP(pv['sequencer.clock-intensity'])
print(pv['sequencer.OLPD-clock-intensity']) 


detunings = f_pump
pv['si21.cleanup_detuning'] = f_pump
pv['si21.probe_detuning'] = detunings



seq = [ds.RectangularPulse(1e-3, 1, phase=0., frequency=f_pump),
       ds.Wait(10e-3),
       ds.RectangularPulse(1e-3, 1)]
seq = {0: seq}
tmp_str = jsonpickle.dumps(seq, keys=True)
print(tmp_str)
pv['fpga_dds.sequences'] = tmp_str

pv['ad9914_clock_dds.dds_profiles'] = {'0': [f_pump+100, 0., 0.8],
                                       '1': [f_pump+100, 0., 0.8],
                                       '2': [f_pump+100, 0., 0.8],
                                       '3': [f_pump+100.0, 0., 0.8],
                                       '4': [f_pump+140, 0., 0.3],
                                       '5': [f_pump+150, 0., 0.3],
                                       '6': [f_pump+160, 0., 0.3],
                                       '7': [f_pump+170, 0., 0.3],
                                       }
pv['ad9914_clock_dds.dds_frequency_0'] = detunings
pv['ad9914_clock_dds.dds_frequency_1'] = f_pump #f_pump
pv['ad9914_clock_dds.dds_frequency_2'] = detunings  #detunings 
pv['ad9914_clock_dds.dds_phase_0'] = 0. 
pv['ad9914_clock_dds.dds_phase_1'] = 0. 
pv['ad9914_clock_dds.dds_phase_2'] = 0. 
pv['ad9914_clock_dds.dds_prog_modulus_freq'] = f_pump
pv['ad9914_clock_dds.program_dds'] = 1.

spectroscopy_sequence = 'rabi-clock-x-CLKOLPD'
#spectroscopy_sequence = 'rabi-clock-x'

times0 = np.linspace(1e-6, 2*T_pi , 20)
times1 = np.linspace(8*T_pi, 10*T_pi , 21)
times  = np.concatenate([times0, times1])
#times = np.linspace(1e-6, 4 * T_pi , 41)
#times = np.repeat(100*T_pi, 10)

np.random.shuffle(times)
print(times)

pv['sequencer.clock-intensity-pi'] = 0.2 # cleanup
pv['sequencer.OLPD-clock-intensity-pi'] = get_OLPD_SP(pv['sequencer.clock-intensity-pi']) 

pv['sequencer.Trabi-x'] = times
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
#    'evaporate-stage2',
#    'evaporate-trans-on',
    'TenS4',
#    'polarize3_test',
    'polarize2',
    'load-lattice',

    'rabi-clock-cleanup-CLKOLPD',
    spectroscopy_sequence,
        
    'image-princeton-single',
    'image-princeton-single',
#    'rabi-clock-readout',
#    'image-princeton-single',ad9914_clock_dds.dds_phase_0
#    'image-princeton-single',

    'image-princeton-single-repump',
    'image-princeton-single',
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
pv['sequencer.H2-I3'] = pv['sequencer.H2-I0'] - 3.5 * 47.0 / 85.8
pv['sequencer.H2-Imax'] = pv['sequencer.H2-I3']
pv['sequencer.V-I1'] = pv['sequencer.V-I0'] - 3.0 * 2.5 / 43
pv['sequencer.V-I2'] = pv['sequencer.V-I0'] - 3.0 * 10.0 / 43
pv['sequencer.V-I3'] = pv['sequencer.V-I0'] - 3.0 * 47.4 / 51
pv['sequencer.V-Imax'] = pv['sequencer.V-I3']


  
if __name__ == '__main__':
    from settings.experiment import Experiment
    import os

    #script_path = os.path.abspath(__file__)
    #settings_dir = os.path.join(os.path.dirname(script_path), 'settings')
    #pv['save_script.names'] = [script_path,
    #                           os.path.join(settings_dir, 'defaults.py'),
    #                           ]
    
    my_experiment = Experiment(
        name='scan',
        parameter_values=pv,
        loop=False,
        )
    my_experiment.queue(run_immediately=True)
