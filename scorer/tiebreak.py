from scorer.player import Player

class Tiebreak:
    '''A class to score a tennin tiebreak'''

    GAME_KEY = "Tiebreak"

    def __init__(self, server: Player, returner: Player) -> None:
        self.server = server
        self.returner = returner
        self.serverRallyPoints = 0
        self.returnerRallyPoints = 0

    def isOver(self):
        return self.serverRallyPoints>6  or self.returnerRallyPoints>6 



