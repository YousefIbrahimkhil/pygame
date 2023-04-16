import pygame
from pygame import mixer
from PIL import Image

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
paused = False
dt = 0
speed = 10
size = 50
direction = "right"
level = []
count = 0
row = 0
starting_x = 0
starting_y = 0
font = pygame.font.SysFont('Consolas', 20)
counter = 0
text = ""
seconds = 0
minutes = 0

#Textures
wallTexture = pygame.image.load('wall.png')
floorTexture = pygame.image.load('floor.png')
playerTexture = pygame.image.load('player.png')
checkpointTexture = pygame.image.load('checkpoint.png')

pygame.time.set_timer(pygame.USEREVENT, 1)


mixer.init()
mixer.music.load("music-0.mp3")
mixer.music.set_volume(0.7)
mixer.music.play()

sound_effect = pygame.mixer.Sound('pop.ogg')



def rectangle(start_x, start_y, size):
    x = start_x-(size/2)
    y = start_y-(size/2)
    return pygame.Rect(x, y, size, size)

with Image.open("level-0.png") as im:
    (width, height) = (im.width, im.height)
    pixels = list(im.getdata())
    
for x in pixels:
    if x == (168, 230, 29, 255):
        starting_x = count * size
        starting_y = row * size
    count += 1
    if count > width - 1:
        count = 0
        row += 1

player_pos = rectangle(starting_x + (size / 2), starting_y + (size / 2), size)

surface = pygame.Surface((width * size, height * size))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            counter += 1
            milliseconds = 60 * (counter / 1000)
            if counter > 1000:
                seconds += 1
                counter = 0
                milliseconds = 0
            if seconds > 59:
                minutes += 1
                seconds = 0
            text = str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + ":" + str(int(milliseconds)).zfill(2)

    if paused == False:
    
        screen.fill((3,26,34))
        surface.fill((3,26,34))
        screen.blit(font.render(text, True, (255, 255, 255)), (screen.get_width()-140, 30))

        count = 0
        row = 0
        level = []
        collide = False

        for x in pixels:
            wallcolor = "white"
            if x == (0,0,0,255):
                level_rect = rectangle(count * size + (size / 2), row * size + (size / 2), size)
                level.append(level_rect)
                pygame.draw.rect(surface, (255,255,255,0), level_rect)
                surface.blit(wallTexture, (count * size, row * size))
            elif x == (237, 28, 36, 255):
                level_rect = rectangle(count * size + (size / 2), row * size + (size / 2), size)
                level.append(level_rect)
                pygame.draw.rect(surface, (0,0,0,0), level_rect)
                surface.blit(checkpointTexture, (count * size, row * size))
            else:
                level_rect = rectangle(count * size + (size / 2), row * size + (size / 2), size)
                level.append(level_rect)
                pygame.draw.rect(surface, (0,0,0,0), level_rect)
                surface.blit(floorTexture, (count * size, row * size))
            count += 1
            if count > width - 1:
                count = 0
                row += 1

        for index, i in enumerate(level):
            this_collide = i.colliderect(player_pos)
            if this_collide and pixels[index] == (0,0,0,255):
                sound_effect.play()
                collide = True
            elif this_collide and pixels[index] == (237,28,36,255):
                print('YOU WON!')
                paused = True
                
        player = pygame.draw.rect(surface, (49, 86, 57, 0), player_pos)

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
        surface.blit(playerTexture, player_pos)

        if collide:
            player_pos = rectangle(starting_x + (size / 2), starting_y + (size / 2), size)
            speed = 10
            direction = "right"

        screen.blit(surface, ((screen.get_width() / 2) - player_pos.x, (screen.get_height() / 2) - player_pos.y))
        pygame.display.flip()
        dt = clock.tick(60) / 1000

pygame.quit()