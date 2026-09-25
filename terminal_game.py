import pygame
import pygame_gui

from config import Config


class Game:
    def __init__(self, config: Config):
        self.running = False
        self.config = config

    def __enter__(self):
        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=512,
            allowedchanges=pygame.AUDIO_ALLOW_ANY_CHANGE,
        )

        pygame.init()
        pygame.mixer.set_num_channels(16)

        self.screen = pygame.display.set_mode(
            (self.config.window_width, self.config.window_height)
        )

        pygame.display.set_caption("Hacker's terminal")
        self.clock = pygame.time.Clock()

        self._load_font()
        self._load_images()
        self._load_sounds()

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.manager = pygame_gui.UIManager(
            (self.config.window_width, self.config.window_height)
        )
        self.manager.add_font_paths(
            "BlackOpsOne", "fonts/BlackOpsOne-Regular.ttf"
        )
        self.manager.get_theme().load_theme("terminal_theme.json")

        self.score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 200), (200, 40)),
            text="Hacker's terminal",
            manager=self.manager,
        )

        self.running = True
        return self

    def __exit__(self, *args):
        pygame.quit()

    def _load_font(self) -> None:
        self.font = pygame.font.Font(
            self.config.font_path, self.config.gui_font_size
        )

    def _load_images(self) -> None:
        pass

    def _load_sounds(self) -> None:
        pass

    def run(self):
        while self.running:
            self.dt = self.clock.tick(self.config.fps) / 1000
            self.watch_for_events()
            self.update()
            self.draw()

    def watch_for_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.manager.process_events(event)

    def update(self):
        self.all_sprites.update(self.dt)

        self.manager.update(self.dt)

    def draw(self):
        self.all_sprites.draw(self.screen)

        self.manager.draw_ui(self.screen)

        pygame.display.flip()
