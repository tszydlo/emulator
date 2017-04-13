import collections

import numpy as np

class MeasurementVector():

    def __init__(self):
        self.vector = collections.namedtuple("TemperatureVector", ['temperature'])
        self.vector.temperature = 0


class Space():

    def __init__(self):
        self.length = 50
        self.width = 50
        self.points = [[MeasurementVector() for i in range(self.length)] for j in range(self.width)]


def transformation(space, time):
    dt = 0.1
    # heating device
    Gr = np.eye(10) * 2000
    for iGr in range(10):
        Gr[iGr, -iGr - 1] = 2000
    for i in range(0, 10):
        for j in range(0, 10):
            point = space.points[i+20][j+10]
            if Gr[i, j]:
                point.vector.temperature = Gr[i, j]
    for i in range(0, 10):
        for j in range(0, 10):
            point = space.points[i + 20][j + 30]
            if Gr[i, j]:
                point.vector.temperature = Gr[i, j]
    T = np.arange(0, 10, dt)
    MM = []
    for i in range(len(T)):
        for j in range(1, space.length - 1):
            for i in range(1, space.width - 1):

                space.points[i][j].vector.temperature = (space.points[i - 1][j].vector.temperature
                                      + space.points[i + 1][j].vector.temperature
                                      + space.points[i][j - 1].vector.temperature
                                      + space.points[i][j + 1].vector.temperature) / 4

        # Re-assert heaters
        for i in range(0, 10):
            for j in range(0, 10):
                point = space.points[i + 20][j + 10]
                if Gr[i, j]:
                    point.vector.temperature = Gr[i, j]
        for i in range(0, 10):
            for j in range(0, 10):
                point = space.points[i + 20][j + 30]
                if Gr[i, j]:
                    point.vector.temperature = Gr[i, j]

        MM.append(space.points.copy())
    return MM