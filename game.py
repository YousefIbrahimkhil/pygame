# Example file showing a circle moving on screen
# To install run the following commands:
# python3 -m pip install --upgrade pip
# python3 -m pip install --upgrade Pillow

import pygame
from PIL import Image

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
speed = 10
size = 50
direction = "down"

def rectangle(start_x, start_y, size):
    x = start_x-(size/2)
    y = start_y-(size/2)
    return pygame.Rect(x, y, size, size)

rect_pos = rectangle(screen.get_width() / 2, (screen.get_height() / 2) + 100, 100)

player_pos = rectangle(screen.get_width() / 2, screen.get_height() / 2, 20)

with Image.open("level-0.png") as im:
    (width, height) = (im.width, im.height)
    pixels = list(im.getdata())
    


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    count = 0
    row = 0

    for x in pixels:
        wallcolor = "white"
        if x == (0,0,0,255):
            wallcolor = "white"
        else:
            wallcolor = "black"
        pygame.draw.rect(screen, wallcolor, rectangle(count * size, row * size, size))
        count += 1
        if count > width - 1:
            count = 0
            row += 1
            
    # point = pygame.player_pos.get_pos()
    collide = rect_pos.colliderect(player_pos)
    color = (255, 0, 0) if collide else (255, 255, 255)
    pygame.draw.rect(screen, color, player_pos)
    pygame.draw.rect(screen, "green", rect_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        direction = "up"
    if keys[pygame.K_s]:
        direction = "down"
    if keys[pygame.K_a]:
        direction = "left"
    if keys[pygame.K_d]:
        direction = "right"

    if direction == "down":
        player_pos.y += speed * dt
    elif direction == "up":
        player_pos.y -= speed * dt
    elif direction == "left":
        player_pos.x -= speed * dt
    else:
        player_pos.x += speed * dt

    speed += 1


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()