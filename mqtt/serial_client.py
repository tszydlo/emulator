import serial
import time


class SerialClient():
    def __init__(self, port):
        self.callbacks_register = {}
        self.ser = serial.Serial(port, 38400, timeout=1)
        #it is necessary because otherwise it resets arduino
        time.sleep(5)

    def publish(self, message):
        self.ser.write(message)
        self.ser.flush()
        print(message)
