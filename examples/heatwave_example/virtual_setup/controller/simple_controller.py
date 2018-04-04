#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.

import sys
import mosquitto
import time
import thread

def on_connect(mqttc, obj, rc):
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

	
def io_thread():
    temp1=0
    dt1=1
    temp2=0
    while True:
        temp1 = temp1 + dt1
        if temp1 > 99:
            dt1=-1
        elif temp1<1:
            dt1=1
        temp2=100-temp1
        mqttc.publish(device1_topic, str(temp1*2), 0, True) 
        mqttc.publish(device2_topic, str(temp2*2), 0, True) 
        time.sleep(1)
	
# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mosquitto.Mosquitto() 
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
#mqttc.connect("127.0.0.1", 1883, 60)

# setting testament for that client
#mqttc.will_set("temp/floor1/room1/pref1", "broken", 0, True)

mqttc.connect("iot.eclipse.org", 1883, 60)

# publishing message on topic with QoS 0 and the message is not Retained
# mqttc.publish("temp/floor1/room1/pref1", "20", 0, False)

device1_topic="fogdevicesplatform/fog_device_1/slave/ADC/0"
device2_topic="fogdevicesplatform/fog_device_2/slave/ADC/0"

thread.start_new_thread( io_thread,() )  

mqttc.loop_forever()
 