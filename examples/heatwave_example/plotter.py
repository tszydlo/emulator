import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from examples.heatwave_example.entities import World


class Observer():

    def __init__(self):
        self.world = World()

    def start_observing(self):
        self.world.start_time_transformation()

        fig = plt.figure()
        pcm = plt.pcolormesh(np.array([[self.world.space[j][i].vector.temperature for i in range(self.world.length)]
                                       for j in range(self.world.width)]), cmap='jet')
        plt.colorbar()

        def step(i):
            pcm.set_array(np.array([[self.world.space[j][k].vector.temperature for k in range(self.world.length)]
                                    for j in range(self.world.width)]).ravel())
            plt.draw()

        anim = FuncAnimation(fig, step, interval=1000)
        plt.show()