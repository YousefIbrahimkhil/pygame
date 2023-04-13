# Example file showing a circle moving on screen
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
speed = 10
direction = "down"

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "blue", player_pos, 10)

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