# modules
import flet
from flet import *
from datetime import datetime
import sqlite3


def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

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
            )
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
                        border=border.all(0.5, "blue"),
                        padding=padding.only(top=35, left=20, right=20),
                        clip_behavior=ClipBehavior.HARD_EDGE,
                        content=Column(
                            alignment=MainAxisAlignment.CENTER,
                            expand=True,
                            controls=[
                                # main colum
                                _main_column_,
                                # form class
                            ],
                        ),
                    )
                ],
            ),
        )
    )
    page.update()
    pass


if __name__ == "__main__":
    flet.app(target=main)
