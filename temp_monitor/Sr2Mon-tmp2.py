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

class Sr2Mon():
    def __init__(self):
        self.PTCLogPath = "Z:\\SrQ\\temp_data\\"
        self.PTCLog = '' 
	#Initialize data dictionaries
        self.PTCData = {'MJD': np.array({}),'seconds': np.array([]),  'Array1': np.array([]),'Array2': np.array([]),'Array3': np.array([]),'Array4': np.array([]),'Array5': np.array([]),
                    'Array6': np.array([]),'Array7': np.array([]),'Array8': np.array([]), 'tau': np.array([]),'mdevArray1': np.array([]),'mdevArray2': np.array([]),'mdevArray3': np.array([]),
                    'mdevArray4': np.array([]),'mdevArray5': np.array([]),'mdevArray6': np.array([]),'mdevArray7': np.array([]),'mdevArray8': np.array([]), }
        self.PTCDCLogPath = "Z:\\SrQ\\temp_data_DC\\"
        
        self.PTCDCLog = '' 
        self.PTCDCData = {'MJD': np.array({}),'seconds': np.array([]),  'Array1': np.array([]),  'Array2': np.array([]),   'Array3': np.array([])}

        #self.KTHLog = '' 
        #self.KTHData = {'MJD': np.array({}),'seconds': np.array([]),  'Array1': np.array([]) }
        #self.KTHbeta = 3943
        #self.KTHT0 = 25 + 273.15
        #self.KTHR0 = 30e3
        plt.ion()
        self.f, self.ax11 = plt.subplots(1, 1)
        


    def get_PTC_log(self):
        list_of_files = os.listdir(self.PTCLogPath)
        sorted_files = sorted(list_of_files)
        self.PTClog = self.PTCLogPath + str(max(list_of_files))

    def get_PTCDC_log(self):
        list_of_files = os.listdir(self.PTCDCLogPath)
        sorted_files = sorted(list_of_files)
        self.PTCDClog = self.PTCDCLogPath + str(max(list_of_files))
        #print(self.PTCDClog)

#    def get_KTH_log(self):
#        list_of_files = os.listdir(self.KTHLogPath)
#        self.KTHlog = self.KTHLogPath + str(max(list_of_files))    

    def get_most_recent_logs(self):
        self.get_PTC_log()
        #self.get_KTH_log()
        self.get_PTCDC_log()

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

        #KTHdata = pd.read_csv(self.KTHlog,sep='\t',header=None,usecols=[0,1],
        #                                                    names=['MJD', 'Array1'])
        #self.KTHData['MJD'] = (KTHdata.MJD.values - KTHdata.MJD.values[0])[1:]*86400
        #self.KTHData['Array1'] = (np.log(KTHdata.Array1.values[1:]/self.KTHR0)/self.KTHbeta + 1./self.KTHT0)**-1 - 273.15

        
        #self.KTHData['MJD'] = (KTHdata.MJD.values - data.MJD.values[0])[1:]*86400
        #self.KTHData['Array1'] = (np.log(KTHdata.Array1.values[1:]/self.KTHR0)/self.KTHbeta + 1./self.KTHT0)**-1 - 273.15
        
        PTCDCData = pd.read_csv(self.PTCDClog,sep='\t',header=None,usecols=[0,1,2,3],
                                                            names=['MJD', 'Array1','Array2','Array3'])

        #Write data to corresponding numpy arrays
        self.PTCDCData['MJD'] = (PTCDCData.MJD.values - PTCDCData.MJD.values[0])[1:]*86400
        self.PTCDCData['Array1'] = PTCDCData.Array1.values[1:]
        self.PTCDCData['Array2'] = PTCDCData.Array2.values[1:]
        self.PTCDCData['Array3'] = PTCDCData.Array3.values[1:]



#    def compute_mDev(self):
#        #Compute mod sigma for temperature and frequency fluctuations
#        d_rate = 1/((self.PTCData['MJD'][1] - self.PTCData['MJD'][0])) 
#        (self.PTCData['tau'], self.PTCData['mdevArray1'], err, n) = allantools.mdev(self.PTCData['Array1'], rate=d_rate, data_type="freq", taus="decade")
#        (self.PTCData['tau'], self.PTCData['mdevArray2'], err, n) = allantools.mdev(self.PTCData['Array2'], rate=d_rate,data_type="freq", taus="decade")
#        (self.PTCData['tau'], self.PTCData['mdevArray3'], err, n) = allantools.mdev(self.PTCData['Array3'], rate=d_rate,data_type="freq", taus='decade')
#        (self.PTCData['tau'], self.PTCData['mdevArray4'], err, n) = allantools.mdev(self.PTCData['Array4'], rate=d_rate, data_type="freq", taus='decade')
#        (self.PTCData['tau'], self.PTCData['mdevArray5'], err, n) = allantools.mdev(self.PTCData['Array5'], rate=d_rate, data_type="freq", taus='decade')
#        (self.PTCData['tau'], self.PTCData['mdevArray6'], err, n) = allantools.mdev(self.PTCData['Array6'], rate=d_rate, data_type="freq", taus='decade')
#        (self.PTCData['tau'], self.PTCData['mdevArray7'], err, n) = allantools.mdev(self.PTCData['Array7'], rate=d_rate,data_type="freq", taus='decade')
#        (self.PTCData['tau'], self.PTCData['mdevArray8'], err, n) = allantools.mdev(self.PTCData['Array8'], rate=d_rate,data_type="freq", taus='decade')
    def plot_data(self):
		

        self.ax11.clear()
        self.ax11.plot(self.PTCDCData['MJD']/3600/24, self.PTCDCData['Array1'], label = 'Distribution center outside air: ' + str(np.round(np.nanmean(self.PTCDCData['Array1']),1)) + r'$ ^\circ C $' , alpha = .8)
        self.ax11.plot(self.PTCDCData['MJD']/3600/24, self.PTCDCData['Array2'], label = 'Distribution center outside box: ' + str(np.round(np.nanmean(self.PTCDCData['Array2']),1)) + r'$ ^\circ C $' , alpha = .8)
        self.ax11.plot(self.PTCDCData['MJD']/3600/24, self.PTCDCData['Array3'], label = r'Distribution center Sr2 $\phi$: ' + str(np.round(np.nanmean(self.PTCDCData['Array3']),1)) + r'$ ^\circ C $' , alpha = .8)

        #self.ax21.plot(self.PTCData['MJD']/3600, self.PTCData['Array8'] - np.mean(self.PTCData['Array8']))
        self.ax11.grid(True,which='both',ls='-')
        self.ax11.set_ylabel('Temp (C)')
        self.ax11.set_xlabel('Time (days)') 

        self.ax11.legend(fontsize = 10)

#        self.ax22.clear()
#        self.ax22.loglog(self.PTCData['tau'], self.PTCData['mdevArray5'], '-o', label = 'Air in box basement')
#        self.ax22.loglog(self.PTCData['tau'], self.PTCData['mdevArray6'], '-o', label = 'Mezzanine south')
#        self.ax22.loglog(self.PTCData['tau'], self.PTCData['mdevArray7'], '-o', label = 'Mezzanine north')
#        #self.ax22.loglog(self.PTCData['tau'], self.PTCData['mdevArray8'], '-o')
#        self.ax22.set_ylabel(r'$\sigma$ (K)')
#        self.ax22.set_xlabel('Averaging time (s)')
#        self.ax22.grid(True,which='both',ls='-')
#        self.ax22.legend()



        plt.pause(0.01)



if __name__ == "__main__":
    meas = Sr2Mon()
    meas.get_most_recent_logs()
    meas.load_log_data()
    #meas.compute_mDev()
    while True:
        try:
            meas.get_most_recent_logs()
            meas.load_log_data()
            #meas.compute_mDev()
            meas.plot_data()
            time.sleep(10)
        except KeyboardInterrupt:
            plt.close()
            break
