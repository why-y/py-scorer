import flet as ft

class AppHeader(ft.UserControl):
    def __init__(self, title):
        super().__init__()
        self.title = title
    
    def build(self) -> ft.Row:
        self.title_text = ft.Text(
            value = self.title,
            size=42,
            weight=ft.FontWeight.BOLD
        )
        return ft.Row(controls=[self.title_text])
