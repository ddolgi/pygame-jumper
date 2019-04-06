#!/usr/bin/env python3
import sys

import pygame
from pygame.locals import *

from level import *
from player import *

class Config(object):
    width = 17 * 64
    height = 11 * 64
    img_dir = "image/"
    audio_dir = "audio/"
    level_dir = "level/"

pygame.init()
screen = pygame.display.set_mode((Config.width, Config.height))


print("Loading...")

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound(Config.audio_dir + "shoot.wav")
shoot_sound.set_volume(0.05)

# pygame.mixer.music.load(Config.audio_dir + "moonlight.wav")
# pygame.mixer.music.play(-1, 0.0)
# pygame.mixer.music.set_volume(0.25)

nLevel = 1
level = Level(Config, nLevel)

player1 = Player(Config, "player1.png", 80, 500)
# player2 = Player(Config, "player2.png", 950, 500)

# player1.addThings(level.platforms)
# player2.addThings(level.platforms)
# player1.addThing(player2)
# player2.addThing(player1)

level.addActive(player1)
# level.addActive(player2)

class Key(object):
    def __init__(self, mapping):
        self.mapping = mapping
        self.state = {'u':False, 'l':False, 'd':False, 'r':False}

    def check(self, event):
        if event.type == pygame.KEYDOWN:
            k = self.mapping.get(event.key, '')
            if k: self.state[k] = True
        if event.type == pygame.KEYUP:
            k = self.mapping.get(event.key, '')
            if k: self.state[k] = False
        return 0

key1 = Key({K_w:'u', K_a:'l', K_s:'d', K_d:'r'})
# key2 = Key({K_UP:'u', K_LEFT:'l', K_DOWN:'d', K_RIGHT:'r'})

clock = pygame.time.Clock()

def checkQuit(e):   
    if e.type == pygame.KEYDOWN and e.key == K_ESCAPE:  return True
    return e.type == pygame.QUIT

while True:
    for event in pygame.event.get():
        if checkQuit(event):
            pygame.quit() 
            exit(0) 
        key1.check(event)
        # key2.check(event)


    # print(keys.up, keys.left,keys.down, keys.right)
    ret = player1.update(key1, level)
    if ret == 'next':
        nLevel += 1
        del level
        level = Level(Config, nLevel)

        del player1
        player1 = Player(Config, "player1.png", 80, 500)
        # player1.addThings(level.platforms)
        level.addActive(player1)
    elif ret == 'dead':
        print('dead')
        break

    level.draw(screen)

    clock.tick(60)
    pygame.display.flip()

deadImg = pygame.image.load(Config.img_dir + "dead.png")
print('dead screen')
screen.blit(deadImg, (0,0))

while 1:
    pygame.display.flip()
    for event in pygame.event.get():
        if checkQuit(event):
            pygame.quit()
            exit(0)
