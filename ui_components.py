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
    """
    A task list item with a checkbox for marking completion status.
    
    This widget displays a task with its description, due date, and provides 
    functionality to mark tasks as completed or delete them.
    
    Attributes:
        checkbox (MDCheckbox): Reference to the checkbox widget
        task_label (MDLabel): Reference to the label containing task text
        index (int): Database ID of the associated task
    """
    def __init__(self, index: int = None, text: str = None, date_text: str = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.checkbox: MDCheckbox = self.ids.check
        self.task_label: MDLabel = self.ids.task_label
        self.task_label.text = text
        self.ids.task_date_label.text = date_text
        self.index: int = index

    def mark(self, *args) -> None:
        """
        Toggle the completion status of a task.
        
        This method updates both the visual appearance of the task and its
        completion status in the database when the checkbox is toggled.
        """
        self.checkbox.unbind(active = self.mark)

        if self.checkbox.active:
            if self.task_label.text[0:6] != '[s][i]':
                self.task_label.text = f'[s][i]{self.task_label.text}[/i][/s]'
            DATABASE.mark_task_as_complete(self.index)
        else:
            if self.task_label.text[0:6] == '[s][i]':
                self.task_label.text = self.task_label.text[6:-8]
            DATABASE.mark_task_as_incomplete(self.index)
        
        self.checkbox.bind(active = self.mark)

        from kivymd.app import MDApp
        app: MDApp = MDApp.get_running_app()
        if hasattr(app, 'update_task_statistics'):
            app.update_task_statistics()
        self.update_task_statistics()
    
    def delete_items(self) -> None:
        """
        Delete this task from both the UI and database.
        
        Removes the task widget from its parent and deletes the corresponding
        record from the database.
        """
        try:
            self.parent.remove_widget(self)
            DATABASE.delete_task(self.index)
        except Exception as e:
            print(f'Error deleting task: {e}')

class NavBar(CommonElevationBehavior, MDFloatLayout):
    """
    Navigation bar for the application.
    
    Provides a bottom navigation bar with icons for switching between different
    screens of the application.
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.spacing = '10dp'
        self.size_hint = (1, None)
        self.height = '80dp'

class DialogContent(MDBoxLayout):
    """
    Content for the task creation dialog.
    
    Provides UI elements for entering a new task description and selecting a due date.
    
    Attributes:
        app (MDApp): Reference to the main application
        task_text (MDTextField): Text field for task description
        date_text (MDLabel): Label showing selected due date
    """
    def __init__(self, app: MDApp, **kwargs) -> None:
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
        self.date_text.text = str(datetime.now().strftime('%A, %d %B %Y'))
    
    def on_task_entered(self, *args) -> None:
        """
        Handle task submission when Enter key is pressed in the text field.
        
        Creates a new task with the entered description and selected date.
        """
        self.app.add_task(self.task_text, self.date_text)
        self.task_text.text = ''

    def show_date_picker(self, *args) -> None:
        """
        Display a date picker dialog for selecting the task due date.
        """
        date_dialog: MDModalDatePicker = MDModalDatePicker()
        date_dialog.bind(on_ok = self.on_ok, on_cancel = self.on_dismiss)
        date_dialog.open()
    
    def on_dismiss(self, instance_date_picker: MDModalDatePicker) -> None:
        """
        Handle the dismissal of the date picker dialog.
        """
        instance_date_picker.dismiss()
    
    def on_ok(self, instance_date_picker: MDModalDatePicker) -> None:
        """
        Process the selected date when user confirms in the date picker.
        
        Formats the selected date and updates the date label in the dialog.
        """
        try:
            date_obj: list[int] = instance_date_picker.get_date()
            date_year: str = str(date_obj[0])
            date: str = instance_date_picker.set_text_full_date()
            date = date_format(date)
            self.date_text.text = str(date + ' ' + date_year[0:4])
        except Exception as e:
            print(f'Error setting date: {e}')
        
        instance_date_picker.dismiss()


def main() -> None:
    print('RUN `main.py`!!!')
    exit()

kivy.require('2.3.0')
if __name__ == '__main__':
    main()
