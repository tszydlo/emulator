import collections
import numpy as np


class MeasurementVector():
    def __init__(self):
        self.vector = collections.namedtuple("TemperatureVector", ['temperature'])
        self.vector.temperature = 0


class Space(object):
    def __init__(self):
        self.length = 50
        self.width = 50
        self.points = [[MeasurementVector() for i in range(self.length)] for j in range(self.width)]

    def transformation(self):
        # heating device
        gr = np.eye(10) * 2000
        for iGr in range(10):
            gr[iGr, -iGr - 1] = 2000
        for i in range(0, 10):
            for j in range(0, 10):
                point = self.points[i + 20][j + 10]
                if gr[i, j]:
                    point.vector.temperature = gr[i, j]
        for i in range(0, 10):
            for j in range(0, 10):
                point = self.points[i + 20][j + 30]
                if gr[i, j]:
                    point.vector.temperature = gr[i, j]

            for j in range(1, self.length - 1):
                for i in range(1, self.width - 1):
                    self.points[i][j].vector.temperature = (self.points[i - 1][j].vector.temperature
                                                            + self.points[i + 1][j].vector.temperature
                                                            + self.points[i][j - 1].vector.temperature
                                                            + self.points[i][j + 1].vector.temperature) / 4

            # Re-assert heaters
            for i in range(0, 10):
                for j in range(0, 10):
                    point = self.points[i + 20][j + 10]
                    if gr[i, j]:
                        point.vector.temperature = gr[i, j]
            for i in range(0, 10):
                for j in range(0, 10):
                    point = self.points[i + 20][j + 30]
                    if gr[i, j]:
                        point.vector.temperature = gr[i, j]