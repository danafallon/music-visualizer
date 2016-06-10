from itertools import cycle
import sys

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from analyze import get_song_data


EX_FILEPATH = 'songs/imitosis.wav'

colors = (
    (1, 0, 0),
    (1, 0.5, 0),
    (1, 1, 0),
    (0.5, 1, 0),
    (0, 1, 0),
    (0, 1, 0.5),
    (0, 1, 1),
    (0, 0.5, 1),
    (0, 0, 1),
    (0.5, 0, 1),
    (1, 0, 1),
    (1, 0, 0.5)
    )


def plot_chromagram(chroma_frame):
    # chroma_frame is a 1d numpy array with length 12
    x_vals = [i * (1 / 6.0) - 1 for i in range(12)]
    glLineWidth(10.0)
    glBegin(GL_LINES)
    for x, y, color in zip(x_vals, chroma_frame, colors):
        glColor(color)
        glVertex(x, 0, 0)
        glVertex(x, y, 0)
    glEnd()


def draw_amp_wave(amp):
    x_abs = np.pi * 6
    x_vals = np.linspace(-x_abs, x_abs, 200)
    glLineWidth(1.0)
    glColor((1, 1, 1))
    glBegin(GL_LINE_STRIP)
    for x, y in zip(x_vals, np.sin(x_vals)):
        glVertex(x / x_abs, y * amp * 10 / x_abs - 0.5, 0)
    glEnd()


def animate(song_filepath):
    song_data = get_song_data(song_filepath)
    chromagram = song_data['chromagram']
    amplitudes = song_data['amplitudes']
    chroma_frame_length_ms = song_data['chroma_frame_length_ms']

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.1, 0.0, -3)

    pygame.mixer.init()
    pygame.mixer.music.load(song_filepath)
    pygame.mixer.music.play()
    pygame.time.delay(int(chroma_frame_length_ms))
    num_frames = chromagram.shape[0]
    for frame_i in range(num_frames):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # glRotate(0.3, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        plot_chromagram(chromagram[frame_i])
        draw_amp_wave(amplitudes[frame_i])

        pygame.display.flip()
        pygame.time.delay(int(chroma_frame_length_ms))


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        filepath = args[1]
    else:
        filepath = EX_FILEPATH
    animate(filepath)
