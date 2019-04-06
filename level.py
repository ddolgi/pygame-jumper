import csv
import pygame
from pygame.locals import *

class Tile(pygame.sprite.Sprite):
# x location, y location, img width, img height, img file    
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.convert_alpha()
        # self.image.set_alpha(None)
        # print(self.image.get_alpha(),img)
        # self.image.convert_alpha()
        # self.image.set_colorkey()

        self.rect = self.image.get_rect()
        self.rect.x = x * self.image.get_width()
        self.rect.y = y * self.image.get_height()
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
    skyblue = Color(80, 100, 200)
    def __init__(self, conf, nLevel):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.actives = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        # self.items = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.thones = pygame.sprite.Group()

        # Background image
        # self.background = self.skyblue
        self.bgImg = pygame.image.load(conf.img_dir + "bg%02d.png" % nLevel)
        self.pfImg = pygame.image.load(conf.img_dir + "pf%02d.png" % nLevel)
        self.ptImg = pygame.image.load(conf.img_dir + 'portal.png')
        self.tnImg = pygame.image.load(conf.img_dir + 'thone.png')

        for y,row in enumerate(open(conf.level_dir + "%02d.map" % nLevel)):
            for x,v in enumerate(row.strip('\n')):
                if v == '-':    # platform
                    self.platforms.add(Tile(self.pfImg, x, y))
                elif v == 'p':  # portal
                    self.portals.add(Tile(self.ptImg, x, y))
                elif v == 't':  # 
                    self.thones.add(Tile(self.tnImg, x, y))

    def addActive(self, player):
        self.actives.add(player)

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platforms.update()
        self.actives.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.blit(self.bgImg, (0,0))
        # screen.fill(self.background)
 
        # Draw all the sprite lists that we have
        self.actives.draw(screen)
        self.platforms.draw(screen)
        self.portals.draw(screen)
        self.thones.draw(screen)
 