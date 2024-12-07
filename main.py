import kivy
import kivymd
kivy.require('2.3.0')

from database import Database
from sys import platform

from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window

from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView

from kivymd.icon_definitions import md_icons
from kivymd.uix.widget import Widget
from kivymd.uix.list import MDList, MDListItem
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFabButton
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldMaxLengthText
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel

db: Database = Database()

if platform == 'android':
    from android.permissions import Permission, request_permissions
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
else:
    Config.set('graphics', 'width', '378')
    Config.set('graphics', 'height', '672')

    Window.size = (378, 672)
    Window.borderless = False
    Window.resizable = False

class ListItemWithCheckbox(MDFloatLayout):
    def __init__(self: 'ListItemWithCheckbox', pk: int = None, text: str = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.ids.task_label.text = text
        self.pk: int = pk
    
    def mark(self: 'ListItemWithCheckbox', check, the_list_item) -> None:
        if check.active == True:
            the_list_item.text = f'[s][i]{the_list_item.text}[/i][/s]'
            db.mark_task_as_complete(self.pk)
        else:
            the_list_item.text = the_list_item.text[6:-8]
            db.mark_task_as_incomplete(self.pk)
            
    def delete_items(self: 'ListItemWithCheckbox', the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

class DialogContent(MDBoxLayout):
    def __init__(self: 'DialogContent', **kwargs) -> None:
        super().__init__(**kwargs)

class NavBar(CommonElevationBehavior, MDFloatLayout):
    def __init__(self: 'NavBar', **kwargs) -> None:
        super().__init__(**kwargs)

class Wendrowny_PlanerApp(MDApp):
    task_list_dialog = None

    def on_start(self: 'Wendrowny_PlanerApp') -> None:
        try:
            uncompleted_tasks, completed_tasks = db.get_tasks()

            if uncompleted_tasks != []:
                for task in uncompleted_tasks:
                    add_task: ListItemWithCheckbox = ListItemWithCheckbox(pk = task[0], text = f'[b]{task[1]}[/b]')
                    self.root.ids.container.add_widget(add_task)
            
            if completed_tasks != []:
                for task in completed_tasks:
                    add_task: ListItemWithCheckbox = ListItemWithCheckbox(pk = task[0], text = f'[s][i][b]{task[1]}[/b][/s][/i]')
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        
        except Exception as e:
            print(e)
            pass

    def change_color(self: 'Wendrowny_PlanerApp', instance) -> None:
        if instance in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
            for i in range(4):
                if f'nav_icon{i + 1}' == current_id:
                    self.root.ids[f'nav_icon{i + 1}'].text_color = 1, 1, 1, 1
                else:
                    self.root.ids[f'nav_icon{i + 1}'].text_color = 0, 0, 0, 1

    def show_task_dialog(self: 'Wendrowny_PlanerApp') -> None:
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
    
    def close_dialog(self: 'Wendrowny_PlanerApp', *args) -> None:
        self.task_list_dialog.dismiss()
    
    def add_task(self: 'Wendrowny_PlanerApp', task: MDTextField) -> None:
        if task.text:
            created_task = db.create_task(task.text)

            if len(task.text) <= 50:
                self.root.ids['container'].add_widget(ListItemWithCheckbox(pk = created_task[0], text = f'[b]{created_task[1]}[/b]'))
                task.text = ''

    def exit_app(self: 'Wendrowny_PlanerApp') -> None:
        self.stop()

    def build(self: 'Wendrowny_PlanerApp') -> None:
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Olive'
        return Builder.load_file('./wendrowny_planer.kv')

def main() -> None:
    Wendrowny_PlanerApp().run()

if __name__ == '__main__':
    main()
