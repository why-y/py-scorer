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
        if(self.isOver()):
            return None
        else:
            serverScore = self.__ralliesToScore(self.__getServerRallyPoints(), self.__getReturnerRallyPoints())
            returnerScore = self.__ralliesToScore(self.__getReturnerRallyPoints(), self.__getServerRallyPoints())
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
        if(self.isOver()):
            return self.__leadingPlayer()
        else:
            return None

    def __leadingPlayer(self) -> Player:
        return self.server if self.__getServerRallyPoints() > self.__getReturnerRallyPoints() else self.returner
    
    def __getServerRallyPoints(self) -> int:
        return self.rallyPoints.get(self.server)

    def __getReturnerRallyPoints(self) -> int:
        return self.rallyPoints.get(self.returner)


    @classmethod
    def __ralliesToScore(cls, points, opponentPoints) -> str:
        if(points < 3):  
            # 0 is 0, 1 is 15, 2 is 30
            return points * 15
        elif(points == opponentPoints):
            # >2 and equal is deuce
            return "D"
        elif(points == 3 or points < opponentPoints):
            # 3 is 40, A for opponent is 40
            return 40
        else:
            return "A"


