class vBME280():
    device_message = "F|%d|%s\n"
    device_create_message = "C|%d|BME280\n"


    def __init__(self, id, serial_client):
        self.id = id
        self.serial_client = serial_client

        self.serial_client.publish((self.device_create_message % (self.id)).encode())

    def set_temp_v(self, temp_v):
        self.temperature = temp_v
        self.send_temperature()

    def set_humidity_v(self, hum_v):
        self.humidity = hum_v
        self.send_humidity()

    def set_pressure_v(self, press_v):
        self.pressure = press_v
        self.send_pressure()

    def send_temperature(self):
        self.serial_client.publish((self.device_message % (self.id,"T"+str(self.temperature))).encode())

    def send_pressure(self):
        self.serial_client.publish((self.device_message % (self.id,"P"+str(self.pressure))).encode())

    def send_humidity(self):
        self.serial_client.publish((self.device_message % (self.id,"H"+str(self.humidity))).encode())
