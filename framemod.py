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
import cv2

def image_to_video():
    """
    Creates video file from images stored in a folder.
    """

    def add_leading_zeros_to_fname(folder_name):
        """
        Add leading zeros to files names so that they all have the same number of digits.
        10 digits max.

        Input:
        -folder_name    string
        """

        files = [file for file in os.listdir(folder_name) if file.endswith(".png")]

        max_digits = len(max(files, key=len))

        for file in files:

            leading_zeros = ""

            missing_zeros = max_digits - len(file)

            for i in range(missing_zeros):

                leading_zeros += "0"

            os.rename(folder_name + "/" + file, folder_name + "/" + leading_zeros + file)

    folder_name = "temp"
    video_name = "video.avi"

    add_leading_zeros_to_fname(folder_name)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    fps = 30

    images = [img for img in os.listdir(folder_name) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(folder_name, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, fourcc, fps, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(folder_name, image)))

    cv2.destroyAllWindows()
    video.release()

def save_frame(frame_count):
    """
    Save current frame to file.
    Input:
    -count  integer
    """

    if not os.path.isdir("temp"):

        os.mkdir("temp")

    surface = pygame.display.get_surface()

    pygame.image.save(surface, "temp/{}.png".format(frame_count))

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
