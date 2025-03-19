from sys import platform

import kivy
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogContentContainer, MDDialogHeadlineText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.widget import Widget

from database import Database
from ui_components import ListItemWithCheckbox, DialogContent

DATABASE: Database = Database()

if platform == 'android':
    from android.permissions import Permission, request_permissions # type: ignore
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
else:
    Config.set('graphics', 'width', '378')
    Config.set('graphics', 'height', '672')

    Window.size = (378, 672)
    Window.borderless = False
    Window.resizable = False

class Wendrowny_PlanerApp(MDApp):
    task_list_dialog = None

    def on_start(self: 'Wendrowny_PlanerApp') -> None:
        def add_task(task: list[str], complite: bool = False) -> None:
            add_task_var: ListItemWithCheckbox = ListItemWithCheckbox(task[0], f'[b]{task[1]}[/b]', task[2])
            if complite:
                add_task_var.checkbox.active = True
                add_task_var.mark()
            self.root.ids.container.add_widget(add_task_var)

        try:
            uncompleted_tasks, completed_tasks = DATABASE.get_tasks()

            if uncompleted_tasks != []:
                for task in uncompleted_tasks:
                    add_task(task)
            
            if completed_tasks != []:
                for task in completed_tasks:
                    add_task(task, True)

        except Exception as e:
            print(e)

    def change_color(self: 'Wendrowny_PlanerApp', instance) -> None:
        if instance in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
            for i in range(4):
                if f'nav_icon{i + 1}' == current_id:
                    self.root.ids[f'nav_icon{i + 1}'].text_color = 1, 1, 1, 1
                else:
                    self.root.ids[f'nav_icon{i + 1}'].text_color = 0, 0, 0, 1

    def show_task_dialog(self: 'Wendrowny_PlanerApp') -> None:
        def handle_add_task(instance, task_text: MDTextField, date_text: MDLabel) -> None:
            self.add_task(task_text, date_text)
        
        if not self.task_list_dialog:
            _DialogContent = DialogContent(app = self)
            self.task_list_dialog = MDDialog(
                MDDialogHeadlineText(text = 'Create Task', halign = 'left'),
                MDDialogContentContainer(_DialogContent),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(MDButtonText(text = 'Cancle'), on_release = self.close_dialog),
                    MDButton(MDButtonText(text = 'Add'), on_release = lambda instance: handle_add_task(instance, _DialogContent.__getattribute__("task_text"), _DialogContent.__getattribute__("date_text"))),
                    spacing = '10dp'
                ),
                size_hint = (0.85, 0.35)
            )
        self.task_list_dialog.open()
    
    def close_dialog(self: 'Wendrowny_PlanerApp', *args) -> None:
        self.task_list_dialog.dismiss()
    
    def add_task(self: 'Wendrowny_PlanerApp', task: MDTextField, task_date: MDLabel) -> None:
        if task.text:
            created_task = DATABASE.create_task(task.text, task_date.text)

            if len(task.text) <= 50:
                self.root.ids['container'].add_widget(ListItemWithCheckbox(created_task[0], f'[b]{created_task[1]}[/b]', task_date.text))
                task.text = ''

    def exit_app(self: 'Wendrowny_PlanerApp') -> None:
        self.stop()

    def build(self: 'Wendrowny_PlanerApp') -> None:
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Olive'
        return Builder.load_file('./wendrowny_planer.kv')

def main() -> None:
    Wendrowny_PlanerApp().run()

kivy.require('2.3.0')
if __name__ == '__main__':
    main()
