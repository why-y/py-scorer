import unittest
import scorer

from scorer.player import Player

class TestPlayer(unittest.TestCase):

    NAME = "Paul"

    def setUp(self) -> None:
        self.player = Player(TestPlayer.NAME)

    def test_init_name(self):
        initialName = self.player.name
        self.assertEqual(initialName, TestPlayer.NAME)

if __name__ == '__main__':
    unittest.main()
