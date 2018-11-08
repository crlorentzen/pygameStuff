#! /usr/bin/env python
import pygame

# === BEGIN CONSTANTS ===
# Escape Room Time:
Minute = 45
Second = 0
# Player
PlayerID="ONE"
#PlayerID="TWO"

#Colors
Black = (0,0,0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
White = (255, 255, 255)

# === END CONSTANTS ===

running = True

pygame.init()

#Screen
#size = width, height = 640, 360 #Make sure background image is same size
size = width, height = 640, 360 #Make sure background image is same size
screen = pygame.display.set_mode(size)
border = height/20

#Clock
Clock = pygame.time.Clock()
CLOCKTICK = pygame.USEREVENT+1
pygame.time.set_timer(CLOCKTICK, 1000) # fired once every Second


# #Fonts
FontSize=height/5
Font = pygame.font.SysFont("Trebuchet MS", FontSize)

screen.fill(Black)

Clock = pygame.time.Clock()
CLOCKTICK = pygame.USEREVENT+1
pygame.time.set_timer(CLOCKTICK, 1000) # fired once every Second

# Initial Screen
print("{0:02}:{1:02}").format(Minute,Second)
print("Player {} NOT READY".format(PlayerID))
# Time, HH:MM
TimeFont = Font.render("{0:02}:{1:02}".format(Minute,Second),True, White)
TimeFontR = TimeFont.get_rect()
TimeFontR.center=(width/2,(FontSize/2)+border)

PlayerFont = Font.render("Player {} NOT READY".format(PlayerID),True,Red)
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

            screen.fill(Black)
            TimeFont = Font.render("{0:02}:{1:02}".format(Minute,Second),True, White)
            screen.blit(TimeFont, TimeFontR)

            pygame.display.flip()

            Second -= 1

    Clock.tick(60) # ensures a maximum of 60 frames per Second

pygame.quit()

# pygame.init()
# start_ticks=pygame.time.get_ticks() #starter tick
# while True: # mainloop
#     Seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many Seconds
#     if Seconds>60: # if more than 10 Seconds close the game
#         clock -= 1
#         print
#         break
#     print (Seconds) #print how many Seconds
