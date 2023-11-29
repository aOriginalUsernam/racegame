import pygame
import pyautogui
import os
from models.player import Player

def __main__() -> None:
    pygame.init()

    # make full screen
    full_screen_size: tuple[int] = pyautogui.size()
    screen: pygame.Surface = pygame.display.set_mode(full_screen_size)

    # Load background image
    fullscreen_background = pygame.image.load(os.path.join(os.getcwd(), "image/grass.png")).convert()
    fullscreen_background = pygame.transform.smoothscale(fullscreen_background, full_screen_size)
    
    original_background = pygame.image.load(os.path.join(os.getcwd(), "image/road_0.png"))
    background_width, background_height = original_background.get_size()

    # Calculate the position to center the background image
    background_x = (full_screen_size[0] - background_width) // 2
    background_y = (full_screen_size[1] - background_height) // 2
    background_image = pygame.transform.smoothscale(original_background, (background_width, background_height))
    # make header
    pygame.display.set_caption("ned for spied")
    icon: pygame.Surface = pygame.image.load(
        os.path.join(os.getcwd(), "image\siep.jpg")).convert()
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    # player settings
    pygame.mouse.set_visible(0)
    player_x = 999
    player_y = 999

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
            player_has_rotated = False
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
                                    player.turn(-10)
                                    player_has_rotated = True
                            case pygame.K_s | pygame.K_DOWN:
                                # go down
                                player_dy = player_speed
                            case pygame.K_d | pygame.K_RIGHT:
                                # go right
                                player_dx = player_speed
                                if player.degree <= 30:
                                    player.turn(10)
                                    player_has_rotated = True
                    case pygame.KEYUP:
                        # stop moving when key is released
                        match event.key:
                            case pygame.K_w | pygame.K_s | pygame.K_UP | pygame.K_DOWN:
                                player_dy = 0
                            case pygame.K_a | pygame.K_d | pygame.K_LEFT | pygame.K_RIGHT:
                                player_dx = 0
                                player.turn(player.degree * -1)
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

        # Draw fullscreen background image
        screen.blit(fullscreen_background, (0, 0))
        # Draw background image
        screen.blit(background_image, (background_x, background_y))

        # draw the player(s)
        players.draw(screen)

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)  # wait until the next frame (at 60 FPS)

if __name__ == "__main__":
    __main__()
