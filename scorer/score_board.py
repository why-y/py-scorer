from scorer.match import Match

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

        # game
        serverLine += ScoreBoard.__format_game(self.match.sets[-1], self.match.server)
        returnerLine += ScoreBoard.__format_game(self.match.sets[-1], self.match.returner)
        return "{}\n{}".format(serverLine, returnerLine)

    @classmethod
    def __format_name(cls, name) -> str:
        return "{}|".format(name.ljust(20,' '))

    @classmethod
    def __format_set(cls, set, player) -> str:
        return " {} |".format(str(set.score().get("Set").get(player.name)).rjust(1,' '))

    @classmethod
    def __format_game(cls, currentSet, player) -> str:
        gameScore = currentSet.score().get("Set").get("Game")
        gamePoints = str(gameScore.get(player.name)) if gameScore is not None else " "
        return " {} |".format(gamePoints).rjust(3,' ')
