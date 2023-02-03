"""
PrimalBots Game
"""
import random

import arcade
from buildings import Cave, GoldMine
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

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.scene = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Buildings")

        _cave = Cave()
        _cave.center_x = 100
        _cave.center_y = 100
        self.scene.add_sprite("Buildings", _cave)

        for i in range(10):
            _simplebot = Simplebot()
            _simplebot.center_x = random.randrange(SCREEN_WIDTH)
            _simplebot.center_y = random.randrange(SCREEN_HEIGHT)
            self.scene.add_sprite("Buildings", _simplebot)
            _cave.workers.append(_simplebot)
            _simplebot.parameters["home_base"] = _cave


        _gold_mine = GoldMine(0.1, (700, 500))
        self.scene.add_sprite("Buildings", _gold_mine)

        _cave.resource_sources["gold"].append(_gold_mine)


        _simplebot.current_task = _simplebot.task_list["collect_resource"]

    def on_draw(self):
        """Render the screen."""

        self.clear()
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
