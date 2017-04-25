from time import sleep

from examples.heatwave_example.entities import World
from scenario.executor import after, every_event, every, start_world

world = World()


@every_event(event="iteration_completed")
def steps():
    print("Iteration has completed: " + str(world.iteration_counter))

@after(seconds=4)
def steps():
    print("Apply new function after 4 seconds")


@after(seconds=1)
def steps():
    print("Some task after 1 second")


@every(seconds=2)
def steps():
    print("Some task every 2 seconds")


@every(seconds=5)
def steps():
    print("I execute every 5 seconds")


@after(seconds=11)
def steps():
    print("I execute after 11 seconds")


@every(start=15, seconds=5)
def steps():
    print("Some task after 5 seconds starting at 15 seconds")

sleep(4)
start_world(world)

