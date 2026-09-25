import pygame
import pygame_gui

from config import Config

MARGIN = 50
INPUT_HEIGHT = 80


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

        self.input_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (MARGIN, self.config.window_height - INPUT_HEIGHT),
                (self.config.window_width - 2 * MARGIN, MARGIN),
            ),
            manager=self.manager,
            object_id="#input_field",
        )
        self.input_field.set_text("> ")

        self.manager.set_focus_set(self.input_field)

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
                case pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_element == self.input_field:
                        text = self.input_field.get_text()
                        if text in ("", ">"):
                            self.input_field.set_text("> ")
                case pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.input_field:
                        command = event.text[2:]
                        self.process_command(command)
                        self.input_field.set_text("> ")

            self.manager.process_events(event)

    def process_command(self, command: str):
        match command:
            case "quit" | "q":
                pygame.event.post(pygame.Event(pygame.QUIT))
                return
            case _:
                print(f"Command entered: {command}")

    def update(self):
        self.all_sprites.update(self.dt)

        self.manager.update(self.dt)

    def draw(self):
        self.all_sprites.draw(self.screen)

        self.manager.draw_ui(self.screen)

        pygame.display.flip()
