from datetime import datetime
#import dateutil.tz
import socket
import re
#from influxdb import InfluxDBClient
import pyvisa
import os
import numpy as np
import time
import json
import glob
import os
import h5py

import matplotlib.pyplot as plt

import scipy
from scipy import signal

plt.ion()

import labrad
import json
cxn = labrad.connect()

while True:
    def gauss(x, a, b, c, d):
        return a + b*np.exp(-(x-c)**2/2/d**2)

## Find directory ##

    most_recent_calibration = None

    directory = "Q://data"
#print(os.listdir(directory))
    newest_folder = max(glob.glob(os.path.join(directory, '*/')),key = os.path.getmtime)
#print(newest_folder)
    scans = sorted(glob.glob(os.path.join(newest_folder, '*/')),key = os.path.getmtime)
    print(scans)

## Check newest file in folder

        


#print(newest_scan)
    for i in np.arange(1, len(scans), 1):    
        newest_scan = sorted(glob.glob(os.path.join(newest_folder, '*/')),key = os.path.getmtime)[-i]


        tag = 'cal'
        file_type = "\*hdf5"
        count = []
        if tag in newest_scan:

            #print('Latest scan is calibration!')
            conductor_files = glob.glob(newest_scan + file_type)
            sorted_files = sorted(conductor_files, key = os.path.getctime)
            #print(len(sorted_files))
            if len(sorted_files) > 8:
                print('Newest calibration:')
                print(newest_scan)
                #print('Scan done!')
                DATADIR = directory

                pixel_size = 16e-6 / (3.88 * 10)
                gain = 2.79 / 0.85 / 0.65 # HR abs
                cross_section = 0.1014e-12 * 0.46
                linewidth = 30.5e6 * 1.69
                pulse_length = 1.0e-6 - 150e-9
                fluorescence_gain = 1.28e-6
                img_type = 'abs'

                """ normal pi """
                N = 2e3, 2e5
                p0 = 0, -1.0, 0.5, 1 / 9e-3, 9e-3


                x0, y0 = 555, 800
                runpath = newest_scan
                print(runpath)
                print(DATADIR)
                cloud_size = 15
                x, y = np.meshgrid(range(1200), range(1200))
                x2 = (x - x0)**2
                y2 = (y - y0)**2
                r2 = x2 + y2
                zoom = (x2 <= 60**2) & (y2 <= 60**2)
                cloud = (x2 <= cloud_size**2) & (y2 <= cloud_size**2)
                norm = (~cloud) & (x2 <= 55**2) & (y2 <= 55**2)

                conductor_params = [
                    'timestamp',
                    'sequencer.I-1354',
                    ]

                kuro_params = [
                    'g',
                    'b',
                    'e',
                    's',
                    ]

                packedpath = os.path.join(DATADIR, runpath, f'packed.npz')

                if True:
                #if not os.path.exists(packedpath):
                    packed = {}
                    packed['nloaded'] = 0
                    packed['nprocessed'] = 0
                    np.savez(packedpath, **packed)

                packed = dict(np.load(packedpath, allow_pickle=True))
                nloaded = packed['nloaded']

                nconductor = len(glob.glob(os.path.join(DATADIR, runpath, '*.conductor.json')))
                nkuro = len(glob.glob(os.path.join(DATADIR, runpath, '*.kuro.hdf5')))

                for i in range(nloaded, min(nconductor, nkuro)):
                    print(f'loading shot #{i}', end='\r')
                    try:
                        with open(os.path.join(DATADIR, runpath, f'{i}.conductor.json'), 'r') as infile:
                            cdata = json.load(infile)
                        with h5py.File(os.path.join(DATADIR, runpath, f'{i}.kuro.hdf5'), 'r') as infile:
                            kdata = {k: infile[k][:] for k in infile}
                    except Exception as e:
                #        raise e
                        cdata = {}
                        kdata = {}

                #    print(kdata)
                    
                    try:
                        for cp in conductor_params:
                            if cp not in packed:
                                packed[cp] = np.empty(i+1).astype(type(cdata[cp]))
                            packed[cp].resize(i+1)
                            if cdata[cp] is not None:
                                packed[cp][i] = cdata[cp] 
                        for kp in kuro_params:
                            if kp not in packed:
                                packed[kp] = np.empty((i+1, zoom.sum())).astype('int')
                            packed[kp].resize((i+1, zoom.sum())) 
                            if kdata[kp] is not None:
                                packed[kp][i] = kdata[kp][zoom]
                    except Exception as e:
                        print(e)
                    
                    packed['nloaded'] += 1

                """ process absorption images """

                #refpath = os.path.join(DATADIR, '20220913/scan#14', f'packed.hdf5')
                refpath = os.path.join(DATADIR, '20221012', f'kuro.ref.hdf5')
                packedref = h5py.File(refpath, 'r')
                g_ref = packedref['processed/g.mean'][:]
                b_ref = packedref['processed/b.mean'][:]
                e_ref = packedref['processed/e.mean'][:]
                s_ref = packedref['processed/s.mean'][:]
                packedref.close()


                images_g = packed['g'][:] - g_ref[None,zoom]
                brights = packed['b'][:] - b_ref[None,zoom]
                images_e = packed['e'][:] - e_ref[None,zoom]
                images_s = packed['s'][:] - s_ref[None,zoom]

                if img_type == 'abs':
                    brights_g = brights * (images_g[:,norm[zoom]].mean(1) / brights[:,norm[zoom]].mean(1))[:,None]
                    mx = ((x - x0)[None,norm] * (images_g - brights_g)[:,norm[zoom]]).mean(1) / x2[None,norm].mean(1)
                    my = ((y - y0)[None,norm] * (images_g - brights_g)[:,norm[zoom]]).mean(1) / y2[None,norm].mean(1)
                    brights_g += mx[:,None] * (x - x0)[zoom] + my[:,None] * (y - y0)[zoom]
                    
                    brights_e = brights * (images_e[:,norm[zoom]].mean(1) / brights[:,norm[zoom]].mean(1))[:,None]
                    mx = ((x - x0)[None,norm] * (images_e - brights_e)[:,norm[zoom]]).mean(1) / x2[None,norm].mean(1)
                    my = ((y - y0)[None,norm] * (images_e - brights_e)[:,norm[zoom]]).mean(1) / y2[None,norm].mean(1)
                    brights_e += mx[:,None] * (x - x0)[zoom] + my[:,None] * (y - y0)[zoom]
                    
                    brights_s = brights * (images_s[:,norm[zoom]].mean(1) / brights[:,norm[zoom]].mean(1))[:,None]
                    mx = ((x - x0)[None,norm] * (images_s - brights_s)[:,norm[zoom]]).mean(1) / x2[None,norm].mean(1)
                    my = ((y - y0)[None,norm] * (images_s - brights_s)[:,norm[zoom]]).mean(1) / y2[None,norm].mean(1)
                    brights_s += mx[:,None] * (x - x0)[zoom] + my[:,None] * (y - y0)[zoom]
                    
                    valid = (images_g > 0) & (brights_g > 0) 
                    logs_g = np.full(brights_g.shape, np.nan)
                    logs_g[valid] = np.log(brights_g[valid] / images_g[valid])
                    diffs_g = np.full(brights_g.shape, np.nan)
                    diffs_g[valid] = brights_g[valid] - images_g[valid]
                    counts_g = logs_g * pixel_size**2 / cross_section + diffs_g * gain / (np.pi * linewidth * pulse_length)
                    counts_g -= counts_g[:,norm[zoom]].mean(1)[:,None]
                    
                    valid = (images_e > 0) & (brights_e > 0)
                    logs_e = np.full(brights_e.shape, np.nan)
                    logs_e[valid] = np.log(brights_e[valid] / images_e[valid])
                    diffs_e = np.full(brights_e.shape, np.nan)
                    diffs_e[valid] = brights_e[valid] - images_e[valid]
                    counts_e = logs_e * pixel_size**2 / cross_section + diffs_e * gain / (np.pi * linewidth * pulse_length)
                    counts_e -= counts_e[:,norm[zoom]].mean(1)[:,None]
                    
                    valid = (images_s > 0) & (brights_s > 0)
                    logs_s = np.full(brights_s.shape, np.nan)
                    logs_s[valid] = np.log(brights_s[valid] / images_s[valid])
                    diffs_s = np.full(brights_s.shape, np.nan)
                    diffs_s[valid] = brights_s[valid] - images_s[valid]
                    counts_s = logs_s * pixel_size**2 / cross_section + diffs_s * gain / (np.pi * linewidth * pulse_length)
                    counts_s -= counts_s[:,norm[zoom]].mean(1)[:,None]
                elif img_type == 'flu':
                    counts_g = gain * (images_g - images_g[:,norm[zoom]].mean(1)[:,None]) * a_QPN / pulse_length 
                    counts_e = gain * (images_e - images_e[:,norm[zoom]].mean(1)[:,None]) * a_QPN / pulse_length
                    counts_s = gain * (images_s - images_s[:,norm[zoom]].mean(1)[:,None]) * a_QPN / pulse_length

                #print(counts_g.shape)
                #print(counts_e.shape)
                #print(zoom.sum())
                #print(cloud[zoom].shape)

                packed['counts_g'] = counts_g[:,cloud[zoom]]
                packed['counts_e'] = counts_e[:,cloud[zoom]]
                packed['counts_s'] = counts_s[:,cloud[zoom]]
                    
                np.savez(packedpath, **packed)

                """ reload data """
                timestamps = np.empty(shape=0)
                pulses = np.empty(shape=0)
                counts_g = np.empty(shape=(0, r2[cloud].size))
                counts_e = np.empty(shape=(0, r2[cloud].size))
                counts_s = np.empty(shape=(0, r2[cloud].size))
                #print(counts_g.shape)

                packedpath = os.path.join(DATADIR, runpath, f'packed.npz')
                packed = np.load(packedpath, allow_pickle=True)
                timestamps = np.append(timestamps, packed['timestamp'][2:])
                pulses = np.append(pulses, packed['sequencer.I-1354'][2:])
                counts_g = np.append(counts_g, packed['counts_g'][2:], 0)
                counts_e = np.append(counts_e, packed['counts_e'][2:], 0)
                counts_s = np.append(counts_s, packed['counts_s'][2:], 0)


                """ process """
                indices = np.indices(timestamps.shape)[0]
                counts_sd = counts_e - counts_g
                counts_st = counts_e + counts_g 
                counts_sz = np.clip(counts_sd / counts_st, -1.0, 1.0)

                sums_g = counts_g.sum(1)
                sums_e = counts_e.sum(1) 
                szs = (sums_e ) / (sums_e + sums_g)
                sts = (sums_e + sums_g)
                tots = (sums_e + sums_g)

                
                sort = np.argsort(pulses)

                #print(szs)
                
                

                popt, pcov = scipy.optimize.curve_fit(gauss,pulses[sort], szs[sort], p0 = [0.8, -1, 3.896, .1], bounds = [[-1, -1, 0, 0], [1, 1, 5, 100]])
                print(popt)
                #print(popt[2])
                most_recent_calibration = np.round(popt[2], 4)
                print(most_recent_calibration)
                plot_pulses = np.linspace(pulses[sort][0], pulses[sort][-1], 1000)

                plt.plot(plot_pulses, gauss(plot_pulses, *popt), color = 'r', linestyle = '--')
                
                #num_sigmas = 4
                #offset_list = []
                #sigmas_list = np.linspace(-num_sigmas, num_sigmas, 2*num_sigmas + 1)
                #for sigma in range(len(sigmas_list)):
                #    offset = popt[2] + sigmas_list[sigma]*popt[3]
                #    offset_list.append(np.round(offset, 4))
                #    plt.plot(offset,  gauss(offset, *popt), 'gx', markersize = 20)
                num_sigmas = 5
                offset_list = []
                sigmas_list = np.linspace(-4, 4, 9)
                for sigma in range(len(sigmas_list)):
                    offset = popt[2] + sigmas_list[sigma]*popt[3]
                    offset_list.append(np.round(offset, 4))
                    plt.plot(offset,  gauss(offset, *popt), 'gx', markersize = 20) 

                print(offset_list)
                print(runpath[8:])
                np.savetxt('Q:/data/' + runpath[8:] + 'fitted_current.txt', np.array(offset_list))
                plt.plot(pulses[sort], szs[sort], 'ko')
                plt.xlabel('1.354 um laser modulation voltage', fontsize = 20)
                plt.ylabel(r'$p_{e}$', fontsize = 20)
                plt.title(runpath + r"   $f_{0}$ =  " + str(np.round(popt[2], 4)) + " V, " + r"$\sigma$ = " +  str(np.round(popt[3], 4)), fontsize = 20)
                plt.draw()
                plt.pause(30)
                plt.clf()
                
                #request = {"sequencer.I-1354": most_recent_calibration}
                #cxn.conductor.set_parameter_values(json.dumps(request))

                break

            else:
                print("INCOMPLETE SCAN")
                plt.pause(180)
        

