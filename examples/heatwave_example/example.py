import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from examples.heatwave_example.entities import Space, transformation

space = Space()
transformation_result = transformation(space, 1)

MM = np.array([[[transformation_result[i][j][k].vector.temperature for k in range(space.width)]
                for j in range(space.length)] for i in range(100)])

fig = plt.figure()
pcm = plt.pcolormesh(MM[0])
plt.colorbar()


# # Function called to update the graphic
# def step(i):
#     if i >= len(MM):
#         return
#     pcm.set_array(MM[i].flatten())
#     plt.draw()
#
# anim = FuncAnimation(fig, step, interval=50)
plt.show()
