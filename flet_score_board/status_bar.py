import flet as ft
from loguru import logger

class StatusBar(ft.UserControl):
    def __init__(self):
        super().__init__()
    
    def build(self) -> ft.Row:
        self.status_text = ft.Text(
            value = "Status: ",
            size=10
        )
        return ft.Row(controls=[self.status_text])
    
    def update_status_text(self, text:str):
        self.status_text.value=text
        self.update()
