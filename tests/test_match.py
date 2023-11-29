import pytest
import scorer

from scorer.match import Match
from scorer.player import Player
from tests.scorer_test_helper import ScorerTestHelper


class TestMatch:

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
    def test_default_match(self, test_server:Player, test_returner:Player) -> Match:
        return Match(test_server, test_returner)
    
    @pytest.fixture
    def test_bestof_five_match(self, test_server:Player, test_returner:Player) -> Match:
        return Match(test_server, test_returner, 5)
    
    def test_start_match_server_is_tom(self, test_default_match:Match):
        assert test_default_match.server.name == self.SERVER_NAME

    def test_start_match_returner_is_eric(self, test_default_match:Match):
        assert test_default_match.returner.name == self.RETURNER_NAME

    def test_new_match_is_not_over(self, test_default_match:Match):
        assert not test_default_match.isOver()

    def test_2_0_is_over(self, test_default_match:Match, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, 2*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        assert test_default_match.isOver()

    def test_2_0_winner_is_Tom(self, test_default_match:Match, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, 2*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        assert test_default_match.winner().name == self.SERVER_NAME
    
    def test_2_0_is_not_over_on_best_of_five(self, test_bestof_five_match:Match, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_bestof_five_match, test_server, 2*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        assert not test_bestof_five_match.isOver()

    def test_3_0_is_over_on_best_of_five(self, test_bestof_five_match:Match, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_bestof_five_match, test_server, 3*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        assert test_bestof_five_match.isOver()

    def test_2_1_winner_is_tom(self, test_default_match:Match, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, 2*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        assert test_default_match.winner().name == self.SERVER_NAME

    def test_cannot_score_terminated_match(self, test_default_match:Match, test_server:Player):
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, 2*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        #terminated
        with pytest.raises(ValueError):
            test_default_match.rallyPointFor(test_server)

    def test_1_1_is_not_over(self, test_default_match:Match, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        assert not test_default_match.isOver()

    def test_2_1_is_over(self, test_default_match:Match, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, 2*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        assert test_default_match.isOver()
   
    def test_score_6_0__0_6__4_3__15_30(self, test_default_match:Match, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, 4*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_returner, 3*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, 1)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_returner, 2)

        assert test_default_match.score() ==  {
                "Set1":{
                    self.SERVER_NAME: 6,
                    self.RETURNER_NAME: 0
                },
                "Set2":{
                    self.SERVER_NAME: 0,
                    self.RETURNER_NAME: 6
                },
                "Set3":{
                    self.SERVER_NAME: 4,
                    self.RETURNER_NAME: 3,
                    ScorerTestHelper.GAME_KEY: {
                        self.SERVER_NAME: 15,
                        self.RETURNER_NAME: 30                     
                    }
                }
            }
        
    def test_score_set_after_tiebreak_7_6__3_1(self, test_default_match:Match, test_server:Player, test_returner:Player):
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> tiebreak
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        # 7:6 -> next set
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_server, 3*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(test_default_match, test_returner, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 7:6, 3:1 -> check
        assert test_default_match.score() ==  {
                "Set1":{
                    self.SERVER_NAME: 7,
                    self.RETURNER_NAME: 6,
                    ScorerTestHelper.TIEBREAK_KEY: {
                        self.SERVER_NAME: 7,
                        self.RETURNER_NAME: 0,    
                    }
                },
                "Set2":{
                    self.SERVER_NAME: 3,
                    self.RETURNER_NAME: 1,
                    ScorerTestHelper.GAME_KEY: {
                        self.SERVER_NAME: 0,
                        self.RETURNER_NAME: 0                     
                    }
                }
            }
