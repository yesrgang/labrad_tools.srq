import numpy as np

sequence = [
    'blue_mot',
    'red_mot',
    'load_odt-trans',
    'depolarize',
    'evaporate',
    'tof',
    'image',
    ]

parameters = {
#        'clock_lock': {},
    }

pv = {
#    'lattice_alignment.h1_retro_blocked': False,
#    'lattice_alignment.h2_retro_blocked': False,
    'toptica_intensity': 3.0,
    'sequencer.AHbm': -3.8,
    'sequencer.AHrm': -0.135,
    'sequencer.AIf': 3.5,
    'sequencer.AIff': 0.01,#0.05 (20220123),
    'sequencer.AIi': 4.3,
    'sequencer.alpha_trans': .35, #0.15 (20220606) # (20220222) 0.6,
    'sequencer.alpha-img-int': -0.05,
    'sequencer.alpha-pol-int': 0.08, # 20240326 recorded value
    'sequencer.alpha-pol-12': 0.6,#0.64, # 0.6
    'sequencer.alpha-pol-11': 0.49,#0.52, # 0.48
    'sequencer.alpha-pol-10': 0.38, #0.40,
    'sequencer.alpha-pol-9': 0.27,#0.29,
    'sequencer.alpha-pol-8': 0.16,#0.17,
    'sequencer.alpha-pol-7': 0.05, #0.05,
    'sequencer.alpha-pol-6': -0.066, #-0.07,
    'sequencer.alpha-pol-5': -0.17, #-0.19,
    'sequencer.alpha-pol-4': -0.28, #-0.31,
    'sequencer.alpha-pol-3': -0.39, #-0.43,
    'sequencer.alpha-pol-2': -0.50, #-0.55,
    'sequencer.alpha-pol-1': -0.61, #-0.65, #-0.68,
    'sequencer.AItrans': 0.04, #0.045 (20220606) # 0.025 (20220125) #.04 (20210123) ,#  0.02 (20210729),
    'sequencer.BItrans': 0.018, #0.030 (20220606) # 0.025 (20220125) # .04 (20220123),#  0.023 (20210729),
    'sequencer.BItrans_noatt': 0.03,
    'sequencer.BIi': 1.1, # 1.5
    'sequencer.BIf': 0.25,
    'sequencer.BIff': .07,#0.04 (20210729) ,
    'sequencer.HODTo': 0.010,
    'sequencer.HODT-compress': -0.6,

#    'sequencer.HODTi': -0.52,
#    'sequencer.HODT0': -0.52,
#    'sequencer.HODT1': -0.47,
#    'sequencer.HODT2': -0.39,
#    'sequencer.HODT3': -0.31,
#    'sequencer.HODT4': -0.23,
#    'sequencer.HODT5': -0.16,
#    'sequencer.HODT6': -0.08,
#    'sequencer.HODT7': -0.06,

    'sequencer.I-bm-load-1': -1.4,
    'sequencer.I-bm-load-2':-1.40, # 2024-08-09 power crappy -> reduced from -1.45 # optimized power on 20240328 - increased to 1.55; used to be -1.50, changed to -1.40 on 20240326 ; used to be -1.6,  changed to -1.55 in the evening of 20231215 since 3d2 power since to decayed.
    'sequencer.I-bm-load-3': -0.80, # was 0.65, more power is available now
#    'sequencer.I-bm-load-1': -0.55,
#    'sequencer.I-bm-load-2': -0.3,
#    'sequencer.I-bm-load-3': -0.07,
    'sequencer.I_hpol': -0.2,
    'sequencer.I_redimg': -.22,
    'sequencer.img-detuning': -0.899,
    'sequencer.Ioff': 0.04,
    'sequencer.mot-detuning': -0.927,
    'sequencer.OSG_I': -0.4,
    'sequencer.OSG_FM': 0.,
    'sequencer.polarize-int': -0.8, #-2.0, #-0.06,
    'sequencer.sequence': sequence,
    'sequencer.T_813l': 0.15,
    'sequencer.T_813l2': 0.11,
    'sequencer.T_bm': 2.5,
    'sequencer.T_lr-abs': 5e-6,
    'sequencer.T_hr-abs': 1e-6,
    'sequencer.T_pre-bm': 1.,
    'sequencer.T_top': 1e-5,
#    'sequencer.T-trans': 0.4,
    'sequencer.T_trans': 0.2,
    'sequencer.Thold': 0.5,
    'sequencer.t-TenS4': 2e-3,
    'sequencer.Toptica-int': 1.0,
    'sequencer.T-pol': 5e-3,
    'sequencer.T-tof': 1e-6,
    'sequencer.T_redimg': 5e-05,
    'sequencer.VODT-compress': -0.9,
    'sequencer.VODT-load': -0.9,
    'sequencer.VODT-osg': -0.9,
    'sequencer.VODTi': -0.4,
    'sequencer.VODTm': -0.4,
    'sequencer.VODTf': -0.4,
    'sequencer.VODTo': 0.03,
    'sequencer.XCC0': 0.65,
    'sequencer.XCCclk': 0.644,
    'sequencer.XCCbm': 0.59,
    'sequencer.XCCrm': 0.435,
    'sequencer.XCCrimg': 0.74, #0.65,
    'sequencer.XCCpol': 0.8, # 0.65
    'sequencer.YCC0': 0.21,
    'sequencer.YCCclk': 0.2335,
    'sequencer.YCCpol': -1.4 * 4, #-1.4,
    'sequencer.YCCrimg': -1.4 * 4,
    'sequencer.YCCimg': -9.0,
    'sequencer.ZCC0': -0.017,
    'sequencer.ZCCclk': -0.031,
    'sequencer.ZCCrimg': 0.07, #-0.03,
    'sequencer.ZCCpol': 0.12, # -0.03

    'sequencer.ZCCtrans': 0.425,
    'sequencer.AHtrans': -.125,
    'sequencer.AI0': 0.18,
    'sequencer.BI0': 0.035,

    'sequencer.Tevap8': 1.51,
    'sequencer.HODT8:': -0.038,
    'sequencer.Tevap9': 2.01,
    'sequencer.HODT9': -0.035,


    #'sequencer.XCC-tens4': 3.5 ,
    #'sequencer.YCC-tens4': -9.0,
    #'sequencer.ZCC-tens4': 2.0, # 0.45 (20210812)
    'sequencer.XCC-tens4': 0.65,
    'sequencer.YCC-tens4': 0.21,
    'sequencer.ZCC-tens4': -9.0,
    'sequencer.I-1354': 3.915,
    'sequencer.RF-1354': 2.5,
    }

pv['sequencer.H1-I0'] = 0.015
pv['sequencer.H2-I0'] = 0.008
pv['sequencer.V-I0'] = 0.008
pv['sequencer.H1-I1'] = pv['sequencer.H1-I0'] - 3.0 * 2.5 / 90
pv['sequencer.H1-I2'] = pv['sequencer.H1-I0'] - 3.0 * 10.0 / 90
pv['sequencer.H1-I3'] = pv['sequencer.H1-I0'] - 3.0 * 90.0 / 90
pv['sequencer.H1-Imax'] = pv['sequencer.H1-I3']
pv['sequencer.H2-I1'] = pv['sequencer.H2-I0'] - 3.0 * 2.5 / 60
pv['sequencer.H2-I2'] = pv['sequencer.H2-I0'] - 3.0 * 10.0 / 60
pv['sequencer.H2-I3'] = pv['sequencer.H2-I0'] - 3.0 * 60.0 / 60
pv['sequencer.H2-Imax'] = pv['sequencer.H2-I3']
pv['sequencer.V-I1'] = pv['sequencer.V-I0'] - 3.0 * 2.5 / 70
pv['sequencer.V-I2'] = pv['sequencer.V-I0'] - 3.0 * 10.0 / 70
pv['sequencer.V-I3'] = pv['sequencer.V-I0'] - 3.0 * 70.0 / 70
pv['sequencer.V-Imax'] = pv['sequencer.V-I3']

   
pv['sequencer.Tlat1'] = 50e-3
pv['sequencer.Tlat2'] = 50e-3
pv['sequencer.Tlat3'] = 50e-3
    
pv['sequencer.I-bm-cool-1'] = -0.4
pv['sequencer.I-bm-cool-2'] = -0.4
pv['sequencer.I-bm-cool-3'] = -0.07
    
pv['sequencer.XCCbm'] = 0.59
pv['sequencer.XCCrm'] = 0.435
pv['sequencer.YCCbm'] = 0.2
pv['sequencer.YCCrm'] = 0.02
pv['sequencer.ZCCbm'] = 0.345
pv['sequencer.ZCCrm'] = 0.335 #(20230112 0.0345)

pv['sequencer.alpha-fm-bb'] = 0.0
pv['sequencer.alpha-fm-sf'] = 0.1
pv['sequencer.alpha-fm-odt'] = -0.01
pv['sequencer.alpha-fm-trans'] = 0.35
pv['sequencer.alpha-int-sf'] = 3.5
pv['sequencer.alpha-int-odt'] = 0.01
pv['sequencer.alpha-int-trans'] = 0.04
pv['sequencer.beta-fm-bb'] = 0.00
pv['sequencer.beta-fm-sf'] = 0.0175
pv['sequencer.beta-fm-odt'] = 0.03
pv['sequencer.beta-fm-trans'] = 0.034 #0.027
pv['sequencer.beta-int-sf'] = 0.45
pv['sequencer.beta-int-odt'] = 0.12
pv['sequencer.beta-int-trans'] = 0.025

''' evap from -.05 to -.4 in 1 s '''
pv['sequencer.Tcompress0'] = 0.195
pv['sequencer.Tcompress1'] = 0.152
pv['sequencer.Tcompress2'] = 0.127
pv['sequencer.Tcompress3'] = 0.110
pv['sequencer.Tcompress4'] = 0.098 
pv['sequencer.Tcompress5'] = 0.089
pv['sequencer.Tcompress6'] = 0.081
pv['sequencer.Tcompress7'] = 0.075
pv['sequencer.Tcompress8'] = 0.071

pv['sequencer.Hcompress0'] = -.089
pv['sequencer.Hcompress1'] = -.128
pv['sequencer.Hcompress2'] = -.167
pv['sequencer.Hcompress3'] = -.206
pv['sequencer.Hcompress4'] = -.244 
pv['sequencer.Hcompress5'] = -.283
pv['sequencer.Hcompress6'] = -.322
pv['sequencer.Hcompress7'] = -.361
pv['sequencer.Hcompress8'] = -.400


''' evap from -.06 to -.4 in 1 s '''
#pv['sequencer.Tcompress0'] = 0.187
#pv['sequencer.Tcompress1'] = 0.150
#pv['sequencer.Tcompress2'] = 0.127
#pv['sequencer.Tcompress3'] = 0.111
#pv['sequencer.Tcompress4'] = 0.099 
#pv['sequencer.Tcompress5'] = 0.090
#pv['sequencer.Tcompress6'] = 0.084
#pv['sequencer.Tcompress7'] = 0.077
#pv['sequencer.Tcompress8'] = 0.072

#pv['sequencer.Hcompress0'] = -.098
#pv['sequencer.Hcompress1'] = -.135
#pv['sequencer.Hcompress2'] = -.173
#pv['sequencer.Hcompress3'] = -.211
#pv['sequencer.Hcompress4'] = -.248 
#pv['sequencer.Hcompress5'] = -.286
#pv['sequencer.Hcompress6'] = -.324
#pv['sequencer.Hcompress7'] = -.362
#pv['sequencer.Hcompress8'] = -.400

# optimized for evap HODT to 0.045 and 1.0 s hold
#pv['sequencer.T-trans'] = 0.5
#pv['sequencer.Tevap1'] = 0.006
#pv['sequencer.Tevap2'] = 0.0125
#pv['sequencer.Tevap3'] = 0.025
#pv['sequencer.Tevap4'] = 0.05 
#pv['sequencer.Tevap5'] = 0.1
#pv['sequencer.Tevap6'] = 0.15
#pv['sequencer.Thold'] = 1.0

## optimized for evap HODT to 0.06 and 0.01 s hold
#pv['sequencer.Tevap1'] = 0.1
#pv['sequencer.Tevap2'] = 0.2
#pv['sequencer.Tevap3'] = 0.3
#pv['sequencer.Tevap4'] = 0.4
#pv['sequencer.Tevap5'] = 0.5
#pv['sequencer.Tevap6'] = 0.6
#pv['sequencer.Tevap7'] = 0.71
#pv['sequencer.Thold'] = 0.01

# optimized for evap HODT to 0.05 and 0.01 s hold, changed VODT focus
pv['sequencer.Tevap1'] = 0.1
pv['sequencer.Tevap2'] = 0.4
pv['sequencer.Tevap3'] = 1.0
pv['sequencer.Tevap4'] = 1.0
pv['sequencer.Tevap5'] = 1.0
pv['sequencer.Tevap6'] = 1.0
pv['sequencer.Tevap7'] = 1.0
pv['sequencer.Thold'] = 0.01

pv['sequencer.HODTi'] = -0.42
pv['sequencer.HODT0'] = -0.42
pv['sequencer.HODT1'] = -0.36
pv['sequencer.HODT2'] = -0.30
pv['sequencer.HODT3'] = -0.24
pv['sequencer.HODT4'] = -0.18
pv['sequencer.HODT5'] = -0.12
pv['sequencer.HODT6'] = -0.06
pv['sequencer.HODT7'] = -0.05

pv['sequencer.HODT-decompress'] = -0.05
pv['sequencer.HODT-compress'] = -0.05

pv['sequencer.VODTi'] = -0.4
pv['sequencer.VODT-decompress'] = -0.4
pv['sequencer.VODT-compress'] = -0.4

pv['T-hr-shutter'] = 4e-3 #3.2e-3
pv['sequencer.clock-intensity-pi'] = 1.5

pv['save_script.names'] = [] # prevent save_script.name conductor parameter from saving old script when not supplying a new file path

parameter_values = pv
