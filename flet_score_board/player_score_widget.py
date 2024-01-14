import flet as ft
from loguru import logger
import flet_score_board.score_dict_helper as ScoreHelper
import flet_score_board.score_board as score_board

ROW_SET_OFFSET=3

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
                self.__create_set_score_field(),
                self.__create_set_score_field(),
                self.__create_set_score_field()
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
    
    def reset(self):
        self.player_score_button.visible=False
        self.player_name.visible=True
        self.set_bestof_mode(3)
        self.reset_score()
        self.update()

    def reset_score(self):
        self.player_points.value=""
        for set_index in range(0,self.__get_no_of_set_cells()):
            self.__clear_cell(set_index)
        self.update()

    def set_bestof_mode(self, best_of:int):
        no_of_set_fields = len(self.player_score_row.controls)-ROW_SET_OFFSET
        if no_of_set_fields < best_of:
            for _ in range(best_of-no_of_set_fields):
                self.player_score_row.controls.append(self.__create_set_score_field())
        elif no_of_set_fields > best_of:
            for _ in range(no_of_set_fields-best_of):     
                self.player_score_row.controls.pop()
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
        no_of_sets=len(player_set_scores)
        for set_index in range(0, no_of_sets):
            set_score=ScoreHelper.get_set_score_by_index(set_index, match_score)
            self.__get_set_cell(set_index).value = player_set_scores[set_index]
            if ScoreHelper.set_has_terminated_tieabreak(set_score):
                set_badge=self.__get_set_badge(set_index)
                set_badge.text=str(ScoreHelper.get_tiebreak_points_for(player_name, set_score))
                set_badge.label_visible=True
        
    def __create_set_score_field(self):
        return ft.Container(
            expand=score_board.COL_SET_EXPAND,
            content= ft.Badge(
                content=ft.Text(
                    value="", 
                    expand=True,
                    width=1000,
                    text_align=ft.TextAlign.RIGHT,
                    size=score_board.FONT_SIZE
                ),
                text="",
                label_visible=False,
                alignment=ft.alignment.top_right,
                text_color=score_board.TIEBREAK_BADGE_TEXT_COLOR,
                bgcolor=score_board.TIEBREAK_BADGE_COLOR
            )
        )
    
    def __clear_cell(self, set_index:int):
        self.__get_set_badge(set_index).label_visible=False
        self.__get_set_cell(set_index).value=""

    def __get_no_of_set_cells(self) -> int:
        return len(self.player_score_row.controls)-ROW_SET_OFFSET

    def __get_set_cell(self, set_index:int) -> ft.Text:
        return self.__get_set_badge(set_index).content
    
    def __get_set_badge(self, set_index:int) -> ft.Badge:
        row_position=ROW_SET_OFFSET+set_index
        return self.player_score_row.controls[row_position].content       


    