import pytest
import scorer

from scorer.player import Player

class TestPlayer:

    NAME = "Paul"
    player = Player(NAME)

    def test_init_name(self):
        initialName = self.player.name
        assert initialName == self.NAME
