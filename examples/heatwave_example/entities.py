import collections
import threading
from queue import Queue

import numpy as np

from scenario.executor import queues_dictionary, emit_event
from simulation_entities.world import WorldEntity


class MeasurementVector:
    def __init__(self):
        self.vector = collections.namedtuple("TemperatureVector", ['temperature'])
        self.vector.temperature = 0


class World(WorldEntity):
    PAUSED_EVENT = "world_paused"
    WORLD_PAUSE_EVENT = "world_pause"
    CAN_RESUME = "world_can_resume"
    ITERATION_COMPLETED = "iteration_completed"

    def __init__(self):
        self.update_rate = 1
        self.iteration_counter = 0
        self.length = 50
        self.width = 50
        self.space = [[MeasurementVector() for _ in range(self.length)] for _ in range(self.width)]

    def transformation(self):
        # heating device
        gr = np.eye(10) * 2000
        for iGr in range(10):
            gr[iGr, -iGr - 1] = 2000
        for i in range(0, 10):
            for j in range(0, 10):
                point = self.space[i + 20][j + 10]
                if gr[i, j]:
                    point.vector.temperature = gr[i, j]
        for i in range(0, 10):
            for j in range(0, 10):
                point = self.space[i + 20][j + 30]
                if gr[i, j]:
                    point.vector.temperature = gr[i, j]

            for j in range(0, self.length):
                for k in range(0, self.width):
                    upper = None if j == self.length - 1 else self.space[k][j + 1].vector.temperature
                    down = None if j == 0 else self.space[k][j - 1].vector.temperature
                    left = None if k == 0 else self.space[k - 1][j].vector.temperature
                    right = None if k == self.width - 1 else self.space[k + 1][j].vector.temperature
                    elems = [y for y in filter(lambda x: x is not None, (upper, down, left, right))]
                    self.space[k][j].vector.temperature = sum(elems) / len(elems)

            # Re-assert heaters
            for k in range(0, 10):
                for j in range(0, 10):
                    point = self.space[k + 20][j + 10]
                    if gr[k, j]:
                        point.vector.temperature = gr[k, j]
            for k in range(0, 10):
                for j in range(0, 10):
                    point = self.space[k + 20][j + 30]
                    if gr[k, j]:
                        point.vector.temperature = gr[k, j]

    def start_transformation(self):
        # TODO: make world initialization
        self.transformation()
        queues_dictionary[World.WORLD_PAUSE_EVENT] = Queue()
        queues_dictionary[World.PAUSED_EVENT] = Queue()
        queues_dictionary[World.CAN_RESUME] = Queue()

        def transform_each_seconds():
            if not queues_dictionary[World.WORLD_PAUSE_EVENT].empty():
                emit_event(World.PAUSED_EVENT)
                queues_dictionary[World.WORLD_PAUSE_EVENT].get()
                queues_dictionary[World.CAN_RESUME].get(block=True)
                print("WORLD RESUMED\n")
            self.transformation()
            self.iteration_counter += 1
            emit_event(World.ITERATION_COMPLETED)
            threading.Timer(self.update_rate, transform_each_seconds).start()

        transform_each_seconds()
