"""
main script for ships.

version of the 20180722.

optional arguments:
  -h, --help      show this help message and exit
  -config CONFIG  custom configuration file
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
import inspect

def read_config(config_file, config_dict):
    """
    Read config file and store parameters in dictionnary.

    Input:
    -config_file    string
    -config_dict     dictionnary
    """

    with open(config_file, "r") as file:

        file_contents = file.readlines()

    for line in file_contents:

        if not line.startswith("#"):

            param = line.split("=")[0].split()[0]

            value = line.split("=")[1].split()[0]

            config_dict[param] = value

    return config_dict

def write_txt_file(a, e, i, raan, om, s, dur, shift_ranges):
    """
    Writes txt file containing parameters.
    Input:
    -a              float
    -e              float
    -i              float
    -raan           float
    -om             float
    -step           float
    -dur            float
    -shif_ranges    dict
    """

    if not os.path.isdir("output"):

        os.mkdir("output")

    with open("output/" + datetime.now().strftime("%Y%m%d-%H%M") + "-info.txt", "w") as file:

        file.write("ships version 1.1 \n\n")

        file.write("time parameters: \n")
        file.write(
        "step (s)   {}\n".format(step)
        + "dur  (s)   {}\n".format(dur)
        )

        file.write("\norbital parameters: \n")
        file.write(
        "a    (km)  {}\n".format(a)
        + "e    (-)   {}\n".format(e)
        + "i    (deg) {}\n".format(i)
        + "raan (deg) {}\n".format(raan)
        + "om   (deg) {}\n".format(om)
        )

        file.write("\nshift: \n")

        for key in shift_ranges:

            file.write("{:5s}".format(key))

            for value in shift_ranges[key][:-1]:

                file.write("{},".format(value))

            file.write("{}\n".format(shift_ranges[key][-1]))

def display_animation(ships_list, save_frames):
    """
    Displays animation.

    Input:
    -ships_list     list of scmod.Ship
    -save_frames    boolean
    """

    if os.path.dirname(inspect.getfile(inspect.currentframe())) == "":
        output_dir = "output"
    else:
        output_dir = os.path.dirname(inspect.getfile(inspect.currentframe())) + "/output"

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

            if save_frames == "True":

                framemod.image_to_video(output_dir)

                framemod.image_to_gif(output_dir)

                pygame.quit()

                quit()

            else:

                frame_count = 0

                pygame.display.flip()

                pygame.time.wait(10)

        else:

            for ship in ships_list:

                framemod.draw_line((
                    ship.vertices[frame_count, 1:],
                    ship.vertices[frame_count + 1, 1:]
                ))

            frame_count += 1

            pygame.display.flip()

            if save_frames == "True":

                framemod.save_frame(frame_count, output_dir)

            pygame.time.wait(10)

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Orbital animations.")
    parser.add_argument("-config", help="custom configuration file")
    args = parser.parse_args()

    if os.path.dirname(inspect.getfile(inspect.currentframe())) == "":
        config_default_file = "config_default.txt"
    else:
        config_default_file = os.path.dirname(inspect.getfile(inspect.currentframe())) \
            + "/config_default.txt"

    config = read_config(config_default_file, {})

    if args.config != None:
        config = read_config(args.config, config)

    a = float(config["a"])
    e = float(config["e"])
    inc = float(config["inc"])
    raan = float(config["raan"])
    om = float(config["om"])

    MU_PLANET = float(config["mu_planet"])
    PLANET_ROT = float(config["planet_rot"])

    step = float(config["step"])
    dur = float(config["dur"])

    time_list = np.arange(0, dur, step)

    ships_list = []

    shift_ranges = {
        "time":np.arange(
            float(config["time_shift"].split(",")[0]),
            float(config["time_shift"].split(",")[1]),
            float(config["time_shift"].split(",")[2])
        ),
        "a":np.arange(
            float(config["a_shift"].split(",")[0]),
            float(config["a_shift"].split(",")[1]),
            float(config["a_shift"].split(",")[2])
        ),
        "e":np.arange(
            float(config["e_shift"].split(",")[0]),
            float(config["e_shift"].split(",")[1]),
            float(config["e_shift"].split(",")[2])
        ),
        "inc":np.arange(
            float(config["inc_shift"].split(",")[0]),
            float(config["inc_shift"].split(",")[1]),
            float(config["inc_shift"].split(",")[2])
        ),
        "raan":np.arange(
            float(config["raan_shift"].split(",")[0]),
            float(config["raan_shift"].split(",")[1]),
            float(config["raan_shift"].split(",")[2])
        ),
        "om":np.arange(
            float(config["om_shift"].split(",")[0]),
            float(config["om_shift"].split(",")[1]),
            float(config["om_shift"].split(",")[2])
        ),
    }

    for time_shift in shift_ranges["time"]:
        for a_shift in shift_ranges["a"]:
            for e_shift in shift_ranges["e"]:
                for inc_shift in shift_ranges["inc"]:
                    for raan_shift in shift_ranges["raan"]:
                        for om_shift in shift_ranges["om"]:

                            ships_list.append(
                                scmod.Ship(
                                    [
                                        a + a_shift,
                                        e + e_shift,
                                        inc + inc_shift,
                                        raan + raan_shift,
                                        om + om_shift
                                    ],
                                    len(time_list)
                                )
                            )

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
                                    PLANET_ROT * (time_list[i] + time_shift)
                                )

    if config["vid"] == "True":

        write_txt_file(a, e, inc, om, raan, step, dur, shift_ranges)

    framemod.initiate_pygame_frame()

    display_animation(ships_list, config["vid"])


    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot(
    #     ships_list[0].vertices[:, 1],
    #     ships_list[0].vertices[:, 2],
    #     ships_list[0].vertices[:, 3]
    # )
    # plt.show()
