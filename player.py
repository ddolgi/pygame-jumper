import pygame

class Player(pygame.sprite.Sprite):
    # max_speed = 20
    max_momentum = 30

    addum = 5
    resist = 5

    jump_power = 50
    gravity = 5

    def __init__(self, conf, imgfile, x, y):
        super(Player, self).__init__()
        # pygame.sprite.Sprite.__init__(self)
        # super().__init__()

        self.image = pygame.image.load(conf.img_dir + imgfile)
        self.pwidth = self.image.get_width()
        self.pheight = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0
        self.dy = 0
        self.swidth = conf.width
        self.sheight = conf.height

    def onFloor(self, level):
        self.rect.y += self.gravity
        ret = pygame.sprite.spritecollide(self, level.platforms, False)
        self.rect.y -= self.gravity
        return ret

    def update(self, keys, level):
        if keys.state['l']:
            self.dx = max(self.dx - self.addum, -self.max_momentum)
        elif self.dx < 0:
            self.dx += self.resist

        if keys.state['r']:
            self.dx = min(self.dx + self.addum, self.max_momentum)
        elif self.dx > 0:
            self.dx -= self.resist

        if self.onFloor(level):   # Still?
            if keys.state['u']:
                self.dy -= self.jump_power
            else:
                self.dy = 0
        else: 
            self.dy += self.gravity

        if pygame.sprite.spritecollide(self, level.portals, False):
            return 'next'

        if pygame.sprite.spritecollide(self, level.thones, False):
            return 'dead'

        self.rect.x += self.dx
        hits = pygame.sprite.spritecollide(self, level.platforms, False)
        for hit in hits:
            if self.dx > 0:
                self.rect.right = hit.rect.left
            elif self.dx < 0:
                self.rect.left = hit.rect.right
        if hits:    self.dx = 0

        self.rect.y += self.dy
        hits = pygame.sprite.spritecollide(self, level.platforms, False)
        for hit in hits:
            if self.dy > 0:
                self.rect.bottom = hit.rect.top
                self.dy = 0
            elif self.dy < 0:
                self.rect.top = hit.rect.bottom
        if hits:    self.dy = 0

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, self.swidth)

        self.rect.bottom = min(self.rect.bottom, self.sheight)
        # if self.rect.bottom > self.sheight:
        #     print("GAME OVER")
        #     pygame.quit()
        #     sys.exit(0)
