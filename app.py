import logging

from scorer.match import Match
from scorer.player import Player

logging.basicConfig(level=logging.DEBUG)

def match_to_str(match) -> str:
    return match.score()

def __match_to_str(match) -> str:
    
    # name
    serverLine   = format_name(match.server.name)
    returnerLine = format_name(match.returner.name)
    # sets
    for set in match.sets:
        serverLine +=  format_set(set, 0)
        returnerLine +=  format_set(set, 1)
    # game
    serverLine += format_game(match.sets[-1], 0)
    returnerLine += format_game(match.sets[-1], 1)
    return "{}\n{}".format(serverLine, returnerLine)

def format_name(name) -> str:
    return "{}|".format(name.ljust(20,' '))

def format_set(set, pos) -> str:
    return " {} |".format(str(set.score().get("Set")[pos]).rjust(1,' '))

def format_game(currentSet, pos) -> str:
    gamePoints = str(currentSet.score().get("Game")[pos]) if currentSet.score().get("Game") is not None else " "
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