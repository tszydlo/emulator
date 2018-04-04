from enum import Enum


class ButtonState(Enum):
    ON = 1
    OFF = 2


class ButtonV:
    device_topic = "fogdevicesplatform/fog_device_%d/slave/GPIO/%d"

    def __init__(self, dev, gpio_pin, mqtt_client):
        self.dev = dev
        self.gpio_pin = gpio_pin
        self.state = ButtonState.OFF
        self.mqtt_client = mqtt_client

    def set_state_v(self, state):
        if self.state != state:
            self.state = state
            self.send_state()
        else:
            self.state = state

    def send_state(self):
        self.mqtt_client.mqttc.publish(self.device_topic % (self.dev, self.gpio_pin),
                                       0 if self.state == ButtonState.OFF else 1, 0, True)
