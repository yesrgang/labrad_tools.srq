import h5py
import numpy as np
import os
from collections import deque
from conductor.parameter import ConductorParameter

#DATADIR = '/home/srgang/srqdata/data/'
##runpath = '20210827/ref#11'
##with open(os.path.join(DATADIR, runpath, 'means.kuro.npy'), 'rb') as f:
##    image_ref = np.load(f)
##    bright_ref = np.load(f)
##    dark_ref = np.load(f)
##
#with open(os.path.join(DATADIR, '20210806/clock-detuning-scan#4', 'means.kuro.npy'), 'rb') as f:
#    image_ref = np.load(f)
#    bright_ref = np.load(f)
#    dark_ref = np.load(f)
#
#x0, y0 = 599, 592
#x0, y0 = 598, 593
#x, y = np.meshgrid(range(1200), range(1200))
#x2 = (x - x0)**2
#y2 = (y - y0)**2
#r2 = x2 + y2
#zoom = (r2 < 50**2)
#norm = (r2 > 20**2) & (r2 < 100**2)
#cloud = (r2 < 10**2)
#
#pixel_size = 16e-6 / 18
#gain = 0.91 / 0.85
#cross_section = 0.1014e-12 * 0.46
#linewidth = 32e6 * 0.89
#pulse_length = 2.5e-6
#tot_min = 2e2
#
#def get_sz_from_image_path(image_path):
##    kdata = h5py.File(image_path, 'r')
##    image_g = (kdata['image'][:] - image_ref)
##    image_e = (kdata['bright'][:] - bright_ref)
##    bright = (kdata['dark'][:] - dark_ref)
##    kdata.close()
##
##    bright_g = bright * image_g[norm].mean() / bright[norm].mean()
###    mx = ((x - x0)[norm] * (image_g - bright_g)[norm]).mean() / x2[norm].mean()
###    my = ((y - y0)[norm] * (image_g - bright_g)[norm]).mean() / y2[norm].mean()
###    bright_g += mx * (x - x0) + my * (y - y0)
###    
##    bright_e = bright * image_e[norm].mean() / bright[norm].mean()
###    mx = ((x - x0)[norm] * (image_e - bright_e)[norm]).mean() / x2[norm].mean()
###    my = ((y - y0)[norm] * (image_e - bright_e)[norm]).mean() / y2[norm].mean()
###    bright_e += mx * (x - x0) + my * (y - y0)
##
###    valid = (image_g > 0) & (image_e > 0) & (bright_g > 0) & (bright_e > 0)
##
###    log_g = np.full(bright_g.shape, np.nan)
###    log_g[valid] = np.log(bright_g[valid] / image_g[valid])
###    diff_g = np.full(bright_g.shape, np.nan)
###    diff_g[valid] = bright_g[valid] - image_g[valid]
###    count_g = log_g * pixel_size**2 / cross_section + diff_g * gain / (np.pi * linewidth * pulse_length)
###
###    log_e = np.full(bright_e.shape, np.nan)
###    log_e[valid] = np.log(bright_e[valid] / image_e[valid])
###    diff_e = np.full(bright_e.shape, np.nan)
###    diff_e[valid] = bright_e[valid] - image_e[valid]
###    count_e = log_e * pixel_size**2 / cross_section + diff_e * gain / (np.pi * linewidth * pulse_length)
##    
##    log_g = np.log(bright_g / image_g)
##    diff_g = bright_g - image_g
##    count_g = log_g * pixel_size**2 / cross_section + diff_g * gain / (np.pi * linewidth * pulse_length)
##    
##    log_e = np.log(bright_e / image_e)
##    diff_e = bright_e - image_e
##    count_e = log_e * pixel_size**2 / cross_section + diff_e * gain / (np.pi * linewidth * pulse_length)
##
##    sum_g = np.nansum(count_g[cloud])
##    sum_e = np.nansum(count_e[cloud])
##    tot = sum_e + sum_g
##    print('sg', 'se', sum_g, sum_e)
##    print('tot', tot)
##    if tot > tot_min:
##        return 0.5 * (sum_e - sum_g) / (sum_e + sum_g)
#    h5f = h5py.File(image_path, 'r')
#    image_g = h5f['image'][:] - image_ref
#    image_e = h5f['bright'][:] - bright_ref
#    bright = h5f['dark'][:] - dark_ref
#    h5f.close()
#    
##    print("norm g: {:.3f}".format(image_g[norm].mean()))
##    print("norm e: {:.3f}".format(image_e[norm].mean()))
##    print("norm b: {:.3f}".format(bright[norm].mean()))
#    
#    saturation = bright * cross_section / (np.pi * gain * pixel_size**2 * linewidth * pulse_length)
#
#    bright_g = bright * image_g[norm].mean() / bright[norm].mean()
#    od = np.log(bright_g / image_g)
#    diff = bright_g - image_g
#    counts_g = od * pixel_size**2 / cross_section + diff * gain / (np.pi * linewidth * pulse_length)
#    
#    bright_e = bright * image_e[norm].mean() / bright[norm].mean()
#    od = np.log(bright_e / image_e)
#    diff = bright_e - image_e
#    counts_e = od * pixel_size**2 / cross_section + diff * gain / (np.pi * linewidth * pulse_length)
#
#    counts_tot = counts_e + counts_g
#    counts_diff = counts_e - counts_g
#    counts_sz = 0.5 * counts_diff / counts_tot
#
#    ng = counts_g[cloud].sum()
#    ne = counts_e[cloud].sum()
#    t = ng + ne
#    sz = 0.5 * (ne - ng) / t 
##    print('e', 'g', ne, ng)
##    print('t', t)
#    print('processing...', image_path, sz) 
#
#    if t > tot_min:
#        return sz
#
#
#class PID(object):
#    def __init__(self, **kwargs):
#        self.sampling_period = 1.0
#        self.overall_gain = 1.0
#        self.prop_gain = 1.0
#        self.int_gain = 0.0
#        self.diff_gain = 0.0
#        self.input_offset = 0.0
#        self.output_offset = 0.0
#        self.output = None
#        self.output_range = [-np.inf, np.inf]
#        self.drift_rate = 0
#        self.modulation_depth = 0
#
#        self.xbuffer = deque([0., 0.], maxlen=2)
#        self.ybuffer = deque([0., 0.], maxlen=2)
#        self.error = None
#
#        self.set_parameters(**kwargs)
#
#        # contains filename of image to process
#        self.inputs = {
#            +1: None,
#            -1: None,
#        }
#        self.output = self.output_offset
#
#    def set_parameters(self, **kwargs):
#        for k, v in kwargs.items():
#            setattr(self, k, v)
#        
#        G = self.overall_gain
#        T = self.sampling_period
#        p = G * self.prop_gain
#        i = G * self.int_gain
#        d = G * self.diff_gain
#
#        print('gains', G, T, p, i, d)
#
#        self.filter_coefficients = {
#            'b_0': p + i * T / 2. + d * 2. / T,
#            'b_1': i * T - d * 4. / T,
#            'b_2': i * T / 2. - p + d * 2. / T,
#            'a_1': 0.,
#            'a_2': 1.
#        }
#
#    def update_output(self):
#        in_l = self.inputs[-1]
#        in_r = self.inputs[+1]
#
#        if (in_l == None) or (in_r == None):
#            return
#
#
#        self.error = in_l - in_r - self.input_offset
#
#        b_0 = self.filter_coefficients['b_0']
#        b_1 = self.filter_coefficients['b_1']
#        b_2 = self.filter_coefficients['b_2']
#        a_1 = self.filter_coefficients['a_1']
#        a_2 = self.filter_coefficients['a_2']
#
#        x = self.error
#        x_ = self.xbuffer
#        y_ = self.ybuffer
#        y  = b_0*x + b_1*x_[-1] + b_2*x_[-2] + a_2*y_[-2]
#
#        x_.append(x)
#        y_.append(y)
#    
#        # output offset
#        self.output_offset += self.drift_rate * self.sampling_period
#
#        # clamp
#        y = sorted([self.output_range[0], y, self.output_range[1]])[1]
#        
#        self.output = y + self.output_offset
#
#
class Parameter(ConductorParameter):
    """ 
    example_config = {
        '+9/2': {
            'output_offset': 429e12, # [Hz]
            'drift_rate': 12.7e-6, # [Hz / s]
            'overall_gain': linewidth,
            'sampling_period': cycle_time,
            'prop_gain: 0.6,
            'int_gain': 0.2,
            'modulation_depth': 1.0, # [Hz]
        }
    """
    autostart = False
    priority = 17
    value_type = 'list'
    update_queue = deque([], maxlen=2)
    locks = {}

    def initialize(self, config):
#        super(Parameter, self).initialize(config)
        for name, settings in config.items():
            self.locks[name] = PID(**settings)

    def update(self):
        """ e.g. ["+9/2", -1] """
        for i in range(len(self.update_queue)-1):
            name, sign, image_path = self.update_queue.popleft()
            sz = get_sz_from_image_path(image_path)
            self.locks[name].inputs[sign] = sz
            if sign == -1:
                print('updating {}'.format(name), self.locks[name].inputs)
                self.locks[name].update_output()
#            print(name, sign, self.locks[name].error, self.locks[name].output)
        
        if self.value is not None:
            name, sign = self.value
            name = str(name)
            sign = int(sign)
            
            lock_out = self.locks[name].output
            dither = sign * self.locks[name].modulation_depth

            request = {
                'si21.probe_detuning': self.locks[name].output,
                'si21.cleanup_detuning': self.locks[name].output,
                'sequencer.phi-0': sign * self.locks[name].modulation_depth,
                'locks.{}.output'.format(name): self.locks[name].output,
                'locks.{}.output_offset'.format(name): self.locks[name].output_offset,
                'locks.{}.error'.format(name): self.locks[name].error,
                }
            self.server._set_parameter_values(request)

            kuropath = self.server.parameters.get('kuro.record_path').value
#            i = self.server.experiment.get('shot_number')
            image_path = os.path.join(DATADIR, *kuropath.split('\\')[2:])
            print(name, sign, kuropath.split('\\')[2:])

            if self.server.experiment.get('shot_number') > 1:
                self.update_queue.append((name, sign, image_path))
