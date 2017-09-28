from pynput import keyboard

from mqtt.mqtt_client import MQTTClient
from virtual_devices.switch_v import Switch_V, SwitchState

client1 = MQTTClient("149.156.100.177")
switch1 = Switch_V(2, 3, client1)
switch2 = Switch_V(2, 4, client1)
switch3 = Switch_V(2, 5, client1)

switches = [switch1, switch2, switch3]

#TODO: test it and fix

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        switches[int(key.char)].set_state_v(SwitchState.ON)
    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):
    print('{0} released'.format(key))
    # switches[key].set_state_v(SwitchState.OFF)

    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
