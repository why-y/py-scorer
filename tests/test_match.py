import unittest
import scorer

from scorer.match import Match
from scorer.player import Player
from tests.helper import Helper


class TestMatch(unittest.TestCase):

    SERVER = Player("Tom")
    RETURNER = Player("Eric")

    def setUp(self) -> None:
        self.match = Match(TestMatch.SERVER, TestMatch.RETURNER)

    def test_start_match_server_is_tom(self):
        self.assertEqual(self.match.server, TestMatch.SERVER)

    def test_start_match_returner_is_eric(self):
        self.assertEqual(self.match.returner, TestMatch.RETURNER)

    def test_new_match_is_not_over(self):
        self.assertFalse(self.match.isOver())

    def test_2_0_is_over(self):
        Helper.scoreXtimesServer(self.match, 2*Helper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertTrue(self.match.isOver())

    def test_2_1_winner_is_tom(self):
        Helper.scoreXtimesReturner(self.match, 1*Helper.NO_OF_RALLIES_TO_WIN_SET)
        Helper.scoreXtimesServer(self.match, 2*Helper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertTrue(self.match.isOver())

    def test_cannot_score_terminated_match(self):
        Helper.scoreXtimesServer(self.match, 2*Helper.NO_OF_RALLIES_TO_WIN_SET)
        #terminated
        with self.assertRaises(ValueError):
            self.match.rallyForServer()

    def test_1_1_is_not_over(self):
        Helper.scoreXtimesReturner(self.match, Helper.NO_OF_RALLIES_TO_WIN_SET)
        Helper.scoreXtimesServer(self.match, Helper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertFalse(self.match.isOver())

    def test_2_1_is_over(self):
        Helper.scoreXtimesReturner(self.match, Helper.NO_OF_RALLIES_TO_WIN_SET)
        Helper.scoreXtimesServer(self.match, 2*Helper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertTrue(self.match.isOver())

if __name__ == '__main__':
    unittest.main()
