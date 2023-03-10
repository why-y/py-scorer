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

    def test_winner_is_none(self):
        self.assertIsNone(self.testTiebreak.winner())

    def test_6_0_is_not_over(self):
        ScorerTestHelper.scoreXtimesFor(self.testTiebreak, TestTiebreak.SERVER, 6)
        self.assertFalse(self.testTiebreak.isOver())

    def test_7_0_is_over(self):
        ScorerTestHelper.scoreXtimesFor(self.testTiebreak, TestTiebreak.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        self.assertTrue(self.testTiebreak.isOver())

    def test_7_6_is_not_over(self):
        ScorerTestHelper.scoreXtimesFor(self.testTiebreak, TestTiebreak.RETURNER, 6)
        ScorerTestHelper.scoreXtimesFor(self.testTiebreak, TestTiebreak.SERVER, 7)
        self.assertFalse(self.testTiebreak.isOver())

    def test_7_0_winner_is_Tom(self):
        ScorerTestHelper.scoreXtimesFor(self.testTiebreak, TestTiebreak.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        self.assertEqual(self.testTiebreak.winner(), self.SERVER)

    def test_cannot_score_terminated_tiebreak(self):
        ScorerTestHelper.scoreXtimesFor(self.testTiebreak, TestTiebreak.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        #terminated
        with self.assertRaises(ValueError):
            self.testTiebreak.rallyPointFor(TestTiebreak.SERVER)

    def test_start_tiebreak_score_0_0(self):
        self.assertEqual(self.testTiebreak.score(), TestTiebreak.__format_score(self.testTiebreak.server, 0, self.testTiebreak.returner, 0))

    def test_score_1_0(self):
        self.testTiebreak.rallyPointFor(TestTiebreak.SERVER)
        self.assertEqual(self.testTiebreak.score(), TestTiebreak.__format_score(self.testTiebreak.server, 1, self.testTiebreak.returner, 0))

    @classmethod
    def __format_score(cls, server:Player, serverScore, returner:Player, returnerScore):
        return {
            ScorerTestHelper.TIEBREAK_KEY: {
                server.name: serverScore,
                returner.name: returnerScore
            }
        }   

if __name__ == '__main__':
    unittest.main()
