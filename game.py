import pygame
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
font = pygame.font.SysFont('Consolas', 30)
counter = 0
text = ""
seconds = 0
minutes = 0



pygame.time.set_timer(pygame.USEREVENT, 1)




def rectangle(start_x, start_y, size):
    x = start_x-(size/2)
    y = start_y-(size/2)
    return pygame.Rect(x, y, size, size)

with Image.open("level-0.png") as im:
    (width, height) = (im.width, im.height)
    pixels = list(im.getdata())


def camera_movement(x, CameraX, y, CameraY):
    screen.blit(pixels,(0 -CameraX,0 -CameraY))
    screen.blit(player_pos,(x -CameraX,y -CameraY))
    return pygame.display.flip()

    
for x in pixels:
    if x == (168, 230, 29, 255):
        starting_x = count * size
        starting_y = row * size
    count += 1
    if count > width - 1:
        count = 0
        row += 1

print(starting_x)
print(starting_y)
player_pos = rectangle(starting_x, starting_y, size)

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
    
        screen.fill("black")
        screen.blit(font.render(text, True, (255, 255, 255)), (screen.get_width()-150, 48))

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
                paused = True
                
        color = (255, 0, 0) if collide else (213, 227, 16)
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
            player_pos = rectangle(starting_x, starting_y, size)
            speed = 10
            direction = "right"

    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()