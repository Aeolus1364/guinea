import pygame
import entity
import cfg
import time
import random

pygame.init()
cfg.init()


class Main:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.surface = pygame.display.set_mode(cfg.dim)

        self.running = True
        self.group = entity.Group()
        self.player = entity.Player()
        self.floor = entity.Floor()

        self.jumping = False
        self.time_init = 0.0
        self.wait = 0.0
        self.maxspd = 2.5
        self.minspd = 0.8

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.jumping = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.jumping = False

            if self.jumping:
                if self.player.grounded:
                    self.player.vely = cfg.jumpheight

            self.spawn()

            self.player.update()
            if self.group.update(self.player.rect):
                self.group.clear()
                self.player.rect.centery = -100
                self.player.vely = 0
                self.player.score = 0
            for ent in self.group.ents:
                if ent.passed and ent.point:
                    self.player.score += 1
                    ent.point = False

            if self.player.score >= 200:
                self.group.speed(-18)
                self.maxspd = 1
                self.minspd = 0.5
            elif self.player.score >= 150:
                self.group.speed(-16)
                self.maxspd = 1
                self.minspd = 0.55
                self.player.mspeed = 1
            elif self.player.score >= 100:
                self.group.speed(-14)
                self.maxspd = 1.3
                self.minspd = 0.6
                self.player.mspeed = 2
            elif self.player.score >= 50:
                self.group.speed(-12)
                self.maxspd = 1.6
                self.minspd = 0.65
                self.player.mspeed = 3
            elif self.player.score >= 25:
                self.group.speed(-10)
                self.maxspd = 1.9
                self.minspd = 0.7
                self.player.mspeed = 4
            elif self.player.score >= 10:
                self.group.speed(-8)
                self.maxspd = 2.2
                self.minspd = 0.75
                self.player.mspeed = 5
            else:
                self.group.speed(-6)
                self.maxspd = 2.5
                self.minspd = 0.8
                self.player.mspeed = 6

            font = pygame.font.SysFont("Arial", 50)
            render = font.render(str(self.player.score), True, (0, 0, 0))
            fontrect = render.get_rect()
            fontrect.centerx = cfg.dim[0] / 2
            fontrect.bottom = cfg.dim[1] - 50

            self.surface.fill((255, 255, 255))
            self.floor.draw(self.surface)
            pygame.draw.rect(self.surface, (0, 100, 0), (0, 200, cfg.dim[0], 75))
            self.group.draw(self.surface)

            self.player.draw(self.surface)

            self.surface.blit(render, fontrect)

            pygame.display.update()
            self.clock.tick(self.FPS)

    def spawn(self):
        if time.time() - self.time_init > self.wait:
            self.time_init = time.time()
            self.wait = random.uniform(self.minspd, self.maxspd)
            self.group.add(entity.Spike())


main = Main()
main.game_loop()

pygame.quit()