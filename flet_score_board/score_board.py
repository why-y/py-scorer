import flet as ft
from loguru import logger

from scorer.player import Player
from scorer.match import Match

from flet_score_board.match_configuration_widget import MatchConfigurationWidget
from flet_score_board.status_bar import StatusBar
from flet_score_board.score_labels_widget import ScoreLabelsWidget
from flet_score_board.player_score_widget import PlayerScoreWidget
from flet_score_board.app_header import AppHeader

#FONT_SIZE = 32
#COL_NAME_EXPAND = 3
#COL_SET_EXPAND=1
COL_POINTS_EXPAND=1

class ScoreBoard(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.with_tiebreak=True
        self.best_of=3
        self.label_row = ScoreLabelsWidget()
        self.server_row = PlayerScoreWidget(self.__score_point_for_server)
        self.returner_row = PlayerScoreWidget(self.__score_point_for_returner)
        self.match_setup_row = MatchConfigurationWidget(self.__on_best_of_change, self.__start_match)
        self.status_bar = StatusBar()

    def __start_match(self, event):
        server = Player(self.server_row.get_player_name())
        returner = Player(self.returner_row.get_player_name())
        logger.info("---- START MATCH: {} against {} best-of {}".format(server.name, returner.name, self.best_of))
        self.match = Match(server, returner, bestOf=self.best_of, withTiebreaks=self.with_tiebreak)
        self.server_row.set_player_name(server.name)
        self.server_row.reset_score()
        self.returner_row.set_player_name(returner.name)
        self.returner_row.reset_score()                
        self.match_setup_row.visible=False
        self.update()

    def __on_best_of_change(self, event:ft.ControlEvent):
        self.best_of = self.match_setup_row.get_best_of()
        self.label_row.set_bestof_mode(self.best_of)
        self.server_row.set_bestof_mode(self.best_of)
        self.returner_row.set_bestof_mode(self.best_of)            

    def __score_point_for_server(self, event):
        self.__score_point_for(self.match.server)

    def __score_point_for_returner(self, event):
        self.__score_point_for(self.match.returner)

    def __score_point_for(self, player:Player):
        self.match.rallyPointFor(player)
        self.__update_scoreboard()
        if self.match.isOver():
            self.status_bar.update_status_text("Match OVER! Winner: {}".format(self.match.winner().name))
            self.__disable_score_buttons()
            
    def __update_scoreboard(self):
        score = self.match.score()
        self.label_row.update_labels(score)
        self.server_row.update_score_for(self.match.server.name, score)
        self.returner_row.update_score_for(self.match.returner.name, score)
        self.status_bar.update_status_text(str(score))

    def __disable_score_buttons(self):
        self.server_row.disable_score_button()
        self.returner_row.disable_score_button()
        
    def build(self):
         
        self.points_title = ft.Text(
            value="Game",
            text_align=ft.TextAlign.RIGHT,
            expand=COL_POINTS_EXPAND
        )
        
        return ft.Container(
            width=600,
            padding=40,
            bgcolor=ft.colors.LIGHT_GREEN,
            border_radius=ft.border_radius.all(20),
            content=ft.Column(
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
