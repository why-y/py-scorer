import flet as ft

#from typing import Any, List, Optional, Union
#from flet_core.control import Control, OptionalNumber
#from flet_core.ref import Ref
#from flet_core.types import AnimationValue, CrossAxisAlignment, MainAxisAlignment, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue, ScrollMode

from loguru import logger

from flet_score_board.score_board import ScoreBoard

def main(page: ft.Page):
    page.title = "Tennis Score Board"

    # create application instance
    score_board = ScoreBoard()

    # add application's root control to the page
    page.add(score_board)
    page.update()

ft.app(target=main)