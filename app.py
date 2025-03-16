# modules
import flet
from flet import *
from datetime import datetime
import sqlite3


class FormContainer(UserControl):
    def __init__(self):
        self.func = None
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


def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # toggle container visibility
    def CreateToDoTask(e):
        if form.height != 200:
            form.height = 200
            form.opacity = 1
        else:
            form.height = 80
            form.opacity = 0
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
                        Icons.ADD_CIRCLE_ROUNDED,
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
                                FormContainer(),
                            ],
                        ),
                    )
                ],
            ),
        )
    )
    page.update()

    form = page.controls[0].content.controls[0].content.controls[1].controls[0]


if __name__ == "__main__":
    flet.app(target=main)
