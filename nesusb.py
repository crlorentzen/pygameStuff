#!/usr/bin/env python

# import pygame
#
# pygame.init()
# j = pygame.joystick.Joystick(0)
# j.init()
# print 'Initialized Joystick : %s' % j.get_name()
#
# """
# Returns a vector of the following form:
# [LThumbstickX, LThumbstickY, Unknown Coupled Axis???,
# RThumbstickX, RThumbstickY,
# Button 1/X, Button 2/A, Button 3/B, Button 4/Y,
# Left Bumper, Right Bumper, Left Trigger, Right Triller,
# Select, Start, Left Thumb Press, Right Thumb Press]
#
# Note:
# No D-Pad.
# Triggers are switches, not variable.
# Your controller may be different
# """
#
# def get():
#     out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#     it = 0 #iterator
#     pygame.event.pump()
#
#     #Read input from the two joysticks
#     for i in range(0, j.get_numaxes()):
#         out[it] = j.get_axis(i)
#         it+=1
#     #Read input from buttons
#     for i in range(0, j.get_numbuttons()):
#         out[it] = j.get_button(i)
#         it+=1
#     return out
#
# # def test():
# #     while True:
# #         j.get_hat(1)
# #         # print get()
#
# # NES Controller enumeration
# self.buttons = ['up', 'down', 'left', 'right', 'select, ''start', 'A', 'B']
#
# axis=j.get_numaxes()
# buttons=j. get_numbuttons()
# hats=j.get_numhats()
# print("axis: {}").format(axis)
# print("buttons: {}").format(buttons)
# print("hats: {}").format(hats)
# while True:
#     print("Press Select")
#     pygame.event.wait
#     event=pygame.event.poll()
#     print(event)
#     exit()
#     print("Press Start")
#     pygame.event.wait()
#     print("Press B")
#     pygame.event.wait()
#     print("Press A")
#
#
#
# # while True:
# #     # get_numbuttons
# #     for i in range(0,buttons):
# #         print("{}: {}, ").format(i,j.get_button(i)),
# #     print("\n"),
# #     # for i in range(0,axis):
# #     #     print("{}: {}").format(i,j.get_axis(i))

import pygame
from pygame import locals
from collections import deque

running=True

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

def konami(button, queue=deque(maxlen=7)):
    queue.append(button)
    if tuple(queue) == ("L", "R", "L", "R", "B", "A", "START"):
        return True
    return False

def player_ready():
    exit()
    # Do indicator on screen

def get_direction(x,y):
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


while running:
    for event in pygame.event.get(): # iterate over event stack
        print 'event : ' + str(event.type)
        if event.type == pygame.locals.JOYAXISMOTION: # 7
            x, y = j.get_axis(0), j.get_axis(1)
            JoyDir=get_direction(x, y)
            print(JoyDir)
            if JoyDir=="":
                continue
            else:
                konami(JoyDir)
            #print 'x and y : ' + str(x) +' , '+ str(y)
        elif event.type == pygame.locals.JOYBALLMOTION: # 8
            print 'ball motion'
        elif event.type == pygame.locals.JOYHATMOTION: # 9
            print 'hat motion'
        elif event.type == pygame.locals.JOYBUTTONDOWN: # 10
            if event.button in BTN:
                print('Button: {} down').format(BTN[event.button])
                if konami(BTN[event.button]):
                    player_ready()
            else:
                print("Button: Unknown down")
        elif event.type == pygame.locals.JOYBUTTONUP: # 11
            if event.button in BTN:
                print('Button: {} up').format(BTN[event.button])
            else:
                print("Button: Unknown up")


        # if START button, then check if Konami code in buffer
        # exit or flush_buffer
        #if UP UP DOWN DOWN LEFT RIGHT LEFT RIGHT B A START exit



# When start pressed start 45 minute timer

# How long is a code? reset?
