import pygame
import pyautogui
import os
from models.player import Player


def __main__() -> None:
    pygame.init()

    # make full screen
    full_screen_size: tuple[int] = pyautogui.size()
    screen: pygame.Surface = pygame.display.set_mode(full_screen_size)

    # make header
    pygame.display.set_caption("ned for spied")
    icon: pygame.Surface = pygame.image.load(
        os.path.join(os.getcwd(), "image\siep.jpg")
    ).convert()
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    # player settings
    pygame.mouse.set_visible(0)
    player_x = 250
    player_y = 400

    # create player
    players = pygame.sprite.Group()
    player = Player(player_x, player_y)
    players.add(player)

    # player velocity
    player_speed = 5
    player_dx, player_dy = 0, 0

    while True:
        try:
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
                            case pygame.K_s | pygame.K_DOWN:
                                # go down
                                player_dy = player_speed
                            case pygame.K_d | pygame.K_RIGHT:
                                # go right
                                player_dx = player_speed
                    case pygame.KEYUP:
                        # stop moving when key is released
                        match event.key:
                            case pygame.K_w | pygame.K_s | pygame.K_UP | pygame.K_DOWN:
                                player_dy = 0
                            case pygame.K_a | pygame.K_d | pygame.K_LEFT | pygame.K_RIGHT:
                                player_dx = 0
        except SystemExit:
            pygame.quit()
            break

        # Update player position based on velocity
        player.rect.x += player_dx
        player.rect.y += player_dy

        # Do logical updates here.
        # ...
        screen.fill("purple")  # Fill the display with a solid color

        # Render the graphics here.

        # draw the player(s)
        players.draw(screen)

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)  # wait until the next frame (at 60 FPS)


if __name__ == "__main__":
    __main__()
