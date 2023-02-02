"""
PrimalBots Game
"""
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

        _simplebot = Simplebot()
        _simplebot.center_x = 600
        _simplebot.center_y = 400
        self.scene.add_sprite("Buildings", _simplebot)

        _gold_mine = GoldMine(0.1)
        _gold_mine.center_x = 700
        _gold_mine.center_y = 500
        self.scene.add_sprite("Buildings", _gold_mine)

        _simplebot.resource_point = _gold_mine
        _simplebot.task_destination = _gold_mine
        _simplebot.main_base = _cave
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
