import kivy
import kivymd
kivy.require('2.3.0')

from database import Database
from sys import platform
from datetime import datetime

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window

from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp, sp

from kivymd.icon_definitions import md_icons
from kivymd.uix.widget import Widget
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.list import MDList, MDListItem
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFabButton
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldMaxLengthText
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel

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

class ListItemWithCheckbox(MDFloatLayout):
    def __init__(self: 'ListItemWithCheckbox', index: int = None, text: str = None, date_text: str = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.checkbox: MDCheckbox = self.ids.check
        self.task_label: MDLabel = self.ids.task_label
        self.task_label.text = text
        self.ids.task_date_label.text = date_text
        self.index: int = index
    
    #! napraw to zjebie / juz jest lepiej ale dalej nie wiem co się zjebało / To nie problem z tą metodą / †
    #! Tu się dzieje jakaś jebana anomalia, według logiki wszystko jest w porządku, ale checkbox z jakigegoś powodu się zaznacza ponownie
    def mark(self: 'ListItemWithCheckbox') -> None:
        if self.checkbox.active:
            if self.task_label.text[0:6] != '[s][i]':
                self.task_label.text = f'[s][i]{self.task_label.text}[/i][/s]'
            DATABASE.mark_task_as_complete(self.index)
        else:
            if self.task_label.text[0:6] == '[s][i]':
                self.task_label.text = self.task_label.text[6:-8]
            DATABASE.mark_task_as_incomplete(self.index)
        print(self.checkbox.state)
            
    def delete_items(self: 'ListItemWithCheckbox'):
        self.parent.remove_widget(self)
        DATABASE.delete_task(self.index)

class NavBar(CommonElevationBehavior, MDFloatLayout):
    def __init__(self: 'NavBar', **kwargs) -> None:
        super().__init__(**kwargs)
        self.spacing = '10dp'
        self.size_hint

class DialogContent(MDBoxLayout):
    def __init__(self: 'DialogContent', app: MDApp, **kwargs) -> None:
        super().__init__(**kwargs)
        self.app: MDApp = app
        self.orientation = 'vertical'
        self.spacing = '10dp'
        self.height = '105dp'
        self.size_hint = (1, None)
        self.task_text = MDTextField(
            MDTextFieldHintText(text = "Add Task..."),
            MDTextFieldMaxLengthText(max_text_length = 50),
            id = 'task_text',
            pos_hint = {'center_y': 0.4},
            on_text_validate = self.on_task_entered
        )
        self.date_text = MDLabel(id = 'date_text')
        self.add_widget(
            MDGridLayout(
                self.task_text,
                MDIconButton(
                    icon = 'calendar-blank',
                    pos_hint = {'center_y': 0.7},
                    on_press = self.show_date_picker,
                    padding = '10dp'
                ),
                rows = 1,
                cols = 2
            )
        )
        self.add_widget(self.date_text)
        self.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))
    
    def on_task_entered(self: 'DialogContent', *args) -> None:
        self.app.add_task(self.task_text, self.date_text)
        self.task_text.text = ''

    def show_date_picker(self: 'DialogContent') -> None:
        date_dialog: MDModalDatePicker = MDModalDatePicker
        date_dialog.bind(on_save = self.on_save)
        date_dialog.open()
    
    def on_save(self: 'DialogContent', instance, value, date_range) -> None:
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

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

if __name__ == '__main__':
    main()
