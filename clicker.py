import pygame
import pygame_gui


def main():
    pygame.init()

    WINDOW_SIZE = (800, 600)

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Clicker")

    manager = pygame_gui.UIManager(WINDOW_SIZE, theme_path="theme.json")

    click_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 300), (100, 50)),
        text="Click!",
        manager=manager,
    )

    score_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((350, 200), (100, 40)),
        text="Score: 0",
        manager=manager,
    )

    score = 0
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    is_running = False

                case pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == click_button:
                        score += 1
                        score_label.set_text(f"Score: {score}")

            manager.process_events(event)

        manager.update(dt)

        screen.fill("#006699")
        manager.draw_ui(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
