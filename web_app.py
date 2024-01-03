import flet
from flet import (
    Column,
    Container,
    ElevatedButton,
    Page,
    Row,
    Text,
    UserControl,
    FontWeight,
    TextAlign,
    border_radius,
    colors,
)

from loguru import logger

from scorer.match import Match
from scorer.player import Player
from scorer.set import Set
from scorer.game import Game
from scorer.tiebreak import Tiebreak

FONT_SIZE = 32

SERVER_NAME = "Harry Benalli"
RETURNER_NAME = "Kenny Roncow"
COL_NAME_EXPAND = 3
COL_POINTS_EXPAND = 1
COL_SET_EXPAND = 1

class ScoreBoardApp(UserControl):

    def score_point_for(self, event):
        player = event.control.data
        self.match.rallyPointFor(player)
        if self.match.isOver():
            self.write_status("Match OVER! Winner: {}".format(self.match.winner().name))
        self.__update_scoreboard()

    def __update_scoreboard(self):
        match_score=self.match.score()
        logger.info(match_score)
        running_set = self.match.sets[-1]
        self.__update_points_score(running_set)
        self.__update_sets_score()
        self.write_status(str(self.match.score()))
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
        for set_index in range(len(self.match.sets)):
            self.server_set_scores[set_index].value = self.match.sets[set_index].score().get(Set.KEY).get(self.server.name)
            self.returner_set_scores[set_index].value = self.match.sets[set_index].score().get(Set.KEY).get(self.returner.name)
        
    def write_status(self, text:str):
        self.status_text.value=text

    def build(self):
        
        self.best_of=5
        self.with_tiebreak=True
        self.server = Player(SERVER_NAME)
        self.returner = Player(RETURNER_NAME)
        self.match = Match(self.server, self.returner, bestOf=self.best_of, withTiebreaks=self.with_tiebreak)

        self.header_row = Row(
            controls= [
                Text(
                    value = "Tennis Score Board",
                    size=42,
                    weight=FontWeight.BOLD
                )
            ]
        )
 
        self.returner_name = ElevatedButton(
            text=self.match.returner.name, 
            data=self.match.returner,
            expand=COL_NAME_EXPAND,
            on_click=self.score_point_for
        )

        self.server_name = ElevatedButton(
            text=self.match.server.name, 
            data=self.match.server,
            expand=COL_NAME_EXPAND,
            on_click=self.score_point_for
        )
        
        self.server_points = Text(
            value="0",
            expand=COL_POINTS_EXPAND,
            text_align=TextAlign.RIGHT,
            weight=FontWeight.BOLD, 
            size=FONT_SIZE
        )

        self.returner_points = Text(
            value="0",
            expand=COL_POINTS_EXPAND,
            text_align=TextAlign.RIGHT,
            weight=FontWeight.BOLD, 
            size=FONT_SIZE
        )

        self.set_labels=[]
        self.server_set_scores=[]
        self.returner_set_scores=[]
        for set_no in range(1, self.best_of+1):
            self.set_labels.append(
                Text(
                    value="Set "+str(set_no),
                    text_align=TextAlign.RIGHT,
                    expand=COL_SET_EXPAND
                )
            )
            self.server_set_scores.append(
                Text(
                    value="",
                    text_align=TextAlign.RIGHT,
                    expand=COL_SET_EXPAND,
                    size=FONT_SIZE
                )
            )
            self.returner_set_scores.append(
                Text(
                    value="",
                    text_align=TextAlign.RIGHT,
                    expand=COL_SET_EXPAND,
                    size=FONT_SIZE
                )
            )

        self.points_title = Text(
            value="Game",
            text_align=TextAlign.RIGHT,
            expand=COL_POINTS_EXPAND
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
                    Row(
                        controls=[
                            Text(value="Player", expand=COL_NAME_EXPAND),
                            self.points_title
                        ] + self.set_labels
                    ),
                    # 1st Player row
                    Row(
                        controls=[
                            self.server_name,
                            self.server_points
                        ] + self.server_set_scores
                    ),
                    # 2nd Player row
                    Row(
                        controls=[
                            self.returner_name,
                            self.returner_points
                        ] + self.returner_set_scores
                    ),
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