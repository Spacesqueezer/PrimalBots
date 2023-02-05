"""Менеджер игровых ресурсов."""


class ResManager:
    """Менеджер игровых ресурсов."""
    def __init__(self):
        self.mines = {
            "gold": [],
            "wood": [],
        }

        self.player_resources = {
            "gold": 0,
            "wood": 0,
        }
