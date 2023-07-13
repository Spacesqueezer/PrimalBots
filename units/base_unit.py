"""Модули"""
import glob
import math
import random
import arcade
import time


class BaseUnit(arcade.Sprite):
    """Базовый класс пехоты"""

    def __init__(self, scale=1):
        super().__init__()
        self.scale = scale
        self.images_path = None
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
            "is_gather_resource": False,
            "current_animation": self.animations["moving_up"],
            "cargo": None,
            "resource_source": None,
            "home_base": None,
            "gathering_start_time": None,
            "gathering_end_time": None,
            "resource_manager": None,
        }

        # Список задач, которые умеет юнит. Каждая задача может состоять из нескольких подзадач.
        self.task_list = {
            "moving": self.move_to_position,
            'standing': self.stand
        }

        # Список подзадач, которые умеют юнит.
        self.subtask_list = {
            "move_to_position": self.move_to_position,
            "standing": self.stand
        }

        # Определяем нынешнюю задачу и подзадачу.
        self.current_task = self.stand
        self.current_subtask = self.stand

        self.joke_to_say = None

        self.index = None

    def initialize(self):
        # Загружает файлы анимации по ключам в словаре. Ключ является маской для поиска файла.
        for key, value in self.animations.items():
            _current_animations = glob.glob(self.images_path + f"{key}_" + '[0-9].png')
            for anim in _current_animations:
                value.append(arcade.load_texture(anim))

    def move_to_position(self):
        """Метод движения к указанной точке"""
        # расстояние между юнитом и точкой назначения
        _delta_x = self.center_x - self.parameters["position_move_to"][0]
        _delta_y = self.center_y - self.parameters["position_move_to"][1]
        _speed = self.parameters["speed"]

        # Если юнит стоит на месте, то высчитать его скорость по осям.
        if not self.parameters["is_moving"]:
            self.calculate_xy_movement_speed()

        if abs(_delta_x) >= _speed:
            self.center_x += self.change_x
        if abs(_delta_y) >= _speed:
            self.center_y += self.change_y
        if abs(_delta_x) <= _speed and abs(_delta_y) <= _speed:
            self.parameters["is_moving"] = False

    def calculate_xy_movement_speed(self):
        """Вычисление скорости по Х и У"""
        _delta_x = self.center_x - self.parameters["position_move_to"][0]
        _delta_y = self.center_y - self.parameters["position_move_to"][1]
        _distance = math.sqrt(_delta_x ** 2 + _delta_y ** 2)
        _time = _distance / self.parameters["speed"]
        self.change_x = -_delta_x / _time
        self.change_y = -_delta_y / _time
        self.parameters["is_moving"] = True

        _abs_delta_y_distance = abs(_delta_y / _distance)
        _delta_x_sign = 1 if _delta_x > 0 else -1
        _delta_y_sign = 1 if _delta_y > 0 else -1

        if _abs_delta_y_distance < 0.3826:
            if _delta_x < 0:
                self.parameters["current_animation"] = self.animations["moving_right"]
            else:
                self.parameters["current_animation"] = self.animations["moving_left"]
        elif _abs_delta_y_distance > 0.7652:
            if _delta_y > 0:
                self.parameters["current_animation"] = self.animations["moving_down"]
            else:
                self.parameters["current_animation"] = self.animations["moving_up"]
        else:
            if _delta_x < 0 and _delta_y < 0:
                self.parameters["current_animation"] = self.animations["moving_upright"]
            elif _delta_x > 0 and _delta_y < 0:
                self.parameters["current_animation"] = self.animations["moving_upleft"]
            elif _delta_x < 0 and _delta_y > 0:
                self.parameters["current_animation"] = self.animations["moving_downright"]
            else:
                self.parameters["current_animation"] = self.animations["moving_downleft"]

    def get_new_destination_point(self):
        """Задаёт случайную точку для движения"""
        self.parameters["position_move_to"] = (random.randint(0, 1000), random.randint(0, 650))

    def update_animation(self, delta_time: float = 1 / 60):
        current_animation = self.parameters["current_animation"]
        self.animation_counter += 0.1
        if self.animation_counter >= len(current_animation):
            self.animation_counter = 0
        self.texture = current_animation[math.floor(self.animation_counter)]

    def stand(self):
        pass

    def say_joke(self):
        jokes_file = 'jokes'
        jokes = []
        current_joke = ''
        joke_to_say = ''

        with open(jokes_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    current_joke += line
                elif current_joke:
                    jokes.append(current_joke.strip())
                    current_joke = ''

        if current_joke:
            jokes.append(current_joke.strip())

        if jokes:
            joke_to_say = random.choice(jokes)

        self.joke_to_say = joke_to_say

        print(joke_to_say)

    def show_text_bubble(self):
        if self.joke_to_say:
            bubble_width = len(self.joke_to_say) * 10 + 20
            bubble_height = 70
            bubble_padding = 10

            # отрисовка тела облака
            arcade.draw_rectangle_filled(self.center_x + bubble_width / 2,
                                         self.center_y - bubble_height / 2,
                                         bubble_width,
                                         bubble_height,
                                         (255, 255, 255))
        else:
            pass

    def update(self):
        self.current_task()
        self.current_subtask()
        self.show_text_bubble()
