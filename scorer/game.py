import scorer.scorer_helper as Helper
from scorer.player import Player

class Game:
    '''A class to score a tennis game'''

    KEY = "Game"

    def __init__(self, server: Player, returner: Player) -> None:
        self.server = server
        self.returner = returner
        self.rallyPoints = {server:0, returner:0}

    def score(self):            
        serverScore = self.__ralliesToScore(self.__getServerRallyPoints(), self.__getReturnerRallyPoints())
        returnerScore = self.__ralliesToScore(self.__getReturnerRallyPoints(), self.__getServerRallyPoints())
        if(self.isOver()):
            serverScore = "W" if self.winner() is self.server else ""
            returnerScore = "W" if self.winner() is self.returner else ""
        return {
            Game.KEY : {
                self.server.name : serverScore, 
                self.returner.name : returnerScore
            }
        }

    def rallyPointFor(self, player:Player) -> None:
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated game!")
        self.rallyPoints[player] += 1

    def isOver(self):
        return max(self.rallyPoints.values())>3 and Helper.twoAppart(self.__getServerRallyPoints(), self.__getReturnerRallyPoints())

    def winner(self):
        return self.__leadingPlayer() if self.isOver() else None

    def __leadingPlayer(self) -> Player:
        return self.server if self.__getServerRallyPoints() > self.__getReturnerRallyPoints() else self.returner
    
    def __getServerRallyPoints(self) -> int:
        serverRallyPoints = self.rallyPoints.get(self.server)
        if serverRallyPoints is None:
            raise LookupError("cannot find rally points for player: " + self.server.name)
        return serverRallyPoints

    def __getReturnerRallyPoints(self) -> int:
        returnerRallyPoints = self.rallyPoints.get(self.returner)
        if returnerRallyPoints is None:
            raise LookupError("cannot find rally points for player: " + self.returner.name)
        return returnerRallyPoints


    @classmethod
    def __ralliesToScore(cls, points, opponentPoints) -> str:
        if(points < 3):  
            # 0 is 0, 1 is 15, 2 is 30
            return str(points * 15)
        elif(points == opponentPoints):
            # >2 and equal is deuce
            return "D"
        elif(points == 3 or points < opponentPoints):
            # 3 is 40, A for opponent is 40
            return "40"
        else:
            return "A"


