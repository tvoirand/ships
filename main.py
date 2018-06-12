"""
main script for generative_art

version of the 20180610
"""

import numpy as np
import framemod
import pygame
import pygame.locals
from OpenGL.GL import *
from OpenGL.GLU import *

def from_orbital_to_cartesian_coordinates(a, e, i, RAAN, om, t, mu):
    '''
    Converting from orbital parameters to cartesian coordinates.
    - Inputs:
            a         float   semi-major axis (km)
    		e         float   eccentricity (-)
    		i         float   inclination (deg)
    		RAAN      float   right ascension of the ascending node (deg)
    		om        float   argument of periapsis (deg)
    		t         float   time spent since passage at periapsis (s)
    		mu	      float   gravitational parameter of the central body	(km3/s2)
    - Outputs:
    		pos   	  numpy array of floats (shape (3,)) (km)
    '''

    # converting angles from degrees to radians
    i = i * np.pi / 180
    RAAN = RAAN * np.pi / 180
    om = om * np.pi / 180

    # computing mean anomaly
    n = np.sqrt(mu / np.power(a, 3.0))
    M = n * t

    # computing eccentric anomaly
    E = [M]
    for j in range(100):
        E.append(E[j] + (M - E[j] + e * np.sin(E[j])) / (1 - e * np.cos(E[j])))
        if(abs(E[j+1] - E[j]) < 1e-8):
            E = E[j+1]
            break

    # computing true anomaly
    nu = 2 * np.arctan2(
            np.sqrt(1 - e) * np.cos(E / 2),
            np.sqrt(1 + e) * np.sin(E / 2)
        ) % (np.pi * 2)

    # computing radius
    r = a * (1 -np.power(e, 2.0)) / (1 + e * np.cos(nu))

    # computing position vector
    pos = np.asarray((
        r * (np.cos(om + nu) * np.cos(RAAN) - np.sin(om + nu) * np.sin(RAAN) * np.cos(i)),
        r * (np.cos(om + nu) * np.sin(RAAN) - np.sin(om + nu) * np.cos(RAAN) * np.cos(i)),
        r * (np.sin(om + nu) * np.sin(i))
    ))

    return pos

a = 6000.0
e = 0.0
i = 20.0
raan = 0.0
om = 0.0
mu = 398600.0

SCALE = 0.0005

vertices_list = []

ship_count = 0

for shift in range(0, 6000, 1000):

    time_list = np.arange(0, 86400, 100) + shift

    vertices_list.append(np.zeros((len(time_list), 4), dtype = np.float32))

    for i in range(len(time_list)):

        vertices_list[ship_count][i, 0] = time_list[i]

        vertices_list[ship_count][i, 1:] = SCALE * from_orbital_to_cartesian_coordinates(
            a,
            e,
            i,
            raan,
            om,
            time_list[i],
            mu
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
