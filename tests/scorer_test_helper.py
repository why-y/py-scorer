from scorer.player import Player

class ScorerTestHelper:
    '''A helper class for tennis scorer unit tests'''

    NO_OF_RALLIES_TO_WIN_GAME = 4
    NO_OF_RALLIES_TO_WIN_TIEBREAK = 7
    NO_OF_RALLIES_TO_WIN_SET = 6 * NO_OF_RALLIES_TO_WIN_GAME
    SET_KEY = "Set"
    GAME_KEY = "Game"
    TIEBREAK_KEY = "Tiebreak"

    def __init__(self) -> None:
        pass

    @classmethod
    def scoreXtimesFor(cls, scoreUnit, player:Player, noOfRallies:int):
        for _ in range(noOfRallies):
            scoreUnit.rallyPointFor(player)

    @classmethod
    def format_score_set_and_game(cls, server_name:str, retruner_name:str, server_games_no:int, returner_games_no:int, server_points:int, returner_points:int):
        return {
            ScorerTestHelper.SET_KEY : {
                server_name: server_games_no,
                retruner_name: returner_games_no,
                ScorerTestHelper.GAME_KEY: {
                    server_name: server_points,
                    retruner_name: returner_points
                }
            }
        }

    @classmethod
    def format_score_set_and_tiebreak(cls, server_name:str, retruner_name:str, server_games_no:int, returner_games_no:int, server_points:int, returner_points:int):
        return {
            ScorerTestHelper.SET_KEY : {
                server_name: server_games_no,
                retruner_name: returner_games_no,
                ScorerTestHelper.TIEBREAK_KEY: {
                    server_name: server_points,
                    retruner_name: returner_points
                }
            }
        }
    
    @classmethod
    def format_score_game(cls, server_name:str, retruner_name:str, server_points:int, returner_points:int):
        return {
            ScorerTestHelper.GAME_KEY: {
                server_name: server_points,
                retruner_name: returner_points
            }
        }

