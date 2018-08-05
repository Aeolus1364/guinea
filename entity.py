import pygame
import cfg
import res


class Entity:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class Group:
    def __init__(self, ents=None):
        self.ents = []
        if type(ents) is Spike:
            self.ents.append(ents)
        elif type(ents) is list:
            self.ents = self.ents + ents

    def draw(self, surf):
        if self.ents:
            for i in self.ents:
                i.draw(surf)

    def add(self, ents=None):
        if type(ents) is Spike:
            self.ents.append(ents)
        elif type(ents) is list:
            self.ents = self.ents + ents

    def clear(self):
        self.ents = []

    def list(self):
        return self.ents

    def update(self, rect):
        r = False
        if self.ents:
            for c, ent in enumerate(self.ents):
                ent.update()
                if ent.rect.right < 0:
                    del self.ents[c]
                if ent.rect.colliderect(rect):
                    r = True
                if ent.rect.right < rect.left:
                    ent.passed = True
        return r

    def speed(self, spd):
        if self.ents:
            for ent in self.ents:
                ent.velx = spd


class Player(Sprite):
    def __init__(self):
        self.images = res.walk
        self.cycle = 0
        self.speed = 0
        self.mspeed = 6
        super().__init__(res.walk[0])
        self.rect.center = cfg.dim[0] / 2, -100

        self.vely = 0
        self.accy = cfg.grav

        self.score = 0
        self.grounded = False

    def update(self):
        self.vely += self.accy
        self.rect.y += self.vely

        if self.rect.bottom > cfg.flr2:
            self.rect.bottom = cfg.flr2
            self.grounded = True
        else:
            self.grounded = False

        self.speed +=1
        if self.speed >= self.mspeed:
            self.speed = 0
            self.cycle += 1
        if self.cycle >= len(self.images):
            self.cycle = 0
        self.image = self.images[self.cycle]

        if not self.grounded:
            self.image = self.images[2]


class Spike(Sprite):
    def __init__(self):
        super().__init__(res.spike)
        self.rect.x = cfg.dim[0]
        self.rect.bottom = cfg.dim[1] - cfg.flr
        self.velx = 0
        self.passed = False
        self.point = True

    def update(self):
        self.rect.x += self.velx


class Floor(Entity):
    def __init__(self):
        super().__init__(pygame.Rect(0, 0, cfg.dim[0], cfg.flr), (120, 30, 0))
        self.rect.bottom = cfg.dim[1]

