import scorer.scorer_helper as Helper
from scorer.player import Player

class Tiebreak:
    '''A class to score a tennin tiebreak'''

    KEY = "Tiebreak"

    def __init__(self, server: Player, returner: Player) -> None:
        self.server = server
        self.returner = returner
        self.serverRallyPoints = 0
        self.returnerRallyPoints = 0

    def score(self):
        return {Tiebreak.KEY:(self.serverRallyPoints, self.returnerRallyPoints)}

    def rallyForServer(self) -> None:
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated tiebreak!")
        self.serverRallyPoints +=1
 
    def rallyForReturner(self) -> None:       
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated tiebreak!")
        self.returnerRallyPoints +=1

    def isOver(self):
        return self.serverRallyPoints > 6 and Helper.twoAhead(self.serverRallyPoints, self.returnerRallyPoints) \
            or self.returnerRallyPoints > 6 and Helper.twoAhead(self.returnerRallyPoints, self.serverRallyPoints) 

    def winner(self):
        if(self.isOver()):
            return self.server if self.serverRallyPoints > self.returnerRallyPoints else self.returner
        else:
            return None           



