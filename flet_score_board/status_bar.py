import flet as ft
from loguru import logger

class StatusBar(ft.UserControl):

    def __init__(self, callback):
        super().__init__()
        self.status_text = ft.Text(
            value = "Status: ",
            size=10
        )
        self.reset_button = ft.TextButton(
            text="Reset",
            visible=False,
            on_click=callback
        )
    
    def build(self) -> ft.Row:
        return ft.Row(
            controls=[
                self.reset_button,
                self.status_text
            ]
        )
    
    def update_status_text(self, text:str):
        self.status_text.value=text
        self.update()

    def show_reset_button(self):
        self.reset_button.visible=True

    def hide_reset_button(self):
        self.reset_button.visible=False
