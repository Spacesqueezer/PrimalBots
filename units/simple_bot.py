"""Модули"""
import glob
import arcade


class Simplebot(arcade.Sprite):
    """Класс рабочего юнита"""

    def __init__(self, scale=1):
        super().__init__()
        self.scale = scale
        self.images_path = "images/1st_bot/"

        # загрузка анимаций
        self.animations = {
            "moving_up": [],
            "moving_upleft": [],
            "moving_upright": [],
            "moving_left": [],
            "moving_right": [],
            "moving_down": [],
            "moving_downleft": [],
            "moving_downright": [],
        }

        for key, value in self.animations.items():
            _current_animations = glob.glob(self.images_path + f"{key}_" + '[0-9].png')
            for anim in _current_animations:
                value.append(arcade.load_texture(anim))

        self.texture = self.animations["moving_up"][2]
