import unittest
import scorer

from scorer.match import Match
from scorer.player import Player
from tests.helper import Helper


class TestMatch(unittest.TestCase):

    SERVER = Player("Tom")
    RETURNER = Player("Eric")

    def setUp(self) -> None:
        self.testMatch = Match(TestMatch.SERVER, TestMatch.RETURNER)

    def test_start_match_server_is_tom(self):
        self.assertEqual(self.testMatch.server, TestMatch.SERVER)

    def test_start_match_returner_is_eric(self):
        self.assertEqual(self.testMatch.returner, TestMatch.RETURNER)

    def test_new_match_is_not_over(self):
        self.assertFalse(self.testMatch.isOver())

    def test_2_0_is_over(self):
        Helper.scoreXtimesServer(self.testMatch, 2*Helper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertTrue(self.testMatch.isOver())

    def test_2_1_winner_is_tom(self):
        Helper.scoreXtimesReturner(self.testMatch, 1*Helper.NO_OF_RALLIES_TO_WIN_SET)
        Helper.scoreXtimesServer(self.testMatch, 2*Helper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertTrue(self.testMatch.isOver())

    def test_cannot_score_terminated_match(self):
        Helper.scoreXtimesServer(self.testMatch, 2*Helper.NO_OF_RALLIES_TO_WIN_SET)
        #terminated
        with self.assertRaises(ValueError):
            self.testMatch.rallyForServer()

    def test_1_1_is_not_over(self):
        Helper.scoreXtimesReturner(self.testMatch, Helper.NO_OF_RALLIES_TO_WIN_SET)
        Helper.scoreXtimesServer(self.testMatch, Helper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertFalse(self.testMatch.isOver())

    def test_2_1_is_over(self):
        Helper.scoreXtimesReturner(self.testMatch, Helper.NO_OF_RALLIES_TO_WIN_SET)
        Helper.scoreXtimesServer(self.testMatch, 2*Helper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertTrue(self.testMatch.isOver())

    def test_6_0__6_0_winner_is_Tom(self):
        Helper.scoreXtimesServer(self.testMatch, 2*Helper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertEqual(self.testMatch.winner(), self.SERVER)
    
    def test_score_6_0__0_6__4_3__15_30(self):
        Helper.scoreXtimesServer(self.testMatch, Helper.NO_OF_RALLIES_TO_WIN_SET)
        Helper.scoreXtimesReturner(self.testMatch, Helper.NO_OF_RALLIES_TO_WIN_SET)
        Helper.scoreXtimesServer(self.testMatch, 4*Helper.NO_OF_RALLIES_TO_WIN_GAME)
        Helper.scoreXtimesReturner(self.testMatch, 3*Helper.NO_OF_RALLIES_TO_WIN_GAME)
        Helper.scoreXtimesServer(self.testMatch, 1)
        Helper.scoreXtimesReturner(self.testMatch, 2)
        self.assertEqual(
            {
                "Set1":(6,0),
                "Set2":(0,6),
                "Set3":(4,3),
                "Game":(15,30)            
            }, self.testMatch.score())

if __name__ == '__main__':
    unittest.main()
