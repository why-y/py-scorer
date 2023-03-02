import unittest
import scorer

from scorer.game import Game
from scorer.player import Player
from tests.scorer_test_helper import ScorerTestHelper


class TestGame(unittest.TestCase):

    SERVER = Player("Tom")
    RETURNER = Player("Eric")

    def setUp(self) -> None:
        self.testGame = Game(TestGame.SERVER, TestGame.RETURNER)

    def test_start_game_server_is_tom(self):
        self.assertEqual(self.testGame.server, TestGame.SERVER)  
    
    def test_start_game_returner_is_eric(self):
        self.assertEqual(self.testGame.returner, TestGame.RETURNER)  
    
    def test_game_over(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER,3)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 4)
        self.assertFalse(self.testGame.isOver())
        self.testGame.rallyPointFor(self.SERVER)
        self.assertTrue(self.testGame.isOver())

    def test_winner_is_none(self):
        self.testGame.rallyPointFor(self.SERVER)
        self.testGame.rallyPointFor(self.RETURNER)
        self.assertIsNone(self.testGame.winner())

    def test_start_game_score_love_all(self):
        self.assertEqual(self.testGame.score(), TestGame.__format_score((0, 0)))

    def test_score_15_0(self):
        self.testGame.rallyPointFor(self.SERVER)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((15, 0)))

    def test_score_15_all(self):
        self.testGame.rallyPointFor(self.SERVER)
        self.testGame.rallyPointFor(self.RETURNER)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((15, 15)))

    def test_score_15_30(self):
        self.testGame.rallyPointFor(self.SERVER)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 2)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((15, 30)))

    def test_score_30_all(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 2)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 2)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((30, 30)))

    def test_score_40_30(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 2)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 3)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((40, 30)))

    def test_winner_is_server(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 4)
        self.assertEqual(self.testGame.winner(), TestGame.SERVER)

    def test_winner_is_returner(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 4)
        self.assertEqual(self.testGame.winner(), TestGame.RETURNER)

    def test_score_deuce(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 3)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 3)
        self.assertEqual(self.testGame.score(), TestGame.__format_score(("D", "D")))

    def test_score_deuce_long_game(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 3)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 4)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 2)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 1)
        self.assertEqual(self.testGame.score(), TestGame.__format_score(("D", "D")))

    def test_score_advantage_server(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 3)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 4)
        self.assertEqual(self.testGame.score(), TestGame.__format_score(("A", 40)))

    def test_score_advantage_retruner(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 3)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 4)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((40, "A")))

    def test_score_advantage_long_game(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 3)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 4)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 2)
        self.assertEqual(self.testGame.score(), TestGame.__format_score(("A", 40)))

    def test_score_15_30(self):
        self.testGame.rallyPointFor(self.SERVER)
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 2)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((15, 30)))

    def test_score_is_none_on_terminated_game(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.RETURNER, 4)
        self.assertIsNone(self.testGame.score())

    def test_error_score_on_terminated_game(self):
        ScorerTestHelper.scoreXtimesFor(self.testGame, TestGame.SERVER, 4)
        #terminated
        with self.assertRaises(ValueError):
            self.testGame.rallyPointFor(self.RETURNER)

    @classmethod
    def __format_score(cls, score):
        return {ScorerTestHelper.GAME_KEY:score}

if __name__ == '__main__':
    unittest.main()
