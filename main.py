"""
PrimalBots Game
"""
import random
import arcade.gui

import arcade
from buildings import Cave, BaseMine
from units import Simplebot
from managers import ResManager
from GUI import GUIManager


# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "PrimalBots"


class Section(arcade.Section):
    def __init__(self, left: int, bottom: int, width: int, height: int,
                 **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)
        self.visible = False
        self.game = None

    def on_draw(self):
        if self.visible:
            self.game.scene.draw()


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.add_section(Section(0, 0, SCREEN_WIDTH, int(SCREEN_HEIGHT * 0.9)))
        self.add_section(Section(SCREEN_WIDTH, 0, int(SCREEN_WIDTH * 0.9), int(SCREEN_HEIGHT * 0.1)))

    def on_draw(self):
        self.clear(arcade.color.RED)


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.res_manager = None
        self.gui_manager = None
        self.cave = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.background = arcade.load_texture("images/landscape.jpg")
        self.scene = None

    def setup(self):
        # Создаётся новая сцена
        self.scene = arcade.Scene()

        # Создаётся список спрайтов зданий
        self.scene.add_sprite_list("Buildings")

        # Назначение менеджеров
        self.res_manager = ResManager()
        self.gui_manager = GUIManager()
        self.gui_manager.enable()
        self.gui_manager.create_resources_gui()

        cave = Cave()
        cave.center_x = 100
        cave.center_y = 100
        self.scene.add_sprite("Buildings", cave)
        for i in range(50):
            simplebot = Simplebot()
            simplebot.index = i
            simplebot.center_x = random.randrange(SCREEN_WIDTH)
            simplebot.center_y = random.randrange(SCREEN_HEIGHT)
            self.scene.add_sprite("Buildings", simplebot)
            cave.workers.append(simplebot)
            simplebot.parameters["home_base"] = cave
            simplebot.parameters["resource_manager"] = self.res_manager
        self.cave = cave
        gold_mine = BaseMine(resource_type="gold", scale=0.1, position=(500, 500), resource_amount=100)
        self.scene.add_sprite("Buildings", gold_mine)
        self.res_manager.mines["gold"].append(gold_mine)
        wood_mine = BaseMine(resource_type="wood", scale=0.1, position=(200, 550), resource_amount=100)
        self.scene.add_sprite("Buildings", wood_mine)
        self.res_manager.mines["wood"].append(wood_mine)
        leather_mine = BaseMine(resource_type="leather", scale=0.1, position=(300, 250), resource_amount=100)
        self.scene.add_sprite("Buildings", leather_mine)
        self.res_manager.mines["leather"].append(leather_mine)
        iron_mine = BaseMine(resource_type="iron", scale=0.1, position=(600, 300), resource_amount=100)
        self.scene.add_sprite("Buildings", iron_mine)
        self.res_manager.mines["iron"].append(iron_mine)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for worker in self.cave.workers:
                if worker.collides_with_point((x, y)):
                    print(worker.parameters)

    def on_draw(self):
        arcade.start_render()
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.scene.draw()
        self.gui_manager.draw()

    def on_update(self, delta_time):
        # Получаем количество ресурсов
        resources_amount = {
            'gold': self.res_manager.player_resources["gold"],
            'wood': self.res_manager.player_resources["wood"],
            'leather': self.res_manager.player_resources["leather"],
            'iron': self.res_manager.player_resources["iron"],
        }

        # Передаём в менеджер для апдейта
        self.gui_manager.update_data(resources_amount)

        self.scene.update_animation(delta_time)
        self.scene.update()


def main():
    window = MyGame()
    view = GameView()
    window.show_view(view)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
