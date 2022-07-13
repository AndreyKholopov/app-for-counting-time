import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('data.db', check_same_thread=False)
        self.cursor = self.con.cursor()
        self.create_task_table()

    def create_task_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, minutes varchar(2), hours varchar(50))")
        self.con.commit()

    def create_task(self, task, minutes, hours):
        self.cursor.execute("INSERT INTO tasks(task, minutes, hours) VALUES(?, ?, ?)", (task, minutes, hours,))
        self.con.commit()

        created_task = self.cursor.execute("SELECT id, task, minutes, hours FROM tasks WHERE task = ?", (task,)).fetchall()
        return created_task[-1]
        
    def change_task(self, taskid, task, minutes, hours):
        self.cursor.execute("UPDATE tasks SET task = ?, minutes = ?, hours = ? WHERE id = ?", (task, minutes, hours, taskid,))
        self.con.commit()

        created_task = self.cursor.execute("SELECT id, task, minutes, hours FROM tasks WHERE task = ?", (task,)).fetchall()
        return created_task[-1]

    def get_tasks(self):
        tasks = self.cursor.execute("SELECT id, task, minutes, hours FROM tasks").fetchall()
        return tasks

    def delete_task(self, taskid):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()