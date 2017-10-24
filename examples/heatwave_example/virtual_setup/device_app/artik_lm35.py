import requests
import pprint
import time
import sys
from upm import pyupm_lm35 as sensorObj
import mraa

artikcloud = "https://api.artik.cloud/v1.1/messages"
bearer = ''
sdid = ''

if len(sys.argv) == 3:
    bearer = 'Bearer ' + sys.argv[1]
    sdid = sys.argv[2]

    print(bearer +" "+ sdid)

else:
    print("Usage: temp_client.py [token] [device_id]")
    sys.exit(0)

headers_dict =  {
     "Content-Type": "application/json",
     "Authorization": bearer
   }

sensor = sensorObj.LM35(0)

led1 = mraa.Gpio(0)
led1.dir(mraa.DIR_OUT)

while True:
    led1.write(1)
    temp = int(sensor.getTemperature())
    print("Temperature:", temp , "C")
    data_dict = ' {"sdid": "' + sdid + '","type": "message","data": {"temperature": "'+str(temp)+'" } }'
    r = requests.post(artikcloud, headers = headers_dict, data=data_dict)
    #pprint.pprint(r.headers)
    pprint.pprint(r.content)
    time.sleep(10)

