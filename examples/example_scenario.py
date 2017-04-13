# init of test scenario
from datetime import time
from time import sleep

from scenario.executor import after, every, start_world
from simulation_entities.sensor import HumiditySensor

humidity_sensor = HumiditySensor()
humidity_sensor2 = HumiditySensor()


# scenario of the test
@after(seconds=4)
def steps():
    print("Apply new function after 4 seconds")
    humidity_sensor.apply_formula(lambda x: x ** 2)


@after(seconds=1)
def steps():
    print("Some task after 1 second")


@every(seconds=2)
def steps():
    print("humidity: " + str(humidity_sensor.get_measurement()))


@every(seconds=5)
def steps():
    print("Some other humidity: " + str(humidity_sensor2.get_measurement()))


@after(seconds=11)
def steps():
    print("Some task after 11 seconds")


@every(start=15, seconds=5)
def steps():
    print("Some task after 5 seconds staring at 15 seconds")

sleep(15)
start_world()