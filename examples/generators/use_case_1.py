import math

from emulator.executor import every, executor, start_executing
from virtual_devices.lm35_v import LM35_V
from virtual_devices.mqtt_client import MQTTClient


client1 = MQTTClient("149.156.100.177")

sensor1 = LM35_V(1, 0, client1)
sensor2 = LM35_V(2, 0, client1)

@every(start=1, seconds=1)
def generator_step():
    tt = executor.get_time()
    print("---------")
    sensor1.set_temp_v(math.sin((tt % 60) / 60.0 * 2 * 3.14))
    sensor2.set_temp_v(math.cos((tt % 60) / 60.0 * 2 * 3.14))

if __name__ == '__main__':
    start_executing()





