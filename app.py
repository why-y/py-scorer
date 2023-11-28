from loguru import logger
import argparse

from scorer.match import Match
from scorer.player import Player
from scorer.score_board import ScoreBoard

COPYRIGHT_SIGN = chr(0x00A9)
    
def app():
    commandline_args = parse_commandline_arguments()
 #   logger.info(commandline_args)
    server_name = commandline_args.get("server_name")
    returner_name = commandline_args.get("returner_name")
    print('Start Match between {} and {}.'.format(server_name, returner_name))
    print('{} serves.'.format(server_name))

    match = Match(Player(server_name), Player(returner_name), 3)
    scoreBoard = ScoreBoard(match)
    print(scoreBoard.formatted_score())

    while not match.isOver():
        rallyFor = input(' -> enter [a] to score for {} or [b] to score for {}  : '.format(server_name, returner_name))
        if(rallyFor == 'a'):
            match.rallyPointFor(match.server)
            print(scoreBoard.formatted_score())

        elif(rallyFor == 'b'):
            match.rallyPointFor(match.returner)
            print(scoreBoard.formatted_score())
        elif(rallyFor.lower() == 'exit' or rallyFor.lower() == 'quit'):
            quit()
        else:
            print('!! Type either of: [a] or [b] to score or [exit] to terminate!')
            pass
    
    print('Match is over! {} has won by:'.format(match.winner().name))
    print(scoreBoard.formatted_score())

def parse_commandline_arguments() -> dict:
    parser = argparse.ArgumentParser(
        prog="py-scorer",
        description="A simple Tennis score board in Python",
        epilog=COPYRIGHT_SIGN + 'copyright by GRY Inc.')
    parser.add_argument("server", type=str, help="Name of the first server")
    parser.add_argument("returner", type=str, help="Name of the first returner")
    parser.add_argument("-n", "--no-tiebreaks", action="store_true", help="Long sets are decided by two games margin.")
    parser.add_argument("-b", "--bestof", type=int, default=3, choices=[3,5], help="Number of max. played sets. I.e. best of ...!")
    args = parser.parse_args()
    return {
        "server_name" : args.server,
        "returner_name" : args.returner,
        "bestof": args.bestof,
        "with_tiebreak": not args.no_tiebreaks
    }

app()