import pygame
from pygame import locals
from collections import deque

pygame.init()
pygame.joystick.init() # main joystick device system
try:
	j = pygame.joystick.Joystick(0) # create a joystick instance
	j.init() # init instance
	print 'Enabled joystick: ' + j.get_name()
except pygame.error:
	print 'no joystick found.'

BTN = {
0 : "A",
1 : "B",
2 : "SELECT",
3 : "START",
}

def get_direction():
    x, y = j.get_axis(0), j.get_axis(1)
    LocalDir=""
    if y <= -0.95:
        # UP
        LocalDir+="U"
    if y >= 0.95:
        # DOWN
        LocalDir+="D"
    if x >= 0.95:
        # RIGHT
        LocalDir+="R"
    if x <= -0.95:
        # LEFT
        LocalDir+="L"
    return LocalDir

def get_button(event):
    if event.button in BTN:
        return BTN[event.button]
    else:
        return False
