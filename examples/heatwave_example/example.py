import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from examples.heatwave_example.entities import Space

space = Space()
space.transformation()

fig = plt.figure()
pcm = plt.pcolormesh(np.array([[space.points[j][i].vector.temperature for i in range(space.length)]
                               for j in range(space.width)]), cmap='jet')
plt.colorbar()


def step(i):
    space.transformation()
    pcm.set_array(np.array([[space.points[j][k].vector.temperature for k in range(space.length)]
                            for j in range(space.width)]).ravel())
    plt.draw()


anim = FuncAnimation(fig, step, interval=1000)
plt.show()