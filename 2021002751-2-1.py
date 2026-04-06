import glfw
from OpenGL.GL import *
import numpy as np

prim = GL_LINE_LOOP

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(prim)
    for i in range(12):
        glVertex2fv(np.array([np.cos(i * np.pi / 6), np.sin(i * np.pi / 6)]))
    
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global prim
    if key == glfw.KEY_0:
        if action == glfw.PRESS:
            prim = GL_POLYGON
    if key == glfw.KEY_1:
        if action == glfw.PRESS:
            prim = GL_POINTS
    if key == glfw.KEY_2:
        if action == glfw.PRESS:
            prim = GL_LINES
    if key == glfw.KEY_3:
        if action == glfw.PRESS:
            prim = GL_LINE_STRIP
    if key == glfw.KEY_4:
        if action == glfw.PRESS:
            prim = GL_LINE_LOOP
    if key == glfw.KEY_5:
        if action == glfw.PRESS:
            prim = GL_TRIANGLES
    if key == glfw.KEY_6:
        if action == glfw.PRESS:
            prim = GL_TRIANGLE_STRIP
    if key == glfw.KEY_7:
        if action == glfw.PRESS:
            prim = GL_TRIANGLE_FAN
    if key == glfw.KEY_8:
        if action == glfw.PRESS:
            prim = GL_QUADS
    if key == glfw.KEY_9:
        if action == glfw.PRESS:
            prim = GL_QUAD_STRIP

def main():
    global prim

    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "2021002751-2-1", None, None);
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    # render loop
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()