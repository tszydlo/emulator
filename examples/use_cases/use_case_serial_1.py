from scenario_engine.executor import every, start_executing
from mqtt.serial_client import SerialClient
from virtual_devices.vGPIO_Sensor import vGPIO_Sensor, vGPIO_SensorState

#we are using virtualized sensors on Arduino connected via USB
s_client = SerialClient("COM9")
#virtual wiring - virtual switch with ID=1 is exposed on pin PD13
switch1 = vGPIO_Sensor(1, "PD13", s_client)
#virtual wiring - virtual BME280 sensor with ID=2 is exposed on pin PD4 and PD5
#TBD

@every(start=1, seconds=2)
def event_on():
    switch1.set_state_v(vGPIO_SensorState.ON)


@every(start=0, seconds=2)
def event_off():
    switch1.set_state_v(vGPIO_SensorState.OFF)


if __name__ == '__main__':
    start_executing()
