
class Helper:
    '''A helper class for tennis scorer unit tests'''

    def __init__(self) -> None:
        pass

    @classmethod
    def scoreXtimesServer(cls, scoreUnit, noOfRallies):
        for _ in range(noOfRallies):
            scoreUnit.rallyForServer()

    @classmethod
    def scoreXtimesReturner(cls, scoreUnit, noOfRallies):
        for _ in range(noOfRallies):
            scoreUnit.rallyForReturner()

