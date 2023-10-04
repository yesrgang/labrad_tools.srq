from yoctopuce.yocto_api import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_humidity import *
from yoctopuce.yocto_pressure import *
import time

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error :" + errmsg.value)

#serial_number = 'METEOMK1-BA853'

#m = YModule.FindModule(serial_number)
#m.set_luminosity(0)

while True:
    labels = ['temperature', 'pressure', 'humidity']
    output = []

    t = YTemperature.FirstTemperature()
    temp = t.get_currentRawValue()
    output.append(temp)
    print(temp)

    p = YPressure.FirstPressure()
    press = p.get_currentRawValue()
    output.append(press)
    print(press)

    h = YHumidity.FirstHumidity()
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

    time.sleep(10)


