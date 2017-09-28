from scenario_engine.executor import start_executing, every_event
from virtual_devices.led_v import LED_V
from mqtt.mqtt_client import MQTTClient

client1 = MQTTClient("iot.eclipse.org")

led1 = LED_V(1, 0, client1, "led/event/1")
led2 = LED_V(1, 1, client1, "led/event/2")
led3 = LED_V(1, 2, client1, "led/event/3")

leds = {"led/event/1": led1, "led/event/2": led2, "led/event/3": led3}

"""
Example shows reversed action: information about state is being forwarded from virtual device to observers and not the 
other way around. The MQTT topic pattern usage for event matching is presented. One observer is catching all led events
using '+' wildcard and then reads state of the led which has sent the event. 
"""


@every_event(event='led/event/+')
def led_notification(event):
    print("State of the LED %s is %d" % (event, (leds[event].get_state_v())))


if __name__ == '__main__':
    start_executing()
