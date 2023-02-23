import logging
from scorer.player import Player
from scorer.game import Game

logging.basicConfig(level=logging.DEBUG)

class Set:
    '''A class to score a tennis sets'''

    def __init__(self, server: Player, returner: Player) -> None:
        self.server = server
        self.returner = returner
        self.games = []

    def score(self):
        noOfGamesWonByServer = Set.__getNoOfGamesWonBy(self.games, self.server)
        noOfGamesWonByReturner = Set.__getNoOfGamesWonBy(self.games, self.returner)       
        return (noOfGamesWonByServer, noOfGamesWonByReturner)
    
    def rallyForServer(self) -> None:
        
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated set!")
        
        if not (self.__hasRunningGame()):
            self.games.append(Game(self.server, self.returner))

        self.__getRunningGame().rallyForServer()
 
    def rallyForReturner(self) -> None:
        
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated set!")
        
        if not (self.__hasRunningGame()):
            self.games.append(Game(self.server, self.returner))

        self.__getRunningGame().rallyForReturner()

    def isOver(self):
        if(self.__hasRunningGame()):
            return False
        else:
            serverGames = Set.__getNoOfGamesWonBy(self.games, self.server)
            returnerGames = Set.__getNoOfGamesWonBy(self.games, self.returner)
            return True if \
                (serverGames >=6 or returnerGames >=6) and \
                (Set.__twoGamesAhead(serverGames, returnerGames) or Set.__twoGamesAhead(returnerGames, serverGames)) \
                 else False
            

    def __getRunningGame(self) -> Game:
        return None if len(self.games)==0 or self.games[-1].isOver() else self.games[-1]

    def __hasRunningGame(self) -> None:
        return False if self.__getRunningGame() is None else True

    @classmethod
    def __twoGamesAhead(cls, myGames:int, opponentGames:int) -> bool:
        return myGames > opponentGames + 1

    @classmethod
    def __getNoOfGamesWonBy(cls, allGames, player: Player) -> int:
        noOfGamesWon = 0
        for game in allGames:
            if game.winner() == player:
                noOfGamesWon += 1
        return noOfGamesWon
        
