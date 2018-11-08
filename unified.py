#! /usr/bin/env python
import pygame
from pygame import locals
from collections import deque

import sys
import socket
import select

# === BEGIN CONSTANTS ===
Player1=True
# Escape Room Time:
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

### GET NES Controller
pygame.init()

pygame.joystick.init() # main joystick device system


try:
	j = pygame.joystick.Joystick(0) # create a joystick instance
	j.init() # init instance
	print 'Enabled joystick: ' + j.get_name()
except pygame.error:
	print("no joystick found.")

### GET socket
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 10000))
s.listen(1)

### Synchornize session
Synched = False
Player1Sync="P1 INIT"
Player2Sync="P2 INIT"

print("Waiting for Player {} to Synchronize".format(Player2ID))
while not Synched:
	conn, addr = s.accept()
	data = conn.recv(BUFFER_SIZE)
	if data != Player2Sync:
		print("I don't understand: {}".format(data))
		continue
	else:
		print(data)
		conn.send(Player1Sync)
		Synched = True

# SYNCHED - Continuing

running = True



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
		global Player1Ready
		global Player2Ready
		Player1Ready=True
		if s:
			conn.send("P1 READY")
		print("@@@@@PLAYER ONE READY@@@@@")

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
	print("P1: {0},P2 {1}".format(Player1Ready,Player2Ready))
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




Clock = pygame.time.Clock()
CLOCKTICK = pygame.USEREVENT+1
pygame.time.set_timer(CLOCKTICK, 1000) # fired once every Second

# Initial Screen

while running:
	# Time, HH:MM
	screen.fill(background)

	print("Player {}".format(Player1ID if Player1 else Player2ID))
	PlayerFont = Font.render("Player {}".format(Player1ID if Player1 else Player2ID),True, White)
	PlayerFontR = PlayerFont.get_rect()
	PlayerFontR.center=(width/2,border+(FontSize/2))
	screen.blit(PlayerFont, PlayerFontR)

	print("{0:02}:{1:02}").format(Minute,Second)
	TimeFont = Font.render("{0:02}:{1:02}".format(Minute,Second),True, White)
	TimeFontR = TimeFont.get_rect()
	TimeFontR.center=(width/2,border+(FontSize/2)*3)
	screen.blit(TimeFont, TimeFontR)

	### BEGIN Player1Ready Status
	if Player1Ready:
		print("Player {} Ready".format(Player1ID))
		Player1Font = Font.render("Player {} Ready".format(Player1ID),True,Blue)
	else:
		print("Player {} NOT Ready".format(Player1ID))
		Player1Font = Font.render("Player {} Not Ready".format(Player1ID),True,Red)
	Player1FontR = Player1Font.get_rect()
	Player1FontR.center=(width/2,border+(FontSize/2)*5)

	screen.blit(Player1Font, Player1FontR)
	### END Player1Ready Status

	### BEGIN Player2Ready Status
	if Player2Ready:
		print("Player {} Ready".format(Player2ID))
		Player2Font = Font.render("Player {} Ready".format(Player2ID),True,Blue)
	else:
		print("Player {} NOT Ready".format(Player2ID))
		Player2Font = Font.render("Player {} Not Ready".format(Player2ID),True,Red)
	Player2FontR = Player2Font.get_rect()
	Player2FontR.center=(width/2,border+(FontSize/2)*7)

	screen.blit(Player2Font, Player2FontR)
	### END Player2Ready Status

	pygame.display.flip()

	### P2 Data Check
	ready_to_read, ready_to_write, in_error = select.select([conn], [], [], 0.001)
	if ready_to_read:
		print("READ")
		data = conn.recv(BUFFER_SIZE)
		print("DATA: {}".format(data))
		if data == "P2 READY":
			print("Entered Player2Ready")
			Player2Ready=True
	### P2 Data Check Complete
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
