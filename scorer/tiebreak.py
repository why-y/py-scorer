import scorer.scorer_helper as Helper
from scorer.player import Player

class Tiebreak:
    '''A class to score a tennis tiebreak'''

    KEY = "Tiebreak"

    def __init__(self, server: Player, returner: Player) -> None:
        self.server = server
        self.returner = returner
        self.rallyPoints = {server:0, returner:0}

    def score(self):
        return {
            Tiebreak.KEY : {
                self.server.name : self.__getServerRallyPoints(), 
                self.returner.name : self.__getReturnerRallyPoints()
            }
        }    

    def rallyPointFor(self, player:Player) -> None:
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated game!")
        self.rallyPoints[player] += 1

    def isOver(self):
        return max(self.rallyPoints.values()) > 6 and Helper.twoAppart(self.__getServerRallyPoints(), self.__getReturnerRallyPoints())

    def winner(self):
        return self.__leadingPlayer() if self.isOver() else None

    def __leadingPlayer(self) -> Player:
        return self.server if self.__getServerRallyPoints() > self.__getReturnerRallyPoints() else self.returner
    
    def __getServerRallyPoints(self) -> int:
        return self.rallyPoints.get(self.server)

    def __getReturnerRallyPoints(self) -> int:
        return self.rallyPoints.get(self.returner)



