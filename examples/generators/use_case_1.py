import math

from scenario.executor import every, executor, start_executing



# time1 = time2 = time3 = time.time()
# print(time1)
#
# @every(start=1, seconds=1)
# def test1():
# global time1
#     time1 = time.time()
#     print("%f %f %f" % (time1 - time2, time2 - time3, time3 - time1))
#     pass
#
#
# @every(start=1, seconds=1)
# def test2():
#     global time2
#     time2 = time.time()
#     pass
#
#
# @every(start=1, seconds=1)
# def test3():
#     global time3
#     time3 = time.time()
#     pass
from virtual_devices.MQTTClient import MQTTClient
from virtual_devices.virtual_sensors import LM35_V


@every(start=1, seconds=1)
def generator_step():
    tt = executor.get_time()
    print("---------")
    print(math.sin((tt % 60) / 60.0 * 2 * 3.14))
    print(math.cos((tt % 60) / 60.0 * 2 * 3.14))


if __name__ == '__main__':
    start_executing()

    client1 = MQTTClient("iot.eclipse.org")

    sensor1 = LM35_V(1, 0, client1)
    sensor2 = LM35_V(2, 0, client1)



