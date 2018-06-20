"""
main script for ships.

version of the 20180618.

parameters:
-a      semi-major axis
-e      eccentricity
-i      inclination
-om     argument of periapsis
-s      step duration
--vid   make video option
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
import argparse

def display_animation(ships_list, save_frames):
    """
    Displays animation.

    Input:
    -ships_list     list of scmod.Ship
    -save_frames    boolean
    """

    frame_count = 0

    while True:

        # closing animation window at any event
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # resetting counter to zero when whole array displayed
        if frame_count == (len(time_list) - 1):

            if save_frames:

                framemod.image_to_video()

                pygame.quit()

                quit()

            else:

                frame_count = 0

                pygame.display.flip()

                pygame.time.wait(300)

        else:

            for ship in ships_list:

                framemod.draw_line((
                    ship.vertices[frame_count, 1:],
                    ship.vertices[frame_count + 1, 1:]
                ))

            frame_count += 1

            pygame.display.flip()

            if save_frames:

                framemod.save_frame(frame_count)

            pygame.time.wait(10)

parser = argparse.ArgumentParser()
parser.add_argument("-a", default = 10000)
parser.add_argument("-e", default = 0)
parser.add_argument("-i", default = 0)
parser.add_argument("-om", default = 0)
parser.add_argument("-s", default = 50)
parser.add_argument("--vid", action="store_true")
args = parser.parse_args()

a = float(args.a)
e = float(args.e)
inc = float(args.i)
raan = 0.0
om = float(args.om)

MU_PLANET = 398600.0
PLANET_ROT = 360 / 86400 # degrees per second

step = float(args.s)

time_list = np.arange(0, 30000, step)

ships_list = []

for time_shift in np.arange(1e4, 2e4, 1e3):
    for inc_shift in np.arange(0, 90, 20):



        ships_list.append(scmod.Ship([a, e, inc + inc_shift, raan, om], len(time_list)))

        ship = ships_list[scmod.Ship.ships_count - 1]

        for i in range(len(time_list)):

            ship.vertices[i, 0] = time_list[i] + time_shift

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

display_animation(ships_list, args.vid)



# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(
#     ships_list[0].vertices[:, 1],
#     ships_list[0].vertices[:, 2],
#     ships_list[0].vertices[:, 3]
# )
# plt.show()
