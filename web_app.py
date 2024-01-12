import flet as ft

from loguru import logger

from flet_score_board.score_board import ScoreBoard

def main(page: ft.Page):
    page.title = "Tennis Score Board"
    page.theme = ft.Theme(color_scheme_seed=ft.colors.GREEN_800)

    # create application instance
    score_board = ScoreBoard()

    # add application's root control to the page
    page.add(score_board)
    page.update()

ft.app(target=main)