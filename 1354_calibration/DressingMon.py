import numpy as np
import time
import os
from astropy.time import Time
from datetime import datetime
import sys
from matplotlib import pyplot as plt
#import allantools
from collections import deque
import pandas as pd
from matplotlib import mlab
import glob
import h5py


class DressingMon():
    def __init__(self):
        self.CalibrationPath = ""
        self.CalibratedCurrent = ""
        self.directory = "Q:\\data"

        
#        plt.ion()
#        self.f, self.ax = plt.subplots()
    def find_most_recent_calibration(self):
        newest_folder = max(glob.glob(os.path.join(self.directory, '*/')),key = os.path.getmtime)
        scans = sorted(glob.glob(os.path.join(newest_folder, '*/')),key = os.path.getmtime)

        for i in np.arange(1, len(scans), 1):
            #print(i)

            newest_scan = sorted(glob.glob(os.path.join(newest_folder, '*/')),key = os.path.getmtime)[-i]
            #print(newest_scan)
    
            tag = "cal"
            file_type = "\*hdf5"
            count = []
            if tag in newest_scan:
                #print(newest_scan)
                conductor_files = glob.glob(newest_scan + file_type)
                sorted_files = sorted(conductor_files, key = os.path.getctime)
                if len(sorted_files) > 20:
                    #print('Newest calibration complete')
                    self.CalibrationPath = newest_scan
                    break
                else:
                    print("NEWEST CALIBRATION INCOMPLETE")
                    #break
        print("NEWEST CALIBRATION: " + str(newest_scan))

        plt.pause(0.01)




if __name__ == "__main__":
    meas = DressingMon()
    meas.find_most_recent_calibration()
    meas.plot_calibration()
    while True:
        try:
            meas.find_most_recent_calibration()
            time.sleep(10)
        except KeyboardInterrupt:
            plt.close()
            break
