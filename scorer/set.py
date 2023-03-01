import logging
import scorer.scorer_helper as Helper
from scorer.player import Player
from scorer.game import Game

logging.basicConfig(level=logging.DEBUG)

class Set:
    '''A class to score a tennis sets'''

    SET_KEY = "Set"

    def __init__(self, server: Player, returner: Player) -> None:
        self.server = server
        self.returner = returner
        self.games = []
        self.games.append(Game(self.server, self.returner))

    def score(self):
        noOfGamesWonByServer = Set.__getNoOfGamesWonBy(self.games, self.server)
        noOfGamesWonByReturner = Set.__getNoOfGamesWonBy(self.games, self.returner)
        score = {
            Set.SET_KEY : (noOfGamesWonByServer, noOfGamesWonByReturner)
        }
        runningGame = self.__getRunningGame()
        gameScore = runningGame.score() if runningGame is not None else {Game.GAME_KEY:(0,0)}
        score.update(gameScore)
        return score
    
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
                (Helper.twoAhead(serverGames, returnerGames) or Helper.twoAhead(returnerGames, serverGames)) \
                 else False

    def winner(self):
        if(self.isOver()):
            serverGames = Set.__getNoOfGamesWonBy(self.games, self.server)
            returnerGames = Set.__getNoOfGamesWonBy(self.games, self.returner)
            return self.server if serverGames>returnerGames else self.returner
        else:
            return None           

    def __getRunningGame(self) -> Game:
        return None if len(self.games)==0 or self.games[-1].isOver() else self.games[-1]

    def __hasRunningGame(self) -> None:
        return False if self.__getRunningGame() is None else True

    @classmethod
    def __getNoOfGamesWonBy(cls, allGames, player: Player) -> int:
        noOfGamesWon = 0
        for game in allGames:
            if game.winner() == player:
                noOfGamesWon += 1
        return noOfGamesWon
        

