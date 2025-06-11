from picographics import PicoGraphics

SCREEN_PAD = 10
NAV_WIDTH = 16
NAV_ARROW_SIZE = 11
NAV_CIRCLE_SIZE = 6
ARROW_Y_OFFSET = 50

class Screen:
    navigating_direction = 0

    def __init__(self, display: PicoGraphics, current_index: int, total_screens: int) -> None:
        self.display = display
        self.current_index = current_index
        self.total_screens = total_screens

        width, height = display.get_bounds()
        self.WIDTH = width
        self.HEIGHT = height
        self.SCREEN_WIDTH = width - NAV_WIDTH

        self.COLORS = {
            "BACKGROUND": display.create_pen(0, 0, 0),
            "FOREGROUND": display.create_pen(255, 255, 255),
            "UI": display.create_pen(127, 127, 127),
            "UI_2": display.create_pen(48, 48, 48),
            "GREEN": display.create_pen(0, 255, 0),
            "RED": display.create_pen(255, 0, 0),
            "BLUE": display.create_pen(0, 0, 255),
            "GREY": display.create_pen(179, 179, 179)
        }

    def set_current_index(self, index: int) -> None:
        self.current_index = index

    def set_navigating(self, direction: int) -> None:
        self.navigating_direction = direction;

    def draw(self):
        self.display.set_backlight(0.6)
        self.display.set_font("bitmap8")

        self.display.set_pen(self.COLORS["BACKGROUND"])
        self.display.clear()

        self.draw_navbar()

    def draw_text(self, message: str, center = False, scale = 2):
        self.display.set_pen(self.COLORS["FOREGROUND"])

        if (center):
            text_width = self.display.measure_text(message, scale)
            self.display.text(message, int((NAV_WIDTH + (self.SCREEN_WIDTH / 2)) - (text_width / 2)), SCREEN_PAD, self.SCREEN_WIDTH, scale)
        else:
            self.display.text(message, SCREEN_PAD + NAV_WIDTH, SCREEN_PAD, self.WIDTH, scale)

    def draw_table(self, lines: list[tuple[str, str, int | None]], offset = 0, text_scale = 2, line_space = 8):
        font_size = 8
        line_height = (font_size * text_scale)
        dot_width = self.display.measure_text(".", text_scale)

        for i, (a, b, color) in enumerate(lines):
            self.display.set_pen(self.COLORS["FOREGROUND"])
            y = offset + SCREEN_PAD + (line_height * i) + (line_space if i > 0 else 0)
            # Draw left side
            left_width = self.display.measure_text(a, text_scale)
            self.display.text(a, SCREEN_PAD + NAV_WIDTH, y, self.SCREEN_WIDTH, text_scale)

            # Draw right side
            self.display.set_pen(self.COLORS["FOREGROUND"] if color is None else color)
            right_width = self.display.measure_text(b, text_scale)
            self.display.text(b, NAV_WIDTH + self.SCREEN_WIDTH - SCREEN_PAD - right_width, y, self.SCREEN_WIDTH, text_scale)

            # Draw connecting dots
            self.display.set_pen(self.COLORS["UI"])
            width_of_dots = self.SCREEN_WIDTH - (SCREEN_PAD * 2) - left_width - right_width
            num_dots_needed = int(width_of_dots / dot_width)
            dot_str = "." * num_dots_needed
            self.display.text(dot_str, NAV_WIDTH + SCREEN_PAD + left_width, y, self.SCREEN_WIDTH, text_scale)

    def draw_navbar(self):
        # Draw the frame
        self.display.set_pen(self.COLORS["UI"])
        self.display.rectangle(0, 0, NAV_WIDTH, int(self.HEIGHT / 2))
        self.display.set_pen(self.COLORS["UI"])
        self.display.rectangle(0, int(self.HEIGHT / 2), NAV_WIDTH, int(self.HEIGHT / 2))

        # Draw the up arrow
        # up_point1 = (int(NAV_WIDTH / 2), ARROW_Y_OFFSET)
        # up_point2 = (int((NAV_WIDTH / 2) - (NAV_ARROW_SIZE / 2)), int(ARROW_Y_OFFSET + NAV_ARROW_SIZE))
        # up_point3 = (int((NAV_WIDTH / 2) + (NAV_ARROW_SIZE / 2)), int(ARROW_Y_OFFSET + NAV_ARROW_SIZE))
        # self.display.set_pen(self.COLORS["FOREGROUND"] if self.navigating_direction == -1 else self.COLORS["BACKGROUND"])
        # self.display.triangle(*up_point1, *up_point2, *up_point3)

        # # Draw the down arrow
        # down_point1 = (int(NAV_WIDTH / 2), HEIGHT - ARROW_Y_OFFSET)
        # down_point2 = (int((NAV_WIDTH / 2) - (NAV_ARROW_SIZE / 2)), int(HEIGHT - ARROW_Y_OFFSET - NAV_ARROW_SIZE))
        # down_point3 = (int((NAV_WIDTH / 2) + (NAV_ARROW_SIZE / 2)), int(HEIGHT - ARROW_Y_OFFSET - NAV_ARROW_SIZE))
        # self.display.set_pen(self.COLORS["FOREGROUND"] if self.navigating_direction == 1 else self.COLORS["BACKGROUND"])
        # self.display.triangle(*down_point1, *down_point2, *down_point3)

        self.draw_pagination()

        self.navigating_direction = 0

    def draw_pagination(self):
        space_between_circles = 4
        total_size = ((NAV_CIRCLE_SIZE + space_between_circles) * self.total_screens) - space_between_circles

        x = int(NAV_WIDTH / 2)
        initial_y = int((self.HEIGHT / 2) - (total_size / 2))
        for i in range(self.total_screens):
            self.display.set_pen(self.COLORS["FOREGROUND"] if self.current_index == i else self.COLORS["UI_2"])
            self.display.circle(x, initial_y + (NAV_CIRCLE_SIZE * i) + (space_between_circles * i), int(NAV_CIRCLE_SIZE / 2))