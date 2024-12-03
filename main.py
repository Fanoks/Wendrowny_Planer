import kivy
import kivymd
kivy.require('2.3.0')

from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window

from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivymd.icon_definitions import md_icons
from kivymd.uix.widget import Widget
from kivymd.uix.list import MDList, MDListItem, MDListItemLeadingIcon
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFabButton
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldMaxLengthText
from kivy.uix.checkbox import CheckBox
from kivymd.uix.label import MDLabel

Config.set('graphics', 'width', '378')
Config.set('graphics', 'height', '672')

Window.size = (378, 672)
Window.borderless = False
Window.resizable = False

class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class NavBar(CommonElevationBehavior, MDFloatLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class Wendrowny_PlanerApp(MDApp):
    task_list_dialog = None

    def change_color(self, instance) -> None:
        if instance in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
            for i in range(4):
                if f'nav_icon{i + 1}' == current_id:
                    self.root.ids[f'nav_icon{i + 1}'].text_color = 1, 1, 1, 1
                else:
                    self.root.ids[f'nav_icon{i + 1}'].text_color = 0, 0, 0, 1

    def show_task_dialog(self) -> None:
        if not self.task_list_dialog:
            self.task = MDTextField(
                MDTextFieldHintText(text = 'Add task'),
                MDTextFieldMaxLengthText(max_text_length = 50),
                size_hint_x = None,
                width = '275dp',
                )
            self.task_list_dialog = MDDialog(
                MDDialogHeadlineText(text = 'Create Task', halign = 'left'),
                MDDialogContentContainer(
                    self.task,
                    orientation = 'vertical'
                ),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(MDButtonText(text = 'Cancle'), on_release = self.close_dialog),
                    MDButton(MDButtonText(text = 'Add'), on_release = lambda x: self.add_task(self.task)),
                    spacing = '10dp'
                ),
                size_hint = (0.85, 0.35)
            )
        self.task_list_dialog.open()
    
    def close_dialog(self, *args) -> None:
        self.task_list_dialog.dismiss()
    
    def add_task(self, task) -> None:
        print(task.text)
        task.text = ''

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Olive'
        return Builder.load_file('./wendrowny_planer.kv')

def main() -> None:
    Wendrowny_PlanerApp().run()

if __name__ == '__main__':
    main()
#! https://dev.to/ngonidzashe/how-to-create-a-simple-to-do-list-application-with-kivymd-d89
#! https://kivymd.readthedocs.io/en/latest/components/dialog/#kivymd.uix.dialog.dialog.MDDialog
