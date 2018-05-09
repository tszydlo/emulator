import math

from scenario_engine.executor import every, start_executing, executor
from mqtt.serial_client import SerialClient
from virtual_devices.vBME280 import vBME280
from virtual_devices.vGPIO_Sensor import vGPIO_Sensor, vGPIO_SensorState

#we are using virtualized sensors on Arduino connected via USB
s_client = SerialClient("COM4")
#virtual wiring - virtual BME280 sensor with ID=2 is exposed on I2C bus (pin PD4 and PD5)
env_sensor = vBME280(1,s_client)
#virtual wiring - virtual switch with ID=1 is exposed on pin PD13
switch1 = vGPIO_Sensor(2, "PD13", s_client)

@every(start=1, seconds=3)
def event_on():
    switch1.set_state_v(vGPIO_SensorState.ON)

@every(start=0, seconds=3)
def event_off():
    switch1.set_state_v(vGPIO_SensorState.OFF)

@every(start=2, seconds=3)
def generator_step():
    tt = executor.get_time()
    print("---------")
    env_sensor.set_temp_v(math.sin((tt % 60) / 60.0 * 2 * 3.14)*10 + 20 )
    env_sensor.set_pressure_v(math.cos((tt % 60) / 60.0 * 2 * 3.14) * 10 + 950)
    env_sensor.set_humidity_v(math.sin((tt % 60) / 60.0 * 2 * 3.14) * 40 + 50)


if __name__ == '__main__':
    start_executing()
