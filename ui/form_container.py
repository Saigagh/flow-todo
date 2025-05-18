import flet as ft


class FormContainer(ft.UserControl):
    def __init__(self, func):
        self.func = func
        super().__init__()

    def build(self):
        return ft.Container(
            width=314,
            height=80,
            bgcolor="white",
            opacity=0,
            border_radius=20,
            margin=ft.margin.only(left=-20, right=-20),
            animate=ft.animation.Animation(400, "decelerate"),
            animate_opacity=200,
            padding=ft.padding.only(top=25, bottom=50),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.TextField(
                        height=44,
                        width=276,
                        filled=True,
                        text_size=12,
                        color="black",
                        border_color="transparent",
                        hint_text="Введите описание",
                        hint_style=ft.TextStyle(size=11, color="black"),
                    ),
                    ft.IconButton(
                        content=ft.Text("Добавить задачу", color="white"),
                        width=276,
                        height=44,
                        on_click=self.func,
                        style=ft.ButtonStyle(
                            bgcolor={"": "black"},
                            shape={"": ft.RoundedRectangleBorder(radius=8)},
                        ),
                    ),
                ],
            ),
        )
