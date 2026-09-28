import random

import pygame
import pygame_gui

from config import Config
from os_command_runner import OSCommandRunner

MARGIN = 50
INPUT_HEIGHT = 80
TARGET_IP = "192.168.1.1"


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

        self.output = pygame_gui.elements.UITextBox(
            html_text="<font color=#00ff00>Hacking system core initialized...</font>\n",
            relative_rect=pygame.Rect(
                (MARGIN, MARGIN),
                (
                    self.config.window_width - 2 * MARGIN,
                    self.config.window_height - 2 * MARGIN - INPUT_HEIGHT,
                ),
            ),
            manager=self.manager,
            object_id="#console_output",
        )
        self.output.set_active_effect(
            pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
            params={"time_per_letter": 0.05},
        )

        self.os_command_runner = OSCommandRunner(
            on_output_callback=lambda text: self.print_to_output(
                text, color="#aaaaaa"
            )
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

    def _gen_success(self) -> str:
        if random.random() > 0.3:
            self.print_to_output("Success!", "#00ff00")
        else:
            self.print_to_output("Failure. Try again", "#ff0000")

    def process_command(self, command: str):
        match command:
            case "quit" | "q":
                self.print_to_output("Quitting...")
                pygame.event.post(pygame.Event(pygame.QUIT))
                return
            case "help":
                self.print_to_output(
                    "Available commands: help, scan, hack, clear",
                    "#aaaaaa",
                )
            case "scan":
                self.print_to_output(
                    f"Running nmap on target IP {TARGET_IP}...",
                    "#006699",
                )
                self._gen_success()
            case "hack":
                self.print_to_output(
                    f"Hacking target IP {TARGET_IP}...",
                    "#006699",
                )
                self._gen_success()
            case "clear":
                self.output.clear()
            case "hello, friend":
                self.print_to_output("Domo Arigato, Mr. Roboto")
            case _:
                self.print_to_output(f"h4ck3r: {command}")
                self.os_command_runner.run(command)

    def print_to_output(self, text: str, color: str = "#ffffff"):
        html = f"<font color={color}>{text}</font><br>"
        self.output.append_html_text(html)

    def update(self):
        self.all_sprites.update(self.dt)

        self.manager.update(self.dt)

    def draw(self):
        self.all_sprites.draw(self.screen)

        self.manager.draw_ui(self.screen)

        pygame.display.flip()
