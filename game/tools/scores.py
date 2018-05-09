import os

import game.tools.constants as c


def getHighScore():
    """Get the current high score saved in a text file in the game folder.

    This function only acknowledges the six rightmost digits of a high score (i.e., it reads 1234567 as 234567,
    or 6 as 000006).
    If highScoreFile does not exist, this function creates a new highScoreFile with a saved score of 0.
    If there is a ValueError in casting the saved high score to an int, the score defaults to 0.

    Returns:
        highScore: An integer showing the current high score.
    """
    try:
        with open(os.path.join(c.RESOURCE_FOLDER, "clu_high_score.txt"), "r") as highScoreFile:
            highScore = int(highScoreFile.read()[-6:])
    except ValueError:
        highScore = 0
        setHighScore(highScore)
    except FileNotFoundError:
        highScore = 0
        setHighScore(highScore)
    return highScore


def setHighScore(highScore):
    """Write the passed score to a text file, creating the file if it does not already exist.

    Args:
        highScore: An integer of the score which should be written to highScoreFile.
    """
    with open(os.path.join(c.RESOURCE_FOLDER, "clu_high_score.txt"), "w") as highScoreFile:
        highScoreFile.write(str(highScore))
