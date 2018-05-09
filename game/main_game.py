import pygame as pg

from game.gameplay.state import checkQuitGame
from game.tools import constants as c
from game.gameplay.title import displayTitleScreen


def main():
    """Set the current score for each player to 0, then run the logic to display the title screen and acknowledge
    player input.

    This code loops, so the groups are emptied and the title screen is displayed again if the players all get a
    game over.
    """
    currentScores = [0, 0, 0, 0]

    while True:
        c.SCREEN.fill(c.BLACK)
        checkQuitGame()

        for group in c.allGroups:
            if group is not c.itemGroup:
                group.empty()
        playerScores = displayTitleScreen(currentScores)
        for num, score in enumerate(playerScores):
            currentScores[num] = score
        pg.display.update()
        c.CLOCK.tick(c.FPS)


if __name__ == "__main__":
    main()
