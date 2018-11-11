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
Player1=False

HOST="192.168.1.200"
# HOST = "127.0.0.1"
PORT = 10000
BUFFER_SIZE = 1024

### Synchronize session
Connected = False
Synched = False
Running = False

Player1Sync="P1 INIT"
Player2Sync="P2 INIT"
StartGame="Start Game"
QuitGame="Quit Game"

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
def AllPlayersReady():
	global Player1Ready
	global Player2Ready
	log.debug("P1: {0},P2 {1}".format(Player1Ready,Player2Ready))
	if Player1Ready & Player2Ready:
		return True
	else:
		return False


pygame.init()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
log.info("Connecting to {}:{}".format(HOST,PORT))
while not Connected:
	try:
		s.connect((HOST, PORT))
		log.info("Connected")
		Connected=True
	except:
		log.info("Retry in 1 seconds")
		time.sleep(1)

s.send(Player2Sync)
data = s.recv(BUFFER_SIZE)
log.debug(data)

if data != Player1Sync:
	print("Synchronization Failed")
else:
	Synched = True
	print("Synched")

# SYNCHED - Continuing

#Half 720p windowed
# size = width, height = 640, 360 #Make sure background image is same size
# screen = pygame.display.set_mode(size)
#Fullscreen 720p
size = width, height = 1280, 720 #Make sure background image is same size
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)

# #Fonts
FontSize=height/5
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
		if (event.type == KEYDOWN and event.key == K_f):
			if screen.get_flags() & FULLSCREEN:
				pygame.display.set_mode(size)
			else:
				pygame.display.set_mode(size, FULLSCREEN)

	### BEGIN P1 Data Check
	rlist, wlist, xlist = select.select([s], [], [], 0.001)

	for i in rlist:
		data = i.recv(BUFFER_SIZE)
		log.info("DATA: {}".format(data))
		if not data:
			break
		if data == StartGame:
			log.info("Starting")
			Running=True
	### END P1 Data Check

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
		### BEGIN P1 Data Check
			rlist, wlist, xlist = select.select([s], [], [], 0.001)
			for i in rlist:
				data = i.recv(BUFFER_SIZE)
				log.info("DATA: {}".format(data))
				if not data:
					break
				elif data == "P1 READY":
					log.info("Entered Player1Ready")
					Player1Ready=True
			### END P1 Data Check

			if Minute == 0:
				if Second == 0:
					running = False
			if Second == 0:
				Minute -= 1
				Second = 60
			Second -= 1

	Clock.tick(60) # ensures a maximum of 60 frames per Second

while not Running:
	### BEGIN P1 Data Check
	rlist, wlist, xlist = select.select([s], [], [], 0.001)

	if rlist:
		log.info(QuitGame)
		pygame.quit()
		sys.exit()
	for event in pygame.event.get():
		if (event.type == KEYDOWN and event.key == K_f):
			if screen.get_flags() & FULLSCREEN:
				pygame.display.set_mode(size)
			else:
				pygame.display.set_mode(size, FULLSCREEN)
