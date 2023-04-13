import pygame
from PIL import Image

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
speed = 10
size = 50
direction = "right"
level = []

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    count = 0
    row = 0
    level = []
    collide = False

    for x in pixels:
        wallcolor = "white"
        if x == (0,0,0,255):
            wallcolor = "white"
        else:
            wallcolor = "black"
        level_rect = rectangle(count * size, row * size, size)
        level.append(level_rect)
        pygame.draw.rect(screen, wallcolor, level_rect)
        count += 1
        if count > width - 1:
            count = 0
            row += 1

    for index, i in enumerate(level):
        this_collide = i.colliderect(player_pos)
        if this_collide and pixels[index] == (0,0,0,255):
            collide = True
        elif this_collide and pixels[index] == (237,28,36,255):
            print('YOU WON!')
            running = False
            
    color = (255, 0, 0) if collide else (255, 255, 255)
    pygame.draw.rect(screen, color, player_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        direction = "up"
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        direction = "down"
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        direction = "left"
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
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

    if collide:
        player_pos = rectangle(screen.get_width() / 2, screen.get_height() / 2, 20)
        speed = 10


    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()