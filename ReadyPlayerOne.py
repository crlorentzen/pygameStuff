#! /usr/bin/env python
import sys
import time
import logging

import pygame
from pygame import locals
from collections import deque

logging.getLogger().addHandler(logging.StreamHandler())
log = logging.getLogger()
log.setLevel(logging.DEBUG)


# === BEGIN CONSTANTS ===
# Escape Room Time:
Minute = 45
Second = 0
# Player
PlayerID="ONE"
#PlayerID="TWO"
PlayerReady=False

P1Ready=PlayerReady
P2Ready=True

#Colors
Black = (0,0,0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Purple = (80, 25, 128)
White = (255, 255, 255)

# === END CONSTANTS ===

running = True

pygame.init()

pygame.joystick.init() # main joystick device system

# try:
# 	j = pygame.joystick.Joystick(0) # create a joystick instance
# 	j.init() # init instance
# 	print 'Enabled joystick: ' + j.get_name()
# except pygame.error:
# 	print 'no joystick found.'
#
# if not pygame.joystick.get_count():
#     log.critical("No Joystick Found")
#     sys.exit()

j = None

Joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for Joystick in Joysticks:
	log.debug(Joystick.get_name())
	if "NES" in Joystick.get_name():
		j = pygame.joystick.Joystick(Joystick.get_id())
		j.init()
		break

log.info("Enabled joystick: {}".format(j.get_name()))



BTN = {
0 : 'A',
1 : 'B',
2 : 'SELECT',
3 : 'START'
}

def exit(button, queue=deque(maxlen=4)):
    queue.append(button)
    if tuple(queue) == ("SELECT", "START",
                        "B", "A"):
        return True
def konami(button, queue=deque(maxlen=11)):
    queue.append(button)
    if tuple(queue) == ("UP", "UP",
                        "DOWN", "DOWN",
                        "LEFT", "RIGHT",
                        "LEFT", "RIGHT",
                        "B", "A", "START"):
        global PlayerReady
        global P1Ready
        PlayerReady=True
        P1Ready=True
        print("@@@@@PLAYER READY@@@@@")

def get_direction(x,y):
    LocalDir=""
    if y <= -0.95:
        # UP
        LocalDir+="UP"
    if y >= 0.95:
        # DOWN
        LocalDir+="DOWN"
    if x >= 0.95:
        # RIGHT
        LocalDir+="RIGHT"
    if x <= -0.95:
        # LEFT
        LocalDir+="LEFT"
    return LocalDir

def AllPlayersReady():
    global P1Ready
    global P2Ready
    print("P1: {0},P2 {1}".format(P1Ready,P2Ready))
    if P1Ready & P2Ready:
        return True
    else:
        return False

#Half 720p windowed
size = width, height = 640, 360 #Make sure background image is same size
screen = pygame.display.set_mode(size)
#Fullscreen 720p
# size = width, height = 1280, 720 #Make sure background image is same size
# screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
border = height/20
background=Purple

# #Fonts
FontSize=height/5
Font = pygame.font.SysFont("Trebuchet MS", FontSize)

Clock = pygame.time.Clock()
CLOCKTICK = pygame.USEREVENT+1
pygame.time.set_timer(CLOCKTICK, 1000) # fired once every Second

# Initial Screen
# Time, HH:MM
print("{0:02}:{1:02}").format(Minute,Second)
screen.fill(background)
TimeFont = Font.render("{0:02}:{1:02}".format(Minute,Second),True, White)
TimeFontR = TimeFont.get_rect()
TimeFontR.center=(width/2,(FontSize/2)+border)

if PlayerReady:
    print("Player {} Ready".format(PlayerID))
    PlayerFont = Font.render("Player {} Ready".format(PlayerID),True,Blue)
else:
    print("Player {} NOT Ready".format(PlayerID))
    PlayerFont = Font.render("Player {} Not Ready".format(PlayerID),True,Red)
PlayerFontR = PlayerFont.get_rect()
PlayerFontR.center=(width/2,height/2)

screen.blit(TimeFont, TimeFontR)
screen.blit(PlayerFont, PlayerFontR)
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == CLOCKTICK: # count up the clock
            #Timer
            if Minute == 0:
                if Second == 0:
                    done = True
                    pygame.quit()
            if Second == 0:
                Minute -= 1
                Second = 59
            # Minute -= 1
            # redraw time
            print("{0:02}:{1:02}").format(Minute,Second)
            screen.fill(background)
            TimeFont = Font.render("{0:02}:{1:02}".format(Minute,Second),True, White)
            TimeFontR = TimeFont.get_rect()
            TimeFontR.center=(width/2,(FontSize/2)+border)

            if PlayerReady:
                print("Player {} Ready".format(PlayerID))
                PlayerFont = Font.render("Player {} Ready".format(PlayerID),True,Blue)
            else:
                print("Player {} NOT Ready".format(PlayerID))
                PlayerFont = Font.render("Player {} Not Ready".format(PlayerID),True,Red)
            PlayerFontR = PlayerFont.get_rect()
            PlayerFontR.center=(width/2,height/2)

            screen.blit(TimeFont, TimeFontR)
            screen.blit(PlayerFont, PlayerFontR)
            pygame.display.flip()

            Second -= 1
            if AllPlayersReady():
                running=False

        if event.type == pygame.locals.JOYAXISMOTION: # 7
            x, y = j.get_axis(0), j.get_axis(1)
            JoyDir=get_direction(x, y)
            print(JoyDir)
            if JoyDir=="":
                continue
            else:
                konami(JoyDir)
            #print 'x and y : ' + str(x) +' , '+ str(y)
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


    Clock.tick(60) # ensures a maximum of 60 frames per Second

while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(1)
        elif event.type == pygame.locals.JOYBUTTONDOWN: # 10
            if event.button in BTN:
                print('Button: {} down').format(BTN[event.button])
                if exit(BTN[event.button]):
                    pygame.quit()
                    sys.exit()
            else:
                print("Button: Unknown down")
        elif event.type == pygame.locals.JOYBUTTONUP: # 11
            if event.button in BTN:
                print('Button: {} up').format(BTN[event.button])

            else:
                print("Button: Unknown up")
