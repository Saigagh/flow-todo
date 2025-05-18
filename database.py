import sqlite3

class Database:
    @staticmethod
    def connect():
        try:
            db = sqlite3.connect("todo.db")
            c = db.cursor()
            c.execute(
                "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, Task VARCHAR(255) NOT NULL, Date VARCHAR(255) NOT NULL)"
            )
            return db
        except Exception as e:
            print(e)

    @staticmethod
    def read(db):
        c = db.cursor()
        c.execute("SELECT Task, Date FROM tasks")
        return c.fetchall()

    @staticmethod
    def insert(db, values):
        c = db.cursor()
        c.execute("INSERT INTO tasks (Task, Date) VALUES (?, ?)", values)
        db.commit()

    @staticmethod
    def delete(db, values):
        c = db.cursor()
        c.execute("DELETE FROM tasks WHERE Task=?", values)
        db.commit()

    @staticmethod
    def update(db, values):
        c = db.cursor()
        c.execute("UPDATE tasks SET Task=? WHERE Task=?", values)
        db.commit()
