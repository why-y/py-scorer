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
                    label=ft.Text("Best-of-3")
                ),
                ft.Segment(
                    value="5",
                    label=ft.Text("Best-of-5")
                )
            ]
        )
        self.with_tiebreak_switch=ft.Switch(
            label="Tiebreaks", 
            value=True
        )
        self.start_button=ft.ElevatedButton(
            text="Start Match",
            on_click=on_start_match
        ) 

    def get_best_of(self) ->int:
        return int(self.best_of_selector.selected.pop())
    
    def is_tiebreak_switch_on(self) -> bool:
        return bool(self.with_tiebreak_switch.value)
    
    def reset(self):
        self.best_of_selector.selected={"3"}
        self.with_tiebreak_switch.value=True
        self.update()

    def build(self) -> ft.Row:
        return ft.Row(controls=[
                self.best_of_selector,
                self.with_tiebreak_switch,
                self.start_button
        ])
    