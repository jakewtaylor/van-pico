from Screen import Screen

class BatteryScreen(Screen):
    def draw(self):
        super().draw()

        self.draw_text("Power", True)
        self.draw_table([
            ("Voltage", "12V", None),
            ("Load", "1.5A", None)
        ], 20)