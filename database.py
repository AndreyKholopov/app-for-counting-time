import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('data.db')
        self.cursor = self.con.cursor()
        self.create_task_table()

    def create_task_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, time varchar(50))")
        self.con.commit()

    def create_task(self, task, time):
        self.cursor.execute("INSERT INTO tasks(task, time) VALUES(?, ?)", (task, time,))
        self.con.commit()

        created_task = self.cursor.execute("SELECT id, task, time FROM tasks WHERE task = ?", (task,)).fetchall()
        return created_task[-1]

    def get_tasks(self):
        tasks = self.cursor.execute("SELECT id, task, time FROM tasks").fetchall()
        return tasks

    def delete_task(self, taskid):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()