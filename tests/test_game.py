import pytest
import scorer

from scorer.game import Game
from scorer.player import Player
from tests.scorer_test_helper import ScorerTestHelper


class TestGame:

    SERVER_NAME = "Tom"
    RETURNER_NAME = "Eric"

    # Arrange
    @pytest.fixture
    def test_server(self) -> Player:
        return Player(self.SERVER_NAME)
    
    @pytest.fixture
    def test_returner(self) -> Player:
        return Player(self.RETURNER_NAME)
    
    @pytest.fixture
    def test_game(self, test_server:Player, test_returner:Player) -> Game:
        return Game(test_server, test_returner)



   # Test        
    def test_start_game_server_is_tom(self, test_game:Game):
        assert test_game.server.name == self.SERVER_NAME

    def test_start_game_returner_is_eric(self, test_game:Game):
        assert test_game.returner.name == self.RETURNER_NAME
    
    def test_game_over(self, test_game:Game, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 3)
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 4)
        assert not test_game.isOver()
        test_game.rallyPointFor(test_server)
        assert test_game.isOver()

    def test_winner_is_none(self, test_game:Game, test_server:Player, test_returner:Player):
        test_game.rallyPointFor(test_server)
        test_game.rallyPointFor(test_returner)
        assert test_game.winner() == None

    def test_start_game_score_love_all(self, test_game:Game):
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, 0, 0)

    def test_score_15_0(self, test_game:Game, test_server:Player):
        test_game.rallyPointFor(test_server)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, 15, 0)

    def test_score_15_all(self, test_game:Game, test_server:Player, test_returner:Player):
        test_game.rallyPointFor(test_server)
        test_game.rallyPointFor(test_returner)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, 15, 15)

    def test_score_15_30(self, test_game:Game, test_server:Player, test_returner:Player):
        test_game.rallyPointFor(test_server)
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 2)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, 15, 30)

    def test_score_30_all(self, test_game:Game, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 2)
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 2)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, 30, 30)

    def test_score_40_30(self, test_game:Game, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 3)
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 2)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, 40, 30)

    def test_winner_is_server(self, test_game:Game, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 4)
        assert test_game.winner() == test_server

    def test_winner_is_returner(self, test_game:Game, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 4)
        assert test_game.winner() == test_returner

    def test_score_deuce(self, test_game:Game, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 3)
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 3)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, "D", "D")

    def test_score_deuce_long_game(self, test_game:Game, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 3)
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 4)
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 2)
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 1)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, "D", "D")

    def test_score_advantage_server(self, test_game:Game, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 3)
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 4)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, "A", 40)

    def test_score_advantage_retruner(self, test_game:Game, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 3)
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 4)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, 40, "A")

    def test_score_advantage_long_game(self, test_game:Game, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 3)
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 4)
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 2)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, "A", 40)

    def test_score_15_30(self, test_game:Game, test_server:Player, test_returner:Player):
        test_game.rallyPointFor(test_server)
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 2)
        assert test_game.score() == ScorerTestHelper.format_score_game(self.SERVER_NAME, self.RETURNER_NAME, 15, 30)

    def test_score_is_none_on_terminated_game(self, test_game:Game, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_returner, 4)
        assert test_game.score() is None

    def test_error_score_on_terminated_game(self, test_game:Game, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_game, test_server, 4)
        #terminated
        with pytest.raises(ValueError):
            test_game.rallyPointFor(test_returner)
