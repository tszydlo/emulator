from time import sleep

#from virtual_devices import MQTTClient
from examples.heatwave_example.entities import World
from scenario.executor import after, every_event, every, start_executing, emit_event, on_event, queues_dictionary
import matplotlib.pyplot as plt
import numpy as np

world = World()
#client1 = MQTTClient.LM35_V(1, 0, (25, 20), world)
#client2 = MQTTClient.LM35_V(2, 0, (25, 30), world)



@every_event(event=World.ITERATION_COMPLETED)
def function1():
    iteration = world.iteration_counter
    if iteration == 101:
        emit_event("hundred_reached")
    if iteration  == 300:
        emit_event("three_hundred_reached")
    print("Iteration has completed: " + str(world.iteration_counter))


# @every(start=5, seconds=5)
# def function2():
#     temp1 = client1.get_temperature()
#     print("TEMP1" + str(temp1))
#     temp2 = client2.get_temperature()
#     print("TEMP2" + str(temp2))
#     client1.send_temperature(client1.convert_from_celsius(temp1))
#     client2.send_temperature(client2.convert_from_celsius(temp2))
#     print("Clients done")


@on_event(event="hundred_reached")
def function3():
    print("Heater added")
    heater1 = World.Heater(size=10, max_temperature=150, bottom_left_x=30, bottom_left_y=20)
    world.heaters.append(heater1)
    world.place_heaters()

@on_event(event="three_hundred_reached")
def function4():
    print("Heaters removed")
    world.heaters.clear()
    world.is_heater_map.clear()


@after(seconds=11)
def steps():
    print("\nI execute after 11 seconds - I BLOCK WORLD")
    emit_event(World.WORLD_PAUSE_EVENT)
    queues_dictionary[World.PAUSED_EVENT].get(block=True)
    print("WORLD HAS PAUSED\n")
    print(world.space[24][24].vector.temperature)
    sleep(10)
    emit_event(World.CAN_RESUME)

# sleep(4)
if __name__ == '__main__':
    start_executing(world)
