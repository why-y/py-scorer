import unittest
import scorer

from scorer.set import Set

class TestSet(unittest.TestCase):

    SERVER = "Tom"
    RETURNER = "Eric"

    def setUp(self) -> None:
        self.set = Set(TestSet.SERVER, TestSet.RETURNER)

    def test_start_set_server_is_tom(self):
        self.assertEqual(self.set.server, TestSet.SERVER)  
    
    def test_start_set_returner_is_eric(self):
        self.assertEqual(self.set.returner, TestSet.RETURNER)  
    
    def test_new_set_is_not_over(self):
        self.assertFalse(self.set.isOver())

    def test_6_0_is_over(self):
        TestSet.__scoreXtimesServer(self.set, 6)
        self.assertTrue(self.set.isOver())

    def test_cannot_score_terminated_set(self):
        TestSet.__scoreXtimesServer(self.set, 6)
        #terminated
        with self.assertRaises(ValueError):
            self.set.gameForServer()

    def test_6_5_is_not_over(self):
        TestSet.__scoreXtimesReturner(self.set, 5)
        TestSet.__scoreXtimesServer(self.set, 6)
        self.assertFalse(self.set.isOver())

    def test_5_7_is_over(self):
        TestSet.__scoreXtimesReturner(self.set, 5)
        TestSet.__scoreXtimesServer(self.set, 7)
        self.assertTrue(self.set.isOver())

    def test_7_6_is_not_over(self):
        TestSet.__scoreXtimesServer(self.set, 5)
        TestSet.__scoreXtimesReturner(self.set, 6)
        TestSet.__scoreXtimesServer(self.set, 2)
        self.assertFalse(self.set.isOver())

    def test_start_set_score_0_0(self):
        self.assertEqual(self.set.score(), (0, 0))

    def test_score_1_0(self):
        self.set.gameForServer()
        self.assertEqual(self.set.score(), (1, 0))

    @classmethod
    def __scoreXtimesServer(cls, set, noOfGames):
        for _ in range(noOfGames):
            set.gameForServer()

    @classmethod
    def __scoreXtimesReturner(cls, set, noOfGames):
        for _ in range(noOfGames):
            set.gameForReturner()

if __name__ == '__main__':
    unittest.main()
