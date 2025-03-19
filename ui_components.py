from datetime import datetime

import kivy
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldMaxLengthText

from database import Database
from dateformat import date_format

DATABASE: Database = Database()

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
        print(self.checkbox.active)
        if self.checkbox.active:
            if self.task_label.text[0:6] != '[s][i]':
                self.task_label.text = f'[s][i]{self.task_label.text}[/i][/s]'
            DATABASE.mark_task_as_complete(self.index)
        else:
            if self.task_label.text[0:6] == '[s][i]':
                self.task_label.text = self.task_label.text[6:-8]
            DATABASE.mark_task_as_incomplete(self.index)
            
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

    def show_date_picker(self: 'DialogContent', *args) -> None:
        date_dialog: MDModalDatePicker = MDModalDatePicker()
        date_dialog.bind(on_ok = self.on_ok, on_cancel = self.on_dismiss)
        date_dialog.open()
    
    def on_dismiss(self: 'DialogContent', instance_date_picker: MDModalDatePicker) -> None:
        instance_date_picker.dismiss()
    
    def on_ok(self: 'DialogContent', instance_date_picker: MDModalDatePicker) -> None:
        date_year: str = str(instance_date_picker.get_date()[0])
        print(date_year[:4])
        date: str = instance_date_picker.set_text_full_date()
        date = date_format(date)
        print(date)
        instance_date_picker.dismiss()
        self.date_text.text = str(date + ' ' + date_year[0:4])

def main() -> None:
    print('RUN `main.py`!!!')
    exit()

kivy.require('2.3.0')
if __name__ == '__main__':
    main()
