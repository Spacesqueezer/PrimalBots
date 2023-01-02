"""Модули"""
import glob
import math
import arcade
import random


class Simplebot(arcade.Sprite):
    """Класс рабочего юнита"""

    def __init__(self, scale=1):
        super().__init__()
        self.scale = scale
        self.images_path = "images/1st_bot/"
        self.animation_counter = 0

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
        self.parameters = {
            "speed": 2,
            "position_move_to": (500, 500),
            "is_moving": False
        }

        # Загружает файлы анимации по ключам в словаре. Ключ является маской для поиска файла.
        for key, value in self.animations.items():
            _current_animations = glob.glob(self.images_path + f"{key}_" + '[0-9].png')
            for anim in _current_animations:
                value.append(arcade.load_texture(anim))

    def move_to_position(self):
        """Метод движения к указанной точке"""
        _delta_x = self.center_x - self.parameters["position_move_to"][0]  # расстояние между юнитом и точкой назначения
        _delta_y = self.center_y - self.parameters["position_move_to"][1]
        _speed = self.parameters["speed"]

        if not self.parameters["is_moving"]:
            self.calculate_xy_movement_speed()
        else:
            self.calculate_xy_movement_speed()
        if abs(_delta_x) >= _speed and abs(_delta_y) >= _speed:
            self.center_x += self.change_x
            self.center_y += self.change_y
        else:
            self.parameters["is_moving"] = False
            self.get_new_destination_point()

    def calculate_xy_movement_speed(self):
        """Вычисление скорости по Х и У"""
        _delta_x = self.center_x - self.parameters["position_move_to"][0]
        _delta_y = self.center_y - self.parameters["position_move_to"][1]
        _distance = math.sqrt(_delta_x ** 2 + _delta_y ** 2)
        _time = _distance / self.parameters["speed"]
        self.change_x = -_delta_x / _time
        self.change_y = -_delta_y / _time
        self.parameters["is_moving"] = True

    def get_new_destination_point(self):
        self.parameters["position_move_to"] = (random.randint(0, 1000), random.randint(0, 650))


    def update_animation(self, delta_time: float = 1 / 60):
        _current_animation = self.animations["moving_up"]
        self.animation_counter += 0.1
        if self.animation_counter >= len(_current_animation):
            self.animation_counter = 0
        self.texture = _current_animation[math.floor(self.animation_counter)]

    def update(self):
        self.move_to_position()
