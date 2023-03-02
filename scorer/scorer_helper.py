def twoAhead(firstScore, secondScore) -> bool:
    return firstScore > secondScore+1

def twoAppart(first:int, second:int) -> bool:
    return abs(first-second) >=2