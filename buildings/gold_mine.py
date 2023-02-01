"""Модуль графического движка"""
import arcade


class GoldMine(arcade.Sprite):
    """Класс главного здания"""
    def __init__(self, scale=1):
        self.image_file = "images/gold_mine.png"
        super().__init__(self.image_file, scale)
