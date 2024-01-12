import flet as ft

GAME_KEY="Game"
TIEBREAK_KEY="Tiebreak"
SET_KEY="Set"

def get_latest_set_score(match_score:dict) -> dict:
    set_keys = list(match_score.keys())
    set_score = match_score.get(set_keys[-1])
    if type(set_score) == dict:
        return set_score
    else:
        raise ValueError("No SET in match_score: {}".format(match_score))
    
def set_is_terminated(set_score:dict) -> bool:
    return False if set_has_running_game(set_score) or set_has_running_tieabreak(set_score) else True   

def set_has_running_game(set_score:dict) -> bool:
    return set_has(GAME_KEY, set_score)

def set_has_running_tieabreak(set_score:dict) -> bool:
    return set_has(TIEBREAK_KEY, set_score)

def set_has(key:str, set_score:dict) -> bool:
    return False if set_score.get(key) is None else True

def get_point_score_for(player_name:str, set_score:dict) -> str:
    if set_has_running_game(set_score):
        return __get_point_score_for(GAME_KEY, player_name, set_score)
    elif set_has_running_tieabreak(set_score):
        return __get_point_score_for(TIEBREAK_KEY, player_name, set_score)
    else:
        return ""
    
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