"""
pygame framework building module.

version of the 20180610.
"""

import pygame
import pygame.locals
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os

def save_frame(frame_count):
    """
    Save current frame to file.
    Input:
    -count  integer
    """

    if not os.path.isdir("frames"):

        os.mkdir("frames")

    surface = pygame.display.get_surface()

    pygame.image.save(surface, "frames/{}.png".format(frame_count))

def draw_line(vertices):
    """
    Draws a line between two vertices.
    Inputs:
    -vertices   list of tuples of floats
    """

    glBegin(GL_LINES)

    for vertex in vertices:

        glVertex3fv(vertex)

    glEnd()

def initiate_pygame_frame():
    """
    Initiates pygame frame.
    """

    frame_width = 800
    frame_height = 600
    perspective_angle = 70
    horizon_close = 0.1
    horizon_far = 50
    translation = 5

    pygame.init()

    display = (frame_width, frame_height)

    pygame.display.set_mode(display, pygame.locals.DOUBLEBUF|pygame.locals.OPENGL)

    gluPerspective(perspective_angle, (display[0]/display[1]), horizon_close, horizon_far)

    glTranslatef(0.0, 0.0, -translation)

    glEnable(GL_DEPTH_TEST)
