from enum import Enum


class vGPIO_SensorState(Enum):
    ON = 1
    OFF = 2


class vGPIO_Sensor():
    device_message = "F|%d|%d\n"
    device_create_message = "C|%d|GPIOS|%s\n"


    def __init__(self, id, pin, serial_client):
        self.id = id
        self.pin = pin
        self.serial_client = serial_client
        self.state = vGPIO_SensorState.OFF

        self.serial_client.publish((self.device_create_message % (self.id, self.pin)).encode())

    def set_state_v(self, state):
        if self.state != state:
            self.state = state
            self.send_state()
        else:
            self.state = state

    def send_state(self):
        self.serial_client.publish((self.device_message % (self.id,0 if self.state == vGPIO_SensorState.OFF else 1)).encode())

