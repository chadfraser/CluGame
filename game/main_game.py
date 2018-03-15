import pygame as pg

from game.gameplay.state import checkQuitGame
from game.tools import constants as c
from game.gameplay.title import displayTitleScreen


def main():
    currentScores = [0, 0, 0, 0]

    while True:
        c.SCREEN.fill(c.BLACK)
        checkQuitGame()

        for group in c.allGroups:
            if group is not c.itemGroup:
                group.empty()
        playerScores = displayTitleScreen(currentScores[0], currentScores[1], currentScores[2], currentScores[3])
        for num, score in enumerate(playerScores):
            currentScores[num] = score
        pg.display.update()
        c.CLOCK.tick(c.FPS)


main()
