from emulator.executor import start_executing, every_event
from virtual_devices.led_v import LED_V
from virtual_devices.mqtt_client import MQTTClient

# client1 = MQTTClient("149.156.100.177")
client1 = MQTTClient("fogdevices.agh.edu.pl")
led1 = LED_V(1, 0, client1, "led/event/1")
led2 = LED_V(1, 1, client1, "led/event/2")
led3 = LED_V(1, 2, client1, "led/event/3")

leds = {"led/event/1": led1, "led/event/2": led2, "led/event/3": led3}


# scenario spawning events for testing purposes
# @every(seconds=2)
# def steps():
#     print("EVENT 3 emited")
#     emit_event("led/event/3")
#
#
# @every(start=1, seconds=2)
# def steps():
#     print("EVENT 1 emited")
#     emit_event("led/event/1")

# ##################################################

# actual scenario
@every_event(event='led/event/+')
def led_notification(event):
    print("State of the LED %s is %d" % (event, (leds[event].get_state_v())))


if __name__ == '__main__':
    client1.mqttc.subscribe('#')
    start_executing()
