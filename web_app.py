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

FONT_SIZE = 32

SERVER_NAME = "Harry Benalli"
RETURNER_NAME = "Kenny Roncow"
COL_NAME_EXPAND = 3
COL_POINTS_EXPAND = 1
COL_SET_EXPAND = 1

class ScoreBoardApp(UserControl):

    def score_point_for(self, event):
        player = event.control.data
        # type check vor Player required?
        self.match.rallyPointFor(player)
        self.status_text.value = str(self.match.score())
        self.update()

    def build(self):

        self.server = Player(SERVER_NAME)
        self.returner = Player(RETURNER_NAME)
        self.match = Match(self.server, self.returner)

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

        self.server_set1 = Text(
            value="0",
            expand=COL_SET_EXPAND,
            size=FONT_SIZE
        )

        self.returner_set1 = Text(
            value="0",
             expand=COL_SET_EXPAND,
            size=FONT_SIZE
        )

        self.server_set2 = Text(
            value="",
            expand=COL_SET_EXPAND,
            size=FONT_SIZE
        )

        self.returner_set2 = Text(
            value="",
            expand=COL_SET_EXPAND,
           size=FONT_SIZE
        )

        self.server_set3 = Text(
            value="",
            expand=COL_SET_EXPAND,
            size=FONT_SIZE
        )

        self.returner_set3 = Text(
            value="",
            expand=COL_SET_EXPAND,
            size=FONT_SIZE
        )

        self.status_text = Text(
            value = "",
            size=10
        )

        return Container(
            width=600,
            padding=20,
            bgcolor=colors.LIGHT_GREEN,
            border_radius=border_radius.all(20),
            content=Column(
                controls=[
                    self.header_row,
                    # label row
                    Row(
                        controls=[
                            Text(value="Player", expand=COL_NAME_EXPAND),
                            Text(value="Points", expand=COL_POINTS_EXPAND),
                            Text(value="Set 1", expand=COL_SET_EXPAND),
                            Text(value="Set 2", expand=COL_SET_EXPAND),
                            Text(value="Set 3", expand=COL_SET_EXPAND),
                        ]
                    ),
                    # 1st Player row
                    Row(
                        controls=[
                            self.server_name,
                            self.server_points,
                            self.server_set1,
                            self.server_set2,
                            self.server_set3
                        ]
                    ),
                    # 2nd Player row
                    Row(
                        controls=[
                            self.returner_name,
                            self.returner_points,
                            self.returner_set1,
                            self.returner_set2,
                            self.returner_set3
                        ]
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
 #   page.horizontal_alignment = CrossAxisAlignment.CENTER

    # create application instance
    score_board = ScoreBoardApp()

    # add application's root control to the page
    page.add(score_board)
    page.update()

flet.app(target=main)