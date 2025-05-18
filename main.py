import flet
from flet import *
from datetime import datetime

from database import Database
from ui.form_container import FormContainer
from ui.task_item import CreateTask

def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def AddTaskToScreen(e):
        dateTime = datetime.now().strftime("%b, %d, %Y  %I:%M")
        db = Database.connect()
        Database.insert(db, (form.content.controls[0].value, dateTime))
        db.close()

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

    def DeleteFunction(e):
        db = Database.connect()
        Database.delete(db, (e.controls[0].content.controls[0].controls[0].value,))
        db.close()
        _main_column_.controls.remove(e)
        _main_column_.update()

    def UpdateFunction(e):
        form.height, form.opacity = 200, 1
        form.content.controls[0].value = e.controls[0].content.controls[0].controls[0].value
        form.content.controls[1].content.value = "Отредактировать"
        form.content.controls[1].on_click = lambda _: FinalizeUpdate(e)
        form.update()

    def FinalizeUpdate(e):
        db = Database.connect()
        Database.update(db, (
            form.content.controls[0].value,
            e.controls[0].content.controls[0].controls[0].value,
        ))
        db.close()
        e.controls[0].content.controls[0].controls[0].value = form.content.controls[0].value
        e.controls[0].content.update()
        CreateToDoTask(e)

    def CreateToDoTask(e):
        if form.height != 200:
            form.height = 200
            form.opacity = 1
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
                    Text("Все задачи", size=32, weight="bold"),
                    IconButton(
                        icons.ADD_CIRCLE_ROUNDED,
                        icon_size=32,
                        icon_color="black",
                        on_click=CreateToDoTask,
                    ),
                ],
            ),
        ],
    )

    page.add(
        Container(
            width=1500,
            height=800,
            margin=-10,
            bgcolor="#FFFFFF",
            alignment=alignment.center,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        width=314,
                        height=681,
                        image=flet.DecorationImage(
                            src="src/background.jpg",
                            fit=ImageFit.COVER,
                        ),
                        border_radius=33,
                        border=border.all(6.4, "black"),
                        padding=padding.only(top=35, left=20, right=20),
                        clip_behavior=ClipBehavior.HARD_EDGE,
                        content=Column(
                            alignment=MainAxisAlignment.CENTER,
                            expand=True,
                            controls=[
                                _main_column_,
                                FormContainer(AddTaskToScreen),
                            ],
                        ),
                    )
                ],
            ),
        )
    )
    page.update()

    form = page.controls[0].content.controls[0].content.controls[1].controls[0]

    db = Database.connect()
    for task in reversed(Database.read(db)):
        _main_column_.controls.append(
            CreateTask(task[0], task[1], DeleteFunction, UpdateFunction)
        )
    db.close()
    _main_column_.update()

if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")
