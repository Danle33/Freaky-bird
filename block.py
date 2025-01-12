import pygame
from settings import *

class Block:

    width = 60
    speed = 100
    speedmin = 50
    speedmax = 300
    space = (WIDTH - width) / 2
    hole = 150

    def __init__ (self, img, x, height, location):
        self.img = img
        self.x = x
        self.y = 0 if location == 1 else HEIGHT - height + 1
        self.height = height
        self.location = location
        self.img = pygame.transform.scale(self.img, (self.width, height))
        if location == 1:
            self.img = pygame.transform.flip(self.img, False, True)

    
    def setHeight(self, height):
        self.height = height
        self.img = pygame.transform.scale(self.img, (self.width, height))
        self.y = 0 if self.location == 1 else HEIGHT - height + 1
    
    def setImg(self, img):
        self.img = img
    
    def calculatePosition(self):
        if self.x + self.width < 0:
            self.x = WIDTH
            #self.speed += 1
        else:
            self.x -= self.speed/60