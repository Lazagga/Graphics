import glfw
from OpenGL.GL import *
import numpy as np

T = np.array([[1., 0., 0.],
              [0., 1., 0.],
              [0., 0., 1.]])
x = 0.
r = 0.

def render():
    glClear(GL_COLOR_BUFFER_BIT) 
    glLoadIdentity() 
    # draw cooridnate 
    glBegin(GL_LINES) 
    glColor3ub(255, 0, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([1.,0.])) 
    glColor3ub(0, 255, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.])) 
    glEnd() 
    # draw triangle 
    glBegin(GL_TRIANGLES) 
    glColor3ub(255, 255, 255) 
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] ) 
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] ) 
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] ) 
    glEnd() 

def key_callback(window, key, scancode, action, mods):
    global T
    global x
    global r
    if key == glfw.KEY_Q:
        if action == glfw.PRESS:
            x -= .1
    if key == glfw.KEY_E:
        if action == glfw.PRESS:
            x += .1
    if key == glfw.KEY_A:
        if action == glfw.PRESS:
            r += 10 * np.pi / 180
    if key == glfw.KEY_D:
        if action == glfw.PRESS:
            r -= 10 * np.pi / 180
    if key == glfw.KEY_1:
        if action == glfw.PRESS:
            x = 0
            r = 0
    T = np.array([[np.cos(r),   -np.sin(r),   x],
                  [np.sin(r),   np.cos(r),    0.],
                  [0.,          0.,             1.]])

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "2021002751-3-1", None, None);
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