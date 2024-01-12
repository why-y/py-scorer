import logging
from scorer.player import Player
from scorer.set import Set
#from scorer.game import Game
#from scorer.tiebreak import Tiebreak

logging.basicConfig(level=logging.DEBUG)

class Match:
    '''A class to score a tennis match'''

    def __init__(self, server: Player, returner: Player, bestOf:int=3, withTiebreaks:bool=True) -> None:
        self.server = server
        self.returner = returner
        self.bestOf = bestOf
        self.withTiebreak = withTiebreaks
        self.sets = []
        self.sets.append(Set(server, returner, withTiebreaks))

    def score(self):
        score = {}
        setCounter = 0
        for set in self.sets:
            setCounter+=1
            setKey = Set.KEY + str(setCounter)
            score.update({setKey:set.score().get(Set.KEY)})
        return score

    def rallyPointFor(self, player:Player) -> None:
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated match!")
        self.__getRunningSet().rallyPointFor(player)
        if not self.isOver() and not self.__hasRunningSet(): self.sets.append(Set(self.server, self.returner, self.withTiebreak))

    def isOver(self):
        if(self.__hasRunningSet()):
            return False
        else:
            serverSets = Match.__getNoOfSetsWonBy(self.sets, self.server)
            returnerSets = Match.__getNoOfSetsWonBy(self.sets, self.returner)
            return True if \
                (serverSets > self.bestOf/2 or returnerSets > self.bestOf/2) \
                 else False

    def winner(self) -> Player:
        if(self.isOver()):
            serverSets = Match.__getNoOfSetsWonBy(self.sets, self.server)
            returnerSets = Match.__getNoOfSetsWonBy(self.sets, self.returner)
            return self.server if serverSets>returnerSets else self.returner
        else:
            raise ValueError("this Match has no winner since it's not over yet: ()".format(str(self.score())))    

    def __getRunningSet(self) -> Set:
        latestSet = self.sets[-1]
        if latestSet is None:
            raise ValueError("This Match has no running set: {}".format(str(self.score())))
        return latestSet 

    def __hasRunningSet(self) -> bool:
        latestSet = self.sets[-1]
        return True if latestSet is not None and not latestSet.isOver() else False

    @classmethod
    def __getNoOfSetsWonBy(cls, allSets, player: Player) -> int:
        noOfSetsWon = 0
        for set in allSets:
            if set.winner() == player:
                noOfSetsWon += 1
        return noOfSetsWon


