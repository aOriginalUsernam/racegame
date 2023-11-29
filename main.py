import pygame
import pyautogui
import os


def __main__() -> None:
    pygame.init()

    # make full screen
    full_screen_size: tuple[int] = pyautogui.size()
    screen: pygame.Surface = pygame.display.set_mode(full_screen_size)

    # make header
    pygame.display.set_caption("ned for spied")
    icon: pygame.Surface = pygame.image.load(
        os.path.join(os.getcwd(), "img\siep.jpg")
    ).convert()
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    pygame.mouse.set_visible(0)

    # player = pygame.Rect()

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
                                pass
                            case pygame.K_a | pygame.K_LEFT:
                                # go left
                                pass
                            case pygame.K_s | pygame.K_DOWN:
                                # go down
                                pass
                            case pygame.K_d | pygame.K_RIGHT:
                                # go right
                                pass
        except SystemExit:
            pygame.quit()
            break

        # Do logical updates here.
        # ...
        screen.fill("purple")  # Fill the display with a solid color

        # Render the graphics here.
        # ...

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)  # wait until next frame (at 60 FPS)


if __name__ == "__main__":
    __main__()
