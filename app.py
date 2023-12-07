from loguru import logger
import argparse
from pynput.keyboard import Key, Listener, KeyCode

from scorer.match import Match
from scorer.player import Player
from scorer.score_board import ScoreBoard

COPYRIGHT_SIGN = chr(0x00A9
                     )
def parse_commandline_arguments():
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

def print_instrucitons():
    print('!! Type either of: [f] to score for {} or [j] to score for {} or [esc] to terminate!'.format(server_name, returner_name), flush=True)


commandline_args = parse_commandline_arguments()
server_name = commandline_args.get("server_name")
returner_name = commandline_args.get("returner_name")
bestof = commandline_args.get("bestof")

match = Match(Player(server_name), Player(returner_name), bestof if type(bestof) is int else 3)
scoreBoard = ScoreBoard(match)

print('Start best of {} Match between {} and {}.'.format(bestof, server_name, returner_name), flush=True)

def on_press(key):
    try:
        if key.char == 'f':
            match.rallyPointFor(match.server)
            print(scoreBoard.formatted_score(), flush=True)
        elif key.char == 'j':
            match.rallyPointFor(match.returner)
            print(scoreBoard.formatted_score(), flush=True)
        else:
            print_instrucitons()
    except AttributeError:
        if key == Key.esc:
            print(scoreBoard.formatted_score(), flush=True)
            return False
        else:
            print_instrucitons()
    except ValueError:
        return False
    
    if(match.isOver()):
        print('Match is over! {} has won by:'.format(match.winner().name))
        print(scoreBoard.formatted_score())
        return False
    

print(scoreBoard.formatted_score(), flush=True)

# Collect events until released
with Listener(on_press, suppress=True) as listener:
    listener.join()
