from emulator.executor import start_executing, every_event
from virtual_devices.led_v import LED_V
from virtual_devices.mqtt_client import MQTTClient

client1 = MQTTClient("149.156.100.177")
led1 = LED_V(1, 0, client1, "led/event/1")
led2 = LED_V(1, 1, client1, "led/event/2")
led3 = LED_V(1, 2, client1, "led/event/3")

leds = {"led/event/1": led1, "led/event/2": led2, "led/event/3": led3}

# TODO:
@every_event(event="led/event/+")
def led_notification():
    event = "TODO"
    print("State of the LED id " + leds[event].get_state_v())


if __name__ == '__main__':
    start_executing()
