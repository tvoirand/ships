"""
main script for ships.

version of the 20180613.
"""

import numpy as np
import framemod
import scmod
import pygame
import pygame.locals
from OpenGL.GL import *
from OpenGL.GLU import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

a = 6000.0
e = 0.3
inc = 40.0
raan = 0.0
om = 45.0
mu = 398600.0
planet_rotational_velocity = 360 / 86400 # degrees per second

SCALE = 8e-8 * a

vertices_list = []

ship_count = 0

for shift in range(0, 45, 5):

    time_list = np.arange(0, 3 * 86400, 50) + shift * 1000

    vertices_list.append(np.zeros((len(time_list), 4), dtype = np.float32))

    for i in range(len(time_list)):

        vertices_list[ship_count][i, 0] = time_list[i]

        vertices_list[ship_count][i, 1:] = SCALE * scmod.from_orbital_to_cartesian_coordinates(
            a,
            e,
            inc + shift,
            raan,
            om,
            time_list[i],
            mu
        )

        vertices_list[ship_count][i, 1:] = scmod.rotate_frame_around_y(
            vertices_list[ship_count][i, 1:],
            planet_rotational_velocity * time_list[i]
        )

    ship_count += 1

def display_animation(vertices_list):
    """
    Displays animation.

    Input:
    - vertices      list of numpy arrays of floats (shape (nb_of_steps, 4))
                    columns contain: time elapsed, x-coord, y-coord, z-coord
    """

    count = 0

    while True:

        # closing animation window at any event
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # resetting counter to zero when whole array displayed
        if count == (vertices_list[0].shape[0] - 1):

            for ship in range(len(vertices_list)):

                framemod.draw_line((vertices_list[ship][count, 1:], vertices_list[ship][0, 1:]))

            count = 0

            pygame.display.flip()

            pygame.time.wait(300)

        else:

            for ship in range(len(vertices_list)):

                framemod.draw_line((vertices_list[ship][count, 1:], vertices_list[ship][count + 1, 1:]))

            count += 1

            pygame.display.flip()

            pygame.time.wait(10)

framemod.initiate_pygame_frame()

display_animation(vertices_list)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(vertices_list[0][:, 1], vertices_list[0][:, 2], vertices_list[0][:, 3])
# plt.show()
