import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from simulation_entities.temp_simulation_2d_world import TempSimulation2DWorld


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

        anim = FuncAnimation(fig, step, interval=100)
        plt.show()

if __name__ == '__main__':
    world = TempSimulation2DWorld()
    plotter = Plotter(world)
    plotter.world.start_transformation()
    plotter.start_observing()