"""Модуль графического движка"""
import arcade


class GoldMine(arcade.Sprite):
    """Класс главного здания"""
    def __init__(self, scale=1, position=(0, 0)):
        self.image_file = "images/gold_mine.png"
        super().__init__(self.image_file, scale)
        self.gold_amount = 100
        self.position = position
        self.gather_point = (self.center_x + 30, self.center_y - 30)
