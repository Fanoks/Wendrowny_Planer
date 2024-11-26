import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

Config.set('graphics', 'width', '378')
Config.set('graphics', 'height', '672')

Window.size = (378, 672)
Window.borderless = False
Window.resizable = False

class NavigationBar(BoxLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class ItemLabel(RecycleDataViewBehavior, Label):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected = False
    
    def refresh_view_attrs(self, rv, index, data) -> None:
        self.text = data['text']
        self.color = (0, 1, 0, 1) if self.selected else (1, 0, 0, 1)
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch) -> bool:
        if super().on_touch_down(touch):
            return True

        if self.collide_point(*touch.pos):
            self.selected = not self.selected
            self.parent.parent.refresh_from_data()
            return True

        return False

class ItemList(RecycleView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data: list = []

    def add_item(self, item: str) -> None:
        self.data.append({'text': item})
        self.refresh_from_data()

class AddItem(BoxLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget) -> None:
        self.item_list: ItemList = self.parent.parent.ids.item_list

    def on_add_item_button_click(self) -> None:
        task = self.ids.todo_name.text
        if task:
            self.item_list.add_item(task)
            self.ids.todo_name.text = ''

class MainScreen(FloatLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class Wendrowny_PlanerApp(App):
    def build(self) -> MainScreen:
        return MainScreen()

def main() -> None:
    Wendrowny_PlanerApp().run()

if __name__ == '__main__':
    main()
