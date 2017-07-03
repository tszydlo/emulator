from emulator.executor import emit_event


class LED_V():
    device_topic = "fogdevicesplatform/fog_device_%d/slave/GPIO/%d"

    def __init__(self, dev, gpio_pin, mqtt_client, event):
        self.dev = dev
        self.event = event
        self.adc_pin = gpio_pin
        self.state = 0
        self.mqtt_client = mqtt_client

        self.mqtt_client.register(self.event, self.listener)

    def listener(self):
        emit_event(self.device_topic)

    def get_state_v(self):
        return self.state
