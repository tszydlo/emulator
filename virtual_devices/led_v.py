from scenario_engine.executor import emit_event


class LED_V():
    device_topic = "fogdevicesplatform/fog_device_%d/slave/GPIO/%d"

    def __init__(self, dev, gpio_pin, mqtt_client, event):
        self.dev = dev
        self.event = event
        self.adc_pin = gpio_pin
        self.state = 0
        self.mqtt_client = mqtt_client

        self.mqtt_client.register(self.device_topic % (self.dev, self.adc_pin), self.listener)

    def listener(self,msg):
        #print("message is -> "+str(msg.payload))
        emit_event(self.event)
        #print("event is -> "+ self.event)
        self.state = int(msg.payload)

    def get_state_v(self):
        return self.state
