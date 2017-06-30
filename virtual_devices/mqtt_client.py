import paho.mqtt.client as paho


class MQTTClient():

    def __init__(self, broker_host):
        self.mqttc = paho.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.connect(broker_host, 1883, 60)

    @staticmethod
    def convert_from_celsius(t):
        return int((t / 500.0) * 1023.0)

    @staticmethod
    def on_connect(mqttc, obj, rc):
        print("rc: " + str(rc))

    @staticmethod
    def on_message(mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    @staticmethod
    def on_publish(mqttc, obj, mid):
        print("mid: " + str(mid))

    @staticmethod
    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    @staticmethod
    def on_log(self, mqttc, obj, level, string):
        print(string)
