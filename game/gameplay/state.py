import pygame as pg
import sys

from game.tools.asset_cache import playSound
import game.tools.constants as c
from game.tools.controls import controlsDicts


def checkQuitGame():
    """Quit the game if the user attempts to close it."""
    if pg.event.peek(pg.QUIT):
        sys.exit()

# game.gameplay.player_actions imports checkQuitGame, so we import pauseGame here below that function to prevent the
# issues of circular importing.
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

    # If any player presses the pause button, the pauseGame function is called. After that function ends,
    # pausedPlayerNumber is set back to 0, to represent the 'unpaused' state.
    if pausedPlayerNumber != 0:
        pauseGame(pausedPlayerNumber - 1)
        pausedPlayerNumber = 0
    return pausedPlayerNumber


def checkPauseGameWithInput(playerList):
    """Check the keys currently pressed. If any are the pause button, pause the game.

    In situations where keys pressed can have other effects on the game (such as during normal level gameplay),
    do not use this function, as it will pop all events out of the event queue.
    Use checkPauseGame in those cases instead.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
    """
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            for num, player in enumerate(playerList):
                # Players who have run out of lives cannot pause the game.
                # After pausing, the queue is cleared to ensure that no keys pressed during the game preparing to pause
                # take effect while paused.
                if event.key == controlsDicts[num]["pause"] and player.playerState != c.PlayerStates.DEAD:
                    pg.mixer.music.pause()
                    playSound("pause_unpause.wav")
                    pauseGame(num)
                    pg.time.delay(1000)
                    pg.event.clear()
