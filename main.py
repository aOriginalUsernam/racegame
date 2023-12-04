import pygame
import pyautogui
import os
import random
from models.Player import Player
from models.Obstacle import Obstacle


def __main__() -> None:
    pygame.init()

    # make full screen
    full_screen_size: tuple[int] = pyautogui.size()
    screen: pygame.Surface = pygame.display.set_mode(full_screen_size)

    # Load background image
    fullscreen_background = pygame.image.load(
        os.path.join(os.getcwd(), "image/grass.png")
    ).convert()
    fullscreen_background = pygame.transform.smoothscale(
        fullscreen_background, full_screen_size
    )

    original_background = pygame.image.load(
        os.path.join(os.getcwd(), "image/road_0.png")
    )
    background_width, background_height = original_background.get_size()

    # Calculate the position to center the background image
    background_x = (full_screen_size[0] - background_width) // 2
    background_y = (full_screen_size[1] - background_height) // 2
    background_image = pygame.transform.smoothscale(
        original_background, (background_width, background_height)
    )
    # make header
    pygame.display.set_caption("ned for spied")
    icon: pygame.Surface = pygame.image.load(
        os.path.join(os.getcwd(), "image\siep.jpg")
    ).convert()
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    # player settings
    pygame.mouse.set_visible(0)
    player_scale = background_x / 2
    player_x = 999
    player_y = 999

    # create player
    players = pygame.sprite.Group()
    player = Player(player_x, player_y)
    players.add(player)

    # player velocity
    player_speed = 5
    player_dx, player_dy = 0, 0

    # player car sound
    pygame.mixer.music.load(os.path.join(os.getcwd(), "data\sounds\m3.wav"))
    pygame.mixer.music.play(-1)
    the_funni = pygame.mixer.Sound(
        os.path.join(os.getcwd(), "data\\sounds\\the_funni.wav")
    )
    # hardbrake sound settings
    on_hardbrake = False
    hardbrake = pygame.mixer.Sound(
        os.path.join(os.getcwd(), "data\sounds\hardbrake.wav")
    )

    # create obstacles
    obstacles = pygame.sprite.Group()
    ob1 = Obstacle(850, 300)
    obstacles.add(ob1)

    # create animations
    animations = pygame.sprite.Group()
    jover = 200
    while True:
        try:
            # check for game over
            if len(players) == 0:
                pygame.mixer.music.stop()
                # game over :(
                if len(animations) == 0:
                    # wait until kaBOOM sound is jover
                    if jover == 0:
                        raise SystemExit
                    jover -= 1

            # Process player inputs.
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        raise SystemExit
                    case pygame.KEYDOWN:
                        # check which key was pressed
                        match event.key:
                            case pygame.K_ESCAPE:  # esc closes screen
                                raise SystemExit
                            case pygame.K_w | pygame.K_UP:
                                # go up
                                player_dy = -player_speed
                            case pygame.K_a | pygame.K_LEFT:
                                # go left
                                player_dx = -player_speed
                                if player.degree >= -30:
                                    player.turn(350)
                            case pygame.K_s | pygame.K_DOWN:
                                # go down
                                player_dy = player_speed
                                # pygame.mixer.music.pause()
                                if not on_hardbrake:
                                    pygame.mixer.Sound.play(hardbrake, fade_ms=800)
                                    on_hardbrake = True
                                pygame.mixer.music.fadeout(1000)
                            case pygame.K_d | pygame.K_RIGHT:
                                # go right
                                player_dx = player_speed
                                if player.degree <= 30:
                                    player.turn(10)
                    case pygame.KEYUP:
                        # stop moving when key is released
                        match event.key:
                            case pygame.K_w | pygame.K_s | pygame.K_UP | pygame.K_DOWN:
                                player_dy = 0
                                if (
                                    event.key == pygame.K_s
                                    or event.key == pygame.K_DOWN
                                ):
                                    pygame.mixer.Sound.stop(hardbrake)
                                    on_hardbrake = False
                                    pygame.mixer.music.play(-1)
                            case pygame.K_a | pygame.K_d | pygame.K_LEFT | pygame.K_RIGHT:
                                player_dx = 0
                                player.to_default()
                            case pygame.K_DELETE:
                                player.explode(animations)
                            case pygame.K_e:
                                pygame.mixer.Sound.play(the_funni)
        except SystemExit:
            pygame.quit()
            break

        # Update player position based on velocity
        player.move(obstacles, player_dx, player_dy)
        ob1.move(obstacles, 0, -285)

        # Check if the obstacle is out of the border, and spawn a new one
        # ...

        # Check if the obstacle is out of the border, and spawn a new one
        if ob1.rect.bottom >= full_screen_size[1]:
            obstacles.empty()
            obs_x = random.randrange(795, 1138)
            obs_y = random.randrange(-100, 0)
            ob1 = Obstacle(obs_x, obs_y)
            obstacles.add(ob1)

        # Do logical updates here.
        player.rect.x = max(740, min(player.rect.x, 1137))
        player.rect.y = max(10, min(player.rect.y, 1700))
        player.rect.y = min(1025, max(player.rect.y, 10))
        # ...
        screen.fill("purple")  # Fill the display with a solid color

        # Render the graphics here.

        # Draw fullscreen background image
        screen.blit(fullscreen_background, (0, 0))
        # Draw background image
        screen.blit(background_image, (background_x, background_y))

        # draw the player(s)
        players.draw(screen)
        obstacles.draw(screen)

        # draw animations
        for animation in animations.sprites():
            animation.update()
        animations.draw(screen)

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)  # wait until the next frame (at 100 FPS)


if __name__ == "__main__":
    __main__()
