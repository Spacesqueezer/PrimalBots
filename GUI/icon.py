import arcade


class Icon(arcade.Sprite):
    """Иконка
    :param image - картинка
    """
    def __init__(self, image: str, scale=1.0):
        self.image = image
        super().__init__(self.image, scale)