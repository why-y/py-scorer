import flet as ft
from loguru import logger
import flet_score_board.score_board as score_board
from scorer.game import Game
from scorer.tiebreak import Tiebreak

class ScoreLabelsWidget(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.points_title=ft.Text(value="Game", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_POINTS_EXPAND)
        self.score_label_row= ft.Row(
            [
                ft.Text(value="Player", expand=score_board.COL_NAME_EXPAND),
                self.points_title,
                ft.Text(value="Set 1", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_SET_EXPAND),
                ft.Text(value="Set 2", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_SET_EXPAND),
                ft.Text(value="Set 3", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_SET_EXPAND)
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
                ft.Text(value="Set 4", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_SET_EXPAND)
            )
            self.score_label_row.controls.append(
                ft.Text(value="Set 5", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_SET_EXPAND)
            )
        else:
            raise ValueError("Best-Of: {} is not supported!".format(best_of))
        self.update()

    def update_labels(self, match_score:dict):
        latest_set_score = self.__get_latest_set_score(match_score)
        self.points_title.value=Tiebreak.KEY if self.__has_running_tieabreak(latest_set_score) else Game.KEY
        self.update()
            
    def __get_latest_set_score(self, match_score:dict) -> dict:
        set_keys = list(match_score.keys())
        return match_score.get(set_keys[-1])
    
    def __has_running_tieabreak(self, set_score:dict) -> bool:
        return False if set_score.get(Tiebreak.KEY) is None else True
