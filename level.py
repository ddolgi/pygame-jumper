import csv
import pygame
from pygame.locals import *

class Tile(pygame.sprite.Sprite):
# x location, y location, img width, img height, img file    
    def __init__(self, x, y, img=None):
        pygame.sprite.Sprite.__init__(self)
        
        if img:
            self.image = img.convert_alpha()
            self.rect = self.image.get_rect()
        else:
            self.image = None
            self.rect = pygame.Rect(0, 0, 64, 64)        
        # self.image.set_alpha(None)
        # print(self.image.get_alpha(),img)
        # self.image.convert_alpha()
        # self.image.set_colorkey()

        self.rect.x = x * self.image.get_width()
        self.rect.y = y * self.image.get_height()
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
    skyblue = Color(80, 100, 200)
    textbg = Color(200, 0, 0)
    textfg = Color(200, 200, 0)
    def __init__(self, conf, nLevel):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.nLevel = nLevel
        self.actives = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        # self.items = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.thones = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.rgems = pygame.sprite.Group()
        self.bgems = pygame.sprite.Group()
        self.ggems = pygame.sprite.Group()
        self.ygems = pygame.sprite.Group()

        self.font = pygame.font.Font("D2Coding-Ver1.3-20171129.ttf", 32)
        self.bKey = True

        # Background image
        # self.background = self.skyblue
        self.bgImg = pygame.image.load(conf.img_dir + "bg%02d.png" % nLevel)
        self.pfImg = pygame.image.load(conf.img_dir + "pf%02d.png" % nLevel)
        self.ptImg = pygame.image.load(conf.img_dir + 'portal.png')
        self.tnImg = pygame.image.load(conf.img_dir + 'thone.png')
        self.kyImg = pygame.image.load(conf.img_dir + 'key.png')
        self.drImg = pygame.image.load(conf.img_dir + 'door.png')
        self.rgemImg = pygame.image.load(conf.img_dir + 'rgem.png')
        self.bgemImg = pygame.image.load(conf.img_dir + 'bgem.png')
        self.ggemImg = pygame.image.load(conf.img_dir + 'ggem.png')
        self.ygemImg = pygame.image.load(conf.img_dir + 'ygem.png')

        for y,row in enumerate(open(conf.level_dir + "%02d.map" % nLevel)):
            for x,v in enumerate(row.strip('\n')):
                if v == '-':    # platform
                    self.platforms.add(Tile(x, y, self.pfImg))
                elif v == 'p':  # portal
                    self.portals.add(Tile(x, y, self.ptImg))
                elif v == 't':  # thone
                    self.thones.add(Tile(x, y, self.tnImg))
                elif v == 'k':  # thone
                    self.keys.add(Tile(x, y, self.kyImg))
                    self.bKey = True
                elif v == 'd':  # thone
                    self.doors.add(Tile(x, y, self.drImg))
                elif v == 'r':  # invisible platform
                    self.rgems.add(Tile(x, y, self.rgemImg))
                elif v == 'b':  # invisible platform
                    self.bgems.add(Tile(x, y, self.bgemImg))
                elif v == 'g':  # invisible platform
                    self.ggems.add(Tile(x, y, self.ggemImg))
                elif v == 'y':  # invisible platform
                    self.ygems.add(Tile(x, y, self.ygemImg))

    def reset(self):    self.bKey = True
    def gotKey(self):   self.bKey = False

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
        self.platforms.draw(screen)
        self.portals.draw(screen)
        self.thones.draw(screen)
        self.doors.draw(screen)
        self.rgems.draw(screen)
        self.bgems.draw(screen)
        self.ggems.draw(screen)
        self.ygems.draw(screen)
        if self.bKey: self.keys.draw(screen)
        self.actives.draw(screen)

        msg = u"%d 층"%self.nLevel
        text = self.font.render(msg, True, self.textfg, self.textbg)
        textRect = text.get_rect()
        textRect.x = 30
        textRect.y = 24
        screen.blit(text, textRect)

 
