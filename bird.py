import pygame
from settings import *
import math

class Bird:

    jumpRange = 50
    width = 40
    height = 40
    jumpTime = 0
    timeSinceJump = 0
    jumpY = 0

    def __init__ (self, img, x, y):
        self.img = img
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
    
    def calculatePosition(self, t):
        # a = g
        # V = -v0 + gt
        # y = y0 -v0*t + gt2 / 2
        g = GlobalSettings.g
        v0 = math.sqrt(2*g*self.jumpRange)
        self.y = self.jumpY - v0*t + (g*t*t)/2;