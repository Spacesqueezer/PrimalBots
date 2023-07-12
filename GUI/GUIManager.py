import arcade
import arcade.gui

from GUI import Icon


class GUIManager(arcade.gui.UIManager):
    def __init__(self):
        """
        Конструктор класса GUIManager.
        Инициализирует менеджер пользовательского интерфейса.
        """
        super().__init__()
        self.enable()

    def create_resources_gui(self):
        """
        Создает элементы GUI для отображения ресурсов.
        """
        tmp = arcade.texture.load_texture('images/icons/tmp.bmp')
        coins_sprite = Icon('images/icons/gold_coins.png')
        wood_sprite = Icon('images/icons/wood.png')
        leather_sprite = Icon('images/icons/leather.png')
        iron_sprite = Icon('images/icons/iron.png')
        ui_coins_icon = arcade.gui.UISpriteWidget(sprite=coins_sprite, width=30, height=30)
        ui_wood_icon = arcade.gui.UISpriteWidget(sprite=wood_sprite, width=30, height=30)
        ui_leather_icon = arcade.gui.UISpriteWidget(sprite=leather_sprite, width=30, height=30)
        ui_iron_icon = arcade.gui.UISpriteWidget(sprite=iron_sprite, width=30, height=30)
        gold_amount = arcade.gui.UITextArea(text="Test text", width=50)
        wood_amount = arcade.gui.UITextArea(text="Test text", width=50)
        leather_amount = arcade.gui.UITextArea(text="Test text", width=50)
        iron_amount = arcade.gui.UITextArea(text="Test text", width=50)
        resources_gui_box = arcade.gui.UIBoxLayout(vertical=False, children=(
            ui_coins_icon,
            gold_amount,
            ui_wood_icon,
            wood_amount,
            ui_leather_icon,
            leather_amount,
            ui_iron_icon,
            iron_amount
        ))
        self.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                child=arcade.gui.UITexturePane(child=resources_gui_box, tex=tmp)))

    def update_data(self, resources_amount):
        elements = self.children[0][0].child.child.children
        elements[1].text = str(resources_amount['gold'])
        elements[3].text = str(resources_amount['wood'])
        elements[5].text = str(resources_amount['leather'])
        elements[7].text = str(resources_amount['iron'])

