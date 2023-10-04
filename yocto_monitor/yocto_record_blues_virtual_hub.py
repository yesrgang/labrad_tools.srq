from yoctopuce.yocto_api import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_humidity import *
from yoctopuce.yocto_pressure import *
from yoctopuce.yocto_magnetometer import *
from yoctopuce.yocto_accelerometer import *
import time

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error :" + errmsg.value)

serial_number_1 = 'METEOMK1-BA853'
serial_number_2 = 'Y3DMK002-247383'


#m = YModule.FindModule(serial_number)
#m.set_luminosity(0)

while True:
    labels = ['temperature', 'pressure', 'humidity']
    output = []

    t = YTemperature.FindTemperature(serial_number_1 + '.temperature')
    temp = t.get_currentRawValue()
    output.append(temp)
    print(temp)

    p = YPressure.FindPressure(serial_number_1 + '.pressure')
    press = p.get_currentRawValue()
    output.append(press)
    print(press)

    h = YHumidity.FindHumidity(serial_number_1 + '.humidity')
    humid = h.get_currentRawValue()
    output.append(humid)
    print(humid)

    records=[
            {
            "measurement": "Sr2_yocto_blues",
            "tags": {"Name": labels},
            "fields": {"Value": output}
            #"time": datetime.now()
            }
        ]
    print(records)

    token = 'yelabtoken'
    org = 'yelab'
    bucket = 'data_logging'


    with InfluxDBClient(url="http://yesnuffleupagus.colorado.edu:8086", token=token, org=org, debug=False) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            for i in range(len(output)):
                write_api.write(bucket, org, "Sr2_yocto_blues,Channel=" + str(labels[i]) +  " Value=" + str(output[i]))
            client.close()



    labels = ['B1', 'B2', 'B3']
    output = []
    
    #anytilt = YTilt.FirstTilt()
    #m = anytilt.get_module()
    #sn = m.get_serialNumber() 
    #print(m.get_serialNumber())

    m = YMagnetometer.FindMagnetometer(serial_number_2 + '.magnetometer')
    m1 = m.get_xValue()
    m2 = m.get_yValue()
    m3 = m.get_zValue()
    output.append(m1)
    print(m1)
    output.append(m2)
    print(m2)
    output.append(m3)
    print(m3)



    records=[
            {
            "measurement": "Sr2_yocto_mag",
            "tags": {"Name": labels},
            "fields": {"Value": output}
            #"time": datetime.now()
            }
        ]
    print(records)

    token = 'yelabtoken'
    org = 'yelab'
    bucket = 'data_logging'


    with InfluxDBClient(url="http://yesnuffleupagus.colorado.edu:8086", token=token, org=org, debug=False) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            for i in range(len(output)):
                write_api.write(bucket, org, "Sr2_yocto_mag,Channel=" + str(labels[i]) +  " Value=" + str(output[i]))
            client.close()

    time.sleep(10)


    labels = ['A1', 'A2', 'A3']
    output = []
    
    #anytilt = YTilt.FirstTilt()
    #m = anytilt.get_module()
    #sn = m.get_serialNumber() 
    #print(m.get_serialNumber())

    a = YAccelerometer.FindAccelerometer(serial_number_2 + '.accelerometer')
    a1 = a.get_xValue()
    a2 = a.get_yValue()
    a3 = a.get_zValue()
    output.append(a1)
    print(a1)
    output.append(a2)
    print(a2)
    output.append(a3)
    print(a3)



    records=[
            {
            "measurement": "Sr2_yocto_acc",
            "tags": {"Name": labels},
            "fields": {"Value": output}
            #"time": datetime.now()
            }
        ]
    print(records)

    token = 'yelabtoken'
    org = 'yelab'
    bucket = 'data_logging'


    with InfluxDBClient(url="http://yesnuffleupagus.colorado.edu:8086", token=token, org=org, debug=False) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            for i in range(len(output)):
                write_api.write(bucket, org, "Sr2_yocto_acc,Channel=" + str(labels[i]) +  " Value=" + str(output[i]))
            client.close()

    time.sleep(10)


