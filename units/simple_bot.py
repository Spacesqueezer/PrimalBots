"""Модули"""
import glob
import math
import random
import arcade


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
            "is_moving": False,
            "current_animation": self.animations["moving_up"]
        }

        # мусорные переменные
        self.main_base = None
        self.cargo = None
        self.resource_point = None

        # список задач, которые умеет юнит.
        self.task_list = {
            "collect_resource": self.collect_resource,
            "move_to_position": self.move_to_position,
        }
        self.subtask_list = {
            "collect_resource": self.collect_resource,
            "move_to_position": self.move_to_position,
        }
        self.current_task = self.task_list["move_to_position"]

        # Загружает файлы анимации по ключам в словаре. Ключ является маской для поиска файла.
        for key, value in self.animations.items():
            _current_animations = glob.glob(self.images_path + f"{key}_" + '[0-9].png')
            for anim in _current_animations:
                value.append(arcade.load_texture(anim))

        # Здание, к которому движется бот
        self.task_destination = self.resource_point

    def move_to_position(self):
        """Метод движения к указанной точке"""
        # расстояние между юнитом и точкой назначения
        _delta_x = self.center_x - self.parameters["position_move_to"][0]
        _delta_y = self.center_y - self.parameters["position_move_to"][1]
        _speed = self.parameters["speed"]

        if not self.parameters["is_moving"]:
            self.calculate_xy_movement_speed()

        if abs(_delta_x) >= _speed and abs(_delta_y) >= _speed:
            self.center_x += self.change_x
            self.center_y += self.change_y
        else:
            self.parameters["is_moving"] = False
            # self.get_new_destination_point()

    def collect_resource(self):
        self.parameters["position_move_to"] = (self.task_destination.center_x, self.task_destination.center_y)

        # TODO: разобраться с этой хернёй
        if not self.parameters["is_moving"]:
            if self.task_destination == self.resource_point:
                print("Cargo is None")
                print(self.parameters["is_moving"])
                self.task_destination = self.main_base

                # self.cargo = 'gold'
            else:
                self.cargo = None
                self.task_destination = self.main_base
                self.parameters["is_moving"] = True

        # двигаться до рудника
        # взять ресурсы
        # вернуть на базу
        # повторить

    def calculate_xy_movement_speed(self):
        """Вычисление скорости по Х и У"""
        _delta_x = self.center_x - self.parameters["position_move_to"][0]
        _delta_y = self.center_y - self.parameters["position_move_to"][1]
        _distance = math.sqrt(_delta_x ** 2 + _delta_y ** 2)
        _time = _distance / self.parameters["speed"]
        self.change_x = -_delta_x / _time
        self.change_y = -_delta_y / _time
        self.parameters["is_moving"] = True

        if abs(_delta_y / _distance) < 0.3826 and _delta_x < 0:
            self.parameters["current_animation"] = self.animations["moving_right"]
        elif abs(_delta_y / _distance) < 0.3826 and _delta_x > 0:
            self.parameters["current_animation"] = self.animations["moving_left"]
        elif abs(_delta_y / _distance) > 0.7652 and _delta_y > 0:
            self.parameters["current_animation"] = self.animations["moving_down"]
        elif abs(_delta_y / _distance) > 0.7652 and _delta_y < 0:
            self.parameters["current_animation"] = self.animations["moving_up"]
        elif 0.3826 < abs(_delta_y / _distance) < 0.7652 and _delta_x < 0 and _delta_y < 0:
            self.parameters["current_animation"] = self.animations["moving_upright"]
        elif 0.3826 < abs(_delta_y / _distance) < 0.7652 and _delta_x > 0 and _delta_y < 0:
            self.parameters["current_animation"] = self.animations["moving_upleft"]
        elif 0.3826 < abs(_delta_y / _distance) < 0.7652 and _delta_x < 0 and _delta_y > 0:
            self.parameters["current_animation"] = self.animations["moving_downright"]
        elif 0.3826 < abs(_delta_y / _distance) < 0.7652 and _delta_x > 0 and _delta_y > 0:
            self.parameters["current_animation"] = self.animations["moving_downleft"]

    def get_new_destination_point(self):
        """Задаёт случайную точку для движения"""
        self.parameters["position_move_to"] = (random.randint(0, 1000), random.randint(0, 650))

    def update_animation(self, delta_time: float = 1 / 60):
        _current_animation = self.parameters["current_animation"]
        self.animation_counter += 0.1
        if self.animation_counter >= len(_current_animation):
            self.animation_counter = 0
        self.texture = _current_animation[math.floor(self.animation_counter)]

    def update(self):
        self.current_task()
