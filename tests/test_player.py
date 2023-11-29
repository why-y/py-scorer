import pytest
import scorer

from scorer.player import Player

class TestPlayer:

    NAME = "Paul"

    # Arrange
    @pytest.fixture
    def test_player(self) -> Player:
        return Player(self.NAME)

    def test_init_name(self, test_player:Player):
        assert test_player.name == self.NAME
