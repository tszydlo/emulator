from scenario_engine.executor import start_executing, every_event, every
from simulation_entities.temp_simulation_2d_world import TempSimulation2DWorld
from virtual_devices.led_v import LED_V
from virtual_devices.lm35_v import LM35_V
from mqtt.mqtt_client import MQTTClient

import matplotlib.pyplot as plt
import numpy as np

client1 = MQTTClient("127.0.0.1")

# devices
led1 = LED_V(1, 0, client1, "heater/event/1")
sensor1 = LM35_V(1, 0, client1)

# simulation models
world = TempSimulation2DWorld()

# actual scenario
@every_event(event=TempSimulation2DWorld.ITERATION_COMPLETED)
def temp_update(event):
    sensor1.set_temp_v(world.space[24][24].vector.temperature)
    print("*")

@every_event(event='heater/event/+')
def heater_state_notification(event):
    if (led1.get_state_v() == 1):
        heater1 = TempSimulation2DWorld.Heater(size=10, max_temperature=150, bottom_left_x=30, bottom_left_y=20)
        world.heaters.append(heater1)
        world.place_heaters()
        print("heater added")
    else:
        print("heater removed")
        world.heaters.clear()
        world.is_heater_map.clear()

@every(seconds=5)
def plotting():

    # TODO: Fix async handler exception during plot redrawing
    plt.figure()
    plt.pcolormesh(np.array([[world.space[j][i].vector.temperature for i in range(world.length)]
                                   for j in range(world.width)]), cmap='jet')
    plt.colorbar()
    plt.show()

if __name__ == '__main__':
    start_executing()
    print("A")
    world.start_transformation()
    print("B")
