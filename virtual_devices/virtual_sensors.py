class LM35_V():
    device_topic = "fogdevicesplatform/fog_device_%d/slave/ADC/%d"

    def __init__(self, dev, adc_pin, mqtt_client, position=None, world=None):
        self.position = position
        self.world = world
        self.dev = dev
        self.adc_pin = adc_pin
        self.temperature = None
        self.mqtt_client = mqtt_client

    def send_temperature(self):
        self.mqtt_client.mqttc.publish(self.device_topic % (self.dev, self.adc_pin), self.temperature, 0, True)

    def get_temperature_form_world(self):
        if self.world is not None:
            return self.world.space[self.position[0]][self.position[1]].vector.temperature
        else:
            return None
