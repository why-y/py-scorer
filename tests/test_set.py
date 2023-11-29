import pytest
from loguru import logger
import scorer

from scorer.set import Set
from scorer.player import Player
from tests.scorer_test_helper import ScorerTestHelper

class TestSet:

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
    def test_set(self, test_server:Player, test_returner:Player) -> Set:
        return Set(test_server, test_returner)
    
    @pytest.fixture
    def test_long_set(self, test_server:Player, test_returner:Player) -> Set:
        return Set(test_server, test_returner, False)

    # Test    
    def test_start_set_server_is_server(self, test_long_set:Set, test_server:Player):
        assert test_long_set.server == test_server
    
    def test_start_set_returner_is_returner(self, test_long_set:Set, test_returner:Player):
        assert test_long_set.returner == test_returner
    
    def test_new_set_is_not_over(self, test_long_set:Set):
        assert not test_long_set.isOver()

    def test_6_0_is_over(self, test_long_set:Set, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        assert test_long_set.isOver()

    def test_6_0_winner_is_server(self, test_long_set:Set, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        assert test_long_set.winner() == test_server

    def test_cannot_score_terminated_set(self, test_long_set:Set, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        #terminated
        with pytest.raises(ValueError):
            test_long_set.rallyPointFor(test_long_set)

    def test_6_5_is_not_over(self, test_long_set:Set, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_returner, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_server, 6*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        assert not test_long_set.isOver()

    def test_5_7_is_over(self, test_long_set:Set, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_returner, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_server, 7*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        assert test_long_set.isOver()

    def test_7_6_is_not_over(self, test_long_set:Set, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_server, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_returner, 6*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_server, 2*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        assert not test_long_set.isOver()

    def test_start_set_score_0_0(self, test_long_set:Set):
        assert test_long_set.score() == ScorerTestHelper.format_score_set_and_game(self.SERVER_NAME, self.RETURNER_NAME, 0,0,0,0) 

    def test_score_1_0(self, test_long_set:Set, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_long_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        assert test_long_set.score() == ScorerTestHelper.format_score_set_and_game(self.SERVER_NAME, self.RETURNER_NAME, 1,0,0,0) 

    
    # Tiebreak tests
    def test_longset_has_no_tiebreak(self, test_long_set:Set):
        assert not test_long_set.has_tiebreak()

    def test_defaultset_has_tiebreak(self, test_set:Set):
        assert test_set.has_tiebreak()
        
    def test_start_tiebreak_at_6_6(self, test_set:Set, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_set, test_returner, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_set, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> next rally in tiebreak
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, 1)
        assert test_set.score() == ScorerTestHelper.format_score_set_and_tiebreak(self.SERVER_NAME, self.RETURNER_NAME, 6, 6, 1, 0)
            
    def test_tiebreak_set_7_6__7_0_is_over(self, test_set:Set, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_set, test_returner, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_set, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> next rally in tiebreak
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        # 6:6 (7:0) -> set is over
        assert test_set.isOver()

    def test_tiebreak_set_7_6__7_0_is_winner_is_server(self, test_set:Set, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_set, test_returner, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_set, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> next rally in tiebreak
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        # 7:6 (7:0) -> winner is server
        assert test_set.winner() == test_server

    def test_tiebreak_result_7_6__7_0(self, test_set:Set, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_set, test_returner, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_set, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> next rally in tiebreak
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        # 7:6 (7:0) -> verify score
        assert test_set.score() == ScorerTestHelper.format_score_set_and_tiebreak(self.SERVER_NAME, self.RETURNER_NAME, 7, 6, 7, 0)

    def test_has_been_decided_in_tiebreak(self, test_set:Set, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_set, test_returner, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_set, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> next rally in tiebreak
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        # 7:6 (7:0) -> set decided in tiebreak
        assert test_set.hasBeenDecidedInTiebreak()

    def test_has_not_been_decided_in_tiebreak(self, test_set:Set, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_set, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        # 6:0 -> set not decided in tiebreak
        assert not test_set.hasBeenDecidedInTiebreak()
