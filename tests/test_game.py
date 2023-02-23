import unittest
import scorer

from scorer.game import Game
from scorer.player import Player
from tests.helper import Helper


class TestGame(unittest.TestCase):

    SERVER = Player("Tom")
    RETURNER = Player("Eric")

    def setUp(self) -> None:
        self.testGame = Game(TestGame.SERVER, TestGame.RETURNER)

    def test_start_game_server_is_tom(self):
        self.assertEqual(self.testGame.server, TestGame.SERVER)  
    
    def test_start_game_returner_is_eric(self):
        self.assertEqual(self.testGame.returner, TestGame.RETURNER)  
    
    def test_start_game_score_love_all(self):
        self.assertEqual(self.testGame.score(), TestGame.__format_score((0, 0)))

    def test_score_15_0(self):
        self.testGame.rallyForServer()
        self.assertEqual(self.testGame.score(), TestGame.__format_score((15, 0)))

    def test_score_15_all(self):
        self.testGame.rallyForServer()
        self.testGame.rallyForReturner()
        self.assertEqual(self.testGame.score(), TestGame.__format_score((15, 15)))

    def test_score_15_30(self):
        self.testGame.rallyForServer()
        Helper.scoreXtimesReturner(self.testGame, 2)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((15, 30)))

    def test_score_30_all(self):
        Helper.scoreXtimesServer(self.testGame, 2)
        Helper.scoreXtimesReturner(self.testGame, 2)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((30, 30)))

    def test_score_40_30(self):
        Helper.scoreXtimesReturner(self.testGame, 2)
        Helper.scoreXtimesServer(self.testGame, 3)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((40, 30)))

    def test_game_over(self):
        Helper.scoreXtimesReturner(self.testGame, 3)
        Helper.scoreXtimesServer(self.testGame, 4)
        self.assertFalse(self.testGame.isOver())
        self.testGame.rallyForServer()
        self.assertTrue(self.testGame.isOver())

    def test_winner_is_none(self):
        self.testGame.rallyForServer()
        self.testGame.rallyForReturner()
        self.assertIsNone(self.testGame.winner())

    def test_winner_is_server(self):
        Helper.scoreXtimesServer(self.testGame, 4)
        self.assertEqual(self.testGame.winner(), TestGame.SERVER)

    def test_winner_is_returner(self):
        Helper.scoreXtimesReturner(self.testGame, 4)
        self.assertEqual(self.testGame.winner(), TestGame.RETURNER)

    def test_score_deuce(self):
        Helper.scoreXtimesServer(self.testGame, 3)
        Helper.scoreXtimesReturner(self.testGame, 3)
        self.assertEqual(self.testGame.score(), TestGame.__format_score(("D", "D")))

    def test_score_advantage_server(self):
        Helper.scoreXtimesReturner(self.testGame, 3)
        Helper.scoreXtimesServer(self.testGame, 4)
        self.assertEqual(self.testGame.score(), TestGame.__format_score(("A", 40)))

    def test_score_advantage_retruner(self):
        Helper.scoreXtimesServer(self.testGame, 3)
        Helper.scoreXtimesReturner(self.testGame, 4)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((40, "A")))

    def test_score_15_30(self):
        self.testGame.rallyForServer()
        Helper.scoreXtimesReturner(self.testGame, 2)
        self.assertEqual(self.testGame.score(), TestGame.__format_score((15, 30)))

    def test_score_is_none_on_terminated_game(self):
        Helper.scoreXtimesReturner(self.testGame, 4)
        self.assertIsNone(self.testGame.score())

    def test_error_score_on_terminated_game(self):
        Helper.scoreXtimesServer(self.testGame, 4)
        #terminated
        with self.assertRaises(ValueError):
            self.testGame.rallyForReturner()

    @classmethod
    def __format_score(cls, score):
        return {Helper.GAME_KEY:score}

if __name__ == '__main__':
    unittest.main()
