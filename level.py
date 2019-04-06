import csv
import pygame
from pygame.locals import *

class Platform(pygame.sprite.Sprite):
# x location, y location, img width, img height, img file    
    def __init__(self,xloc,yloc,imgw,imgh,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.convert()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
    skyblue = Color(80, 100, 200)
    def __init__(self, conf, bgFile, pfFile, lvlFile):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platforms = pygame.sprite.Group()
        self.actives = pygame.sprite.Group()
         
        # Background image
        # self.background = self.skyblue
        self.background = pygame.image.load(conf.img_dir + bgFile)

        self.pfimage = pygame.image.load(conf.img_dir + pfFile)
        pfw = self.pfimage.get_width()
        pfh = self.pfimage.get_height()

        for y,row in enumerate(csv.reader(open(conf.level_dir + lvlFile))):
            for x,v in enumerate(row):
                if v != '1': continue
                self.platforms.add(Platform(pfw*x,pfh*y,pfw,pfh,self.pfimage))

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
        screen.blit(self.background, (0,0))
        # screen.fill(self.background)
 
        # Draw all the sprite lists that we have
        self.platforms.draw(screen)
        self.actives.draw(screen)
 