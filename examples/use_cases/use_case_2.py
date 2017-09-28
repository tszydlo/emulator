from scenario_engine.executor import every, start_executing
from mqtt.mqtt_client import MQTTClient
from virtual_devices.switch_v import Switch_V, SwitchState

client1 = MQTTClient("149.156.100.177")
switch1 = Switch_V(2, 3, client1)

"""
Example shows simple periodical on/off switching of virtual switch. Consecutive state changes are send each 1 second.
"""


@every(start=1, seconds=2)
def event_on():
    switch1.set_state_v(SwitchState.ON)


@every(start=0, seconds=2)
def event_off():
    switch1.set_state_v(SwitchState.OFF)


if __name__ == '__main__':
    start_executing()
