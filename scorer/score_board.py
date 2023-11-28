from loguru import logger
from scorer.match import Match
from scorer.set import Set

class ScoreBoard:
    '''A class to nicely reveal the score of a match'''

    def __init__(self, match:Match) -> None:
        self.match = match

    def formatted_score(self) -> str:

        # name
        serverLine   = ScoreBoard.__format_name(self.match.server.name)
        returnerLine = ScoreBoard.__format_name(self.match.returner.name)

        # sets
        for set in self.match.sets:
            serverLine +=  ScoreBoard.__format_set(set, self.match.server)
            returnerLine += ScoreBoard.__format_set(set, self.match.returner)

        # game/tiebreak point
        running_set = self.match.sets[-1]
        serverLine += ScoreBoard.__format_points(running_set, self.match.server)
        returnerLine += ScoreBoard.__format_points(running_set, self.match.returner)
        return "{}\n{}".format(serverLine, returnerLine)

    @classmethod
    def __format_name(cls, name) -> str:
        return "{:<20}|".format(name)

    @classmethod
    def __format_set(cls, set, player) -> str:
        return " {:^3} |".format(str(set.score().get("Set").get(player.name)))

    @classmethod
    def __format_points(cls, currentSet:Set, player) -> str:
        game_or_tiebreak_score = currentSet.score().get("Set").get("Tiebreak") if currentSet.hasRunningTiebreak() else currentSet.score().get("Set").get("Game")
        points = str(game_or_tiebreak_score.get(player.name)) if game_or_tiebreak_score is not None else ""
        return " {:>3} |".format(points)
