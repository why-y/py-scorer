import unittest
import scorer

from scorer.set import Set
from scorer.player import Player
from tests.scorer_test_helper import ScorerTestHelper

class TestSet(unittest.TestCase):

    SERVER = Player("Tom")
    RETURNER = Player("Eric")

    def setUp(self) -> None:
        self.testSet = Set(TestSet.SERVER, TestSet.RETURNER)

    def test_start_set_server_is_tom(self):
        self.assertEqual(self.testSet.server, TestSet.SERVER)  
    
    def test_start_set_returner_is_eric(self):
        self.assertEqual(self.testSet.returner, TestSet.RETURNER)  
    
    def test_new_set_is_not_over(self):
        self.assertFalse(self.testSet.isOver())

    def test_6_0_is_over(self):
        ScorerTestHelper.scoreXtimesServer(self.testSet, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertTrue(self.testSet.isOver())

    def test_6_0_winner_is_Tom(self):
        ScorerTestHelper.scoreXtimesServer(self.testSet, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertEqual(self.testSet.winner(), self.SERVER)

    def test_cannot_score_terminated_set(self):
        ScorerTestHelper.scoreXtimesServer(self.testSet, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        #terminated
        with self.assertRaises(ValueError):
            self.testSet.rallyForServer()

    def test_6_5_is_not_over(self):
        ScorerTestHelper.scoreXtimesReturner(self.testSet, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesServer(self.testSet, 6*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        self.assertFalse(self.testSet.isOver())

    def test_5_7_is_over(self):
        ScorerTestHelper.scoreXtimesReturner(self.testSet, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesServer(self.testSet, 7*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        self.assertTrue(self.testSet.isOver())

    def test_7_6_is_not_over(self):
        ScorerTestHelper.scoreXtimesServer(self.testSet, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesReturner(self.testSet, 6*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesServer(self.testSet, 2*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        self.assertFalse(self.testSet.isOver())

    def test_start_set_score_0_0(self):
        self.assertEqual(self.testSet.score(), TestSet.__format_score((0, 0),(0,0)))

    def test_score_1_0(self):
        ScorerTestHelper.scoreXtimesServer(self.testSet, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        self.assertEqual(self.testSet.score(), TestSet.__format_score((1, 0),(0,0)))

    @classmethod
    def __format_score(cls, set_score, game_score):
        return {
            ScorerTestHelper.SET_KEY:set_score,
            ScorerTestHelper.GAME_KEY:game_score
        }



if __name__ == '__main__':
    unittest.main()
