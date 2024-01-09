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

from loguru import logger

from scorer.match import Match
from scorer.player import Player
from scorer.set import Set
from scorer.game import Game
from scorer.tiebreak import Tiebreak

FONT_SIZE = 32
COL_NAME_EXPAND = 3
COL_POINTS_EXPAND=1
COL_SET_EXPAND=1
BEST_OF_DEFAULT=3

class ScoreBoardApp(UserControl):

    def __init__(self):
        super().__init__()
        self.with_tiebreak=True
        self.best_of=BEST_OF_DEFAULT

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
                
        self.setup_row.visible=False
        self.update()

    def __score_point_for_server(self, event):
        self.__score_point_for(self.server)       

    def __score_point_for_returner(self, event):
        self.__score_point_for(self.returner)       

    def __get_best_of_selection(self):
        selected = int(self.best_of_selector.selected.pop())
        logger.info("---- selector.selected:{} ---- type:{}".format(selected, type(selected)))
        return selected

    def __on_best_of_change(self, event:ControlEvent):
        self.best_of = self.__get_best_of_selection()
        if self.best_of == 3:
            self.label_row.controls.pop()
            self.label_row.controls.pop()
            self.server_row.controls.pop()
            self.server_row.controls.pop()
            self.returner_row.controls.pop()
            self.returner_row.controls.pop()
        elif self.best_of == 5:
            self.label_row.controls.append(
                Text(value="Set 4", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND)
            )
            self.label_row.controls.append(
                Text(value="Set 5", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND)
            )
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
        self.points_title.value="Tiebreak"
        tiebreak_score=tiebreak.score().get(Tiebreak.KEY)
        self.server_points.value=str(tiebreak_score.get(self.server.name))
        self.returner_points.value=str(tiebreak_score.get(self.returner.name))

    def __update_running_game_points(self, running_game:Game):
        self.points_title.value="Game"
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
        self.status_text.value=text

    def build(self):
        
        self.header_row = Row(
            controls= [
                Text(
                    value = "Tennis Score Board",
                    size=42,
                    weight=FontWeight.BOLD
                )
            ]
        )
 
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

        self.best_of_selector=SegmentedButton(
            on_change=self.__on_best_of_change,
            selected={BEST_OF_DEFAULT},
            allow_empty_selection=False,
            allow_multiple_selection=False,
            segments=[
                Segment(
                    value="3",
                    label=Text("3")
                ),
                Segment(
                    value="5",
                    label=Text("5")
                )
            ]
        )

        self.label_row = Row(
            controls=[
                Text(value="Player", expand=COL_NAME_EXPAND),
                self.points_title,
                Text(value="Set 11", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND),
                Text(value="Set 22", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND),
                Text(value="Set 33", text_align=TextAlign.RIGHT, expand=COL_SET_EXPAND)
            ]
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

        self.setup_row = Row(
            controls=[
                Text(
                    value="Best Of "
                ),
                self.best_of_selector,
                ElevatedButton(
                    text="Start The Match",
                    on_click=self.__start_match
                )
            ]
        )

        self.status_text = Text(
            value = "",
            size=10
        )

        return Container(
            width=600,
            padding=40,
            bgcolor=colors.LIGHT_GREEN,
            border_radius=border_radius.all(20),
            content=Column(
                controls=[
                    self.header_row,
                    # label row
                    self.label_row,
                    self.server_row,
                    self.returner_row,
                    self.setup_row,
                    # footer row
                    Row(
                        controls=[
                            self.status_text
                        ]
                    )
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