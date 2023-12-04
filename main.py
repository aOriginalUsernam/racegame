import pygame
import pyautogui
import os
import random
from models.Player import Player
from models.Obstacle import Obstacle

def main():
    pygame.init()

    full_screen_size = pyautogui.size()
    screen = pygame.display.set_mode(full_screen_size)

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


    background_x = (full_screen_size[0] - background_width) // 2
    background_y = (full_screen_size[1] - background_height) // 2
    background_image = pygame.transform.smoothscale(
        original_background, (background_width, background_height)
    )

    pygame.display.set_caption("Need for Speed")
    icon = pygame.image.load(
        os.path.join(os.getcwd(), "image/siep.jpg")
    ).convert()
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()


    pygame.mouse.set_visible(0)
    player_scale = background_x / 2
    player_x = 999
    player_y = 999


    players = pygame.sprite.Group()
    player = Player(player_x, player_y)
    players.add(player)


    player_speed = 5
    player_dx, player_dy = 0, 0

    pygame.mixer.music.load(os.path.join(os.getcwd(), "data/sounds/m3.wav"))
    pygame.mixer.music.play(-1)
    the_funni = pygame.mixer.Sound(
        os.path.join(os.getcwd(), "data/sounds/the_funni.wav")
    )

    on_hardbrake = False
    hardbrake = pygame.mixer.Sound(
        os.path.join(os.getcwd(), "data/sounds/hardbrake.wav")
    )

    ob_image = pygame.image.load(
        os.path.join(os.getcwd(), "image/enemy car.jpg")
    )
    ob_image = pygame.transform.rotate(ob_image, 180)
    obstacles = pygame.sprite.Group()
    ob1 = Obstacle(850, 300, ob_image)
    obstacles.add(ob1)


    animations = pygame.sprite.Group()
    game_over_count_down = 150
    score = 0  # Initialize the score
    font = pygame.font.Font(None, 36)  # Create a font object

    # Initialize the player_alive flag
    player_alive = True

    while True:
        try:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        raise SystemExit
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                raise SystemExit
                            case pygame.K_w | pygame.K_UP:
                                player_dy = -player_speed
                            case pygame.K_a | pygame.K_LEFT:
                                player_dx = -player_speed
                                if player.degree >= -30:
                                    player.turn(350)
                            case pygame.K_s | pygame.K_DOWN:
                                player_dy = player_speed
                                if not on_hardbrake:
                                    pygame.mixer.Sound.play(hardbrake, fade_ms=800)
                                    on_hardbrake = True
                                pygame.mixer.music.fadeout(1000)
                            case pygame.K_d | pygame.K_RIGHT:
                                player_dx = player_speed
                                if player.degree <= 30:
                                    player.turn(10)
                    case pygame.KEYUP:
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
                                player_alive = False  # Set the player_alive flag to False
                            case pygame.K_e:
                                pygame.mixer.Sound.play(the_funni)


            # Update player position based on velocity only if the player is alive
            if player_alive:
                player.move(obstacles, player_dx, player_dy)
                ob1.move(players, 0, 17, animations)


            if ob1.rect.bottom >= full_screen_size[1]:
                # Reset obstacles only if the player is alive
                if len(players) > 0:
                    obstacles.empty()
                    obs_x = random.randrange(795, 1138)
                    obs_y = random.randrange(-100, 0)
                    ob1 = Obstacle(obs_x, obs_y, ob_image)
                    obstacles.add(ob1)

            if len(players) > 0:
                score += 1

            screen.fill("purple")
            screen.blit(fullscreen_background, (0, 0))
            screen.blit(background_image, (background_x, background_y))


            players.draw(screen)
            obstacles.draw(screen)


            for animation in animations.sprites():
                animation.update()
            animations.draw(screen)

            # Display the score on the screen
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)

        except SystemExit:
            pygame.quit()
            break

if __name__ == "__main__":
    main()
