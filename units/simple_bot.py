"""Модули"""
import glob
import math
import random
import arcade
import time


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
            "is_gather_resource": False,
            "current_animation": self.animations["moving_up"],
            "cargo": None,
            "resource_source": None,
            "home_base": None,
            "gathering_start_time": None,
            "gathering_end_time": None,
        }

        # Список задач, которые умеет юнит. Каждая задача может состоять из нескольких подзадач.
        self.task_list = {
            "collect_resource": self.collect_resource,
            "moving": self.move_to_position,
        }

        # Список подзадач, которые умеют юнит.
        self.subtask_list = {
            "move_to_position": self.move_to_position,
            "gather_resource": self.gather_resource,
            "standing": self.stand
        }

        # Определяем нынешнюю задачу и подзадачу.
        self.current_task = self.task_list["collect_resource"]
        self.current_subtask = self.stand

        self.index = None

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

    def collect_resource(self):
        """Сбор ресурсов. Выполняется курсирование между главной базой и источником ресурсов."""

        _sp = self.parameters

        # Если нет груза и не определён источник ресурса для сбора,
        # то назначить из списка источников из главной базы.
        if not _sp["cargo"] and not _sp["resource_source"]:
            _sp["resource_source"] = random.choice([_sp["home_base"].resource_sources["gold"][0], _sp["home_base"].resource_sources["wood"][0]])
            _sp["position_move_to"] = _sp["resource_source"].gather_point

        _dist = math.sqrt((_sp["position_move_to"][0] - self.position[0]) ** 2
                          + (_sp["position_move_to"][1] - self.position[1]) ** 2)

        if not _sp["is_moving"] and not _sp["cargo"] and self.current_subtask == self.subtask_list["standing"]:
            self.current_subtask = self.subtask_list["move_to_position"]

        # Если юнит не двигается, пустой и не собирает ресурс,
        # то назначить точкой назначения источник ресурсов.
        if not _sp["is_moving"] and not _sp["cargo"] and not _sp["is_gather_resource"] and _dist <= 30:
            _sp["position_move_to"] = _sp["resource_source"].position
            self.current_subtask = self.subtask_list["gather_resource"]

        if not _sp["is_moving"] and _sp["cargo"] and not _sp["is_gather_resource"] and _dist <= 30:
            _sp["position_move_to"] = _sp["resource_source"].gather_point
            _sp["cargo"] = None
            self.current_subtask = self.subtask_list["move_to_position"]

        if not _sp["is_moving"] and _sp["cargo"] and self.current_subtask == self.subtask_list["gather_resource"]:
            _sp["position_move_to"] = _sp["home_base"].position
            self.current_subtask = self.subtask_list["move_to_position"]

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

    def stand(self):
        pass

    def gather_resource(self):
        start = time.perf_counter()
        end = self.parameters["gathering_end_time"]
        if not self.parameters["is_gather_resource"]:
            self.parameters["gathering_start_time"] = time.perf_counter()
            self.parameters["gathering_end_time"] = self.parameters["gathering_start_time"] + 2
            self.parameters["is_gather_resource"] = True
            start = self.parameters["gathering_start_time"]
            end = self.parameters["gathering_end_time"]
        if end - start <= 0:
            self.parameters["is_gather_resource"] = False
            self.parameters["cargo"] = 'gold'

    def update(self):
        self.current_task()
        self.current_subtask()
