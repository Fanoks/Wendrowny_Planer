import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.config import Config

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

Config.set('graphics', 'width', '378')
Config.set('graphics', 'height', '672')

Window.size = (378, 672)
Window.borderless = False
Window.resizable = False
    
class ItemList(BoxLayout):
    def add_item(self, item: str) -> None:
        new_label: Label = Label(text = item)
        self.add_widget(new_label)

class AddItem(BoxLayout):
    item_list: ItemList = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
    def add_item_list(self) -> None:
        self.item_list = self.parent.ids.item_list

    def on_add_item_button_click(self) -> None:
        if self.item_list == None:
            self.add_item_list()
        self.item_list.add_item(self.ids.todo_name.text)

class MainScreen(FloatLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        #self.item_list: ItemList = ItemList()
        #self.add_item: AddItem = AddItem()
        #self.add_item.add_item_list(self.item_list)
        #self.add_widget(self.item_list)
        #self.add_widget(self.add_item)

class Wendrowny_PlanerApp(App):
    def build(self) -> MainScreen:
        return MainScreen()

def main() -> None:
    Wendrowny_PlanerApp().run()

if __name__ == '__main__':
    main()
