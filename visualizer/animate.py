import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from analyze import get_song_data, EX_FILEPATH


base_vertices = (
    (-1, 0, 0),
    (-0.7, -0.2, 0.8),
    (-0.9, -0.8, 0.4),
    (-0.5, -0.9, -0.2),
    (-0.1, -1, 0),
    (0.3, -0.4, -0.5),
    (0, 0, 0.2),
    (-0.1, 0.4, 0.7),
    (0.2, 0.8, 0.3),
    (0.5, 0.7, -0.4),
    (0.7, 0.5, -0.1),
    (0.7, -0.3, 0),
    (1, 0, 0)
    )

edges = (
    (0, 1, 2, 3),
    (3, 4, 5, 6),
    (6, 7, 8, 9),
    (9, 10, 11, 12),
    )

num_bezier_segments = 50


def calculate_bezier_point(t, p0, p1, p2, p3):
    # for cubic bezier curves
    u = 1 - t
    term1 = np.array(p0) * (u ** 3)
    term2 = np.array(p1) * t * (u ** 2) * 3
    term3 = np.array(p2) * u * (t ** 2) * 3
    term4 = np.array(p3) * (t ** 3)
    return (term1 + term2 + term3 + term4).tolist()


def draw_shape(scale=1):
    # scale vertices
    vertices = []
    for vertex in base_vertices:
        vertices.append(tuple(c * scale for c in vertex))

    # draw edges
    glBegin(GL_LINE_STRIP)
    for edge in edges:
        for i in range(num_bezier_segments):
            t = i / float(num_bezier_segments)
            p0, p1, p2, p3 = vertices[edge[0]], vertices[edge[1]], vertices[edge[2]], vertices[edge[3]]
            glVertex(calculate_bezier_point(t, p0, p1, p2, p3))
    glEnd()


def plot_chromagram(chroma_frame):
    # chroma_frame is a 1d numpy array with length 12
    glBegin(GL_POINTS)
    x_vals = [i * (1 / 6.0) - 1 for i in range(12)]
    for x, y in zip(x_vals, chroma_frame):
        glVertex(x, y, 0)
    glEnd()


def animate():
    song_data = get_song_data(EX_FILEPATH)
    chromagram = song_data['chromagram']
    chroma_frame_length_ms = song_data['chroma_frame_length_ms']

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -3)

    pygame.mixer.init()
    pygame.mixer.music.load(EX_FILEPATH)
    pygame.mixer.music.play()
    for frame_i in range(chromagram.shape[0]):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotate(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        plot_chromagram(chromagram[frame_i])

        pygame.display.flip()
        pygame.time.delay(int(chroma_frame_length_ms))


animate()
