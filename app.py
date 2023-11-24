import logging
import argparse

from scorer.match import Match
from scorer.player import Player
from scorer.score_board import ScoreBoard

logging.basicConfig(level=logging.DEBUG) 
    
def app():
    serverName = input('Enter the servers name   : ')
    returnerName = input('Enter the returners name : ')
    print('Start Match between {} and {}.'.format(serverName, returnerName))
    print('{} serves.'.format(serverName))

    match = Match(Player(serverName), Player(returnerName), 3)
    scoreBoard = ScoreBoard(match)
    print(scoreBoard.formatted_score())

    while not match.isOver():
        rallyFor = input(' -> enter [a] to score for {} or [b] to score for {}  : '.format(serverName, returnerName))
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

app()