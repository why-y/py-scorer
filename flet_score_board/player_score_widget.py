import flet as ft
from loguru import logger
import flet_score_board.score_dict_helper as ScoreHelper
import flet_score_board.score_board as score_board

class PlayerScoreWidget(ft.UserControl):
    def __init__(self, on_score_button_clicked):
        super().__init__()
        self.player_name = ft.TextField(
            hint_text="Server Name",
            expand=score_board.COL_NAME_EXPAND
        )
        self.player_score_button = ft.ElevatedButton(
            expand=score_board.COL_NAME_EXPAND,
            visible=False,
            on_click=on_score_button_clicked
        )
        self.player_points = ft.Text(
            value="",
            expand=score_board.COL_POINTS_EXPAND,
            text_align=ft.TextAlign.RIGHT,
            weight=ft.FontWeight.BOLD, 
            size=score_board.FONT_SIZE
        )
        self.player_score_row = ft.Row(
            controls=[
                self.player_name,
                self.player_score_button,
                self.player_points,
                # set score fields 1-3:
                ft.Text(value="", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_SET_EXPAND, size=score_board.FONT_SIZE),
                ft.Text(value="", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_SET_EXPAND, size=score_board.FONT_SIZE),
                ft.Text(value="", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_SET_EXPAND, size=score_board.FONT_SIZE)
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
                ft.Text(value="", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_SET_EXPAND, size=score_board.FONT_SIZE),
            )
            self.player_score_row.controls.append(
                ft.Text(value="", text_align=ft.TextAlign.RIGHT, expand=score_board.COL_SET_EXPAND, size=score_board.FONT_SIZE),
            )
        else:
            raise ValueError("Best-Of: {} is not supported!".format(best_of))
        self.update()
       
    def disable_score_button(self):
        self.player_score_button.disabled=True
        self.update()

    def update_score_for(self, player_name:str, match_score:dict):
        self.__update_sets_for(player_name, match_score)
        latest_set_score=ScoreHelper.get_latest_set_score(match_score)
        self.player_points.value=ScoreHelper.get_point_score_for(player_name, latest_set_score)
        self.update()

    def write_to_points_field(self, value:str):
        self.player_points.value=value
        self.update()
    
    def __update_sets_for(self, player_name:str, match_score:dict):
        player_set_scores=ScoreHelper.get_player_set_scores(player_name, match_score)
        row_offset=3
        no_of_sets=len(player_set_scores)
        for set_index in range(0, no_of_sets):
            set_row=row_offset+set_index
            self.player_score_row.controls[set_row].value = player_set_scores[set_index]
    