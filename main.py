"""
main script for ships.

version of the 20180618.

parameters:
-a      semi-major axis
-e      eccentricity
-i      inclination
-raan   right ascension of the ascending node
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
from datetime import datetime
import os

def write_txt_file(a, e, i, raan, om, s, dur):
    """
    Writes txt file containing parameters.
    Input:
    -a      float
    -e      float
    -i      float
    -raan   float
    -om     float
    -step   float
    -dur    float
    """

    if not os.path.isdir("output"):

        os.mkdir("output")

    with open("output/" + datetime.now().strftime("%Y%m%d-%H%M") + "-info.txt", "w") as file:

        file.write("ships version 0.10 \n")
        file.write("parameters used: \n")
        file.write(
        "a    (km)  {}\n".format(a)
        + "e    (-)   {}\n".format(e)
        + "i    (deg) {}\n".format(i)
        + "raan (deg) {}\n".format(raan)
        + "om   (deg) {}\n".format(om)
        + "dur  (s)   {}\n".format(step)
        + "step (s)   {}\n".format(dur)
        )

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

                framemod.image_to_gif()

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
parser.add_argument("-a", default = 20000)
parser.add_argument("-e", default = 0)
parser.add_argument("-i", default = 0)
parser.add_argument("-raan", default = 0)
parser.add_argument("-om", default = 0)
parser.add_argument("-s", default = 50)
parser.add_argument("-dur", default = 86400)
parser.add_argument("--vid", action="store_true")
args = parser.parse_args()

a = float(args.a)
e = float(args.e)
inc = float(args.i)
raan = float(args.raan)
om = float(args.om)

MU_PLANET = 398600.0
PLANET_ROT = 360 / 86400 # degrees per second

step = float(args.s)
dur = float(args.dur)

time_list = np.arange(0, dur, step)

ships_list = []

for raan_shift in np.arange(0, 360, 360):
    for time_shift in np.arange(0, dur, dur):
        for inc_shift in np.arange(0, 360, 360):

            ships_list.append(scmod.Ship([a, e, inc + inc_shift, raan, om], len(time_list)))

            ship = ships_list[scmod.Ship.ships_count - 1]
            print(ship.orbital_parameters)
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

if args.vid:

    write_txt_file(a, e, inc, om, raan, step, dur)

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
