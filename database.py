import sqlite3

class Database():
    def __init__(self: 'Database') -> None:
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()
        self.create_task_table()
    
    def create_task_table(self: 'Database') -> None:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            task varchar(50) NOT NULL,
                            due_date varchar(50),
                            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))''')
        self.conn.commit()
    
    def create_task(self: 'Database', task: str, due_date: str = None) -> list[any]:
        self.cursor.execute('INSERT INTO tasks(task, due_date, completed) VALUES(?, ?, 0)', (task, due_date,))
        self.conn.commit()

        created_task: list[any] = self.cursor.execute('SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0', (task,)).fetchall()
        return created_task[-1]

    def get_tasks(self: 'Database') -> tuple[list[any], list[any]]:
        uncomplite_tasks: list[any] = self.cursor.execute('SELECT id, task, due_date, completed FROM tasks WHERE completed = 0').fetchall()
        completed_tasks: list[any] = self.cursor.execute('SELECT id, task, due_date, completed FROM tasks WHERE completed = 1').fetchall()
        return uncomplite_tasks, completed_tasks

    def mark_task_as_complete(self: 'Database', taskid: int) -> None:
        self.cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (taskid,))
        self.conn.commit()
    
    def mark_task_as_incomplete(self: 'Database', taskid: int) -> None:
        self.cursor.execute('UPDATE tasks SET completed = 0 WHERE id = ?', (taskid,))
        self.conn.commit()
    
    def delete_task(self: 'Database', taskid: int) -> None:
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (taskid,))
        self.conn.commit()
    
    def close_db_connection(self: 'Database') -> None:
        self.conn.close()

if __name__ == '__main__':
    exit()
