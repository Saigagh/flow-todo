import flet as ft
from datetime import datetime

from database import Database
from ui.form_container import FormContainer
from ui.task_item import CreateTask


def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def add_task_to_screen(e):
        date_time = datetime.now().strftime("%b, %d, %Y  %I:%M")
        data_base = Database.connect()
        Database.insert(data_base, (form.content.controls[0].value, date_time))
        data_base.close()

        if form.content.controls[0].value:
            main_column.controls.append(
                CreateTask(
                    form.content.controls[0].value,
                    date_time,
                    delete_function,
                    update_function,
                )
            )
            main_column.update()
            create_todo_task(e)

    def delete_function(e):
        data_base = Database.connect()
        Database.delete(
            data_base,
            (e.controls[0].content.controls[0].controls[0].value,),
        )
        data_base.close()
        main_column.controls.remove(e)
        main_column.update()

    def update_function(e):
        form.height = 200
        form.opacity = 1
        form.content.controls[0].value = (
            e.controls[0].content.controls[0].controls[0].value
        )
        form.content.controls[1].content.value = "Отредактировать"
        form.content.controls[1].on_click = lambda _: finalize_update(e)
        form.update()

    def finalize_update(e):
        data_base = Database.connect()
        Database.update(
            data_base,
            (
                form.content.controls[0].value,
                e.controls[0].content.controls[0].controls[0].value,
            ),
        )
        data_base.close()
        e.controls[0].content.controls[0].controls[0].value = (
            form.content.controls[0].value
        )
        e.controls[0].content.update()
        create_todo_task(e)

    def create_todo_task(e):
        if form.height != 200:
            form.height = 200
            form.opacity = 1
        else:
            form.height = 80
            form.opacity = 0
            form.content.controls[0].value = None
            form.content.controls[1].content.value = "Добавить задачу"
            form.content.controls[1].on_click = lambda e: add_task_to_screen(e)
        form.update()

    main_column = ft.Column(
        scroll="hidden",
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("Все задачи", size=32, weight="bold"),
                    ft.IconButton(
                        ft.icons.ADD_CIRCLE_ROUNDED,
                        icon_size=32,
                        icon_color="black",
                        on_click=create_todo_task,
                    ),
                ],
            ),
        ],
    )

    page.add(
        ft.Container(
            width=1500,
            height=800,
            margin=-10,
            bgcolor="#FFFFFF",
            alignment=ft.alignment.center,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=314,
                        height=681,
                        image=ft.DecorationImage(
                            src="src/background.jpg",
                            fit=ft.ImageFit.COVER,
                        ),
                        border_radius=33,
                        border=ft.border.all(6.4, "black"),
                        padding=ft.padding.only(top=35, left=20, right=20),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True,
                            controls=[
                                main_column,
                                FormContainer(add_task_to_screen),
                            ],
                        ),
                    )
                ],
            ),
        )
    )
    page.update()

    form = (
        page.controls[0]
        .content.controls[0]
        .content.controls[1]
        .controls[0]
    )

    data_base = Database.connect()
    for task in reversed(Database.read(data_base)):
        main_column.controls.append(
            CreateTask(task[0], task[1], delete_function, update_function)
        )
    data_base.close()
    main_column.update()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
