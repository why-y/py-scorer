import flet as ft
from loguru import logger

class MatchConfigurationWidget(ft.UserControl):
    def __init__(self, on_bestof_change, on_start_match):
        super().__init__()
        self.best_of_selector=ft.SegmentedButton(
            on_change=on_bestof_change,
            selected={"3"},
            allow_empty_selection=False,
            allow_multiple_selection=False,
            segments=[
                ft.Segment(
                    value="3",
                    label=ft.Text("3")
                ),
                ft.Segment(
                    value="5",
                    label=ft.Text("5")
                )
            ]
        )
        self.start_button=ft.ElevatedButton(
            text="Start The Match",
            on_click=on_start_match
        ) 

    def get_best_of(self) ->int:
        return int(self.best_of_selector.selected.pop())

    def build(self) -> ft.Row:
        return ft.Row(controls=[
                ft.Text(
                    value="Best Of "
                ),
                self.best_of_selector,
                self.start_button
        ])
