import math
import random
import time

from units import BaseUnit


class Worker(BaseUnit):
    def __init__(self):
        super().__init__()
        self.images_path = "images/worker/"
        additional_tasks = {
            "resource_harvesting": self.resource_harvesting,
        }
        additional_subtasks = {
            "gather_resource": self.gather_resource,
        }
        self.initialize()
        self.task_list.update(additional_tasks)
        self.subtask_list.update(additional_subtasks)

        self.current_task = self.resource_harvesting

        self.say_joke()

    def resource_harvesting(self):
        """Сбор ресурсов. Выполняется курсирование между главной базой и источником ресурсов."""

        sp = self.parameters

        # Если нет груза и не определён источник ресурса для сбора,
        # то назначить из списка источников из главной базы.
        if not sp["cargo"] and not sp["resource_source"]:
            _res_type = random.choice(list(sp["resource_manager"].mines.keys()))
            sp["resource_source"] = sp["resource_manager"].mines[_res_type][0]
            sp["position_move_to"] = sp["resource_source"].gather_point

        _dist = math.sqrt((sp["position_move_to"][0] - self.position[0]) ** 2
                          + (sp["position_move_to"][1] - self.position[1]) ** 2)

        if not sp["is_moving"] and not sp["cargo"] and self.current_subtask == self.subtask_list["standing"]:
            self.current_subtask = self.subtask_list["move_to_position"]

        # Если юнит не двигается, пустой и не собирает ресурс,
        # то назначить точкой назначения источник ресурсов.
        if not sp["is_moving"] and not sp["cargo"] and not sp["is_gather_resource"] and _dist <= 30:
            sp["position_move_to"] = sp["resource_source"].position
            self.current_subtask = self.subtask_list["gather_resource"]

        if not sp["is_moving"] and sp["cargo"] and not sp["is_gather_resource"] and _dist <= 30:
            sp["position_move_to"] = sp["resource_source"].gather_point
            self.parameters["resource_manager"].player_resources[sp["cargo"]] += 1
            sp["cargo"] = None
            self.current_subtask = self.subtask_list["move_to_position"]

        if not sp["is_moving"] and sp["cargo"] and self.current_subtask == self.subtask_list["gather_resource"]:
            sp["position_move_to"] = sp["home_base"].position
            self.current_subtask = self.subtask_list["move_to_position"]

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
            self.parameters["cargo"] = self.parameters["resource_source"].resource
