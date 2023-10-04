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


def gauss(x, a, b, c, d):
    return a + b*np.exp(-(x-c)**2/d)

## Find directory ##

most_recent_calibration = None

directory = "Q://data"
#print(os.listdir(directory))
newest_folder = max(glob.glob(os.path.join(directory, '*/')),key = os.path.getmtime)
#print(newest_folder)
scans = sorted(glob.glob(os.path.join(newest_folder, '*/')),key = os.path.getmtime)
#print(scans)

## Check newest file in folder

newest_calibration = []

for i in np.arange(1, len(scans), 1):
    #print(i)

    newest_scan = sorted(glob.glob(os.path.join(newest_folder, '*/')),key = os.path.getmtime)[-i]
    #print(newest_scan)
    
    tag = 'cal'
    file_type = "\*hdf5"
    count = []
    if tag in newest_scan:
        #print(newest_scan)
        conductor_files = glob.glob(newest_scan + file_type)
        sorted_files = sorted(conductor_files, key = os.path.getctime)
        if len(sorted_files) > 20:
            #print('Newest calibration complete')
            newest_calibration = newest_scan
            break
        else:
            print('NEWEST CALIBRATION INCOMPLETE')
            #break
print("NEWEST CALIBRATION")
print(newest_scan)
