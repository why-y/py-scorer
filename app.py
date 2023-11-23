import logging
import argparse

from scorer.match import Match
from scorer.player import Player

logging.basicConfig(level=logging.DEBUG)

def __match_to_str(match) -> str:
    return match.score()

def match_to_str(match) -> str:
    
    # name
    serverLine   = format_name(match.server.name)
    returnerLine = format_name(match.returner.name)

    # sets
    for set in match.sets:
        serverLine +=  format_set(set, match.server)
        returnerLine +=  format_set(set, match.returner)

    # game
    serverLine += format_game(match.sets[-1], match.server)
    returnerLine += format_game(match.sets[-1], match.returner)
    return "{}\n{}".format(serverLine, returnerLine)

def format_name(name) -> str:
    return "{}|".format(name.ljust(20,' '))

def format_set(set, player) -> str:
    return " {} |".format(str(set.score().get("Set").get(player.name)).rjust(1,' '))

def format_game(currentSet, player) -> str:
    gameScore = currentSet.score().get("Set").get("Game")
    gamePoints = str(gameScore.get(player.name)) if gameScore is not None else " "
    return " {} |".format(gamePoints).rjust(2,' ')

def app():
    serverName = input('Enter the servers name   : ')
    returnerName = input('Enter the returners name : ')
    print('Start Match between {} and {}.'.format(serverName, returnerName))
    print('{} serves.'.format(serverName))

    match = Match(Player(serverName), Player(returnerName), 3)
    print(match_to_str(match))

    while not match.isOver():
        rallyFor = input(' -> enter [a] to score for {} or [b] to score for {}  : '.format(serverName, returnerName))
        if(rallyFor == 'a'):
            match.rallyPointFor(match.server)
            print(match_to_str(match))
        elif(rallyFor == 'b'):
            match.rallyPointFor(match.returner)
            print(match_to_str(match))
        elif(rallyFor.lower() == 'exit' or rallyFor.lower() == 'quit'):
            quit()
        else:
            pass
    
    print('Match is over! {} has won by:'.format(match.winner().name))
    print(match_to_str(match))

app()