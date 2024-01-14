import flet as ft
from loguru import logger

from scorer.player import Player
from scorer.match import Match

from flet_score_board.match_configuration_widget import MatchConfigurationWidget
from flet_score_board.status_bar import StatusBar
from flet_score_board.score_labels_widget import ScoreLabelsWidget
from flet_score_board.player_score_widget import PlayerScoreWidget
from flet_score_board.app_header import AppHeader

COL_NAME_EXPAND = 4
COL_SET_EXPAND=1
COL_POINTS_EXPAND=2
FONT_SIZE=24
TIEBREAK_BADGE_COLOR=ft.colors.GREEN_100
TIEBREAK_BADGE_TEXT_COLOR=ft.colors.BLACK

class ScoreBoard(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.best_of=3
        self.label_row = ScoreLabelsWidget()
        self.server_row = PlayerScoreWidget(self.__score_point_for_server)
        self.returner_row = PlayerScoreWidget(self.__score_point_for_returner)
        self.match_setup_row = MatchConfigurationWidget(self.__on_best_of_change, self.__start_match)
        self.status_bar = StatusBar(self.__on_reset_match)

    def __start_match(self, event):
        server = Player(self.server_row.get_player_name())
        returner = Player(self.returner_row.get_player_name())
        with_tiebreaks = self.match_setup_row.is_tiebreak_switch_on()
        logger.info("---- START MATCH: {} against {}; best-of {} ; with tiebreaks:{}".format(server.name, returner.name, self.best_of, with_tiebreaks))
        self.match = Match(server, returner, bestOf=self.best_of, withTiebreaks=with_tiebreaks)
        self.server_row.set_player_name(server.name)
        self.server_row.reset_score()
        self.returner_row.set_player_name(returner.name)
        self.returner_row.reset_score()                
        self.match_setup_row.visible=False
        self.status_bar.show_reset_button()
        self.update()

    def __on_best_of_change(self, event:ft.ControlEvent):
        self.best_of = self.match_setup_row.get_best_of()
        self.label_row.set_bestof_mode(self.best_of)
        self.server_row.set_bestof_mode(self.best_of)
        self.returner_row.set_bestof_mode(self.best_of) 

    def __on_reset_match(self, event:ft.ControlEvent):
        self.label_row.set_bestof_mode(3)
        self.server_row.reset()
        self.returner_row.reset()
        self.match_setup_row.reset()
        self.match_setup_row.visible=True
        self.status_bar.hide_reset_button()
        self.status_bar.update_status_text("Restart Match")
        self.update()

    def __score_point_for_server(self, event):
        self.__score_point_for(self.match.server)

    def __score_point_for_returner(self, event):
        self.__score_point_for(self.match.returner)

    def __score_point_for(self, player:Player):
        self.match.rallyPointFor(player)
        self.__update_scoreboard()
        if self.match.isOver():
            winner = self.match.winner()
            self.status_bar.update_status_text("Match OVER! Winner: {}".format(winner.name))
            self.__highlight_winner(winner)
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

    def __highlight_winner(self, winner:Player):
        if(self.match.isOver()):
            winner_score_row = self.server_row if winner is self.match.winner() else self.returner_row
            winner_score_row.write_to_points_field("W")
        else:
            raise ValueError("Cannot highlight winner since the match is not over yet. Score: {}".format(self.match.score()))
        
    def build(self):
        return ft.Container(
            width=600,
            padding=40,
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
