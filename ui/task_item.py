import flet as ft


class CreateTask(ft.UserControl):
    def __init__(self, task: str, date: str, func1, func2):
        self.task = task
        self.date = date
        self.func1 = func1
        self.func2 = func2
        super().__init__()

    def TaskDeleteEdit(self, name, color, func):
        return ft.IconButton(
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
        icons_row = e.control.content.controls[1]
        if e.data == "true":
            icons_row.controls[0].opacity = 1
            icons_row.controls[1].opacity = 1
        else:
            icons_row.controls[0].opacity = 0
            icons_row.controls[1].opacity = 0
        e.control.content.update()

    def build(self):
        return ft.Container(
            width=276,
            height=60,
            bgcolor="white",
            border_radius=12,
            on_hover=lambda e: self.ShowIcons(e),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            padding=15,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=1,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                value=self.task,
                                size=12,
                                weight="bold",
                            ),
                            ft.Text(
                                value=self.date,
                                size=9,
                                weight="bold",
                                color="black54",
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            self.TaskDeleteEdit(
                                ft.icons.DELETE_ROUNDED,
                                "red500",
                                self.func1,
                            ),
                            self.TaskDeleteEdit(
                                ft.icons.EDIT_ROUNDED,
                                "black54",
                                self.func2,
                            ),
                        ],
                    ),
                ],
            ),
        )
