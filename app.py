from scorer.match import Match

def score_to_str(score) -> str:
    return score

def app():
    serverName = input('Enter the servers name   : ')
    returnerName = input('Enter the returners name : ')
    print('Start Match between {} and {}.'.format(serverName, returnerName))
    print('{} serves.'.format(serverName))

    match = Match(serverName, returnerName)
    print(score_to_str(match.score()))

    while not match.isOver():
        rallyFor = input(' -> enter [a] to score for {} or [b] to score for {}  : '.format(serverName, returnerName))
        if(rallyFor == 'a'):
            match.rallyForServer()
            print(score_to_str(match.score()))
        elif(rallyFor == 'b'):
            match.rallyForReturner()
            print(score_to_str(match.score()))
        elif(rallyFor == 'exit' or rallyFor == 'quit'):
            quit()
        else:
            pass
    
    print('Match is over! {} has won by:'.format(match.winner()))
    print(score_to_str(match.score()))

app()