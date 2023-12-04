import pygame
import pyautogui
import os
from models.button import button
import random
from models.Player import Player
from models.Obstacle import Obstacle


def main():
    pygame.init()

    # make full screen
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

    # calc position of background
    background_x = (full_screen_size[0] - background_width) // 2
    background_y = (full_screen_size[1] - background_height) // 2
    background_image = pygame.transform.smoothscale(
        original_background, (background_width, background_height)
    )

    # make header
    pygame.display.set_caption("Need for Speed")
    icon = pygame.image.load(os.path.join(os.getcwd(), "image/siep.jpg")).convert()
    pygame.display.set_icon(icon)

    # start screen
    clock = pygame.time.Clock()
    amount_of_players = start_screen(clock, screen)
    if amount_of_players == 0:
        return

    pygame.mouse.set_visible(0)
    players: pygame.sprite.Group[Player] = pygame.sprite.Group()
    for p in range(0, amount_of_players):
        # player settings
        player_x = 900 + 200 * p
        player_y = 900
        if amount_of_players == 1:
            player_x += 99

        # create player
        player = Player(player_x, player_y)
        players.add(player)

    player_speed = 5

    # player sounds
    pygame.mixer.music.load(os.path.join(os.getcwd(), "data/sounds/m3.wav"))
    pygame.mixer.music.play(-1)
    the_funni = pygame.mixer.Sound(
        os.path.join(os.getcwd(), "data/sounds/the_funni.wav")
    )

    hardbrake = pygame.mixer.Sound(
        os.path.join(os.getcwd(), "data/sounds/hardbrake.wav")
    )

    # create obstacles
    ob_image = pygame.image.load(os.path.join(os.getcwd(), "image/enemy car.jpg"))
    ob_image = pygame.transform.rotate(ob_image, 180)
    obstacles = pygame.sprite.Group()
    ob1 = Obstacle(850, 300, ob_image)
    obstacles.add(ob1)

    animations = pygame.sprite.Group()
    game_over_count_down = 150
    score = 0  # Initialize the score
    font = pygame.font.Font(None, 36)  # Create a font object
    diff = 5
    game_over = False
    while True:
        # dificulty
        if score > diff * diff:
            diff += 1
        try:
            if len(players) == 0:
                game_over = True
                pygame.mixer.music.stop()
                if game_over_count_down == 0:
                    raise SystemExit
                game_over_count_down -= 1
            if not game_over:
                for event in pygame.event.get():
                    match event.type:
                        case pygame.QUIT:
                            raise SystemExit
                        case pygame.KEYDOWN:
                            match event.key:
                                case pygame.K_ESCAPE:
                                    raise SystemExit
                                case pygame.K_w:
                                    players.sprites()[0].dy = -player_speed
                                case pygame.K_UP:
                                    if len(players) == 2:
                                        players.sprites()[1].dy = -player_speed
                                    else:
                                        players.sprites()[0].dy = -player_speed
                                case pygame.K_a:
                                    players.sprites()[0].dx = -player_speed
                                    if players.sprites()[0].degree >= -30:
                                        players.sprites()[0].turn(350)
                                case pygame.K_LEFT:
                                    if len(players) == 2:
                                        players.sprites()[1].dx = -player_speed
                                        if players.sprites()[1].degree >= -30:
                                            players.sprites()[1].turn(350)
                                    else:
                                        players.sprites()[0].dx = -player_speed
                                        if players.sprites()[0].degree >= -30:
                                            players.sprites()[0].turn(350)
                                case pygame.K_s:
                                    players.sprites()[0].dy = player_speed
                                    if not players.sprites()[0].on_hardbrake:
                                        pygame.mixer.Sound.play(hardbrake, fade_ms=800)
                                        players.sprites()[0].on_hardbrake = True
                                case pygame.K_DOWN:
                                    if len(players) == 2:
                                        players.sprites()[1].dy = player_speed
                                        if not players.sprites()[1].on_hardbrake:
                                            pygame.mixer.Sound.play(
                                                hardbrake, fade_ms=800
                                            )
                                            players.sprites()[1].on_hardbrake = True
                                    else:
                                        players.sprites()[0].dy = player_speed
                                        if not players.sprites()[0].on_hardbrake:
                                            pygame.mixer.Sound.play(
                                                hardbrake, fade_ms=800
                                            )
                                            players.sprites()[0].on_hardbrake = True
                                    pygame.mixer.music.fadeout(1000)
                                case pygame.K_d:
                                    players.sprites()[0].dx = player_speed
                                    if players.sprites()[0].degree <= 30:
                                        players.sprites()[0].turn(10)
                                case pygame.K_RIGHT:
                                    if len(players) == 2:
                                        players.sprites()[1].dx = player_speed
                                        if players.sprites()[1].degree <= 30:
                                            players.sprites()[1].turn(10)
                                    else:
                                        players.sprites()[0].dx = player_speed
                                        if players.sprites()[0].degree <= 30:
                                            players.sprites()[0].turn(10)
                        case pygame.KEYUP:
                            match event.key:
                                case pygame.K_w | pygame.K_s:
                                    players.sprites()[0].dy = 0
                                    if event.key == pygame.K_s:
                                        pygame.mixer.Sound.stop(hardbrake)
                                        players.sprites()[0].on_hardbrake = False
                                        pygame.mixer.music.play(-1)
                                case pygame.K_UP | pygame.K_DOWN:
                                    if len(players) == 2:
                                        players.sprites()[1].dy = 0
                                        if event.key == pygame.K_DOWN:
                                            pygame.mixer.Sound.stop(hardbrake)
                                            players.sprites()[1].on_hardbrake = False
                                            pygame.mixer.music.play(-1)
                                    else:
                                        players.sprites()[0].dy = 0
                                        if event.key == pygame.K_DOWN:
                                            pygame.mixer.Sound.stop(hardbrake)
                                            players.sprites()[0].on_hardbrake = False
                                            pygame.mixer.music.play(-1)
                                case pygame.K_a | pygame.K_d:
                                    players.sprites()[0].dx = 0
                                    players.sprites()[0].to_default()
                                case pygame.K_LEFT | pygame.K_RIGHT:
                                    if len(players) == 2:
                                        players.sprites()[1].dx = 0
                                        players.sprites()[1].to_default()
                                    else:
                                        players.sprites()[0].dx = 0
                                        players.sprites()[0].to_default()

                                case pygame.K_DELETE:
                                    for player in players:
                                        player.explode(animations)
                                case pygame.K_e | pygame.K_KP_1:
                                    if len(players) != 0:
                                        pygame.mixer.Sound.play(the_funni)

            # Update player position based on velocity only if the player is alive
            for player in players:
                tot_collision: pygame.sprite.Group = players.copy()
                tot_collision.remove(player)
                if tot_collision is None:
                    tot_collision = obstacles.copy()
                else:
                    tot_collision.add(obstacles)
                player.move(pygame.sprite.Group(tot_collision), player.dx, player.dy)
                # border
                player.rect.x = max(720, min(player.rect.x, 1100))
                player.rect.y = max(10, min(player.rect.y, 1700))
                player.rect.y = min(1025, max(player.rect.y, 10))

            # ob1.move(players, 0, -5 + diff, animations)
            if len(players) != 0:
                if ob1.rect.bottom >= full_screen_size[1]:
                    # Reset obstacles only if the player is alive
                    obstacles.empty()
                    obs_x = random.randrange(795, 1138)
                    obs_y = random.randrange(-100, 0)
                    ob1 = Obstacle(obs_x, obs_y, ob_image)
                    obstacles.add(ob1)

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


def start_screen(clock: pygame.time.Clock, screen: pygame.surface.Surface) -> int:
    # make buttons
    font = pygame.font.SysFont("Georgia", 40, bold=True)

    # start button
    start_btn = button(font, "START", screen.get_width() / 4, screen.get_height() / 2)

    # quit button
    quit_btn = button(font, "QUIT", screen.get_width() / 4 * 3, screen.get_height() / 2)

    # p1
    p1_btn = button(font, "ONE PLAYER", screen.get_width() / 4, screen.get_height() / 2)

    # p2
    p2_btn = button(
        font, "TWO PLAYERS", screen.get_width() / 4 * 3, screen.get_height() / 2
    )
    btns = pygame.sprite.Group()
    btns.add(start_btn, quit_btn)
    while True:
        screen.fill("black")
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return 0
                case pygame.MOUSEBUTTONDOWN:
                    if start_btn in btns:
                        if start_btn.rect.collidepoint(event.pos):
                            btns.empty()
                            btns.add(p1_btn, p2_btn)
                        elif quit_btn.rect.collidepoint(event.pos):
                            pygame.quit()
                            return 0
                    else:
                        if p1_btn.rect.collidepoint(event.pos):
                            return 1
                        elif p2_btn.rect.collidepoint(event.pos):
                            return 2
        # draw start buttons
        btns.draw(screen)

        pygame.display.flip()
        clock.tick(15)


if __name__ == "__main__":
    main()
