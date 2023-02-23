import logging
from scorer.player import Player
from scorer.set import Set

logging.basicConfig(level=logging.DEBUG)

class Match:
    '''A class to score a tennis match'''

    def __init__(self, server: Player, returner: Player) -> None:
        self.server = server
        self.returner = returner
        self.sets = []
        self.bestOf = 3

    def isOver(self):
        if(self.__hasRunningSet()):
            return False
        else:
            serverSets = Match.__getNoOfSetsWonBy(self.sets, self.server)
            returnerSets = Match.__getNoOfSetsWonBy(self.sets, self.returner)
            return True if \
                (serverSets >= self.bestOf or returnerSets >= self.bestOf) \
                 else False

    def __getRunningSet(self) -> Set:
        return None if len(self.sets)==0 or self.sets[-1].isOver() else self.sets[-1]

    def __hasRunningSet(self) -> Set:
        return False if self.__getRunningSet() is None else True

    @classmethod
    def __getNoOfSetsWonBy(cls, allSets, player: Player) -> int:
        noOfSetsWon = 0
        for set in allSets:
            if set.winner() == player:
                noOfSetsWon += 1
        return noOfSetsWon


