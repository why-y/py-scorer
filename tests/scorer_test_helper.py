
class ScorerTestHelper:
    '''A helper class for tennis scorer unit tests'''

    NO_OF_RALLIES_TO_WIN_GAME = 4
    NO_OF_RALLIES_TO_WIN_TIEBREAK = 7
    NO_OF_RALLIES_TO_WIN_SET = 6 * NO_OF_RALLIES_TO_WIN_GAME
    SET_KEY = "Set"
    GAME_KEY = "Game"
    TIEBREAK_KEY = "Tiebreak"

    def __init__(self) -> None:
        pass

    @classmethod
    def scoreXtimesServer(cls, scoreUnit:int, noOfRallies:int):
        for _ in range(noOfRallies):
            scoreUnit.rallyForServer()

    @classmethod
    def scoreXtimesReturner(cls, scoreUnit:int, noOfRallies:int):
        for _ in range(noOfRallies):
            scoreUnit.rallyForReturner()

