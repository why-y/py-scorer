from scorer.player import Player

class Game:
    '''A class to score a tennis game'''

    GAME_KEY = "Game"

    def __init__(self, server: Player, returner: Player) -> None:
        self.server = server
        self.returner = returner
        self.serverRallyPoints = 0
        self.returnerRallyPoints = 0

    def score(self):
        if(self.isOver()):
            return None
        else:
            serverScore = self.__ralliesToScore(self.serverRallyPoints, self.returnerRallyPoints)
            returnerScore = self.__ralliesToScore(self.returnerRallyPoints, self.serverRallyPoints)
            return {Game.GAME_KEY : (serverScore, returnerScore)}

    def rallyForServer(self) -> None:
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated game!")
        self.serverRallyPoints+=1
        
    def rallyForReturner(self) -> None:
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated game!")
        self.returnerRallyPoints+=1

    def isOver(self):
        return (self.serverRallyPoints>3 and Game.__twoPointsAhead(self.serverRallyPoints, self.returnerRallyPoints) or
            self.returnerRallyPoints>3 and Game.__twoPointsAhead(self.returnerRallyPoints, self.serverRallyPoints))

    def winner(self):
        if(self.isOver()):
            return self.server if self.serverRallyPoints>self.returnerRallyPoints else self.returner
        else:
            return None

    @classmethod
    def __twoPointsAhead(cls, points, opponentPoints):
        return points > opponentPoints + 1

    @classmethod
    def __ralliesToScore(cls, points, opponentPoints):
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


