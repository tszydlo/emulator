from pynput import keyboard

from mqtt.mqtt_client import MQTTClient
from virtual_devices.button_v import ButtonV, ButtonState

client1 = MQTTClient("fogdevices.agh.edu.pl")
button_1 = ButtonV(2, 3, client1)
button_2 = ButtonV(2, 4, client1)
button_3 = ButtonV(2, 5, client1)

buttons = [button_1, button_2, button_3]

"""
Example shows simple simulation of button pressing/releasing in reaction for keyboard pressing. Pressing 0,1,2 keys 
triggers event for appropriate buttons. When button state changes, mqtt message is generated. Scenario decorators are
not used in this example.
"""


def on_press(key):
    if hasattr(key, 'char') and key.char in ['0', '1', '2']:
        print('alphanumeric key {0} pressed'.format(key.char))
        buttons[int(key.char)].set_state_v(ButtonState.ON)
    elif key == keyboard.Key.esc:
        return False
    else:
        print('special key {0} pressed'.format(key))


def on_release(key):
    print('{0} released'.format(key))
    if hasattr(key, 'char') and key.char in ['0', '1', '2']:
        print('alphanumeric key {0} pressed'.format(key.char))
        buttons[int(key.char)].set_state_v(ButtonState.OFF)

    elif key == keyboard.Key.esc:
        return False


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
