import flet as ft
from loguru import logger

COL_NAME_EXPAND = 3
COL_SET_EXPAND=1
COL_POINTS_EXPAND=1

GAME_KEY="Game"
TIEBREAK_KEY="Tiebreak"
SET_KEY="Set"

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

    def update_labels(self, match_score:dict):
        logger.info("Update LABELS --- match score: {}".format(match_score))
        latest_set_score = self.__get_latest_set_score(match_score)
        self.points_title.value=TIEBREAK_KEY if self.__has_running_tieabreak(latest_set_score) else GAME_KEY
        self.update()
            

    def __get_latest_set_score(self, match_score:dict) -> dict:
        set_keys = list(match_score.keys())
        return match_score.get(set_keys[-1])
    
    def __has_running_tieabreak(self, set_score:dict) -> bool:
        return False if set_score.get(TIEBREAK_KEY) is None else True




