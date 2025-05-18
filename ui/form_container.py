from flet import *

class FormContainer(UserControl):
    def __init__(self, func):
        self.func = func
        super().__init__()

    def build(self):
        return Container(
            width=314,
            height=80,
            bgcolor="white",
            opacity=0,
            border_radius=20,
            margin=margin.only(left=-20, right=-20),
            animate=animation.Animation(400, "decelerate"),
            animate_opacity=200,
            padding=padding.only(top=25, bottom=50),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    TextField(
                        height=44,
                        width=276,
                        filled=True,
                        text_size=12,
                        color="black",
                        border_color="transparent",
                        hint_text="Введите описание",
                        hint_style=TextStyle(size=11, color="black"),
                    ),
                    IconButton(
                        content=Text("Добавить задачу", color="white"),
                        width=276,
                        height=44,
                        on_click=self.func,
                        style=ButtonStyle(
                            bgcolor={"": "black"},
                            shape={"": RoundedRectangleBorder(radius=8)},
                        ),
                    ),
                ],
            ),
        )
