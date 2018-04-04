from scenario_engine.executor import every, start_executing
from mqtt.mqtt_client import MQTTClient
from virtual_devices.button_v import ButtonV, ButtonState

client1 = MQTTClient("149.156.100.177")
switch1 = ButtonV(2, 3, client1)

"""
Example shows simple periodical on/off switching of virtual button. Consecutive state changes are send each 1 second.
"""


@every(start=1, seconds=2)
def event_on():
    switch1.set_state_v(ButtonState.ON)


@every(start=0, seconds=2)
def event_off():
    switch1.set_state_v(ButtonState.OFF)


if __name__ == '__main__':
    start_executing()
