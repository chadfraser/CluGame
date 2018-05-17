import pygame as pg

from game.gameplay.state import checkQuitGame, checkPauseGameWithInput
from game.tools.asset_cache import playSound
import game.tools.constants as c


def scoreLevel(playerList, level, time, highScore, stepToScore=0):
    """Increase the players' scores at the end of the level by a particular amount based on stepToScore.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        level: A Level object representing the current level being played.
        time: An integer representing the time the players have remaining after completing the current level.
        highScore: An integer showing the current high score.
        stepToScore: An integer indicating whether the players are currently scoring time remaining, enemies
            killed, or gold collected.

    Returns:
        highScore:
        iconCount:
    """
    iconCountText = []

    # The location of where the players' scores and icons are shown depends on the number of players.
    if len(playerList) < 3:
        scoreDataCoordinates = [(240, 95), (240, 319)]
        scoreIconCountCoordinates = [(140, 143), (140, 367)]
    else:
        scoreDataCoordinates = [(55, 74), (309, 74), (55, 298), (309, 298)]
        scoreIconCountCoordinates = [(64, 147), (320, 147), (64, 371), (320, 371)]

    # Instead of updating the entire screen, this function only draws a black square over the players (to match the
    # background) and then draws the new sprite for each player over those squares.
    for player in playerList:
        player.setLevelEndCountImage()
        pg.draw.rect(c.SCREEN, c.BLACK, pg.rect.Rect(player.coordinates[0], player.coordinates[1], 42, 32))
        c.SCREEN.blit(player.image, player.coordinates)
    iconCount = [0 for _ in playerList]
    looping = True
    while looping:
        frameCount = 0
        checkQuitGame()
        checkPauseGameWithInput(playerList)

        # frameCountLimit represents how many frames the program should wait before calling on the score function
        # again, so the different scoring elements tick down at different speeds.
        # Time is scored faster than gold, and gold is scored faster than urchins.
        if stepToScore == 0:
            if time > 0:
                looping, time, scoreText, highScore = scoreTime(playerList, level, time, highScore)
                frameCountLimit = 4
            else:
                break
        elif stepToScore == 1:
            looping, iconCount, scoreText, iconCountText, highScore = scoreUrchins(playerList, iconCount, highScore)
            frameCountLimit = 24
        else:
            looping, iconCount, scoreText, iconCountText, highScore = scoreGold(playerList, iconCount, highScore)
            frameCountLimit = 8

        for text, coords in zip(iconCountText, scoreIconCountCoordinates):
            pg.draw.rect(c.SCREEN, c.BLACK, pg.rect.Rect(coords[0], coords[1], 48, 16))
            c.SCREEN.blit(text, (coords[0], coords[1]))
        for text, coords in zip(scoreText, scoreDataCoordinates):
            pg.draw.rect(c.SCREEN, c.BLACK, pg.rect.Rect(coords[0], coords[1], 96, 16))
            c.SCREEN.blit(text, (coords[0], coords[1]))
        pg.draw.rect(c.SCREEN, level.backgroundColor, pg.rect.Rect(317, 224, 96, 16))
        highScoreText = c.FONT.render("TOP,{:06d}".format(highScore), False, c.WHITE)
        c.SCREEN.blit(highScoreText, (254, 224))
        pg.display.update()
        while frameCount < frameCountLimit:
            frameCount += 1
            checkQuitGame()
            checkPauseGameWithInput(playerList)
            c.CLOCK.tick(c.FPS)
        c.CLOCK.tick(c.FPS)
    return highScore, iconCount


def scoreTime(playerList, level, time, highScore):
    """Update each players' score based on the current time, 10 points each time this function is called.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        level: A Level object representing the current level being played.
        time: An integer representing the time the players have remaining after completing the current level.
        highScore: An integer showing the current high score.

    Returns:
        looping: A boolean indicating if scoreLevel should call this function again.
        time: An integer representing the time the players have remaining after completing the current level.
        scoreText: A list of the current scores for each of the players.
        highScore: An integer showing the current high score.
    """
    scoreText = []
    timeText = c.FONT.render("TIME,{:03d}".format(time), False, c.WHITE)
    checkQuitGame()
    checkPauseGameWithInput(playerList)

    # All living players increase their score by 10 points each time this function is called.
    for player in playerList:
        if player.lives > 0:
            player.score += 10
        scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
    highScore = compareHighScore(playerList, highScore)

    # The time remaining decreases by 10 counts each time this function is called.
    time = max(0, time - 10 - (time % 10))

    # Instead of updating the entire screen, this function only draws a square over the time's coordinates that matches
    # the background color, then blits the remaining time to the screen.
    pg.draw.rect(c.SCREEN, level.backgroundColor, pg.rect.Rect(160, 224, 48, 16))
    c.SCREEN.blit(timeText, (82, 224))

    # Once the time reaches 0, looping is set to False so scoreTime will not be called again.
    # As long as the time is greater than 0, a sound effect will play as the time counts down.
    if time == 0:
        return False, time, scoreText, highScore
    else:
        playSound("count_points.wav")
        return True, time, scoreText, highScore


def scoreUrchins(playerList, iconCount, highScore):
    """Update each players' score based on the amount of urchins that they have killed.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        iconCount: A list of integers representing how many times each player has gained points from the
            scoreUrchins function this level.
        highScore: An integer showing the current high score.

    Returns:
        looping: A boolean indicating if scoreLevel should call this function again.
        iconCount: A list of integers representing how many times each player has gained points from the
            scoreUrchins function this level.
        scoreText: A list of the current scores for each of the players.
        iconCountText: A list of text objects representing each player's iconCount value.
        highScore: An integer showing the current high score.
    """
    scoreText = []
    iconCountText = []
    checkQuitGame()
    checkPauseGameWithInput(playerList)
    if any(player.killedUrchinCount > 0 for player in playerList):
        playSound("count_points.wav")

    # All living players increase their score by 500 points each time this function is called, until it has been called
    # as many times as they've killed enemies this level.
    for num, player in enumerate(playerList):
        if player.killedUrchinCount > iconCount[num]:
            player.score += 500
            iconCount[num] += 1
        scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
        iconCountText.append(c.FONT.render("+{:02d}".format(iconCount[num] % 100), False, c.WHITE))
    highScore = compareHighScore(playerList, highScore)

    # Once iconCount has reached the correct number of killed enemies for each player, looping is set to False so
    # scoreUrchins will not be called again.
    if all(iconCount[num] == player.killedUrchinCount for num, player in enumerate(playerList)):
        return False, iconCount, scoreText, iconCountText, highScore
    else:
        return True, iconCount, scoreText, iconCountText, highScore


def scoreGold(playerList, iconCount, highScore):
    """Update each players' score based on the amount of gold that they have collected.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        iconCount: A list of integers representing how many times each player has gained points from the
            scoreGold function this level.
        highScore: An integer showing the current high score.

    Returns:
        looping: A boolean indicating if scoreLevel should call this function again.
        iconCount: A list of integers representing how many times each player has gained points from the
            scoreGold function this level.
        scoreText: A list of the current scores for each of the players.
        iconCountText: A list of text objects representing each player's iconCount value.
        highScore: An integer showing the current high score.
    """
    scoreText = []
    iconCountText = []
    checkQuitGame()
    checkPauseGameWithInput(playerList)
    if any(player.goldCollectedCount > 0 for player in playerList):
        playSound("count_points.wav")

    # All living players increase their score by 100 points each time this function is called, until it has been called
    # as many times as they've collected gold this level.
    for num, player in enumerate(playerList):
        if player.goldCollectedCount > iconCount[num]:
            player.score += 100
            iconCount[num] += 1
        scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
        iconCountText.append(c.FONT.render("+{:02d}".format(iconCount[num] % 100), False, c.WHITE))
    highScore = compareHighScore(playerList, highScore)

    # Once iconCount has reached the correct number of collected gold for each player, looping is set to False so
    # scoreGold will not be called again.
    if all(iconCount[num] == player.goldCollectedCount for num, player in enumerate(playerList)):
        return False, iconCount, scoreText, iconCountText, highScore
    else:
        return True, iconCount, scoreText, iconCountText, highScore


def checkIfScoresBonusPoints(playerList, scoreBonus):
    """Checks if any player should score the end-of-level bonus points, and if so, which player should.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        scoreBonus: A boolean indicating if the level has been completed within 300 counts of the timer.

    Returns:
        doesScoreBonus: A boolean indicating if the bonus points should be awarded for this level.
        bonusScoringIndex: An integer indicating which player should score the bonus points.
    """

    # If only one player is playing, bonus points are scored if scoreBonus is True.
    # Otherwise, bonus points are only awarded if one player has collected more gold than any other player.
    if len(playerList) == 1:
        if scoreBonus:
            return True, 0
    else:
        for num, player in enumerate(playerList):
            if all(player.goldCollectedCount > otherPlayer.goldCollectedCount for otherPlayer in playerList if
                   otherPlayer != player):
                return True, num
    return False, 0


def compareHighScore(playerList, highScore):
    """Compare the players' current scores with the stored high score.

    If a player has a higher score than the high score, the current high score value is updated.
    This does not update the high score saved in the clu_high_score.txt file.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        highScore: An integer showing the current high score.

    Returns:
        highScore: An integer showing the current high score.
    """
    for player in playerList:
        if player.score > highScore:
            highScore = player.score
    return highScore
