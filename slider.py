import pygame
from settings import *

class SliderLine:

    width = WIDTH // 2 + 50
    height = 5

    def __init__(self, y):
        self.x = WIDTH // 2 - self.width // 2
        self.y = y - self.height // 2

        self.img = pygame.image.load("Images/sliderline.jpg")
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

class SliderCursor:
    width = 28
    height = 20

    def __init__ (self, x, y):
        self.x = x - self.width // 2
        self.y = y - self.height // 2

        self.img = pygame.image.load("Images/sliderCursor.png")

        self.hitbox = pygame.Rect(x-20, y-20, self.height + 20, self.height + 20)

        self.img = pygame.transform.scale(self.img, (self.width, self.height))
