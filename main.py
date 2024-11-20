import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.config import Config

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

Config.set('graphics', 'width', '378')
Config.set('graphics', 'height', '672')
    
class ItemList(BoxLayout):
    def add_item(self, item: str) -> None:
        new_label: Label = Label(text = item)
        self.add_widget(new_label)

class AddItem(BoxLayout):
    def __init__(self, item_list: ItemList, **kwargs) -> None:
        super().__init__(**kwargs)
        self.item_list = item_list

    def on_add_item_button_click(self) -> None:
        self.item_list.add_item('Abc')

class MainScreen(FloatLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.item_list: ItemList = ItemList()
        self.add_widget(self.item_list)
        self.add_widget(AddItem(self.item_list))

class Wendrowny_PlanerApp(App):
    def build(self) -> MainScreen:
        main_screen: MainScreen = MainScreen()
        return main_screen

def main() -> None:
    Wendrowny_PlanerApp().run()

if __name__ == '__main__':
    main()
