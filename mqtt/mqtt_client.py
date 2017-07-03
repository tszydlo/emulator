import paho.mqtt.client as paho


class MQTTClient():

    def __init__(self, broker_host):
        self.callbacks_register = {}
        self.mqttc = paho.Client("", True, None, paho.MQTTv31)
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.connect(broker_host, 1883, 60)
        self.mqttc.loop_start()

    def register(self, device_topic, callback):
        self.mqttc.subscribe(device_topic)
        self.callbacks_register[device_topic] = callback

    @staticmethod
    def on_connect(mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    def on_message(self, mqttc, obj, msg):
        if msg.topic in self.callbacks_register.keys():
            self.callbacks_register[msg.topic](msg)
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    @staticmethod
    def on_publish(mqttc, obj, mid):
        print("mid: " + str(mid))

    @staticmethod
    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("Connected")
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

