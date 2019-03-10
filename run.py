#!/usr/bin/env python3

import sys
import csv

import pygame
from pygame.locals import *

class Config(object):
    width = 800
    height = 600
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

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
    skyblue = Color(80, 100, 200)
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
 
    def load(self, filename):
        rows = [row for row in csv.reader(Config.level_dir + filename)]

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(skyblue)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 


class Player(object):
    max_speed = 10
    max_momentum = 10

    addum = 2
    resist = 1

    jump_power = 50
    gravity = 10

    def __init__(self, conf):
        super(Player, self).__init__()
        self.img = pygame.image.load(conf.img_dir + "dooly.png")
        self.pwidth = self.img.get_width()
        self.pheight = self.img.get_height()
        # self.img = pygame.image.load(conf.img_dir + "him2.png")
        self.loc = [100, 100]
        self.momentum = [0, 0]
        self.floor = False

    def draw(self):
        self.loc[0] += self.momentum[0]
        self.loc[1] += self.momentum[1]

        max_x = swidth - self.pwidth
        self.loc[0] = max(self.loc[0], 0)
        if self.loc[0] > max_x:
            self.loc[0] = max_x

        max_y = sheight - gheight - self.pheight
        if self.loc[1] > max_y:
            self.loc[1] = max_y
            self.momentum[1] = 0
            self.floor = True

        screen.blit(self.img, self.loc)


    def update(self, keys):
        if keys.state['l']:
            self.momentum[0] -= self.addum
            self.momentum[0] = max(self.momentum[0], -self.max_momentum)
        elif self.momentum[0] < 0:
            self.momentum[0] += self.resist

        if keys.state['r']:
            self.momentum[0] += self.addum
            self.momentum[0] = min(self.momentum[0], self.max_momentum)
        elif self.momentum[0] > 0:
            self.momentum[0] -= self.resist

        if not self.floor:
            self.momentum[1] += self.gravity

        if keys.state['u'] and self.floor:
            self.momentum[1] -= self.jump_power
            self.floor = False
        print(self.loc, self.momentum)
        # elif keys[2]:

player = Player(Config)

class Key(object):
    mapping = {K_w:'u', K_a:'l', K_s:'d', K_d:'r', K_ESCAPE:'q'}
    def __init__(self):
        self.state = {'u':False, 'l':False, 'd':False, 'r':False}

    def check(self, event):
        if event.type == pygame.KEYDOWN:
            k = Key.mapping.get(event.key, '')
            if k == 'q': return -1
            if k: self.state[k] = True
        if event.type == pygame.KEYUP:
            k = Key.mapping.get(event.key, '')
            if k: self.state[k] = False
        return 0

keys = Key()

while True:
    draw_bg()
    player.draw()
    pygame.display.flip()

    for event in pygame.event.get():
        # check if the event is the X button 
        if keys.check(event) < 0 or event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit() 
            exit(0) 

    # print(keys.up, keys.left,keys.down, keys.right)
    player.update(keys)

