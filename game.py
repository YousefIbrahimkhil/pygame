import pygame
from pygame import mixer
from PIL import Image

pygame.init()

# GLOBAL VARIABLES
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
started = False
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
counter = 0
text = ""
seconds = 0
minutes = 0
width = 0
height = 0
win = False
current_level = 0
max_level = 1
finished = False

# FONTS
font_min = pygame.font.Font('ken_fonts/kenpixel_high_square.ttf', 20)
font_large = pygame.font.Font('ken_fonts/kenpixel_high_square.ttf', 35)
font_extralarge = pygame.font.Font('ken_fonts/kenpixel_high_square.ttf', 70)

# TEXTURES
wallTexture = pygame.image.load('wall.png')
floorTexture = pygame.image.load('floor.png')
playerTexture = pygame.image.load('player.png')
checkpointTexture = pygame.image.load('checkpoint.png')
finishedTexture = pygame.image.load('finished.png')
finishedTexture = pygame.transform.scale(finishedTexture, (400, 300))
menuTexture = pygame.image.load('menu.png')
menuTexture = pygame.transform.scale(menuTexture, (400, 200))

# MUSIC
mixer.init()
mixer.music.set_volume(0.7)
mixer.music.load("menu.mp3")
mixer.music.play()

# SOUND EFFECTS
sound_effect = pygame.mixer.Sound('pop.ogg')
sound_win = pygame.mixer.Sound('winner.ogg')

# USER EVENT
pygame.time.set_timer(pygame.USEREVENT, 1)

def rectangle(start_x, start_y, size):
    x = start_x-(size/2)
    y = start_y-(size/2)
    return pygame.Rect(x, y, size, size)


def load_level(level):
    # SPECIFY THE GLOBAL VARIABLES
    global starting_x
    global starting_y
    global count
    global row
    global player_pos
    global surface
    global menu
    global pixels
    global width
    global height
    global paused
    global speed
    global direction
    global win

    # RESET THE COUNT FOR PLAYER POSITON
    count = 0
    row = 0
    
    # FIND THE STARTING POINT
    with Image.open("level-" + str(level) + ".png") as im:
        (width, height) = (im.width, im.height)
        pixels = list(im.getdata())
    for x in pixels:
        if x == (166, 230, 29, 255) or x == (168, 230, 29, 255):
            starting_x = count * size
            starting_y = row * size
        count += 1
        if count > width - 1:
            count = 0
            row += 1

    # SET THE STARTING POINT FOR THE PLAYER
    player_pos = rectangle(starting_x + (size / 2), starting_y + (size / 2), size)

    # RESET THE DEFAULT VALUES
    speed = 10
    direction = "right"
    surface = pygame.Surface((width * size, height * size))
    paused = False
    win = False


def reset_game():
    # RESET GLOBAL VARIABLES
    global text
    global counter
    global seconds
    global minutes
    global height
    global width
    global started
    global running
    global finished
    global current_level
    global mixer

    # SET MUSIC
    mixer.music.stop()
    mixer.music.load("music-0.mp3")
    mixer.music.play()

    counter = 0
    text = "00:00:00"
    seconds = 0
    minutes = 0
    width = 0
    height = 0
    started = True
    running = True
    win = False
    finished = False
    current_level = 0
    load_level(current_level)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if started:
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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_p] and finished:
        reset_game()

    if paused == False and started:

        screen.fill((3,26,34))
        surface.fill((3,26,34))

        screen.blit(font_min.render("TIMER", True, (202, 220, 159)), (screen.get_width()-70, 20))
        screen.blit(font_min.render("LEVEL", True, (202, 220, 159)), (20, 20))
        screen.blit(font_large.render(str(current_level), True, (202, 220, 159)), (20, 40))
        screen.blit(font_large.render(text, True, (202, 220, 159)), (screen.get_width()-121, 40))

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
            elif x == (237, 28, 35, 255):
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
            elif this_collide and pixels[index] == (237,28,35,255):
                if win != True:
                    win = True
                    paused = True
                    if(current_level != max_level):
                        current_level += 1
                        print("Loading: " + str(current_level))
                        load_level(current_level)
                    else:
                        finished = True
                        print("You Won")
                
        player = pygame.draw.rect(surface, (49, 86, 57, 0), player_pos)

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

        if collide and paused == False:
            player_pos = rectangle(starting_x + (size / 2), starting_y + (size / 2), size)
            speed = 10
            direction = "right"

        screen.blit(surface, ((screen.get_width() / 2) - player_pos.x, (screen.get_height() / 2) - player_pos.y))

        if finished:

            sound_win.play()
            mixer.music.stop()
            
            with Image.open("finished.png") as im:
                (finished_width, finished_height) = (im.width, im.height)
            menu = pygame.Surface((400, 300))
            menu.blit(finishedTexture, (0,0))

            text_win = font_large.render("YOU'RE FREE", True, (15, 56, 15))
            text_win_rect = text_win.get_rect(center=(menu.get_width()/2, 70))
            menu.blit(text_win, text_win_rect)

            text_time = font_extralarge.render(str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + ":" + str(int(milliseconds)).zfill(2), True, (15, 56, 15))
            text_time_rect = text_time.get_rect(center=(menu.get_width()/2, 120))
            menu.blit(text_time, text_time_rect)

            text_time_label = font_min.render("C O M P L E T I O N  T I M E", True, (15, 56, 15))
            text_time_label_rect = text_time_label.get_rect(center=(menu.get_width()/2, 170))
            menu.blit(text_time_label, text_time_label_rect)

            # menu.blit(playerTexture, ((menu.get_width() / 2) - 25, -25))

            screen.blit(menu, ((screen.get_width() / 2) - finished_width, (screen.get_height() / 2) - finished_height))

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    elif started == False:
        if keys[pygame.K_p]:
            reset_game()
        screen.fill((3,26,34))
        screen.blit(font_extralarge.render("SQUARES NIGHTMARE", True, (202, 220, 159)), ((screen.get_width() / 2) - 200, screen.get_height() / 2))
        screen.blit(playerTexture, ((screen.get_width() / 2) - 25, (screen.get_height() / 2) - 100))
        screen.blit(menuTexture, ((screen.get_width() / 2) - 200, (screen.get_height() / 2) + 100))
        pygame.display.flip()
        dt = clock.tick(60) / 1000


pygame.quit()