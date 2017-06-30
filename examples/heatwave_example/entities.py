import collections
from queue import Queue

import matplotlib.pyplot as plt
import numpy as np

from emulator.executor import queues_dictionary, emit_event
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


    class Heater():
        def __init__(self, max_temperature, size, bottom_left_x, bottom_left_y):
            self.max_temperature = max_temperature
            self.size = size
            self.bottom_left_x = bottom_left_x
            self.bottom_left_y = bottom_left_y
            self.grid = np.eye(self.size) * self.max_temperature
            for iGr in range(self.size):
                self.grid[iGr, -iGr - 1] = self.max_temperature


    def __init__(self):
        self.update_rate = 1.0
        self.iteration_counter = 0
        self.length = 50
        self.width = 50
        self.space = [[MeasurementVector() for _ in range(self.length)] for _ in range(self.width)]
        self.heaters = []

        self.is_heater_map = set()

    def initizalize(self):
        self.transformation()
        queues_dictionary[World.WORLD_PAUSE_EVENT] = Queue()
        queues_dictionary[World.PAUSED_EVENT] = Queue()
        queues_dictionary[World.CAN_RESUME] = Queue()
        heater = self.Heater(size=10, max_temperature=150, bottom_left_x=10, bottom_left_y=20)

        self.heaters = [heater]

        self.place_heaters()

        plt.figure(1)

    def place_heaters(self):
        for heater in self.heaters:
            for i in range(0, heater.size):
                for j in range(0, heater.size):
                    point = self.space[i + heater.bottom_left_y][j + heater.bottom_left_x]
                    if heater.grid[i, j]:
                        point.vector.temperature = heater.grid[i, j]
                        self.is_heater_map.add((i + heater.bottom_left_y, j + heater.bottom_left_x))

    def is_heater(self, x, y):
        for heater in self.heaters:
            for i in range(0, heater.size):
                for j in range(0, heater.size):
                    if x == i + heater.bottom_left_y and y == j + heater.bottom_left_x and heater.grid[
                        i, j]:
                        return True
        return False


    def transformation(self):

        for j in range(0, self.length):
            for k in range(0, self.width):
                if not (k, j) in self.is_heater_map:
                    upper = None if j == self.length - 1 else self.space[k][j + 1].vector.temperature
                    down = None if j == 0 else self.space[k][j - 1].vector.temperature
                    left = None if k == 0 else self.space[k - 1][j].vector.temperature
                    right = None if k == self.width - 1 else self.space[k + 1][j].vector.temperature
                    elems = [y for y in filter(lambda x: x is not None, (upper, down, left, right))]
                    self.space[k][j].vector.temperature = (sum(elems)) / (len(elems)) * 0.9999

    def start_transformation(self):

        while True:
            if not queues_dictionary[World.WORLD_PAUSE_EVENT].empty():
                emit_event(World.PAUSED_EVENT)
                queues_dictionary[World.WORLD_PAUSE_EVENT].get()
                queues_dictionary[World.CAN_RESUME].get(block=True)
                print("WORLD RESUMED\n")
            self.transformation()
            self.iteration_counter += 1

            if self.iteration_counter % 50 == 0:
                self.plot_itself_to_file(self.iteration_counter)

            emit_event(World.ITERATION_COMPLETED)



            # def transform_each_seconds():
            #
            #
            # if not queues_dictionary[World.WORLD_PAUSE_EVENT].empty():
            # emit_event(World.PAUSED_EVENT)
            #         queues_dictionary[World.WORLD_PAUSE_EVENT].get()
            #         queues_dictionary[World.CAN_RESUME].get(block=True)
            #         print("WORLD RESUMED\n")
            #     self.transformation()
            #     self.iteration_counter += 1
            #
            #     emit_event(World.ITERATION_COMPLETED)
            #     threading.Timer(self.update_rate, transform_each_seconds).start()
            #
            # transform_each_seconds()

    def plot_itself_to_file(self, i):

        if i == 50:
            ax = plt.subplot(221)
            ax.set_title("After 50 iterations")
        elif i == 150:
            ax = plt.subplot(222)
            ax.set_title("After 150 iterations")
        elif i == 300:
            ax = plt.subplot(223)
            ax.set_title("After 300 iterations")
        elif i == 350:
            ax = plt.subplot(224)
            ax.set_title("After 350 iterations")
        else:
            return

        plt.pcolormesh(np.array([[self.space[j][i].vector.temperature for i in range(self.length)]
                                 for j in range(self.width)]), cmap='jet', vmin=0, vmax=150)
        plt.colorbar()

        if i == 350:
            file_name = '../../plots/merged' + '.png'
            plt.tight_layout()
            plt.savefig(file_name)
            plt.close()

