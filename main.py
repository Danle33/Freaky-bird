import pygame
from game import *
import sys

pygame.init()
pygame.display.set_caption("Freaky Bird")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def get_new_x_coordinate(sliderCursorGravity, mouse_pos, draggingGravity, offsetGravity, leftBound, rightBound):
    if draggingGravity:
        new_x = mouse_pos[0] + offsetGravity
        new_x = min(rightBound - 15, new_x)
        new_x = max(leftBound - 15, new_x)
        return new_x
    return sliderCursorGravity.x


firstClick = False
last_click_time = 0
first_click = False
DOUBLE_CLICK_TIME = 500

draggingGravity = False
offsetGravity = 0
draggingSpeed = False
offsetSpeed = 0

birdImg = "pticaBalls.jpg"
blockImg = "holyfuck.jpg"
bgImg = "background.png"
unpauseImg = "unpause.webp"
pauseImg = "pause.webp"

game = Game(screen, bgImg, birdImg, blockImg, pauseImg)
pause = Pause(screen, bgImg, birdImg, blockImg, unpauseImg, pauseImg)  

while 1:
    sliderCursorGravity = pause.sliderCursorGravity
    sliderCursorSpeed = pause.sliderCursorSpeed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game = Game(screen, bgImg, birdImg, blockImg, pauseImg)
            break
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_p) or (event.type == pygame.MOUSEBUTTONDOWN and game.pauseRect.collidepoint(event.pos)):
            game.paused = not game.paused
            if game.paused:
                game.pauseStartTime = pygame.time.get_ticks()
            else:
                game.pausedTime += pygame.time.get_ticks() - game.pauseStartTime
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game.paused:
            firstClick = True
            game.bird.jumpTime = pygame.time.get_ticks()
            game.bird.jumpY = game.bird.y
            game.pausedTime = 0
            break
        
        if game.paused:
            if event.type == pygame.MOUSEBUTTONDOWN and pause.unpauseRect.collidepoint(event.pos):
                game.paused = False
                game.pausedTime += pygame.time.get_ticks() - game.pauseStartTime

            # cursor gravity
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sliderCursorGravity.hitbox.collidepoint(event.pos):
                    draggingGravity = True
                    offsetGravity = sliderCursorGravity.x - event.pos[0]
            
            elif event.type == pygame.MOUSEBUTTONUP:
                draggingGravity = False

            # cursor speed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sliderCursorSpeed.hitbox.collidepoint(event.pos):
                    draggingSpeed = True
                    offsetSpeed = sliderCursorSpeed.x - event.pos[0]
            
            elif event.type == pygame.MOUSEBUTTONUP:
                draggingSpeed = False
    
    mouse_pos = pygame.mouse.get_pos()
    
    sliderCursorGravity.x = x = get_new_x_coordinate(sliderCursorGravity, mouse_pos, draggingGravity, offsetGravity, pause.sliderLineGravity.x, pause.sliderLineGravity.x + pause.sliderLineGravity.width)
    sliderCursorGravity.hitbox = pygame.Rect(x - 6, sliderCursorGravity.y - 10, sliderCursorGravity.height + 20, sliderCursorGravity.height + 20)
    pause.setGravity(x)

    sliderCursorSpeed.x = x = get_new_x_coordinate(sliderCursorSpeed, mouse_pos, draggingSpeed, offsetSpeed, pause.sliderLineSpeed.x, pause.sliderLineSpeed.x + pause.sliderLineSpeed.width)
    sliderCursorSpeed.hitbox = pygame.Rect(x - 6, sliderCursorSpeed.y - 10, sliderCursorSpeed.height + 20, sliderCursorSpeed.height + 20)
    pause.setSpeed(x)

    gameOver = game.over()

    if game.paused:
        pause.renderPause()
    else:
        game.renderGameplay()
        game.renderText(f"{game.score}", WIDTH // 2, HEIGHT // 6, 20)
        if firstClick:
            if not gameOver:
                game.update()
            else:
                game.renderText("GAME OVER", WIDTH // 2, HEIGHT // 6 + 50, 20)
                game.renderText("Press R to restart", WIDTH // 2, HEIGHT // 6 + 90, 15)
        else:
            game.renderText("Press space to jump", WIDTH // 2, HEIGHT // 6 + 50, 15)
            game.renderText("or P to pause", WIDTH // 2, HEIGHT // 6 + 80, 15)

    pygame.display.flip()
    clock.tick(60)


