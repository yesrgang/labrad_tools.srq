from yoctopuce.yocto_api import *
from yoctopuce.yocto_accelerometer import *
from yoctopuce.yocto_magnetometer import *
from yoctopuce.yocto_tilt import *
import time

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error :" + errmsg.value)

sn = 'Y3DMK002-247383'

#m = YModule.FindModule(serial_number)
#m.set_luminosity(0)

while True:
    labels = ['B1', 'B2', 'B3']
    output = []
    
    #anytilt = YTilt.FirstTilt()
    #m = anytilt.get_module()
    #sn = m.get_serialNumber() 
    #print(m.get_serialNumber())

    m = YMagnetometer.FindMagnetometer(sn + '.magnetometer')
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


