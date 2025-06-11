from Screen import Screen

class LightsScreen(Screen):
    def draw(self):
        super().draw()

        self.draw_text("Lights", True)
        self.draw_table([
            ("Fairy Lights", "OFF", self.COLORS["RED"]),
            ("Cabinet Strip", "ON", self.COLORS["GREEN"])
        ], 20)