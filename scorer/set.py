import logging
import scorer.scorer_helper as Helper
from scorer.player import Player
from scorer.game import Game
from scorer.tiebreak import Tiebreak

logging.basicConfig(level=logging.DEBUG)

class Set:
    '''A class to score a tennis sets'''

    KEY = "Set"

    def __init__(self, server: Player, returner: Player, with_tiebreak = True) -> None:
        self.server = server
        self.returner = returner
        self.games = [Game(self.server, self.returner)]
        self.with_tiebreak = with_tiebreak
        self.tiebreak = None

    def has_tiebreak(self):
        return self.with_tiebreak

    def score(self):
        setScore = {}
        setScore.update(self.__scoreOfTerminatedGames())
        if self.__hasRunningGame(): setScore.update(self.__getRunningGame().score())
        if self.tiebreak is not None: setScore.update(self.tiebreak.score())
        return setScore

    def __scoreOfTerminatedGames(self):
        scoreServer = self.__getNoOfGamesWonBy(self.server)
        scoreReturner = self.__getNoOfGamesWonBy(self.returner)
        if self.tiebreak is not None and self.tiebreak.isOver():
            if self.tiebreak.winner() is self.server: scoreServer += 1
            if self.tiebreak.winner() is self.returner: scoreReturner += 1
        
        return {
            Set.KEY : (
                scoreServer, 
                scoreReturner
                )
        }
        
    def rallyPointFor(self, player:Player) -> None:
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated set!")
        elif(self.__hasRunningGame()):
            self.__getRunningGame().rallyPointFor(player)
            if not self.__hasRunningGame() and not self.isOver():
                self.tiebreak = Tiebreak(self.server, self.returner) if self.__needsTiebreak() else self.games.append(Game(self.server, self.returner))  
        elif(self.__hasRunningTiebreak()):
            self.__getRunningTiebreak().rallyPointFor(player)
        elif(self.__needsTiebreak()):
            self.tiebreak = Tiebreak(self.server, self.returner)
            self.tiebreak.rallyPointFor(player)
        else:
            nextGame = Game(self.server, self.returner)
            nextGame.rallyPointFor(player)
            self.games.append(nextGame)

    def isOver(self):
        if(self.__hasRunningGame() or self.__hasRunningTiebreak()):
            return False
        else:
            serverGames = self.__getNoOfGamesWonBy(self.server)
            returnerGames = self.__getNoOfGamesWonBy(self.returner)
            return True if \
                (serverGames >=6 or returnerGames >=6) and \
                (Helper.twoAhead(serverGames, returnerGames) or Helper.twoAhead(returnerGames, serverGames)) \
                 else False

    def winner(self):
        if(self.isOver()):
            serverGames = self.__getNoOfGamesWonBy(self.server)
            returnerGames = self.__getNoOfGamesWonBy(self.returner)
            return self.server if serverGames>returnerGames else self.returner
        else:
            return None           

    def __getRunningGame(self) -> Game:
        latestGame = self.games[-1]
        return None if latestGame.isOver() else latestGame

    def __hasRunningGame(self) -> None:
        return False if self.__getRunningGame() is None else True

    def __needsTiebreak(self) -> bool:
        return self.with_tiebreak and self.__getNoOfGamesWonBy(self.server)==6 and self.__getNoOfGamesWonBy(self.returner)==6

    def __getRunningTiebreak(self) -> Game:
        return None if self.tiebreak is None or self.tiebreak.isOver() else self.tiebreak

    def __hasRunningTiebreak(self) -> None:
        return False if self.__getRunningTiebreak() is None else True

    def __getNoOfGamesWonBy(self, player: Player) -> int:
        noOfGamesWon = 0
        for game in self.games:
            if game.winner() == player:
                noOfGamesWon += 1
        return noOfGamesWon
        

