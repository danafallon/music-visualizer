from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from analyze import get_song_data, EX_FILEPATH


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
    glLineWidth(10.0)
    glBegin(GL_LINES)
    x_vals = [i * (1 / 6.0) - 1 for i in range(12)]
    for x, y, color in zip(x_vals, chroma_frame, colors):
        glColor(color)
        glVertex(x, 0, 0)
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
    glTranslatef(0.1, -0.5, -3)

    pygame.mixer.init()
    pygame.mixer.music.load(EX_FILEPATH)
    pygame.mixer.music.play()
    for frame_i in range(chromagram.shape[0]):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # glRotate(0.3, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        plot_chromagram(chromagram[frame_i])

        pygame.display.flip()
        pygame.time.delay(int(chroma_frame_length_ms))


animate()
