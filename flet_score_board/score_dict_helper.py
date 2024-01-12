import flet as ft
from loguru import logger
from scorer.game import Game
from scorer.tiebreak import Tiebreak

def get_set_score_by_index(set_index, match_score:dict) -> dict:
    set_keys = list(match_score.keys())
    set_key = set_keys[set_index]
    return get_set_score_by_name(set_key, match_score)

def get_latest_set_score(match_score:dict) -> dict:
    set_keys = list(match_score.keys())
    return get_set_score_by_name(set_keys[-1], match_score)

def get_set_score_by_name(set_key:str, match_score:dict) -> dict:
    set_score = match_score.get(set_key)
    if type(set_score) == dict:
        return set_score
    else:
        raise ValueError("No SET in match_score: {}".format(match_score))
        
def set_is_terminated(set_score:dict) -> bool:
    return False if set_has_running_game(set_score) or set_has_running_tieabreak(set_score) else True   

def set_has_running_game(set_score:dict) -> bool:
    return set_has(Game.KEY, set_score)

def set_has_running_tieabreak(set_score:dict) -> bool:
    return set_has(Tiebreak.KEY, set_score)

def set_has_terminated_tieabreak(set_score:dict) -> bool:
    return set_has(Tiebreak.KEY, set_score) and tiebreak_is_over(set_score.get(Tiebreak.KEY))
    
def set_has(key:str, set_score:dict) -> bool:
    return False if set_score.get(key) is None else True

def tiebreak_is_over(tiebreak_score:dict) -> bool:
    points = list(tiebreak_score.values())
    return max(points) > 6 and twoAppart(points)

def twoAppart(points:list) -> bool:
    return abs(points[1]-points[0]) >=2

def get_point_score_for(player_name:str, set_score:dict) -> str:
    if set_has_running_game(set_score):
        return __get_point_score_for(Game.KEY, player_name, set_score)
    elif set_has_running_tieabreak(set_score):
        return __get_point_score_for(Tiebreak.KEY, player_name, set_score)
    else:
        return ""
    
def get_tiebreak_points_for(player_name:str, set_score:dict) -> int:
    if set_has(Tiebreak.KEY, set_score):
        return set_score.get(Tiebreak.KEY).get(player_name)
    raise ValueError("This Set has no tiebreak: {}".format(set_score))
    
def get_player_set_scores(player_name:str, match_score:dict):
    player_set_scores = []
    for set_key in match_score:
        set_score = match_score.get(set_key)
        player_set_scores.append(set_score.get(player_name))
    return player_set_scores

def __get_point_score_for(type:str, player_name:str, set_score:dict) -> str:
    score_unit=set_score.get(type)
    if score_unit is not None:
        return str(score_unit.get(player_name))
    else:
        raise ValueError("Cannot return {} point score since this set has no running {}".format(type, type))