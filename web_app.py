from typing import Any, List, Optional, Union
import flet
from flet import (
    Column,
    Container,
    ElevatedButton,
    SegmentedButton,
    Segment,
    ControlEvent,
    Page,
    Row,
    Text,
    TextField,
    UserControl,
    FontWeight,
    TextAlign,
    Icon,
    border_radius,
    icons,
    colors,
)
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, CrossAxisAlignment, MainAxisAlignment, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue, ScrollMode

from loguru import logger

from scorer.match import Match
from scorer.player import Player
from scorer.set import Set
from scorer.game import Game
from scorer.tiebreak import Tiebreak
from app_header import AppHeader
from match_configuration_widget import MatchConfigurationWidget
from status_bar import StatusBar
from score_labels_widget import ScoreLabelsWidget

FONT_SIZE = 32
COL_NAME_EXPAND = 3
COL_POINTS_EXPAND=1
COL_SET_EXPAND=1

class ScoreBoardApp(UserControl):

    def __init__(self):
        super().__init__()
        self.with_tiebreak=True
        
        self.label_row = ScoreLabelsWidget()
        self.match_setup_row = MatchConfigurationWidget(self.__on_best_of_change, self.__start_match)
        self.status_bar = StatusBar()



    def __start_match(self, event):
        self.server = Player(self.server_name.value)
        self.returner = Player(self.returner_name.value)
        logger.info("---- START MATCH: {} against {} best-of {}".format(self.server.name, self.returner.name, self.best_of))
        self.match = Match(self.server, self.returner, bestOf=self.best_of, withTiebreaks=self.with_tiebreak)
        self.server_points.value="0"
        self.returner_points.value="0"

        self.server_score_button.text = self.server_name.value
        self.server_row.controls[0]=self.server_score_button
        self.server_name.disabled=True
        
        self.returner_score_button.text = self.returner_name.value
        self.returner_row.controls[0]=self.returner_score_button
        self.returner_name.disabled=True
                
        self.match_setup_row.visible=False
        self.update()

    def __score_point_for_server(self, event):
        self.__score_point_for(self.server)       

    def __score_point_for_returner(self, event):
        self.__score_point_for(self.returner)       

    def __on_best_of_change(self, event:ControlEvent):
        self.best_of = self.match_setup_row.get_best_of()
        self.label_row.set_bestof_mode(self.best_of)
        if self.best_of == 3:
            self.server_row.controls.pop()
            self.server_row.controls.pop()
            self.returner_row.controls.pop()
            self.returner_row.controls.pop()
        elif self.best_of == 5:
            self.server_row.controls.append(
                Text(value="", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
            )
            self.server_row.controls.append(
                Text(value="", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
            )
            self.returner_row.controls.append(
                Text(value="", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
            )
            self.returner_row.controls.append(
                Text(value="", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
            )

        else:
            raise ValueError("Best-Of: {} is not supported!".format(self.best_of))
            
        self.update()

    def __score_point_for(self, player:Player):
        self.match.rallyPointFor(player)
        if self.match.isOver():
            self.__write_status("Match OVER! Winner: {}".format(self.match.winner().name))
            self.__disable_score_buttons()
        self.__update_scoreboard()

    def __update_scoreboard(self):
        match_score=self.match.score()
        logger.info(match_score)
        running_set = self.match.sets[-1]
        self.__update_points_score(running_set)
        self.__update_sets_score()
        self.__write_status(str(self.match.score()))
        self.update()

    def __update_points_score(self, running_set:Set):
        set_score = running_set.score()
        if running_set.hasRunningTiebreak():
            self.__update_tiebreak_points(running_set.getTiebreak())
        else:
            self.__update_running_game_points(running_set.getRunningGame())

    def __update_tiebreak_points(self, tiebreak:Tiebreak):
        self.label_row.change_points_title("Tiebreak")
        tiebreak_score=tiebreak.score().get(Tiebreak.KEY)
        self.server_points.value=str(tiebreak_score.get(self.server.name))
        self.returner_points.value=str(tiebreak_score.get(self.returner.name))

    def __update_running_game_points(self, running_game:Game):
        self.label_row.change_points_title("Game")
        game_score=running_game.score().get(Game.KEY)
        self.server_points.value=str(game_score.get(self.server.name))
        self.returner_points.value=str(game_score.get(self.returner.name))

    def __update_sets_score(self):
        set_row_offset = 2 # row offset for name and score-button
        for set_index in range(len(self.match.sets)):
            self.server_row.controls[set_index+set_row_offset].value = self.match.sets[set_index].score().get(Set.KEY).get(self.server.name)
            self.returner_row.controls[set_index+set_row_offset].value = self.match.sets[set_index].score().get(Set.KEY).get(self.returner.name)

    def __disable_score_buttons(self):
        self.server_score_button.disabled=True
        self.returner_score_button.disabled=True
        
    def __write_status(self, text:str):
        self.status_bar.update_status_text(text)

    def build(self):
         
        self.server_name = TextField(
            hint_text="Server Name",
            expand=COL_NAME_EXPAND
        )

        self.server_score_button = ElevatedButton(
            expand=COL_NAME_EXPAND,
            on_click=self.__score_point_for_server
        )

        self.returner_name = TextField(
            hint_text="Retruner Name",
            expand=COL_NAME_EXPAND
        )

        self.returner_score_button = ElevatedButton(
            expand=COL_NAME_EXPAND,
            on_click=self.__score_point_for_returner
        )

        self.server_points = Text(
            value="",
            expand=COL_POINTS_EXPAND,
            text_align=TextAlign.RIGHT,
            weight=FontWeight.BOLD, 
            size=FONT_SIZE
        )

        self.returner_points = Text(
            value="",
            expand=COL_POINTS_EXPAND,
            text_align=TextAlign.RIGHT,
            weight=FontWeight.BOLD, 
            size=FONT_SIZE
        )

        self.points_title = Text(
            value="Game",
            text_align=TextAlign.RIGHT,
            expand=COL_POINTS_EXPAND
        )
        
        self.server_row = Row(
            controls=[
                self.server_name,
                self.server_points,
                Text(value="", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
                Text(value="", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
                Text(value="", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE)
            ]
        )

        self.returner_row = Row(
            controls=[
                self.returner_name,
                self.returner_points,
                Text(value="", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
                Text(value="", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE),
                Text(value="", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND, size=FONT_SIZE)
            ]
        )

        return Container(
            width=600,
            padding=40,
            bgcolor=colors.LIGHT_GREEN,
            border_radius=border_radius.all(20),
            content=Column(
                controls=[
                    AppHeader("Tennis Score Board"),
                    self.label_row,
                    self.server_row,
                    self.returner_row,
                    self.match_setup_row,
                    self.status_bar
                ]
            )
        )


def main(page: Page):
    page.title = "Tennis Score Board"

    # create application instance
    score_board = ScoreBoardApp()

    # add application's root control to the page
    page.add(score_board)
    page.update()

flet.app(target=main)