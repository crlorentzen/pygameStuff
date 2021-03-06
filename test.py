#! /usr/bin/env python
import select
import socket
import sys
import time
import logging

import pygame
from pygame import locals
from collections import deque

logging.getLogger().addHandler(logging.StreamHandler())
log = logging.getLogger()
log.setLevel(logging.INFO)

# === BEGIN CONSTANTS ===
Player1=False

# HOST="198.18.10.4"
HOST = "127.0.0.1"
PORT = 10000
BUFFER_SIZE = 1024

Connected=False
Synched = False
Player1Sync="P1 INIT"
Player2Sync="P2 INIT"

Minute = 45
Second = 0
# Player
Player1ID="ONE"
Player2ID="TWO"

Player1Ready=False
Player2Ready=False

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



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while not Connected:
	try:
		s.connect((HOST, PORT))
		print("Connected")
		Connected=True
	except:
		print("Retry in 2 seconds")
		time.sleep(2)


s.send(Player2Sync)
data = s.recv(BUFFER_SIZE)
print(data)
if data != Player1Sync:
	print("Synchronization Failed")
else:
	running=True
	print("Synched")

# SYNCHED - Continuing

running = True

def player_ready():
	global Player1Ready
	global Player2Ready
	if Player1:
		Player1Ready=True
		log.info("@@@@@PLAYER ONE READY@@@@@")
		s.send("P2 READY")


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
	global Player1Ready
	global Player2Ready
	log.debug("P1: {0},P2 {1}".format(Player1Ready,Player2Ready))
	if Player1Ready & Player2Ready:
		return True
	else:
		return False

#Half 720p windowed
size = width, height = 640, 360 #Make sure background image is same size
screen = pygame.display.set_mode(size)
#Fullscreen 720p
# size = width, height = 1280, 720 #Make sure background image is same size
# screen = pygame.display.set_mode(size,pygame.FULLSCREEN)

# #Fonts
FontSize=height/5
Font = pygame.font.SysFont("Trebuchet MS", FontSize)

border = height/20
background=Purple

#Clock
Clock = pygame.time.Clock()
CLOCKTICK = pygame.USEREVENT+1
pygame.time.set_timer(CLOCKTICK, 1000) # fired once every Second


while running:
	# Time, HH:MM
	screen.fill(background)

	log.debug("Player {}".format(Player1ID if Player1 else Player2ID))
	PlayerFont = Font.render("Player {}".format(Player1ID if Player1 else Player2ID),True, White)
	PlayerFontR = PlayerFont.get_rect()
	PlayerFontR.center=(width/2,border+(FontSize/2))
	screen.blit(PlayerFont, PlayerFontR)

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
	### END Player1Ready Status

	### BEGIN Player2Ready Status
	if Player2Ready:
		log.debug("Player {} Ready".format(Player2ID))
		Player2Font = Font.render("Player {} Ready".format(Player2ID),True,Blue)
	else:
		log.debug("Player {} NOT Ready".format(Player2ID))
		Player2Font = Font.render("Player {} Not Ready".format(Player2ID),True,Red)
	Player2FontR = Player2Font.get_rect()
	Player2FontR.center=(width/2,border+(FontSize/2)*7)

	screen.blit(Player2Font, Player2FontR)
	### END Player2Ready Status

	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == CLOCKTICK: # count up the clock

			### P1 Data Check (once a second)
			# ready_to_read, ready_to_write, in_error = select.select([s], [], [], 0.001)
			# if ready_to_read:
			# 	log.debug("READ")
			# 	data = s.recv(BUFFER_SIZE)
			# 	if data == "P1 READY":
			# 		log.info("Entered Player1Ready")
			# 		Player1Ready=True
            #
			# 		log.info("Entered Player2Ready")
			# 		Player2Ready=True
			# 		s.send("P2 READY")
			# ### P1 Data Check Complete

			#Timer
			if Minute == 0:
				if Second == 0:
					done = True
					pygame.quit()
			if Second == 0:
				Minute -= 1
				Second = 60
			Second -= 1

			if AllPlayersReady():
				running=False

	Clock.tick(60) # ensures a maximum of 60 frames per Second

while not running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(1)
