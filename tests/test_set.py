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
        self.testLongSet = Set(TestSet.SERVER, TestSet.RETURNER, False)

    def test_start_set_server_is_server(self):
        self.assertEqual(self.testLongSet.server, TestSet.SERVER)  
    
    def test_start_set_returner_is_returner(self):
        self.assertEqual(self.testLongSet.returner, TestSet.RETURNER)  
    
    def test_new_set_is_not_over(self):
        self.assertFalse(self.testLongSet.isOver())

    def test_6_0_is_over(self):
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        self.assertTrue(self.testLongSet.isOver())

    def test_6_0_winner_is_server(self):
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
        self.assertEqual(self.testLongSet.score(), {
            ScorerTestHelper.SET_KEY:{
                TestSet.SERVER.name: 0,
                TestSet.RETURNER.name: 0,
                ScorerTestHelper.GAME_KEY: {
                    TestSet.SERVER.name: 0,
                    TestSet.RETURNER.name: 0
                }
            }
        })

    def test_score_1_0(self):
        ScorerTestHelper.scoreXtimesFor(self.testLongSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        self.assertEqual(self.testLongSet.score(), {
            ScorerTestHelper.SET_KEY:{
                TestSet.SERVER.name: 1,
                TestSet.RETURNER.name: 0,
                ScorerTestHelper.GAME_KEY: {
                    TestSet.SERVER.name: 0,
                    TestSet.RETURNER.name: 0
                }
            }
        })
    
    # Tiebreak tests
    def test_longset_has_no_tiebreak(self):
        self.assertFalse(self.testLongSet.has_tiebreak())

    def test_defaultset_has_tiebreak(self):
        self.assertTrue(self.testSet.has_tiebreak())
        
    def test_start_tiebreak_at_6_6(self):
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.RETURNER, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.RETURNER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> next rally in tiebreak
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.SERVER, 1)
        self.assertEqual(self.testSet.score(), {
            ScorerTestHelper.SET_KEY:{
                TestSet.SERVER.name: 6,
                TestSet.RETURNER.name: 6,
                ScorerTestHelper.TIEBREAK_KEY: {
                    TestSet.SERVER.name: 1,
                    TestSet.RETURNER.name: 0
                }
            }
        })
            
    def test_tiebreak_set_7_6__7_0_is_over(self):
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.RETURNER, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.RETURNER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> next rally in tiebreak
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        # 6:6 (7:0) -> set is over
        self.assertTrue(self.testSet.isOver())

    def test_tiebreak_set_7_6__7_0_is_winner_is_server(self):
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.RETURNER, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.RETURNER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> next rally in tiebreak
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        # 7:6 (7:0) -> winner is server
        self.assertEqual(self.testSet.winner().name, TestSet.SERVER.name)

    def test_tiebreak_result_7_6__7_0(self):
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.RETURNER, 5*ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_SET)
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.RETURNER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_GAME)
        # 6:6 -> next rally in tiebreak
        ScorerTestHelper.scoreXtimesFor(self.testSet, TestSet.SERVER, ScorerTestHelper.NO_OF_RALLIES_TO_WIN_TIEBREAK)
        self.assertEqual(self.testSet.score(), {
            ScorerTestHelper.SET_KEY:{
                TestSet.SERVER.name: 7,
                TestSet.RETURNER.name: 6,
                ScorerTestHelper.TIEBREAK_KEY: {
                    TestSet.SERVER.name: 7,
                    TestSet.RETURNER.name: 0
                }
            }
        })


    @classmethod
    def __format_set_game(cls, set_score, game_score):
        return {
            ScorerTestHelper.SET_KEY:set_score,
            ScorerTestHelper.GAME_KEY:game_score
        }



if __name__ == '__main__':
    unittest.main()
