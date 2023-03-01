import unittest
import scorer

from scorer.tiebreak import Tiebreak
from scorer.player import Player
from tests.scorer_test_helper import ScorerTestHelper


class TestTiebreak(unittest.TestCase):

    SERVER = Player("Tom")
    RETURNER = Player("Eric")

    def setUp(self) -> None:
        self.testTiebreak = Tiebreak(TestTiebreak.SERVER, TestTiebreak.RETURNER)

    def test_start_tiebreak_server_is_tom(self):
        self.assertEqual(self.testTiebreak.server, TestTiebreak.SERVER)

    def test_start_tiebreak_returner_is_eric(self):
        self.assertEqual(self.testTiebreak.returner, TestTiebreak.RETURNER)  

    def test_new_tiebreak_not_over(self):
        self.assertFalse(self.testTiebreak.isOver())

#    def test_winner_is_none(self):
#        self.assertIsNone(self.testGame.winner())


if __name__ == '__main__':
    unittest.main()
