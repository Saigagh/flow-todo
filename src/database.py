import sqlite3


class Database:
    @staticmethod
    def connect():
        try:
            data_base = sqlite3.connect("todo.data_base")
            cursor = data_base.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    Task VARCHAR(255) NOT NULL,
                    Date VARCHAR(255) NOT NULL
                )
                """
            )
            return data_base
        except Exception as e:
            print(e)

    @staticmethod
    def read(data_base):
        cursor = data_base.cursor()
        cursor.execute("SELECT Task, Date FROM tasks")
        return cursor.fetchall()

    @staticmethod
    def insert(data_base, values):
        cursor = data_base.cursor()
        cursor.execute("INSERT INTO tasks (Task, Date) VALUES (?, ?)", values)
        data_base.commit()

    @staticmethod
    def delete(data_base, values):
        cursor = data_base.cursor()
        cursor.execute("DELETE FROM tasks WHERE Task=?", values)
        data_base.commit()

    @staticmethod
    def update(data_base, values):
        cursor = data_base.cursor()
        cursor.execute("UPDATE tasks SET Task=? WHERE Task=?", values)
        data_base.commit()
