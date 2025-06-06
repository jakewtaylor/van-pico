from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB565
from pimoroni import RGBLED, Button
from machine import Pin, Timer
from math import ceil
import random

display = PicoGraphics(
    display=DISPLAY_PICO_DISPLAY_2,
    # maybe remove this (falling back to RGB332) if performance becomes an issue... but the colours are much nicer like this!
    pen_type=PEN_RGB565
)
display.set_backlight(0.6)

# button_a = Pin(12, Pin.IN, Pin.PULL_UP)
# button_b = Pin(13, Pin.IN, Pin.PULL_UP)
button_x = Pin(14, Pin.IN, Pin.PULL_UP)
button_y = Pin(15, Pin.IN, Pin.PULL_UP)

# set up constants for drawing
WIDTH, HEIGHT = display.get_bounds()
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

SCREEN_PAD = 10
NAV_WIDTH = 16
NAV_ARROW_SIZE = 11
NAV_CIRCLE_SIZE = 6
ARROW_Y_OFFSET = 50
SCREEN_WIDTH = WIDTH - NAV_WIDTH

SLEEP_TIMEOUT = 10_000

COLORS = {
    "BACKGROUND": display.create_pen(0, 0, 0),
    "FOREGROUND": display.create_pen(255, 255, 255),
    "UI": display.create_pen(127, 127, 127),
    "UI_2": display.create_pen(48, 48, 48),
    "GREEN": display.create_pen(0, 255, 0),
    "RED": display.create_pen(255, 0, 0),
    "BLUE": display.create_pen(0, 0, 255),
    "GREY": display.create_pen(179, 179, 179)
}

# Sets up the RGB LED beside the display screen
led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

class Screen:
    navigating_direction = 0

    def __init__(self, display: PicoGraphics, current_index: int, total_screens: int) -> None:
        self.display = display
        self.current_index = current_index
        self.total_screens = total_screens

    def set_current_index(self, index: int) -> None:
        self.current_index = index

    def set_navigating(self, direction: int) -> None:
        self.navigating_direction = direction;

    def draw(self):
        self.display.set_backlight(0.6)
        self.display.set_font("bitmap8")

        self.display.set_pen(COLORS["BACKGROUND"])
        self.display.clear()

        self.draw_navbar()

    def draw_text(self, message: str, center = False, scale = 2):
        self.display.set_pen(COLORS["FOREGROUND"])

        if (center):
            text_width = self.display.measure_text(message, scale)
            self.display.text(message, int((NAV_WIDTH + (SCREEN_WIDTH / 2)) - (text_width / 2)), SCREEN_PAD, SCREEN_WIDTH, scale)
        else:
            self.display.text(message, SCREEN_PAD + NAV_WIDTH, SCREEN_PAD, WIDTH, scale)

    def draw_table(self, lines: list[tuple[str, str, int | None]], offset = 0, text_scale = 2, line_space = 8):
        font_size = 8
        line_height = (font_size * text_scale)
        dot_width = self.display.measure_text(".", text_scale)

        for i, (a, b, color) in enumerate(lines):
            self.display.set_pen(COLORS["FOREGROUND"])
            y = offset + SCREEN_PAD + (line_height * i) + (line_space if i > 0 else 0)
            # Draw left side
            left_width = self.display.measure_text(a, text_scale)
            self.display.text(a, SCREEN_PAD + NAV_WIDTH, y, SCREEN_WIDTH, text_scale)

            # Draw right side
            self.display.set_pen(COLORS["FOREGROUND"] if color is None else color)
            right_width = self.display.measure_text(b, text_scale)
            self.display.text(b, NAV_WIDTH + SCREEN_WIDTH - SCREEN_PAD - right_width, y, SCREEN_WIDTH, text_scale)

            # Draw connecting dots
            self.display.set_pen(COLORS["UI"])
            width_of_dots = SCREEN_WIDTH - (SCREEN_PAD * 2) - left_width - right_width
            num_dots_needed = int(width_of_dots / dot_width)
            dot_str = "." * num_dots_needed
            self.display.text(dot_str, NAV_WIDTH + SCREEN_PAD + left_width, y, SCREEN_WIDTH, text_scale)

    def draw_navbar(self):
        # Draw the frame
        self.display.set_pen(COLORS["UI"])
        self.display.rectangle(0, 0, NAV_WIDTH, int(HEIGHT / 2))
        self.display.set_pen(COLORS["UI"])
        self.display.rectangle(0, int(HEIGHT / 2), NAV_WIDTH, int(HEIGHT / 2))

        # Draw the up arrow
        # up_point1 = (int(NAV_WIDTH / 2), ARROW_Y_OFFSET)
        # up_point2 = (int((NAV_WIDTH / 2) - (NAV_ARROW_SIZE / 2)), int(ARROW_Y_OFFSET + NAV_ARROW_SIZE))
        # up_point3 = (int((NAV_WIDTH / 2) + (NAV_ARROW_SIZE / 2)), int(ARROW_Y_OFFSET + NAV_ARROW_SIZE))
        # self.display.set_pen(COLORS["FOREGROUND"] if self.navigating_direction == -1 else COLORS["BACKGROUND"])
        # self.display.triangle(*up_point1, *up_point2, *up_point3)

        # # Draw the down arrow
        # down_point1 = (int(NAV_WIDTH / 2), HEIGHT - ARROW_Y_OFFSET)
        # down_point2 = (int((NAV_WIDTH / 2) - (NAV_ARROW_SIZE / 2)), int(HEIGHT - ARROW_Y_OFFSET - NAV_ARROW_SIZE))
        # down_point3 = (int((NAV_WIDTH / 2) + (NAV_ARROW_SIZE / 2)), int(HEIGHT - ARROW_Y_OFFSET - NAV_ARROW_SIZE))
        # self.display.set_pen(COLORS["FOREGROUND"] if self.navigating_direction == 1 else COLORS["BACKGROUND"])
        # self.display.triangle(*down_point1, *down_point2, *down_point3)

        self.draw_pagination()

        self.navigating_direction = 0

    def draw_pagination(self):
        space_between_circles = 4
        total_size = ((NAV_CIRCLE_SIZE + space_between_circles) * self.total_screens) - space_between_circles

        x = int(NAV_WIDTH / 2)
        initial_y = int((HEIGHT / 2) - (total_size / 2))
        for i in range(self.total_screens):
            self.display.set_pen(COLORS["FOREGROUND"] if self.current_index == i else COLORS["UI_2"])
            self.display.circle(x, initial_y + (NAV_CIRCLE_SIZE * i) + (space_between_circles * i), int(NAV_CIRCLE_SIZE / 2))

class SleepScreen(Screen):
    def draw(self):
        self.display.set_backlight(0)

class BatteryIndicator(Screen):
    def draw(self):
        super().draw()

        self.draw_text("Power", True)
        self.draw_table([
            ("Voltage", "12V", None),
            ("Load", "1.5A", None)
        ], 20)

class LightsIndicator(Screen):
    def draw(self):
        super().draw()

        self.draw_text("Lights", True)
        self.draw_table([
            ("Fairy Lights", "OFF", COLORS["RED"]),
            ("Cabinet Strip", "ON", COLORS["GREEN"])
        ], 20)

class WaterIndicator(Screen):
    tank_width = 40
    tank_border_size = 4
    tank_fill_border_size = 2

    clean_fill_level = 0.5
    dirty_fill_level = 0.25

    def get_new_fill_level(self, fill: float):
        amount = random.uniform(0, 0.1)
        direction = 1 if random.random() < 0.5 else -1
        movement = amount * direction
        new_fill = min(1, max(0, fill + movement))
        return new_fill

    def draw(self):
        self.clean_fill_level = self.get_new_fill_level(self.clean_fill_level)
        self.dirty_fill_level = self.get_new_fill_level(self.dirty_fill_level)
        super().draw()

        self.draw_text("Water", True)
        self.draw_tank(int(NAV_WIDTH + (SCREEN_WIDTH / 2)) - 30, self.clean_fill_level, COLORS["BLUE"])
        self.draw_tank(int(NAV_WIDTH + (SCREEN_WIDTH / 2)) + 30, self.dirty_fill_level, COLORS["GREY"])

    def draw_tank(self, x: int, fill_level: float, color: int, offset = 25):
        # determine the position and size of this tank
        y = offset + SCREEN_PAD
        w = self.tank_width
        x = int(x - (w / 2))
        h = HEIGHT - offset - (SCREEN_PAD * 2)

        # Draw the frame
        self.display.set_pen(COLORS["UI"])
        self.display.rectangle(x, y, w, h)

        # Draw an inner background div to create an outline div of the frame
        self.display.set_pen(COLORS["BACKGROUND"])
        inner_x = x + self.tank_border_size
        inner_y = y + self.tank_border_size
        inner_w = w - (self.tank_border_size * 2)
        inner_h = h - (self.tank_border_size * 2)
        self.display.rectangle(inner_x, inner_y, inner_w, inner_h)

        # Draw how filled the tank is
        self.display.set_pen(color)
        self.display.rectangle(
            inner_x,
            ceil(inner_y + ((1 - fill_level) * inner_h)),
            inner_w,
            int((inner_h) * fill_level)
        )

class ScreenController:
    _current_screen = 0
    asleep = False

    @property
    def current_screen(self) -> int: return self._current_screen
    @current_screen.setter
    def current_screen(self, value: int):
        self._current_screen = value
        for screen in self.screens:
            screen.set_current_index(value)

    screens: list[Screen]

    def __init__(self, prev_button: Button, next_button: Button, display: PicoGraphics):
        self.display = display
        self.prev_button = prev_button
        self.next_button = next_button
        self.sleep_screen = SleepScreen(display, 0, 0)
        self.screens = [
            BatteryIndicator(display, self.current_screen, 3),
            LightsIndicator(display, self.current_screen, 3),
            WaterIndicator(display, self.current_screen, 3)
        ]
        self.init_sleep_timer()

    def init_sleep_timer(self):
        self.timer = Timer(-1)
        self.timer.init(mode = Timer.ONE_SHOT, period = SLEEP_TIMEOUT, callback = self.sleep)

    def sleep(self, t: Timer):
        self.asleep = True

    def reset_sleep_timer(self):
        self.asleep = False;
        self.timer.deinit()
        self.init_sleep_timer()

    def get_current_screen(self):
        if (self.asleep): return self.sleep_screen

        if (self.current_screen > len(self.screens) or self.current_screen < 0):
            raise Exception("current_screen out of bounds")

        return self.screens[self.current_screen]

    def change_screen(self, direction: int):
        new_screen = self.current_screen + direction
        max_screen = len(self.screens) - 1
        new_screen = 0 if new_screen > max_screen else max_screen if new_screen < 0 else new_screen
        self.current_screen = new_screen

    def nav_interrupt(self, direction: int):
        if (self.asleep):
            self.asleep = False;
            self.reset_sleep_timer()
            return

        self.reset_sleep_timer()
        self.change_screen(direction)
        screen = self.get_current_screen()
        screen.set_navigating(direction)

    def tick(self):
        if (self.prev_button.read()):
            self.nav_interrupt(-1)
        elif (self.next_button.read()):
            self.nav_interrupt(1)

        screen = screen_controller.get_current_screen()
        screen.draw()
        self.display.update()

a_btn = Button(12)
b_btn = Button(13)

screen_controller = ScreenController(a_btn, b_btn, display)

while True:
    screen_controller.tick()
