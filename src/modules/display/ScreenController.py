from picographics import PicoGraphics
from pimoroni import Button
from machine import Timer

from .Screen import Screen
from .SleepScreen import SleepScreen
from .BatteryScreen import BatteryScreen
from .LightsScreen import LightsScreen
from .WaterScreen import WaterScreen

SLEEP_TIMEOUT = 10_000 # 10 seconds

class ScreenController:
    _current_screen = 2
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
            BatteryScreen(display, self.current_screen, 3),
            LightsScreen(display, self.current_screen, 3),
            WaterScreen(display, self.current_screen, 3)
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

        screen = self.get_current_screen()
        screen.draw()
        self.display.update()