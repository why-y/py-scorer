import logging
from scorer.player import Player
logging.basicConfig(level=logging.DEBUG)

class Set:
    '''A class to score a tennis sets'''

    def __init__(self, server: Player, returner: Player) -> None:
        self.server = server
        self.returner = returner
        self.serverGames = 0
        self.returnerGames = 0

    def score(self):
        return (self.serverGames, self.returnerGames)
    
    def gameForServer(self) -> None:
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated set!")
        self.serverGames += 1

    def gameForReturner(self) -> None:
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated set!")
        self.returnerGames += 1

    def isOver(self):
        return \
            self.serverGames >= 6 and \
                Set.__twoGamesAhead(self.serverGames, self.returnerGames) or \
            self.returnerGames >= 6 and \
                Set.__twoGamesAhead(self.returnerGames, self.serverGames)

    @classmethod
    def __twoGamesAhead(cls, games, opponentGames):
        return games > opponentGames + 1

