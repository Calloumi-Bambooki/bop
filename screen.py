
import sys

import pygame
from pygame.locals import *

import math

deadzone = 0.25

def correctJoy(n):
    if n < deadzone and n > -deadzone:
        return 0
    if n < 0:
        return -n**2
    return n**2


class Screen:
    def __init__(self, game):
        self.game = game
        self.users = {}
        pygame.init()
        if len(self.game.screenSize) == 1:
            self.surface = pygame.display.set_mode((game.screenSize[0], 300), 0, 32)
        else:
            self.surface = pygame.display.set_mode((game.screenSize[0], game.screenSize[1]), 0, 32)
        pygame.display.set_caption("bop")
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

#        pygame.mixer.music.load('bop.wav')

    def addUser(self, user):
        self.users[user.id] = user

    def loop(self):
        keys = pygame.key.get_pressed()
        self.surface.fill((32, 32, 32))

        tempData = self.game.data
        for i in tempData["players"]:
            player = tempData["players"][i]
            textsurface = self.font.render(str(player.sco), False, player.col)
            self.surface.blit(textsurface, (10, i*35+5))
            if len(self.game.screenSize) == 1:
                pygame.draw.rect(self.surface, player.col, (player.pos[0], 0, self.game.size, self.game.screenSize[1]))
            else:
                pygame.draw.rect(self.surface, player.col, (player.pos[0], player.pos[1], self.game.size, self.game.size))

            if i in self.users:
                user = self.users[i]
                if user.controller:
                    player.act[0] = correctJoy(user.joystick.get_axis(0))
                    player.act[2] = correctJoy(user.joystick.get_axis(1))
                else:
                    for key in range(len(user.controls)):
                        player.act[key] = keys[user.controls]

        if len(self.game.screenSize) == 1:
            pygame.draw.rect(self.surface, self.game.data["gold"].col, (self.game.data["gold"].pos[0], 0, self.game.size, self.game.screenSize[1]))
        else:
            pygame.draw.rect(self.surface, self.game.data["gold"].col, (self.game.data["gold"].pos[0], self.game.data["gold"].pos[1], self.game.size, self.game.size))

        if self.game.bop:
#            pygame.mixer.music.play(0)
            self.game.bop = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


