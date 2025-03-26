from sys import platform

import kivy
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogContentContainer, MDDialogHeadlineText
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.widget import Widget

from database import Database
from ui_components import ListItemWithCheckbox, DialogContent

DATABASE: Database = Database()

WINDOW_WIDTH = 378
WINDOW_HEIGHT = 672

if platform == 'android':
    from android.permissions import Permission, request_permissions # type: ignore
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
else:
    Config.set('graphics', 'width', '378')
    Config.set('graphics', 'height', '672')

    Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    Window.borderless = False
    Window.resizable = False

class WedrownyPlanerApp(MDApp):
    """
    Main application class for Wędrowny Planer.

    This class manages the application lifecycle, UI interactions,
    and database operations through the UI.
    """
    task_list_dialog = None

    def on_start(self) -> None:
        """
        Initialize the application on startup.
        
        Loads existing tasks from the database and displays them in the UI.
        """
        def add_task(task: list[str], complite: bool = False) -> None:
            add_task_var: ListItemWithCheckbox = ListItemWithCheckbox(task[0], f'[b]{task[1]}[/b]', task[2])
            if complite:
                add_task_var.checkbox.active = True
                add_task_var.mark()
            self.root.ids.container.add_widget(add_task_var)
        
        self.root.ids['calendar_container'].add_widget(self.build_calendar())

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
        
        self.update_task_statistics()

    def update_task_statistics(self) -> None:
        """Update task statistics in the home screen"""
        try:
            uncompleted_tasks, completed_tasks = DATABASE.get_tasks()
            total: int = len(uncompleted_tasks) + len(completed_tasks)

            if total > 0:
                percent: int = int((len(completed_tasks) / total) * 100.0)
                stats_text: str = f'Tasks: {total} total, {len(completed_tasks)} completed ({percent}%)'
            else:
                stats_text = 'No tasks created yet'
            
            self.root.ids.task_stats.text = stats_text
        except Exception as e:
            print(f'Error updating stats: {e}')

    def change_color(self, instance) -> None:
        """
        Update the navigation bar icons when a different screen is selected.
        
        Highlights the active screen's icon and dims the others.
        
        Args:
            instance: The nav icon that was tapped
        """
        if instance in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
            for i in range(4):
                if f'nav_icon{i + 1}' == current_id:
                    self.root.ids[f'nav_icon{i + 1}'].text_color = 1, 1, 1, 1
                else:
                    self.root.ids[f'nav_icon{i + 1}'].text_color = 0, 0, 0, 1

    def show_task_dialog(self) -> None:
        """
        Display the dialog for creating a new task.
        
        Creates the dialog if it doesn't exist or displays the existing one.
        """
        def handle_add_task(instance, task_text: MDTextField, date_text: MDLabel) -> None:
            self.add_task(task_text, date_text)
        
        if not self.task_list_dialog:
            _DialogContent = DialogContent(app = self)
            self.task_list_dialog = MDDialog(
                MDDialogHeadlineText(text = 'Create Task', halign = 'left'),
                MDDialogContentContainer(_DialogContent),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(MDButtonText(text = 'Cancel'), on_release = self.close_dialog),
                    MDButton(MDButtonText(text = 'Add'), on_release = lambda instance: handle_add_task(instance, _DialogContent.task_text, _DialogContent.date_text)),
                    spacing = '10dp'
                ),
                size_hint = (0.85, 0.35)
            )
        self.task_list_dialog.open()
    
    def close_dialog(self, *args) -> None:
        """Close the task creation dialog."""
        self.task_list_dialog.dismiss()
    
    def add_task(self, task: MDTextField, task_date: MDLabel) -> None:
        """
        Create a new task with the provided description and due date.
        
        Validates the task description, adds it to the database, and displays
        it in the UI.
        
        Args:
            task: Text field containing the task description
            task_date: Label containing the due date
        """
        if not task.text or not task.text.strip():
            MDSnackbar(
                MDSnackbarText(text = 'Task cannot be empty'),
                y = 10,
                pos_hint = {'center_x': 0.5},
                size_hint_x = 0.8
            ).open()
            return
        
        if len(task.text) > 50:
            MDSnackbar(
                MDSnackbarText(text = 'Task must be less than 50 characters'),
                y = 10,
                pos_hint = {'center_x': 0.5},
                size_hint_x = 0.8
            ).open()
            return

        try:
            created_task = DATABASE.create_task(task.text, task_date.text)
            self.root.ids['container'].add_widget(ListItemWithCheckbox(created_task[0], f'[b]{created_task[1]}[/b]', task_date.text))
            task.text = ''
            self.close_dialog()
            self.update_task_statistics()
        except Exception as e:
            print(f'Error adding task: {e}')

    def search_task(self, search_text: str) -> None:
        """
        Filter the task list based on search text.
        
        Shows only tasks containing the search text and hides others.
        
        Args:
            search_text: Text to search for in task descriptions
        """
        if not search_text or not search_text.strip():
            for child in self.root.ids['container'].children[:]:
                child.opacity = 1
            return
        
        search_text = search_text.lower()
        for child in self.root.ids['container'].children[:]:
            if search_text in child.ids.task_label.text.lower():
                child.opacity = 1
            else:
                child.opacity = 0

    def build_calendar(self) -> MDGridLayout:
        """Build a calendar view showing the current month."""
        from calendar import monthcalendar
        from datetime import datetime

        current_date: datetime = datetime.now()
        year: int = current_date.year
        month: int = current_date.month
        
        calender_layout = MDGridLayout(cols = 7, spacing = '2dp', padding = '10dp', size_hint_x = None, width = WINDOW_WIDTH * 0.95)

        for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
            calender_layout.add_widget(MDLabel(text = day, halign = 'center', theme_text_color = 'Primary', font_style = 'Label'))
        
        for week in monthcalendar(year, month):
            for day in week:
                if day == 0:
                    calender_layout.add_widget(Widget(size_hint_x = None, width = '10dp'))
                else:
                    btn: MDButton = MDButton(
                        MDButtonText(text = str(day)),
                        style = 'filled',
                        size_hint = (None, None),
                        size = ('40dp', '40dp'),
                        on_release = lambda x, d = day: self.on_calendar_day_selected(d)
                    )
                    calender_layout.add_widget(btn)
        
        return calender_layout
    
    def on_calendar_day_selected(self, day: int) -> None:
        """
        Handle selection of a specific day in the calendar.
        
        Args:
            day: The day number selected in the calendar
        """
        from datetime import datetime
        selected_date: datetime = datetime(datetime.now().year, datetime.now().month, day)
        formatted_date: str = selected_date.strftime('%A %d %B %Y')
        
        self.root.ids.scr.current = 'todo'

        for child in self.root.ids['container'].children[:]:
            if formatted_date in child.ids.task_date_label.text:
                child.opacity = 1
            else:
                child.opacity = 0.3
        
        MDSnackbar(
            MDSnackbarText(text = f"Showing tasks for {selected_date.strftime('%A %d')}"),
            y = 10,
            pos_hint = {'center_x': 0.5},
            size_hint_x = 0.8
        ).open()

    def clear_tasks(self) -> None:
        """Display a confirmation dialog before clearing all tasks"""
        confirm_dialog = MDDialog(
            MDDialogHeadlineText(text = 'Clear All Tasks?'),
            MDDialogContentContainer(
                MDLabel(
                    text = 'Are you sure you want to clear all tasks? This action cannot be undone.',
                    padding = ('12dp', '12dp', '12dp', '12dp')
                )
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text = 'Cancel'),
                    on_release = lambda x: confirm_dialog.dismiss()
                ),
                MDButton(
                    MDButtonText(text = 'Clear'),
                    on_release = lambda x: self._perform_clear_tasks(confirm_dialog)
                ),
                spacing = '10dp'
            ),
            size_hint = (0.8, 0.3)
        )
        confirm_dialog.open()
    
    def _perform_clear_tasks(self, dialog: MDDialog) -> None:
        """Clear all tasks from the list and database"""
        dialog.dismiss()

        self.root.ids['container'].clear_widgets()

        try:
            uncompleted_tasks, completed_tasks = DATABASE.get_tasks()
            for task in uncompleted_tasks + completed_tasks:
                DATABASE.delete_task(task[0])
            
            self.update_task_statistics()

            MDSnackbar(
                MDSnackbarText(text = 'All tasks cleared'),
                y = 10,
                pos_hint = {'center_x': 0.5},
                size_hint_x = 0.8
            ).open()
        except Exception as e:
            print(f'Error clearing tasks: {e}')
            MDSnackbar(
                MDSnackbarText(text = 'Error clearing tasks'),
                y = 10,
                pos_hint = {'center_x': 0.5},
                size_hint_x = 0.8
            ).open()
    
    def toggle_theme(self) -> None:
        """Toggle between light and dark themes"""
        if self.theme_cls.theme_style == 'Dark':
            self.theme_cls.theme_style = 'Light'
        else:
            self.theme_cls.theme_style = 'Dark'

    def exit_app(self) -> None:
        """Exit the application cleanly"""
        self.stop()

    def on_stop(self) -> None:
        """
        Perform cleanup operations when the application is closing.
        
        Ensures the database connection is properly closed.
        """
        try:
            del DATABASE
        except Exception as e:
            print(f'Error closing database connection: {e}')

    def build(self) -> None:
        """
        Build the application UI from the KV file.
        
        Sets up the application theme and loads the main UI layout.
        """
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Olive'
        return Builder.load_file('./wendrowny_planer.kv')

def main() -> None:
    WedrownyPlanerApp().run()

kivy.require('2.3.0')
if __name__ == '__main__':
    main()
