import logging
from scorer.player import Player
from scorer.set import Set
from scorer.game import Game

logging.basicConfig(level=logging.DEBUG)

class Match:
    '''A class to score a tennis match'''

    def __init__(self, server: Player, returner: Player) -> None:
        self.server = server
        self.returner = returner
        self.sets = []
        self.bestOf = 3

    def score(self):
        score = {}
        setCounter = 0
        for set in self.sets:
            setCounter+=1
            setKey = Set.SET_KEY + str(setCounter)
            score.update({setKey:set.score().get(Set.SET_KEY)})
            score.update({Game.GAME_KEY:set.score().get(Game.GAME_KEY)})
        return score

    def rallyForServer(self) -> None:
        
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated match!")
        
        if not (self.__hasRunningSet()):
            self.sets.append(Set(self.server, self.returner))

        self.__getRunningSet().rallyForServer()
 
    def rallyForReturner(self) -> None:
        
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated match!")
        
        if not (self.__hasRunningSet()):
            self.sets.append(Set(self.server, self.returner))

        self.__getRunningSet().rallyForReturner()

    def isOver(self):
        if(self.__hasRunningSet()):
            return False
        else:
            serverSets = Match.__getNoOfSetsWonBy(self.sets, self.server)
            returnerSets = Match.__getNoOfSetsWonBy(self.sets, self.returner)
            return True if \
                (serverSets > self.bestOf/2 or returnerSets > self.bestOf/2) \
                 else False

    def winner(self):
        if(self.isOver()):
            serverSets = Match.__getNoOfSetsWonBy(self.sets, self.server)
            returnerSets = Match.__getNoOfSetsWonBy(self.sets, self.returner)
            return self.server if serverSets>returnerSets else self.returner
        else:
            return None           

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


