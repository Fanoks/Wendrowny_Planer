import sqlite3

class Database():
    """
    Database manager for the Wędrowny Planer application.
    
    Handles all database operations including creating, retrieving,
    updating, and deleting tasks.
    
    Attributes:
        conn: SQLite database connection
        cursor: Database cursor for executing queries
    """
    def __init__(self) -> None:
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON')
        self.cursor.execute('PRAGMA synchronous = 1')
        self.cursor.execute('PRAGMA journal_mode = WAL')
        self.create_task_table()
    
    def __del__(self) -> None:
        self.close_db_connection()
    
    def create_task_table(self) -> None:
        """Create the tasks table if it does not exist"""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            task varchar(50) NOT NULL,
                            due_date varchar(50),
                            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))''')
        self.conn.commit()
    
    def create_task(self, task: str, due_date: str = None) -> list[any]:
        """
        Add a new task to the database.
        
        Args:
            task: Task description text
            due_date: Optional due date for the task
            
        Returns:
            A list containing the ID, description, and due date of the created task
        """
        self.cursor.execute('INSERT INTO tasks(task, due_date, completed) VALUES(?, ?, 0)', (task, due_date,))
        self.conn.commit()

        created_task: list[any] = self.cursor.execute('SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0', (task,)).fetchall()
        return created_task[-1]

    def get_tasks(self) -> tuple[list[any], list[any]]:
        """
        Retrieve all tasks from the database, separated by completion status.
        
        Returns:
            A tuple containing two lists: incomplete tasks and completed tasks
        """
        uncomplite_tasks: list[any] = self.cursor.execute('SELECT id, task, due_date, completed FROM tasks WHERE completed = 0').fetchall()
        completed_tasks: list[any] = self.cursor.execute('SELECT id, task, due_date, completed FROM tasks WHERE completed = 1').fetchall()
        return uncomplite_tasks, completed_tasks

    def mark_task_as_complete(self, taskid: int) -> None:
        """Mark a task as completed in the database"""
        self.cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (taskid,))
        self.conn.commit()
    
    def mark_task_as_incomplete(self, taskid: int) -> None:
        """Mark a task as incomplete in the database"""
        self.cursor.execute('UPDATE tasks SET completed = 0 WHERE id = ?', (taskid,))
        self.conn.commit()
    
    def delete_task(self, taskid: int) -> None:
        """Delete a task from the database"""
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (taskid,))
        self.conn.commit()
    
    def close_db_connection(self) -> None:
        """Close the database connection"""
        self.conn.close()

def main() -> None:
    print('RUN `main.py`!!!')
    exit()

if __name__ == '__main__':
    main()
