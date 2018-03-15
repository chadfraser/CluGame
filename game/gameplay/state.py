import pygame as pg
import sys


def checkQuitGame():
    """Quit the game if the user attempts to close it."""
    if pg.event.peek(pg.QUIT):
        sys.exit()


from game.gameplay.player_actions import pauseGame


def checkPauseGame(pausedPlayerNumber):
    """Pause the game if any player presses the pause button.

    Args:
        pausedPlayerNumber: An integer representing which of the players pauses the game.
            Defaults to 0 if the game is unpaused.
    Returns:
        pausedPlayerNumber: An integer representing which of the players pauses the game.
            Defaults to 0 if the game is unpaused.
    """
    if pausedPlayerNumber != 0:
        # If any player presses the pause button, the pauseGame function is called. After that function ends,
        # pausedPlayerNumber is set back to 0, to represent the 'unpaused' state.

        pauseGame(pausedPlayerNumber - 1)
        pausedPlayerNumber = 0
    return pausedPlayerNumber
