import unittest
import scorer

from scorer.set import Set
from scorer.player import Player
from tests.scorer_test_helper import ScorerTestHelper

class TestSet(unittest.TestCase):

    SERVER = Player("Tom")
    RETURNER = Player("Eric")

    def setUp(self) -> None:
        self.testLongSet = Set(TestSet.SERVER, TestSet.RETURNER, False)

    def test_start_set_server_is_tom(self):
        self.assertEqual(self.testLongSet.server, TestSet.SERVER)  
    
    def test_start_set_returner_is_eric(self):
        self.assertEqual(self.testLongSet.returner, TestSet.RETURNER)  
    
    def test_new_set_is_not_over(self):
        self.assertFalse(self.testLongSet.isOver())

    def test_6_0_is_over(self):
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertTrue(self.testLongSet.isOver())

    def test_6_0_winner_is_Tom(self):
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertEqual(self.testLongSet.winner(), self.testLongSet.server)

    def test_cannot_score_terminated_set(self):
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        #terminated
        with self.assertRaises(ValueError):
            self.testLongSet.rallyPointFor(TestSet.SERVER)

    def test_6_5_is_not_over(self):
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.RETURNER, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.SERVER, 6*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        self.assertFalse(self.testLongSet.isOver())

    def test_5_7_is_over(self):
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.RETURNER, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.SERVER, 7*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        self.assertTrue(self.testLongSet.isOver())

    def test_7_6_is_not_over(self):
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.SERVER, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.RETURNER, 6*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.SERVER, 2*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        self.assertFalse(self.testLongSet.isOver())

    def test_start_set_score_0_0(self):
        self.assertEqual(self.testLongSet.score(), TestSet.__format_set_game((0, 0),(0,0)))

    def test_score_1_0(self):
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        self.assertEqual(self.testLongSet.score(), TestSet.__format_set_game((1, 0), (0, 0)))
    
    # Tiebreak tests
    def test_longset_has_no_tiebreak(self):
        self.assertFalse(self.testLongSet.has_tiebreak())

    def test_defaultset_has_tiebreak(self):
        testSet = Set(TestSet.SERVER, TestSet.RETURNER)
        self.assertTrue(testSet.has_tiebreak())
        
    def test_start_tiebreak_at_6_6(self):
        testSet = Set(TestSet.SERVER, TestSet.RETURNER)
        ScorerTestHelper.scoreXtimesFor(testSet, TestSet.RETURNER, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(testSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(testSet, TestSet.RETURNER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> next rally in tiebreak
        testSet.rallyPointFor(TestSet.SERVER)
        self.assertEqual(testSet.score(), TestSet.__format_set_tiebreak((6, 6), (1,0)))

    @classmethod
    def __format_set_game(cls, set_score, game_score):
        return {
            ScorerTestHelper.SET_KEY:set_score,
            ScorerTestHelper.GAME_KEY:game_score
        }

    @classmethod
    def __format_set_tiebreak(cls, set_score, tiebreak_score):
        return {
            ScorerTestHelper.SET_KEY:set_score,
            ScorerTestHelper.TIEBREAK_KEY:tiebreak_score
        }



if __name__ == '__main__':
    unittest.main()
