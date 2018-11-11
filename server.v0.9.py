#! /usr/bin/env python
import select
import socket
import sys
import time
import logging

import pygame
from pygame.locals import *
from collections import deque

logging.getLogger().addHandler(logging.StreamHandler())
log = logging.getLogger()
log.setLevel(logging.INFO)

# === BEGIN CONSTANTS ===
Player1=True

HOST = "0.0.0.0"
PORT = 10000

BUFFER_SIZE = 1024

# Escape Room Time:
Minute = 45
Second = 0

# Player
Player1ID="ONE"
Player2ID="TWO"

Player1Ready=False
Player2Ready=True

#Colors
Black = (0,0,0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Purple = (80, 25, 128)
White = (255, 255, 255)

#NES Controller
BTN = {
0 : 'A',
1 : 'B',
2 : 'SELECT',
3 : 'START'
}

# === END CONSTANTS ===
pygame.init()

### GET NES Controller
pygame.joystick.init() # main joystick device system
if not pygame.joystick.get_count():
	log.critical("No Joystick Found")
	sys.exit()

Joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for Joystick in Joysticks:
	log.debug(Joystick.get_name())
	if "NES" in Joystick.get_name():
		j = Joystick
		j.init()
		Running = True
		break
if not Running:
	log.critical("NES Joystick not found!")
	sys.exit()

log.info("Enabled joystick: {}".format(j.get_name()))

# ### GET socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

### Synchronize session
Connected = False
Synched = False
Running = False

Player1Sync="P1 INIT"
Player2Sync="P2 INIT"
StartGame="Start Game"
QuitGame="Quit Game"


log.info("Waiting for Player {} to Synchronize".format(Player2ID))
while not Synched:
	conn, addr = s.accept()
	data = conn.recv(BUFFER_SIZE)
	if data != Player2Sync:
		log.error("I don't understand: {}".format(data))
		continue
	else:
		log.debug(data)
		conn.send(Player1Sync)
		Synched = True
		print("Synched")

# SYNCHED - Continuing



### BEGIN JoyCodes
konami = ("UP","UP","DOWN","DOWN","LEFT","RIGHT","LEFT","RIGHT","B","A","START")
puzzle = ("A","LEFT","DOWN","B","A","UP","UP","DOWN","B","LEFT","RIGHT","RIGHT")

def start_stop(button, queue=deque(maxlen=4)):
	queue.append(button)
	print(queue)
	if tuple(queue) == ("SELECT","START","B","A"):
		return True
	else:
		return False

def konami_code(button, queue=deque(maxlen=12)):
	queue.append(button)
	if tuple(queue) == tuple(konami):
		return True
	else:
		return False

def puzzle_code(button, queue=deque(maxlen=len(puzzle))):
	queue.append(button)
	print("QUEUE: {}".format(queue))
	if tuple(queue) == tuple(puzzle):
		return True
	else:
		return False
### END JoyCodes

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

def player_ready():
	global Player1Ready
	global Player2Ready
	if Player1:
		Player1Ready=True
		log.info("@@@@@PLAYER ONE READY@@@@@")
	else:
		Player2Ready=True
		log.info("@@@@@PLAYER TWO READY@@@@@")

	if s:
		conn.send("P1 READY")

def AllPlayersReady():
	global Player1Ready
	global Player2Ready
	log.debug("P1: {0},P2 {1}".format(Player1Ready,Player2Ready))
	if Player1Ready & Player2Ready:
		return True
	else:
		return False

#Half 720p windowed
# size = width, height = 640, 360 #Make sure background image is same size
# screen = pygame.display.set_mode(size)
#Fullscreen 720p
size = width, height = 1280, 720 #Make sure background image is same size
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)

# #Fonts
FontSize = height/5
Font = pygame.font.SysFont("Trebuchet MS", FontSize)

border = height/20
background=Purple

while (Synched and not Running):
	 # Screen
	 screen.fill(background)

	 log.debug("{0:02}:{1:02}".format(Minute,Second))
	 TimeFont = Font.render("{0:02}:{1:02}".format(Minute,Second),True, White)
	 TimeFontR = TimeFont.get_rect()
	 TimeFontR.center=(width/2,border+(FontSize/2)*3)
	 screen.blit(TimeFont, TimeFontR)

	 ### BEGIN Player1Ready Status
	 log.debug("Player {} WAITING".format(Player1ID))
	 Player1Font = Font.render("Player {} WAITING".format(Player1ID),True,Green)
	 Player1FontR = Player1Font.get_rect()
	 Player1FontR.center=(width/2,border+(FontSize/2)*5)

	 screen.blit(Player1Font, Player1FontR)

	 pygame.display.flip()
	 ### END Screen
	 for event in pygame.event.get():
		 if event.type == JOYBUTTONDOWN:
			 if event.button in BTN:
				 print('Button: {} down').format(BTN[event.button])
				 if start_stop(BTN[event.button]):
					 conn.send(StartGame)
					 Running = True
			 else:
				 print("Button: {} down".format(event.button))
		 elif event.type == JOYBUTTONUP:
			 if event.button in BTN:
				 print('Button: {} up').format(BTN[event.button])
			 else:
				 print("Button: {} up".format(event.button))
		 elif (event.type == KEYDOWN and event.key == K_f):
			 if screen.get_flags() & FULLSCREEN:
				 pygame.display.set_mode(size)
			 else:
				 pygame.display.set_mode(size, FULLSCREEN)

#Clock
Clock = pygame.time.Clock()
CLOCKTICK = pygame.USEREVENT+1
pygame.time.set_timer(CLOCKTICK, 1000) # fired once every Second

while Running:

	# Screen
	screen.fill(background)

	log.debug("{0:02}:{1:02}".format(Minute,Second))
	TimeFont = Font.render("{0:02}:{1:02}".format(Minute,Second),True, White)
	TimeFontR = TimeFont.get_rect()
	TimeFontR.center=(width/2,border+(FontSize/2)*3)
	screen.blit(TimeFont, TimeFontR)

	### BEGIN Player1Ready Status
	if Player1Ready:
		log.debug("Player {} Ready".format(Player1ID))
		Player1Font = Font.render("Player {} Ready".format(Player1ID),True,Blue)
	else:
		log.debug("Player {} NOT Ready".format(Player1ID))
		Player1Font = Font.render("Player {} Not Ready".format(Player1ID),True,Red)
	Player1FontR = Player1Font.get_rect()
	Player1FontR.center=(width/2,border+(FontSize/2)*5)

	screen.blit(Player1Font, Player1FontR)

	pygame.display.flip()
	### END Screen

	if AllPlayersReady():
		Running=False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Running = False

		elif (event.type is KEYDOWN and event.key == K_f):
			if screen.get_flags() & FULLSCREEN:
				pygame.display.set_mode(size)
			else:
				pygame.display.set_mode(size, FULLSCREEN)

		if event.type == CLOCKTICK: # count up the clock
			if Minute == 0:
				if Second == 0:
					done = True
					pygame.quit()
			if Second == 0:
				Minute -= 1
				Second = 60

			Second -= 1

		if event.type == JOYAXISMOTION: # 7
			x, y = j.get_axis(0), j.get_axis(1)
			JoyDir=get_direction(x, y)
			log.info(JoyDir)
			if JoyDir=="":
				continue
			else:
				if puzzle_code(JoyDir):
					player_ready()

		elif event.type == JOYBUTTONDOWN: # 10
			if event.button in BTN:
				log.info("Button: {} down".format(BTN[event.button]))
				if puzzle_code(BTN[event.button]):
					player_ready()
			else:
				log.info("Button: Unknown down")
		elif event.type == JOYBUTTONUP: # 11
			if event.button in BTN:
				log.info("Button: {} up".format(BTN[event.button]))
			else:
				log.info("Button: Unknown up")

	Clock.tick(60) # ensures a maximum of 60 frames per Second

while not Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            log.info(QuitGame)
            conn.send(QuitGame)
            pygame.quit()
            sys.exit(1)
        elif (event.type == KEYDOWN and event.key == K_f):
            if screen.get_flags() & FULLSCREEN:
                pygame.display.set_mode(size)
            else:
                pygame.display.set_mode(size, FULLSCREEN)
        elif event.type == JOYBUTTONDOWN: # 10
            if event.button in BTN:
                print('Button: {} down').format(BTN[event.button])
                if start_stop(BTN[event.button]):
                    pygame.quit()
                    sys.exit()
            else:
				print("Button: Unknown down")
        elif event.type == JOYBUTTONUP: # 11
            if event.button in BTN:
                print('Button: {} up').format(BTN[event.button])
            else:
                print("Button: Unknown up")
