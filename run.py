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

pygame.font.init()

print("Loading...")

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound(Config.audio_dir + "shoot.wav")
shoot_sound.set_volume(0.05)

# pygame.mixer.music.load(Config.audio_dir + "moonlight.wav")
# pygame.mixer.music.play(-1, 0.0)
# pygame.mixer.music.set_volume(0.25)

nLevel = 1 if len(sys.argv) == 1 else int(sys.argv[1])
level = Level(Config, nLevel)

player1 = Player(Config, "player1small.png", 80, 560)
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
        self.reset()

    def reset(self):
        self.state = {'u':False, 'l':False, 'd':False, 'r':False}

    def check(self, event):
        if event.type == pygame.KEYDOWN:
            k = self.mapping.get(event.key, '')
            if k: self.state[k] = True
        if event.type == pygame.KEYUP:
            k = self.mapping.get(event.key, '')
            if k: self.state[k] = False
        return 0

keymap1 = {K_w:'u', K_a:'l', K_s:'d', K_d:'r'}
keymap2 = {K_UP:'u', K_LEFT:'l', K_DOWN:'d', K_RIGHT:'r'}
keymap1.update(keymap2)

key1 = Key(keymap1)
key2 = Key(keymap2)

clock = pygame.time.Clock()

def checkQuit(e):   
    if e.type == pygame.KEYDOWN and e.key == K_ESCAPE:  return True
    return e.type == pygame.QUIT

deadImg = pygame.image.load(Config.img_dir + "dead.png")

def wait():
    while True:
        for event in pygame.event.get():
            if checkQuit(event):
                pygame.quit() 
                exit(0) 

            if event.type == pygame.KEYDOWN:
                return

bKey = False
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
        if nLevel == 10:
            break
        nLevel += 1
        del level
        level = Level(Config, nLevel)

        player1.reset()
        key1.reset()
        level.addActive(player1)
    elif ret == 'dead':
        screen.blit(deadImg, (0,0))
        pygame.display.flip()
        wait()

        player1.reset()
        key1.reset()
        level.reset()
    elif ret == 'key':
        bKey = True
        level.gotKey()
    
    level.draw(screen)

    clock.tick(60)
    pygame.display.flip()

endImg = pygame.image.load(Config.img_dir + "ending.png")
screen.blit(endImg, (0,0))
# player1.reset()
# key1.reset()

pygame.display.flip()
wait()
pygame.quit() 
exit(0) 