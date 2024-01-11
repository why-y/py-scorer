import flet as ft
from loguru import logger

COL_NAME_EXPAND = 3
COL_SET_EXPAND=1
COL_POINTS_EXPAND=1


class ScoreLabelsWidget(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.points_title=ft.Text(value="Game", text_align=ft.TextAlign.RIGHT, expand=COL_POINTS_EXPAND)
        self.score_label_row= ft.Row(
            [
                ft.Text(value="Player", expand=COL_NAME_EXPAND),
                self.points_title,
                ft.Text(value="Set 1", text_align=ft.TextAlign.RIGHT, expand=COL_SET_EXPAND),
                ft.Text(value="Set 2", text_align=ft.TextAlign.RIGHT, expand=COL_SET_EXPAND),
                ft.Text(value="Set 3", text_align=ft.TextAlign.RIGHT, expand=COL_SET_EXPAND)
            ]
        )
    
    def build(self) -> ft.Row:
        return self.score_label_row
    
    def change_points_title(self, text:str):
        self.points_title.value=text
        self.update()

    def set_bestof_mode(self, best_of:int):
        if(best_of==3):
            self.score_label_row.controls.pop()
            self.score_label_row.controls.pop()
        elif(best_of==5):
            self.score_label_row.controls.append(
                ft.Text(value="Set 4", text_align=ft.TextAlign.RIGHT, expand=COL_SET_EXPAND)
            )
            self.score_label_row.controls.append(
                ft.Text(value="Set 5", text_align=ft.TextAlign.RIGHT, expand=COL_SET_EXPAND)
            )
        else:
            raise ValueError("Best-Of: {} is not supported!".format(best_of))
        self.update()






