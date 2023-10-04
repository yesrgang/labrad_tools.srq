from datetime import datetime
import dateutil.tz
import socket
import re
#from influxdb import InfluxDBClient
import pyvisa
import os
import numpy as np
import time
from astropy.time import Time
#import math
import socket

# COMMUNICATE WITH INSTRUMENT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect(('192.168.1.85', 23))



filepath = os.path.normpath("Z:/SrQ/temp_data_DC/") #Save directory
fileMonth = int(time.strftime("%m",time.localtime()))
fileName = 'PTC'+time.strftime("%Y-%m-%d",time.localtime())+'.dat' # Date string for data file
fileName = os.path.join(filepath,fileName)
seconds = 0.0
#datafile = open(fileName,'a+')

print("Logging Temperature data from PTC10.  Type Ctrl-C to stop...")

channels = [0, 1]

while True:
    try:
        #Start new log file each month
        fileMonth = int(time.strftime("%m",time.localtime()))
        current_file = str(max(os.listdir(filepath)))
        if fileMonth > int(current_file[9:10:]):
            #datafile.close()
            #Create new file at the start of each day
            fileMonth = int(time.strftime("%d",time.localtime()))
            fileName = 'PTC'+time.strftime("%Y-%m-%d",time.localtime())+'.dat' # Date string for data file
            fileName = os.path.join(filepath,fileName)
            datafile = open(fileName,'a+')
        else:
            fileName = os.path.join(filepath, current_file)
            datafile = open(fileName, 'a+')

        #Get data from PTC
        
        try:     
            s.send('getOutput\n'.encode())
            _output = s.recv(1024)
            _output = _output.decode("utf-8")
            _output = _output.split(',')
            #print(_output)
            output = _output[:4]
            #print(output)
            output = [float(i) for i in output]
            #voltages = output[0::5]
            #channels = output[3::5]
            #for v,c in zip(voltages,channels):
            #    channelData[int(c)] = float(v)
            seconds = seconds+5.0
            t = Time(datetime.utcnow())
            MJD = t.mjd  #Use MJD format to agree with Dan's LabView code (add rounding???)
            datafile.write('%f\t' %(MJD))
            for i in range(len(output)):
                datafile.write('%.6e\t' %output[i])
            datafile.write('\n')
            datafile.flush()
            time.sleep(10)
        except ConnectionResetError as e:
            print('Error!')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect(('192.168.1.85', 23))
        #except BrokenPipeError as e:
        #    print('Error!')
    except KeyboardInterrupt:
        s.close()
        datafile.close()
