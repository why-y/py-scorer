import pytest
import scorer

from scorer.tiebreak import Tiebreak
from scorer.player import Player
from tests.scorer_test_helper import ScorerTestHelper


class TestTiebreak:

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
    def test_tiebreak(self, test_server:Player, test_returner:Player) -> Tiebreak:
        return Tiebreak(test_server, test_returner)

    def test_start_tiebreak_server_is_tom(self, test_tiebreak:Tiebreak):
        assert test_tiebreak.server.name == self.SERVER_NAME

    def test_start_tiebreak_returner_is_eric(self, test_tiebreak:Tiebreak):
        assert test_tiebreak.returner.name == self.RETURNER_NAME

    def test_new_tiebreak_not_over(self, test_tiebreak:Tiebreak):
        assert not test_tiebreak.isOver()

    def test_winner_is_none(self, test_tiebreak:Tiebreak):
        assert test_tiebreak.winner() is None

    def test_6_0_is_not_over(self, test_tiebreak:Tiebreak, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_tiebreak, test_server, 6)
        assert not test_tiebreak.isOver()

    def test_7_0_is_over(self, test_tiebreak:Tiebreak, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_tiebreak, test_server, 7)
        assert test_tiebreak.isOver()

    def test_7_6_is_not_over(self, test_tiebreak:Tiebreak, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_tiebreak, test_returner, 6)
        ScorerTestHelper.scoreXtimesFor(test_tiebreak, test_server, 7)
        assert not test_tiebreak.isOver()

    def test_7_0_winner_is_Tom(self, test_tiebreak:Tiebreak, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_tiebreak, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        assert test_tiebreak.winner() == test_server
   
    def test_cannot_score_terminated_tiebreak(self, test_tiebreak:Tiebreak, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_tiebreak, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        #terminated
        with pytest.raises(ValueError):
            test_tiebreak.rallyPointFor(test_server)

    def test_start_tiebreak_score_0_0(self, test_tiebreak:Tiebreak):
        assert test_tiebreak.score() == ScorerTestHelper.format_score_tiebreak(self.SERVER_NAME, self.RETURNER_NAME, 0, 0)

    def test_score_1_0(self, test_tiebreak:Tiebreak, test_server:Player):
        test_tiebreak.rallyPointFor(test_server)
        assert test_tiebreak.score() == ScorerTestHelper.format_score_tiebreak(self.SERVER_NAME, self.RETURNER_NAME, 1, 0)

