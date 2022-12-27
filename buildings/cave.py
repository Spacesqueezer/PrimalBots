"""Модуль графического движка"""
import arcade


class Cave(arcade.Sprite):
    """Класс главного здания"""
    def __init__(self, scale=1):
        self.image_file = "images/cave.png"
        super().__init__(self.image_file, scale)
