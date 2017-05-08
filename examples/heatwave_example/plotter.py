import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from examples.heatwave_example.entities import World


class Plotter():

    def __init__(self, world):
        self.world = world

    def start_observing(self):
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

if __name__ == '__main__':
    world = World()
    plotter = Plotter(world)
    plotter.world.start_transformation()
    plotter.start_observing()