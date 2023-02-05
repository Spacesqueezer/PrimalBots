"""Модуль графического движка"""
import arcade


class BaseMine(arcade.Sprite):
    """Класс базового рудника"""

    def __init__(
            self,
            resource_type: str,  # Определяет тип ресурса и внешний вид здания
            scale=1,
            position=(0, 0),
            resource_amount=100,
    ):
        self.image_file = f'images/mines/{resource_type}_mine.png'
        super().__init__(self.image_file, scale)
        self.resource_amount = resource_amount
        self.position = position
        self.resource = resource_type
        self.gather_point = (self.center_x + 30, self.center_y - 30)
