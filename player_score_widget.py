import flet as ft
from loguru import logger

FONT_SIZE = 32
COL_NAME_EXPAND = 3
COL_SET_EXPAND=1
COL_POINTS_EXPAND=1

GAME_KEY="Game"
TIEBREAK_KEY="Tiebreak"
SET_KEY="Set"


class PlayerScoreWidget(ft.UserControl):
    def __init__(self, on_score_button_clicked):
        super().__init__()
        self.player_name = ft.TextField(
            hint_text="Server Name",
            expand=COL_NAME_EXPAND
        )
        self.player_score_button = ft.ElevatedButton(
            expand=COL_NAME_EXPAND,
            visible=False,
            on_click=on_score_button_clicked
        )
        self.player_points = ft.Text(
            value="",
            expand=COL_POINTS_EXPAND,
            text_align=ft.TextAlign.RIGHT,
            weight=ft.FontWeight.BOLD, 
            size=FONT_SIZE
        )
        self.player_score_row = ft.Row(
            controls=[
                self.player_name,
                self.player_score_button,
                self.player_points,
                # set score fields 1-3:
                ft.Text(value="", text_align=ft.TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
                ft.Text(value="", text_align=ft.TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
                ft.Text(value="", text_align=ft.TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE)
            ]
        )
    
    def build(self) -> ft.Row:
        return self.player_score_row
    
    def set_player_name(self, name:str):
        self.player_score_button.text=name
        self.player_name.visible=False
        self.player_score_button.visible=True
        self.update()

    def get_player_name(self) -> str:
        return str(self.player_name.value)
    
    def reset_score(self):
        self.player_points.value="0"
        # set score of 1st set to 0
        fist_set_index=3
        self.player_score_row.controls[fist_set_index].value = "0"
        self.update()

    def set_bestof_mode(self, best_of:int):
        if best_of == 3:
            self.player_score_row.controls.pop()
            self.player_score_row.controls.pop()
        elif best_of == 5:
            self.player_score_row.controls.append(
                ft.Text(value="", text_align=ft.TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
            )
            self.player_score_row.controls.append(
                ft.Text(value="", text_align=ft.TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
            )
        else:
            raise ValueError("Best-Of: {} is not supported!".format(best_of))
        self.update()
       
    def disable_score_button(self):
        self.player_score_button.disabled=True
        self.update()

    def update_score_for(self, player_name:str, match_score:dict):
        latest_set_score=self.__get_latest_set_score(match_score)
        self.__update_sets_for(player_name, match_score)
        self.__update_points_for(player_name, latest_set_score)
        self.update()
    
    def __get_latest_set_score(self, match_score:dict) -> dict:
        set_keys = list(match_score.keys())
        return match_score.get(set_keys[-1])
    
    def __update_points_for(self, player_name:str, set_score:dict):
        if self.__has_running_game(set_score):
            game=set_score.get(GAME_KEY)
            self.player_points.value=str(game.get(player_name))
        elif self.__has_running_tieabreak(set_score):
            tiebreak=set_score.get(TIEBREAK_KEY)
            self.player_points.value=str(tiebreak.get(player_name))
        else:
            self.player_points.value=""

    def __update_sets_for(self, player_name:str, match_score:dict):
        for set_key in match_score:
            set_score = match_score.get(set_key)
            row_index = self.__row_index_by_set_key(set_key)
            self.player_score_row.controls[row_index].value = set_score.get(player_name)

    def __has_running_game(self, set_score:dict) -> bool:
        return self.__has(GAME_KEY, set_score)
    
    def __has_running_tieabreak(self, set_score:dict) -> bool:
        return self.__has(TIEBREAK_KEY, set_score)
    
    def __has(self, key:str, set_score:dict) -> bool:
        return False if set_score.get(key) is None else True
    
    def __row_index_by_set_key(self, set_key:str) -> int:
        row_offset=2
        for set_no in range(1,6):
            if set_key == SET_KEY + str(set_no):
                return set_no+row_offset
        raise ValueError("Cannot determine row index from set-key:{}".format(set_key))







