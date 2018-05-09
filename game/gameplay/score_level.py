import pygame as pg

from game.gameplay.state import checkQuitGame, checkPauseGameWithInput
from game.tools.asset_cache import playSound
import game.tools.constants as c


def scoreLevel(playerList, level, time, highScore, stepToScore=0):
    iconCountText = []
    if len(playerList) < 3:
        scoreDataCoordinates = [(240, 95), (240, 319)]
        scoreIconCountCoordinates = [(140, 143), (140, 367)]
    else:
        scoreDataCoordinates = [(55, 74), (309, 74), (55, 298), (309, 298)]
        scoreIconCountCoordinates = [(64, 147), (320, 147), (64, 371), (320, 371)]
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
    scoreText = []
    timeText = c.FONT.render("TIME,{:03d}".format(time), False, c.WHITE)
    checkQuitGame()
    checkPauseGameWithInput(playerList)
    for player in playerList:
        if player.lives > 0:
            player.score += 10
        scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
    highScore = checkHighScore(playerList, highScore)
    time = max(0, time - 10 - (time % 10))
    pg.draw.rect(c.SCREEN, level.backgroundColor, pg.rect.Rect(160, 224, 48, 16))
    c.SCREEN.blit(timeText, (82, 224))
    if time == 0:
        return False, time, scoreText, highScore
    else:
        playSound("count_points.wav")
        return True, time, scoreText, highScore


def scoreUrchins(playerList, iconCount, highScore):
    scoreText = []
    iconCountText = []
    checkQuitGame()
    checkPauseGameWithInput(playerList)
    if any(player.killedUrchinCount > 0 for player in playerList):
        playSound("count_points.wav")
    for num, player in enumerate(playerList):
        if player.killedUrchinCount > iconCount[num]:
            player.score += 500
            iconCount[num] += 1
        scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
        iconCountText.append(c.FONT.render("+{:02d}".format(iconCount[num] % 100), False, c.WHITE))
    highScore = checkHighScore(playerList, highScore)
    if all(iconCount[num] == player.killedUrchinCount for num, player in enumerate(playerList)):
        return False, iconCount, scoreText, iconCountText, highScore
    else:
        playSound("count_points.wav")
        return True, iconCount, scoreText, iconCountText, highScore


def scoreGold(playerList, iconCount, highScore):
    scoreText = []
    iconCountText = []
    checkQuitGame()
    checkPauseGameWithInput(playerList)
    if any(player.goldCollectedCount > 0 for player in playerList):
        playSound("count_points.wav")
    for num, player in enumerate(playerList):
        if player.goldCollectedCount > iconCount[num]:
            player.score += 100
            iconCount[num] += 1
        scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
        iconCountText.append(c.FONT.render("+{:02d}".format(iconCount[num] % 100), False, c.WHITE))
    highScore = checkHighScore(playerList, highScore)
    if all(iconCount[num] == player.goldCollectedCount for num, player in enumerate(playerList)):
        return False, iconCount, scoreText, iconCountText, highScore
    else:
        playSound("count_points.wav")
        return True, iconCount, scoreText, iconCountText, highScore


def checkScoreBonusPoints(playerList, scoreBonus):
    if len(playerList) == 1:
        if scoreBonus:
            return True, 0
    else:
        for num, player in enumerate(playerList):
            if all(player.goldCollectedCount > otherPlayer.goldCollectedCount for otherPlayer in playerList if
                   otherPlayer != player):
                return True, num
    return False, 0


def checkHighScore(playerList, highScore):
    for player in playerList:
        if player.score > highScore:
            highScore = player.score
    return highScore
