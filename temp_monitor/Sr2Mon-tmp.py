import numpy as np
import time
import os
from astropy.time import Time
from datetime import datetime
import sys
from matplotlib import pyplot as plt
import allantools
from collections import deque
import pandas as pd
from matplotlib import mlab
import glob

class Sr2Mon():
    def __init__(self):
        self.PTCLogPath = "Z:\\SrQ\\temp_data\\"
        self.PTCLog = '' 
	#Initialize data dictionaries
        self.PTCData = {'MJD': np.array({}),'seconds': np.array([]),  'Array1': np.array([]),'Array2': np.array([]),'Array3': np.array([]),'Array4': np.array([]),'Array5': np.array([]),
                    'Array6': np.array([]),'Array7': np.array([]),'Array8': np.array([]), 'tau': np.array([]),'mdevArray1': np.array([]),'mdevArray2': np.array([]),'mdevArray3': np.array([]),
                    'mdevArray4': np.array([]),'mdevArray5': np.array([]),'mdevArray6': np.array([]),'mdevArray7': np.array([]),'mdevArray8': np.array([]), }
        plt.ion()
        self.f, ((self.ax11,self.ax12), (self.ax21,self.ax22)) = plt.subplots(2,2)


    def get_PTC_log(self):
        list_of_files = os.listdir(self.PTCLogPath)
        self.PTClog = self.PTCLogPath + str(max(list_of_files))


        

    def get_most_recent_logs(self):
        self.get_PTC_log()

    def load_log_data(self):
        data = pd.read_csv(self.PTClog,sep='\t',header=None,usecols=[0,1,2,3,4,5,6,7,8],
                                                            names=['MJD', 'Array1','Array2','Array3','Array4','Array5','Array6','Array7','Array8'])

        #Write data to corresponding numpy arrays
        self.PTCData['MJD'] = (data.MJD.values - data.MJD.values[0])[1:]*86400
        self.PTCData['Array1'] = data.Array1.values[1:]
        self.PTCData['Array2'] = data.Array2.values[1:]
        self.PTCData['Array3'] = data.Array3.values[1:]
        self.PTCData['Array4'] = data.Array4.values[1:]
        self.PTCData['Array5'] = data.Array5.values[1:]
        self.PTCData['Array6'] = data.Array6.values[1:]
        self.PTCData['Array7'] = data.Array7.values[1:]
        self.PTCData['Array8']= data.Array8.values[1:]



    def compute_mDev(self):
        #Compute mod sigma for temperature and frequency fluctuations
        d_rate = 1/((self.PTCData['MJD'][1] - self.PTCData['MJD'][0])) 
        (self.PTCData['tau'], self.PTCData['mdevArray1'], err, n) = allantools.mdev(self.PTCData['Array1'], rate=d_rate, data_type="freq", taus="decade")
        (self.PTCData['tau'], self.PTCData['mdevArray2'], err, n) = allantools.mdev(self.PTCData['Array2'], rate=d_rate,data_type="freq", taus="decade")
        (self.PTCData['tau'], self.PTCData['mdevArray3'], err, n) = allantools.mdev(self.PTCData['Array3'], rate=d_rate,data_type="freq", taus='decade')
        (self.PTCData['tau'], self.PTCData['mdevArray4'], err, n) = allantools.mdev(self.PTCData['Array4'], rate=d_rate, data_type="freq", taus='decade')
        (self.PTCData['tau'], self.PTCData['mdevArray5'], err, n) = allantools.mdev(self.PTCData['Array5'], rate=d_rate, data_type="freq", taus='decade')
        (self.PTCData['tau'], self.PTCData['mdevArray6'], err, n) = allantools.mdev(self.PTCData['Array6'], rate=d_rate, data_type="freq", taus='decade')
        (self.PTCData['tau'], self.PTCData['mdevArray7'], err, n) = allantools.mdev(self.PTCData['Array7'], rate=d_rate,data_type="freq", taus='decade')
        (self.PTCData['tau'], self.PTCData['mdevArray8'], err, n) = allantools.mdev(self.PTCData['Array8'], rate=d_rate,data_type="freq", taus='decade')
    def plot_data(self):
		
        self.ax11.clear()
#        self.ax11.plot(self.PTCData['MJD']/3600/24, self.PTCData['Array1'], label = 'Box (ceiling)')
#        self.ax11.plot(self.PTCData['MJD']/3600/24, self.PTCData['Array2'], label = 'Box (basement)')
#        self.ax11.plot(self.PTCData['MJD']/3600/24, self.PTCData['Array3'], label = 'Sub-mezzanine cold plate')
        self.ax11.plot(self.PTCData['MJD']/3600/24, self.PTCData['Array4'], label = 'Room temperature', color = 'red')
        self.ax11.set_ylabel('Temp (C)')
        self.ax11.set_xlabel('Time (days)')
        self.ax11.grid(True,which='both',ls='-')
        self.ax11.legend()

        #self.ax12.clear()
        #self.ax12.loglog(self.PTCData['tau'], self.PTCData['mdevArray1'], '-o', label = 'Box (ceiling)')
        #self.ax12.loglog(self.PTCData['tau'], self.PTCData['mdevArray2'], '-o', label = 'Box (basement)')
        #self.ax12.loglog(self.PTCData['tau'], self.PTCData['mdevArray3'], '-o', label = 'Sub-mezzanine cold plate')
        #self.ax12.loglog(self.PTCData['tau'], self.PTCData['mdevArray4'], '-o', label = 'Air above controller')
        #self.ax12.set_ylabel(r'$\sigma$ (K)')
        #self.ax12.set_xlabel('Averaging time (s)')
        #self.ax12.grid(True,which='both',ls='-')
        #self.ax12.legend()

        plot_len = len(self.PTCData['tau']) - 8640
        plot_len = 0
        self.ax12.clear()
#        self.ax12.plot((self.PTCData['MJD'][plot_len:] - self.PTCData['MJD'][plot_len] )/3600, self.PTCData['Array1'][plot_len:] - np.mean(self.PTCData['Array1'][plot_len:] ), label = 'Box (ceiling) : ' + str(np.round(np.mean(self.PTCData['Array1']),1)) + r'$ ^\circ C $')
#        self.ax12.plot((self.PTCData['MJD'][plot_len:] - self.PTCData['MJD'][plot_len])/3600, self.PTCData['Array2'][plot_len:] - np.mean(self.PTCData['Array2'][plot_len:]), label = 'Box (basement) : '+ str(np.round(np.mean(self.PTCData['Array2']),1)) + r'$ ^\circ C $')
#        self.ax12.plot((self.PTCData['MJD'][plot_len:]- self.PTCData['MJD'][plot_len])/3600, self.PTCData['Array3'][plot_len:] - np.mean(self.PTCData['Array3'][plot_len:]), label = 'Sub-mezzanine cold plate : ' + str(np.round(np.mean(self.PTCData['Array3']),1)) + r'$ ^\circ C $')
        self.ax12.plot((self.PTCData['MJD'][plot_len:]- self.PTCData['MJD'][plot_len])/3600, self.PTCData['Array4'][plot_len:], label = 'Room temperature : ' + str(np.round(np.mean(self.PTCData['Array4']),1)) + r'$ ^\circ C $', color = 'red')
        #self.ax12.plot((self.PTCData['MJD'][plot_len:]- self.PTCData['MJD'][plot_len])/3600, np.ones(len(self.PTCData['MJD'][plot_len:]))*20.1, label = 'Temperature before flood', color = 'black', linestyle = '--')

        self.ax12.set_ylabel('Temp (C)')
        self.ax12.set_xlabel('Time (hr)')
        self.ax12.grid(True,which='both',ls='-')
        self.ax12.legend() 



        self.ax21.clear()
        self.ax21.plot(self.PTCData['MJD']/3600/24, self.PTCData['Array5'], label = 'Air in box basement')
        self.ax21.plot(self.PTCData['MJD']/3600/24, self.PTCData['Array6'], label = 'Mezzanine south')
        self.ax21.plot(self.PTCData['MJD']/3600/24, self.PTCData['Array7'], label = 'Mezzanine north')
        #self.ax21.plot(self.PTCData['MJD']/3600, self.PTCData['Array8'] - np.mean(self.PTCData['Array8']))
        self.ax21.grid(True,which='both',ls='-')
        self.ax21.set_ylabel('Temp (C)')
        self.ax21.set_xlabel('Time (days)') 

        self.ax21.legend()

#        self.ax22.clear()
#        self.ax22.loglog(self.PTCData['tau'], self.PTCData['mdevArray5'], '-o', label = 'Air in box basement')
#        self.ax22.loglog(self.PTCData['tau'], self.PTCData['mdevArray6'], '-o', label = 'Mezzanine south')
#        self.ax22.loglog(self.PTCData['tau'], self.PTCData['mdevArray7'], '-o', label = 'Mezzanine north')
#        #self.ax22.loglog(self.PTCData['tau'], self.PTCData['mdevArray8'], '-o')
#        self.ax22.set_ylabel(r'$\sigma$ (K)')
#        self.ax22.set_xlabel('Averaging time (s)')
#        self.ax22.grid(True,which='both',ls='-')
#        self.ax22.legend()

        self.ax22.clear()
        self.ax22.plot((self.PTCData['MJD'][plot_len:] - self.PTCData['MJD'][plot_len] )/3600, self.PTCData['Array5'][plot_len:] - np.mean(self.PTCData['Array5'][plot_len:] ), label = 'Air in box basement : ' + str(np.round(np.mean(self.PTCData['Array1']),1)) + r'$ ^\circ C $')
        self.ax22.plot((self.PTCData['MJD'][plot_len:] - self.PTCData['MJD'][plot_len])/3600, self.PTCData['Array6'][plot_len:] - np.mean(self.PTCData['Array6'][plot_len:]), label = 'Mezzanine south : '+ str(np.round(np.mean(self.PTCData['Array2']),1)) + r'$ ^\circ C $')
        self.ax22.plot((self.PTCData['MJD'][plot_len:]- self.PTCData['MJD'][plot_len])/3600, self.PTCData['Array7'][plot_len:] - np.mean(self.PTCData['Array7'][plot_len:]), label = 'Mezzanine north : ' + str(np.round(np.mean(self.PTCData['Array3']),1)) + r'$ ^\circ C $')
        self.ax22.set_ylabel('Temp (C)')
        self.ax22.set_xlabel('Time (hr)')
        self.ax22.grid(True,which='both',ls='-')
        self.ax22.legend() 


        plt.pause(0.01)



if __name__ == "__main__":
    meas = Sr2Mon()
    meas.get_most_recent_logs()
    meas.load_log_data()
    meas.compute_mDev()
    while True:
        try:
            meas.get_most_recent_logs()
            meas.load_log_data()
            meas.compute_mDev()
            meas.plot_data()
            time.sleep(1)
        except KeyboardInterrupt:
            plt.close()
            break
