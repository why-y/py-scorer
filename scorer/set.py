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

    def score(self):
        setScore = {}
        setScore.update(self.__scoreOfTerminatedGames())
        if self.hasRunningGame():
            self.__addToScore(setScore.get(Set.KEY), self.__getRunningGame().score())
        if self.hasTiebreak(): 
            self.__addToScore(setScore.get(Set.KEY), self.getTiebreak().score())
        return setScore

    def rallyPointFor(self, player:Player) -> None:
        if(self.isOver()):
            raise ValueError("Cannot score on a terminated set!")
        elif(self.hasRunningGame()):
            self.__getRunningGame().rallyPointFor(player)
            if not self.hasRunningGame() and not self.isOver():
                self.tiebreak = Tiebreak(self.server, self.returner) if self.__needsTiebreak() else self.games.append(Game(self.server, self.returner))  
        elif(self.hasRunningTiebreak()):
            self.getTiebreak().rallyPointFor(player)
        elif(self.__needsTiebreak()):
            self.tiebreak = Tiebreak(self.server, self.returner)
            self.tiebreak.rallyPointFor(player)
        else:
            nextGame = Game(self.server, self.returner)
            nextGame.rallyPointFor(player)
            self.games.append(nextGame)

    def isOver(self):
        if(self.hasRunningGame() or self.hasRunningTiebreak()):
            return False
        elif self.hasTerminatedTiebreak():
            return True
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

    def hasRunningGame(self) -> bool:
        latestGame = self.games[-1]
        return True if latestGame is not None and not latestGame.isOver() else False
    

    def getTiebreak(self) -> Tiebreak:
        if self.tiebreak is None:
            raise ValueError("this set has no running tiebreak!".format(str(self.score())))
        else:
            return self.tiebreak
   
    def hasTiebreak(self) -> bool:
        return False if self.tiebreak is None else True
    
    def hasRunningTiebreak(self) -> bool:
        return True if self.hasTiebreak() and not self.getTiebreak().isOver() else False

    def hasTerminatedTiebreak(self) -> bool:
        return True if self.hasTiebreak() and self.getTiebreak().isOver() else False
    
    def __getRunningGame(self) -> Game:
        latestGame = self.games[-1]
        if latestGame is None:
            raise ValueError("this set has no running Game: {}".format(str(self.score())))
        return latestGame

    def __needsTiebreak(self) -> bool:
        return self.with_tiebreak and self.__getNoOfGamesWonBy(self.server)==6 and self.__getNoOfGamesWonBy(self.returner)==6

    def __scoreOfTerminatedGames(self) -> dict:
        scoreServer = self.__getNoOfGamesWonBy(self.server)
        scoreReturner = self.__getNoOfGamesWonBy(self.returner)
        return {
            Set.KEY : {
                self.server.name: scoreServer, 
                self.returner.name: scoreReturner            
            }
        }
        
    def __getNoOfGamesWonBy(self, player: Player) -> int:
        noOfGamesWon = 0
        if self.hasTerminatedTiebreak() and self.getTiebreak().winner() == player:
            noOfGamesWon = 7
        else: 
            for game in self.games:
                if game.winner() == player:
                    noOfGamesWon += 1
        return noOfGamesWon
    
    def __addToScore(self, setScore, additionalScore:dict):
        setScore.update(additionalScore)

