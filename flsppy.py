import pygame
import random
import sys
from pygame.locals import *

# Global Variables for the game
window_width = 600
window_height = 499
elevation = window_height * 0.8
framepersecond = 32

# Set height and width of window
window = pygame.display.set_mode((window_width, window_height))
game_images = {}

# Image paths
pipeimage = 'D:/new projects/flappy bird/pipe.png'
background_image = 'D:/new projects/flappy bird/background.jpg'
birdplayer_image = 'D:/new projects/flappy bird/bird.png'
sealevel_image = 'D:/new projects/flappy bird/base.jfif'

def load_images():
    """Load all game images and handle errors."""
    try:
        game_images['scoreimages'] = (
            pygame.image.load('D:/new projects/flappy bird/0.png').convert_alpha(),
            pygame.image.load('D:/new projects/flappy bird/1.png').convert_alpha(),
            pygame.image.load('D:/new projects/flappy bird/2.png').convert_alpha(),
            pygame.image.load('D:/new projects/flappy bird/3.png').convert_alpha(),
            pygame.image.load('D:/new projects/flappy bird/4.png').convert_alpha(),
            pygame.image.load('D:/new projects/flappy bird/5.png').convert_alpha(),
            pygame.image.load('D:/new projects/flappy bird/6.png').convert_alpha(),
            pygame.image.load('D:/new projects/flappy bird/7.png').convert_alpha(),
            pygame.image.load('D:/new projects/flappy bird/8.png').convert_alpha(),
            pygame.image.load('D:/new projects/flappy bird/9.png').convert_alpha()
        )
        game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()
        game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
        game_images['background'] = pygame.image.load(background_image).convert_alpha()
        game_images['pipeimage'] = (
            pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
            pygame.image.load(pipeimage).convert_alpha()
        )
    except pygame.error as e:
        print(f"Error loading images: {e}")
        pygame.quit()
        sys.exit()

def flappygame():
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)

    # Generating two pipes for blitting on window
    first_pipe = createPipe()
    second_pipe = createPipe()

    # List containing lower pipes
    down_pipes = [
        {'x': window_width + 300, 'y': first_pipe[1]['y']},
        {'x': window_width + 300 + (window_width / 2), 'y': second_pipe[1]['y']},
    ]

    # List Containing upper pipes
    up_pipes = [
        {'x': window_width + 300, 'y': first_pipe[0]['y']},
        {'x': window_width + 200 + (window_width / 2), 'y': second_pipe[0]['y']},
    ]

    pipeVelX = -4  # pipe velocity along x
    bird_velocity_y = -9  # bird velocity
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1
    bird_flap_velocity = -8
    bird_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        # Check for game over
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            print("Game Over! Your score was:", your_score)
            return  # You can add a restart option here

        # Check for score
        playerMidPos = horizontal + game_images['flappybird'].get_width() / 2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                print(f"Your score is {your_score}")

        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY

        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)

        # Move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        # If the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Blit game images
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0], (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1], (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['sea_level'], (0, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))

        # Fetching the digits of score
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # Finding the width of score images from numbers
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width) / 1.1

        # Blitting the images on the window
        for num in numbers:
            window.blit(game_images['scoreimages'][num], (Xoffset, window_width * 0.02))
            Xoffset += game_images['scoreimages'][num].get_width()

        # Refreshing the game window and displaying the score
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)

def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        return True

    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if (vertical < pipeHeight + pipe['y'] and
                abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True

    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False

def createPipe():
    offset = window_height / 3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + random.randrange(0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2}    # lower Pipe
    ]
    return pipe

# Program where the game starts
if __name__ == "__main__":
    # For initializing modules of pygame library
    pygame.init()
    framepersecond_clock = pygame.time.Clock()

    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird Game')

    # Load all the images which we will use in the game
    load_images()

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    # Here starts the main game
    while True:
        horizontal = int(window_width / 5)
        vertical = int((window_height - game_images['flappybird'].get_height()) / 2)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappygame()
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['flappybird'], (horizontal, vertical))
                    window.blit(game_images['sea_level'], (0, elevation))
                    pygame.display.update()
                    framepersecond_clock.tick(framepersecond)