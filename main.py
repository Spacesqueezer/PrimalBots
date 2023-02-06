"""
PrimalBots Game
"""
import random
import arcade.gui

import arcade
from buildings import Cave, BaseMine
from units import Simplebot
from managers import ResManager

from GUI import Icon

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

        self.res_manager = None
        self.ui_manager = None
        self.cave = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.background = arcade.load_texture("images/landscape.jpg")

        self.scene = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Создание сцены и списков спрайтов.
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Buildings")

        # Создание менеджера ресурсов
        self.res_manager = ResManager()

        # Создание графического интерфейса.
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        _tmp = arcade.texture.load_texture('images/icons/tmp.bmp')

        # Создание спрайтов графического интерфейса.
        _coins_sprite = Icon('images/icons/gold_coins.png')
        _wood_sprite = Icon('images/icons/wood.png')
        _leather_sprite = Icon('images/icons/leather.png')
        _iron_sprite = Icon('images/icons/iron.png')

        # Создание виджетов графического интерфейса.
        _ui_coins_icon = arcade.gui.UISpriteWidget(sprite=_coins_sprite, width=30, height=30)
        _ui_wood_icon = arcade.gui.UISpriteWidget(sprite=_wood_sprite, width=30, height=30)
        _ui_leather_icon = arcade.gui.UISpriteWidget(sprite=_leather_sprite, width=30, height=30)
        _ui_iron_icon = arcade.gui.UISpriteWidget(sprite=_iron_sprite, width=30, height=30)

        # Текстовые поля графического интерфейса.
        _gold_amount = arcade.gui.UITextArea(text="Test text", width=50)
        _wood_amount = arcade.gui.UITextArea(text="Test text", width=50)
        _leather_amount = arcade.gui.UITextArea(text="Test text", width=50)
        _iron_amount = arcade.gui.UITextArea(text="Test text", width=50)

        # Создание графического интерфейса.
        _resources_gui_box = arcade.gui.UIBoxLayout(vertical=False, children=(
            _ui_coins_icon,
            _gold_amount,
            _ui_wood_icon,
            _wood_amount,
            _ui_leather_icon,
            _leather_amount,
            _ui_iron_icon,
            _iron_amount
        ))

        # Создание менеджера графического интерфейса.
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                child=arcade.gui.UITexturePane(child=_resources_gui_box, tex=_tmp)))

        # Создание главного здания.
        _cave = Cave()
        _cave.center_x = 100
        _cave.center_y = 100
        self.scene.add_sprite("Buildings", _cave)

        # Создание рабочих.
        for i in range(50):
            _simplebot = Simplebot()
            _simplebot.index = i
            _simplebot.center_x = random.randrange(SCREEN_WIDTH)
            _simplebot.center_y = random.randrange(SCREEN_HEIGHT)
            self.scene.add_sprite("Buildings", _simplebot)
            _cave.workers.append(_simplebot)
            _simplebot.parameters["home_base"] = _cave
            _simplebot.parameters["resource_manager"] = self.res_manager

        self.cave = _cave  # TODO Разобраться, чо за херня

        # -------------------------Рудники-------------------------
        _gold_mine = BaseMine("gold", 0.1, (500, 500), 100)
        self.scene.add_sprite("Buildings", _gold_mine)
        self.res_manager.mines["gold"].append(_gold_mine)

        _wood_mine = BaseMine("wood", 0.1, (200, 550), 100)
        self.scene.add_sprite("Buildings", _wood_mine)
        self.res_manager.mines["wood"].append(_wood_mine)

        _leather_mine = BaseMine("leather", 0.1, (300, 250), 100)
        self.scene.add_sprite("Buildings", _leather_mine)
        self.res_manager.mines["leather"].append(_leather_mine)

        _iron_mine = BaseMine("iron", 0.1, (600, 300), 100)
        self.scene.add_sprite("Buildings", _iron_mine)
        self.res_manager.mines["iron"].append(_iron_mine)
        # -------------------------Рудники-------------------------

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """
        The on_mouse_press function is called when the user presses a mouse button.
        The parameters x and y are the coordinates of the mouse click, relative to
        the window. The parameter button is an integer value representing which mouse
        button was pressed (e.g., arcade.MOUSE_BUTTON_LEFT). The parameter modifiers is a bitwise
        AND of several constants indicating which modifier keys were active when the
        mouse button was clicked (e.g., arcade.MOD_SHIFT | arcade.MOD_ALT). If you call set_mouse_visible(False),
        you will need to check for mouse clicks

        :param self: Access the class variables :param x:int: Pass the x coordinate of the mouse click :param y:int:
        Specify the y coordinate of the mouse click :param button:int: Check which mouse button was pressed :param
        modifiers:int: Detect if the user is holding down a modifier key (such as shift, ctrl or alt) when they click
        :return: The parameters of the worker that is clicked :doc-author: Trelent
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            for worker in self.cave.workers:
                if worker.collides_with_point((x, y)):
                    print(worker.parameters)

    def on_draw(self):
        """
        The on_draw function is called whenever you need to update your screen.
        It's the function that draws all of your sprites and UI elements, along with their positions.
        This is also where you should put any &quot;animations&quot; (though there are better ways to do animations).
        The arcade library has a timer that will call this function 60 times per second.

        :param self: Access variables that belongs to the class
        :return: The arcade
        :doc-author: Trelent
        """
        arcade.start_render()
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.scene.draw()
        self.ui_manager.draw()

    def on_update(self, delta_time):
        """
        The on_update function is called once per frame, and it is used to update the state of any
        objects that require updating. In this case, the only object that needs updating is the scene
        object. The scene object handles all of the game logic for our game's world.

        :param self: Access the class attributes and methods
        :param delta_time: Update the game at a constant speed, even if the fps drops
        :return: Nothing, but it does update the ui
        :doc-author: Trelent
        """
        _res_fields = self.ui_manager.children[0][0].child.child.children
        _res_fields[1].text = str(self.res_manager.player_resources["gold"])
        _res_fields[3].text = str(self.res_manager.player_resources["wood"])
        _res_fields[5].text = str(self.res_manager.player_resources["leather"])
        _res_fields[7].text = str(self.res_manager.player_resources["iron"])
        self.scene.update_animation(delta_time)
        self.scene.update()


def main():
    """
    The main function is the point of entry for a program in Python.
    It is where execution starts and control flow begins.
    The main function should be defined as follows:

    :return: None
    :doc-author: Trelent
    """
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
