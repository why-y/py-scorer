import unittest
import scorer

from scorer.match import Match
from scorer.player import Player

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

if __name__ == '__main__':
    unittest.main()
