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
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
    )


def draw_cube(scale=1):
    glBegin(GL_LINES)
    vertices = []
    for vertex in base_vertices:
        vertices.append(tuple(c * scale for c in vertex))
    for edge in edges:
        for vertex_i in edge:
            glVertex(vertices[vertex_i])
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
        next_beat_time = beat_times[next_beat_idx] * 100
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
        draw_cube(scale)

        pygame.display.flip()
        pygame.time.delay(10)


animate()
