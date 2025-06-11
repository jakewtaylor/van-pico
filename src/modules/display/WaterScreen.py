import random
from Screen import Screen, NAV_WIDTH, SCREEN_PAD
from math import ceil

class WaterScreen(Screen):
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
        self.draw_tank(int(NAV_WIDTH + (self.SCREEN_WIDTH / 2)) - 30, self.clean_fill_level, self.COLORS["BLUE"])
        self.draw_tank(int(NAV_WIDTH + (self.SCREEN_WIDTH / 2)) + 30, self.dirty_fill_level, self.COLORS["GREY"])

    def draw_tank(self, x: int, fill_level: float, color: int, offset = 25):
        # determine the position and size of this tank
        y = offset + SCREEN_PAD
        w = self.tank_width
        x = int(x - (w / 2))
        h = self.HEIGHT - offset - (SCREEN_PAD * 2)

        # Draw the frame
        self.display.set_pen(self.COLORS["UI"])
        self.display.rectangle(x, y, w, h)

        # Draw an inner background div to create an outline div of the frame
        self.display.set_pen(self.COLORS["BACKGROUND"])
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