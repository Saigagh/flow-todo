# modules
import flet
from flet import *
from datetime import datetime
import sqlite3


class Database:
    def ConnectToDatabase():
        try:
            db = sqlite3.connect("todo.db")
            c = db.cursor()
            c.execute(
                "CREATE TABLE if not exists tasks (id INTEGER PRIMARY KEY, Task VARCHAR(255) NOT NULL, Date VARCHAR(255) NOT NULL)"
            )
            return db
        except Exception as e:
            print(e)

    def ReadDatabase(db):
        c = db.cursor()
        c.execute("SELECT Task, Date FROM tasks")
        records = c.fetchall()
        return records

    def InsertDatabase(db, values):
        c = db.cursor()
        c.execute("INSERT INTO tasks (Task, Date) VALUES (?,?)", values)
        db.commit()

    def DeleteDatabase(db, values):
        c = db.cursor()
        c.execute("DELETE FROM tasks WHERE Task=?", values)
        db.commit()

    def UpdateDatabase(db, values):
        c = db.cursor()
        c.execute("UPDATE tasks SET Task=? WHERE Task=?", values)
        db.commit()


class FormContainer(UserControl):
    def __init__(self, func):
        self.func = func
        super().__init__()

    def build(self):
        return Container(
            width=280,
            height=80,
            bgcolor="bluegrey500",
            opacity=0,
            border_radius=20,
            margin=margin.only(left=-20, right=-20),
            animate=animation.Animation(400, "decelerate"),
            animate_opacity=200,
            padding=padding.only(top=45, bottom=45),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    TextField(
                        height=48,
                        width=255,
                        filled=True,
                        text_size=12,
                        color="black",
                        border_color="transparent",
                        hint_text="Введите описание",
                        hint_style=TextStyle(size=11, color="black"),
                    ),
                    IconButton(
                        content=Text("Добавить задачу", color="white"),
                        width=180,
                        height=44,
                        on_click=self.func,  # pass function here
                        style=ButtonStyle(
                            bgcolor={"": "black"},
                            shape={
                                "": RoundedRectangleBorder(radius=8),
                            },
                        ),
                    ),
                ],
            ),
        )


class CreateTask(UserControl):
    def __init__(self, task: str, date: str, func1, func2):
        self.task = task
        self.date = date
        self.func1 = func1
        self.func2 = func2
        super().__init__()

    def TaskDeleteEdit(self, name, color, func):
        return IconButton(
            icon=name,
            width=30,
            icon_size=18,
            icon_color=color,
            opacity=0,
            animate_opacity=200,
            on_click=lambda e: func(self.GetContainerInstance()),
        )

    def GetContainerInstance(self):
        return self

    def ShowIcons(self, e):
        if e.data == "true":
            (
                e.control.content.controls[1].controls[0].opacity,
                e.control.content.controls[1].controls[1].opacity,
            ) = (1, 1)
            e.control.content.update()
        else:
            (
                e.control.content.controls[1].controls[0].opacity,
                e.control.content.controls[1].controls[1].opacity,
            ) = (0, 0)
            e.control.content.update()

    def build(self):
        return Container(
            width=255,
            height=60,
            border=border.all(0.85, "black54"),
            border_radius=8,
            on_hover=lambda e: self.ShowIcons(e),
            clip_behavior=ClipBehavior.HARD_EDGE,
            padding=10,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        spacing=1,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(value=self.task, size=10, weight="Bold"),
                            Text(value=self.date, size=9, color="black54"),
                        ],
                    ),
                    # Icons Delete and Edit
                    Row(
                        spacing=0,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.TaskDeleteEdit(
                                icons.DELETE_ROUNDED, "red500", self.func1
                            ),
                            self.TaskDeleteEdit(
                                icons.EDIT_ROUNDED, "black54", self.func2
                            ),
                        ],
                    ),
                ],
            ),
        )


def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def AddTaskToScreen(e):
        # get current date
        dateTime = datetime.now().strftime("%b, %d, %Y  %I:%M")

        db = Database.ConnectToDatabase()  # returns the db
        Database.InsertDatabase(db, (form.content.controls[0].value, dateTime))
        db.close()

        # check if there's any content in the textfield
        if form.content.controls[0].value:
            _main_column_.controls.append(
                CreateTask(
                    form.content.controls[0].value,
                    dateTime,
                    DeleteFunction,
                    UpdateFunction,
                )
            )
            _main_column_.update()
            CreateToDoTask(e)
        else:
            db.close()
            pass

    def DeleteFunction(e):

        db = Database.ConnectToDatabase()
        Database.DeleteDatabase(
            db, (e.controls[0].content.controls[0].controls[0].value,)
        )
        db.close()

        _main_column_.controls.remove(e)
        _main_column_.update()

    def UpdateFunction(e):
        form.height, form.opacity = 200, 1
        (
            form.content.controls[0].value,
            form.content.controls[1].content.value,
            form.content.controls[1].on_click,
        ) = (
            e.controls[0].content.controls[0].controls[0].value,
            "Update",
            lambda _: FinalizeUpdate(e),
        )
        form.update()

    def FinalizeUpdate(e):
        db = Database.ConnectToDatabase()
        Database.UpdateDatabase(db, (
            form.content.controls[0].value,
            e.controls[0].content.controls[0].controls[0].value,
            ),
        )

        e.controls[0].content.controls[0].controls[0].value = form.content.controls[
            0
        ].value
        e.controls[0].content.update()
        CreateToDoTask(e)

    # toggle container visibility
    def CreateToDoTask(e):
        if form.height != 200:
            form.height = 200
            form.opacity = 1
            form.update()
        else:
            form.height = 80
            form.opacity = 0
            form.content.controls[0].value = None
            form.content.controls[1].content.value = "Добавить задачу"
            form.content.controls[1].on_click = lambda e: AddTaskToScreen(e)
            form.update()

    _main_column_ = Column(
        scroll="hidden",
        expand=True,
        alignment=MainAxisAlignment.START,
        controls=[
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # title row
                    Text("Список задач", size=18, weight="bold"),
                    IconButton(
                        icons.ADD_CIRCLE_ROUNDED,
                        icon_size=18,
                        on_click=lambda e: CreateToDoTask(e),
                    ),
                ],
            ),
            Divider(height=8, color="grey"),
        ],
    )

    # set up mobile UI
    page.add(
        # window BG container
        Container(
            width=1500,
            height=800,
            margin=-10,
            bgcolor="bluegrey900",
            alignment=alignment.center,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    # main container
                    Container(
                        width=280,
                        height=600,
                        bgcolor="white",
                        border_radius=20,
                        border=border.all(0.7, "black"),
                        padding=padding.only(top=35, left=20, right=20),
                        clip_behavior=ClipBehavior.HARD_EDGE,
                        content=Column(
                            alignment=MainAxisAlignment.CENTER,
                            expand=True,
                            controls=[
                                # main colum
                                _main_column_,
                                # form class
                                FormContainer(lambda e: AddTaskToScreen(e)),
                            ],
                        ),
                    )
                ],
            ),
        )
    )
    page.update()

    form = page.controls[0].content.controls[0].content.controls[1].controls[0]

    db = Database.ConnectToDatabase()
    for task in Database.ReadDatabase(db)[::-1]:  # [::-1] - reverse order
        _main_column_.controls.append(
            CreateTask(
                task[0],
                task[1],
                DeleteFunction,
                UpdateFunction,
            )
        )
    _main_column_.update()


if __name__ == "__main__":
    flet.app(target=main)
