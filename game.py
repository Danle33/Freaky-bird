from bird import *
from block import *
from slider import *
import random

pygame.init()

def randomHeight():
    minHeight = HEIGHT // 6
    return random.randint(minHeight, HEIGHT - minHeight - Block.hole)

class Game:

    def __init__ (self, screen, bgImg, birdImg, blockImg, pauseImg):
        self.screen = screen
        self.startTime = pygame.time.get_ticks() 

        self.bird = Bird(pygame.image.load("Images/" + birdImg), WIDTH // 4, HEIGHT // 2)
        self.bird.jumpY = self.bird.y
        self.bird.jumpTime = pygame.time.get_ticks()
        self.bird.timeSinceJump = 0

        self.bgImg = pygame.image.load("Images/" + bgImg)
        self.bgImg = pygame.transform.scale(self.bgImg, (WIDTH, HEIGHT))

        self.pauseImg = pygame.image.load("Images/" + pauseImg)
        self.pauseImg = pygame.transform.scale(self.pauseImg, (40, 40))
        self.pauseRect = self.pauseImg.get_rect()
        self.pauseRect.center = (25, 25)

        self.score = 0

        self.pauseStartTime = pygame.time.get_ticks()
        self.pausedTime = 0

        randHeight = randomHeight()
        self.block1bottom = Block(pygame.image.load("Images/" + blockImg), WIDTH + Block.space, randHeight, -1)
        self.block1top = Block(pygame.image.load("Images/" + blockImg), WIDTH + Block.space, HEIGHT - randHeight - Block.hole, 1)

        randHeight = randomHeight()
        self.block2bottom = Block(pygame.image.load("Images/" + blockImg), WIDTH + Block.width + 2*Block.space, randHeight, -1)
        self.block2top = Block(pygame.image.load("Images/" + blockImg), WIDTH + Block.width + 2*Block.space, HEIGHT- randHeight - Block.hole, 1)

        self.paused = False
    
    def over(self):
        birdRect = self.bird.img.get_rect(topleft = (self.bird.x, self.bird.y))
        blockRects = []
        
        blockRects.append(self.block1bottom.img.get_rect(topleft = (self.block1bottom.x, self.block1bottom.y))) 
        blockRects.append(self.block1top.img.get_rect(topleft = (self.block1top.x, self.block1top.y)))
        blockRects.append(self.block2bottom.img.get_rect(topleft = (self.block2bottom.x, self.block2bottom.y))) 
        blockRects.append(self.block2top.img.get_rect(topleft = (self.block2top.x, self.block2top.y)))

        for blockRect in blockRects:
            if birdRect.colliderect(blockRect) or self.bird.y < 0 or self.bird.y + self.bird.height >= HEIGHT:
                return True
        return False

    def renderGameplay(self):
        self.screen.blit(self.bgImg, (0,0))
        self.screen.blit(self.bird.img, (self.bird.x, self.bird.y))

        if self.block1bottom.x < WIDTH:
            self.screen.blit(self.block1bottom.img, (self.block1bottom.x, self.block1bottom.y))
            self.screen.blit(self.block1top.img, (self.block1top.x, self.block1top.y))
        if self.block2bottom.x < WIDTH:
            self.screen.blit(self.block2bottom.img, (self.block2bottom.x, self.block2bottom.y))
            self.screen.blit(self.block2top.img, (self.block2top.x, self.block2top.y))
        self.screen.blit(self.pauseImg, self.pauseRect)
        
    def renderText(self, s, x, y, fontSize):
        font = pygame.font.Font("Fonts/8-bit-hud.ttf", fontSize)
        text_surface = font.render(s, True, BLACK)
        text_rect = text_surface.get_rect(center=(x+2, y+2))
        self.screen.blit(text_surface, text_rect)

        font = pygame.font.Font("Fonts/8-bit-hud.ttf", fontSize)
        text_surface = font.render(s, True, WHITE)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def update(self):
        self.bird.timeSinceJump = pygame.time.get_ticks() - self.bird.jumpTime - self.pausedTime
        self.bird.calculatePosition(self.bird.timeSinceJump / 1000)

        randHeight = 0
        if self.block1bottom.x < -Block.width:
            randHeight = randomHeight()
            self.block1bottom.setHeight(randHeight)
            self.block1top.setHeight(HEIGHT - randHeight - Block.hole)
        if self.block2bottom.x < -Block.width:
            randHeight = randomHeight()
            self.block2bottom.setHeight(randHeight)
            self.block2top.setHeight(HEIGHT - randHeight - Block.hole)

        x1Before = self.block1bottom.x
        x2Before = self.block2bottom.x

        self.block1bottom.calculatePosition()
        self.block1top.calculatePosition()
        self.block2bottom.calculatePosition()
        self.block2top.calculatePosition()

        if self.block1bottom.x < self.bird.x - Block.width < x1Before or self.block2bottom.x < self.bird.x - Block.width < x2Before:
            self.score += 1

class Pause(Game):

    def __init__ (self, screen, bgImg, birdImg, blockImg, unpauseImg, pauseImg):
        super().__init__(screen,  bgImg, birdImg, blockImg, pauseImg)

        self.unpauseImg = pygame.image.load("Images/" + unpauseImg)
        self.unpauseImg = pygame.transform.scale(self.unpauseImg, (40, 40))

        self.unpauseRect = self.unpauseImg.get_rect()
        self.unpauseRect.center = (WIDTH//2, 75)

        self.sliderLineGravity = SliderLine(HEIGHT // 4 + 30)
        self.sliderLineSpeed = SliderLine(HEIGHT // 2)

        self.sliderCursorGravity = SliderCursor(WIDTH // 2, self.sliderLineGravity.y + self.sliderLineGravity.height // 2)
        self.sliderCursorSpeed = SliderCursor(WIDTH // 2, self.sliderLineSpeed.y + self.sliderLineSpeed.height // 2)

    def renderPause(self):
        self.screen.fill(LIGHT_BLUE)
        self.screen.blit(self.unpauseImg, self.unpauseRect)
        #pygame.draw.rect(self.screen, (255, 0, 0),self.sliderCursorSpeed.hitbox, 2)  # Debug hitbox

        self.renderText("SETTINGS", WIDTH//2, 30, 20)
        self.renderText("Gravity", WIDTH//2, self.sliderCursorGravity.y - 15, 12)
        self.renderText("Pillar Speed", WIDTH//2, self.sliderCursorSpeed.y - 15, 12)

        #self.renderText("Change bird", WIDTH//2, HEIGHT//2 + 110, 12)

        self.screen.blit(self.sliderLineGravity.img, (self.sliderLineGravity.x, self.sliderLineGravity.y))
        self.screen.blit(self.sliderLineSpeed.img, (self.sliderLineSpeed.x, self.sliderLineSpeed.y))

        self.screen.blit(self.sliderCursorGravity.img, (self.sliderCursorGravity.x, self.sliderCursorGravity.y))
        self.screen.blit(self.sliderCursorSpeed.img, (self.sliderCursorSpeed.x, self.sliderCursorSpeed.y))
    
    def setGravity(self, x):
        a = 0.0558
        b = -5.5861
        c = 189.8182

        GlobalSettings.g = a * x**2 + b*x +c

    def setSpeed(self, x):
        a = 0.00575
        b = -0.8118
        c = 76.204

        Block.speed = a * x**2 + b*x +c
 


    

        






