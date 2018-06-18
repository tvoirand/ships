"""
main script for ships.

version of the 20180618.
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

def display_animation(ships_list):
    """
    Displays animation.

    Input:
    - ships_list    list of scmod.Ship
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
        if count == (len(time_list) - 1):

            count = 0

            pygame.display.flip()

            pygame.time.wait(300)

        else:

            for ship in ships_list:

                framemod.draw_line((ship.vertices[count, 1:], ship.vertices[count + 1, 1:]))

            count += 1

            pygame.display.flip()

            pygame.time.wait(10)

a = 6000.0
e = 0.5
inc = 0.0
raan = 0.0
om = 0.0

MU_PLANET = 398600.0
PLANET_ROT = 360 / 86400 # degrees per second

time_list = np.arange(0, 3 * 86400, 50)

ships_list = []

for shift in range(0, 40, 10):

    ships_list.append(scmod.Ship([a, e, inc + shift, raan, om], len(time_list)))

    ship = ships_list[scmod.Ship.ships_count - 1]

    for i in range(len(time_list)):

        ship.vertices[i, 0] = time_list[i] + shift * 1000

        ship.vertices[i, 1:] = scmod.rotate_frame_around_y(
            ship.scale * scmod.from_orbital_to_cartesian_coordinates(
                ship.orbital_parameters[0],
                ship.orbital_parameters[1],
                ship.orbital_parameters[2],
                ship.orbital_parameters[3],
                ship.orbital_parameters[4],
                ship.vertices[i, 0],
                MU_PLANET
            ),
            PLANET_ROT * time_list[i]
        )

framemod.initiate_pygame_frame()

display_animation(ships_list)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(vertices_list[0][:, 1], vertices_list[0][:, 2], vertices_list[0][:, 3])
# plt.show()
