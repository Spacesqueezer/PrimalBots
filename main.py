"""
PrimalBots Game
"""
import random

import arcade
from buildings import Cave, GoldMine, WoodMine
from units import Simplebot

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "PrimalBots"


class MyGame(arcade.Window):
    """
    Main application class.
    """


    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.cave = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.background = arcade.load_texture("images/landscape.jpg")

        self.scene = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Buildings")

        _cave = Cave()
        _cave.center_x = 100
        _cave.center_y = 100
        self.scene.add_sprite("Buildings", _cave)

        for i in range(50):
            _simplebot = Simplebot()
            _simplebot.index = i
            _simplebot.center_x = random.randrange(SCREEN_WIDTH)
            _simplebot.center_y = random.randrange(SCREEN_HEIGHT)
            self.scene.add_sprite("Buildings", _simplebot)
            _cave.workers.append(_simplebot)
            _simplebot.parameters["home_base"] = _cave

        self.cave = _cave

        _gold_mine = GoldMine(0.1, (500, 500))
        self.scene.add_sprite("Buildings", _gold_mine)

        _wood_mine = WoodMine(0.1, (200, 550))
        self.scene.add_sprite("Buildings", _wood_mine)

        _cave.resource_sources["gold"].append(_gold_mine)
        _cave.resource_sources["wood"].append(_wood_mine)

        _simplebot.current_task = _simplebot.task_list["collect_resource"]

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for worker in self.cave.workers:
                if worker.collides_with_point((x, y)):
                    print(worker.parameters)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()

        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        # Code to draw the screen goes here
        self.scene.draw()

    def on_update(self, delta_time):
        self.scene.update_animation(delta_time)
        self.scene.update()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
