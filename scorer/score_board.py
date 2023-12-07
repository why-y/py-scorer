from loguru import logger
from scorer.match import Match
from scorer.set import Set
from scorer.game import Game
from scorer.tiebreak import Tiebreak
from scorer.player import Player

class ScoreBoard:
    '''A class to nicely reveal the score of a match'''

    def __init__(self, match:Match) -> None:
        self.match = match

    def formatted_score(self) -> str:

        # name
        serverLine   = self.__format_name(self.match.server.name)
        returnerLine = self.__format_name(self.match.returner.name)

        # sets
        for set in self.match.sets:
            serverLine +=  self.__format_set(set, self.match.server)
            returnerLine += self.__format_set(set, self.match.returner)
        
        # game/tiebreak point
        if not self.match.isOver() :
            running_set = self.match.sets[-1]
            serverLine += self.__format_points(running_set, self.match.server)
            returnerLine += self.__format_points(running_set, self.match.returner)
        
        ruler = self.__ruler(len(returnerLine))
        return "{}\n{}\n{}\n{}".format(ruler, serverLine, returnerLine, ruler)

    def __ruler(self, len:int) -> str:
        return "-" * len

    def __format_name(self, name) -> str:
        return "{:<20}|".format(name)
    
    def __format_set(self, set:Set, player:Player) -> str:
        no_of_games = str(self.__get_set_score_from_set(set).get(player.name))
        if set.hasTerminatedTiebreak():
            no_of_games += "(" + str(self.__get_tiebreak_score_from_set(set).get(player.name)) + ")"
        return " {:^3} |".format(no_of_games)

    def __format_points(self, currentSet:Set, player) -> str:
        game_or_tiebreak_score = self.__get_tiebreak_score_from_set(currentSet) if currentSet.hasRunningTiebreak() else self.__get_current_game_score_from_set(currentSet)
        points = str(game_or_tiebreak_score.get(player.name)) if game_or_tiebreak_score is not None else ""
        return " {:>3} |".format(points)

    def __get_set_score_from_set(self, set:Set) -> dict:
        set_score = set.score().get(Set.KEY)
        if set_score is None:
            raise LookupError("Set structure has no Set section: " + str(set.score()))
        return set_score
    
    def __get_tiebreak_score_from_set(self, set:Set) -> dict:
        tiebreak_score = self.__get_set_score_from_set(set).get(Tiebreak.KEY)
        if tiebreak_score is None:
            raise LookupError("Set structure has no Tiebreak section: " + str(set.score()))
        return tiebreak_score
    
    def __get_current_game_score_from_set(self, set:Set) -> dict:
        game_score = self.__get_set_score_from_set(set).get(Game.KEY)
        if game_score is None:
            raise LookupError("Set structure has no Game section: " + str(set.score()))
        return game_score