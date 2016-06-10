import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from analyze import get_song_data, EX_FILEPATH


base_vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1),
    )

edges = (
    (0, 1, 2),
    (2, 3, 0),
    (4, 5, 6),
    (6, 7, 4),
    (5, 1, 0),
    (5, 4, 0),
    (2, 6, 5),
    (0, 3, 7)
    )

num_bezier_segments = 50


def calculate_bezier_point(t, p0, p1, p2):
    u = 1 - t
    return (np.array(p0) * (u * u) + np.array(p1) * 2 * u * t + (t * t) * np.array(p2)).tolist()


def draw_shape(scale=1):
    # scale vertices
    vertices = []
    for vertex in base_vertices:
        vertices.append(tuple(c * scale for c in vertex))

    # draw edges
    for edge in edges:
        glBegin(GL_LINE_STRIP)
        for i in range(num_bezier_segments):
            t = i / float(num_bezier_segments)
            p0, p1, p2 = vertices[edge[0]], vertices[edge[1]], vertices[edge[2]]
            glVertex(calculate_bezier_point(t, p0, p1, p2))

        glEnd()


def animate():
    song_data = get_song_data(EX_FILEPATH)
    beat_times = song_data['beat_times']
    song_length = song_data['song_length']  # in seconds
    next_beat_idx = 0

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    for centisecond in range(song_length * 100):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotate(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        scale = 1
        try:
            next_beat_time = beat_times[next_beat_idx] * 100
        except IndexError:
            # no beats left
            pass
        if centisecond == next_beat_time - 1:
            scale = 1.05
        elif centisecond == next_beat_time:
            scale = 1.1
        elif centisecond == next_beat_time + 1:
            scale = 1.05
            next_beat_idx += 1
        # catch missed beats
        elif centisecond > next_beat_time + 1:
            next_beat_idx += 1
        draw_shape(scale)

        pygame.display.flip()
        pygame.time.delay(10)


animate()
