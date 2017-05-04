from time import sleep

from examples.heatwave_example.entities import World
from scenario.executor import after, every_event, every, start_world, emit_event, on_event, queues_dictionary

world = World()


@every_event(event=World.ITERATION_COMPLETED)
def steps():
    iteration = world.iteration_counter
    if iteration % 3 == 0:
        emit_event("third_iteration")
    if iteration % 7 == 0:
        emit_event("seventh_iteration")
    print("Iteration has completed: " + str(world.iteration_counter))


@every_event(event="third_iteration")
def steps():
    print("Third iteration done")


@every(seconds=2)
def steps():
    print("Some task every 2 seconds")


@every(seconds=5)
def steps():
    print("I execute every 5 seconds")


@on_event(event="seventh_iteration")
def steps():
    print("Seventh_iteration occured")


@after(seconds=11)
def steps():
    print("\nI execute after 11 seconds - I BLOCK WORLD")
    emit_event(World.WORLD_PAUSE_EVENT)
    queues_dictionary[World.PAUSED_EVENT].get(block=True)
    print("WORLD HAS PAUSED\n")
    print(world.space[24][24].vector.temperature)
    sleep(10)
    emit_event(World.CAN_RESUME)


@every(start=15, seconds=5)
def steps():
    print("Some task after 5 seconds starting at 15 seconds")


sleep(4)
start_world(world)
