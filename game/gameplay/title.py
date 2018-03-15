import pygame as pg
import sys

from game.demo.demo import animateDemo
from game.gameplay.menu import chooseNumberOfPlayers, displayChangeControlMenu
from game.gameplay.play_level import playLevel
from game.gameplay.level import getLevelOrder
from game.gameplay.state import checkQuitGame
from game.sprites.title import TitleBoxSprite, TitleTextSprite
from game.sprites.player import PlayerSprite
from game.sprites.player_arm import PlayerArmSprite
import game.tools.constants as c
from game.tools.controls import controlsDicts
from game.tools.scores import getHighScore


def displayTitleScreen(playerOneScore=0, playerTwoScore=0, playerThreeScore=0, playerFourScore=0):
    """Display the title screen, including all players' current scores and the recorded high score.

    Args:
        playerOneScore: An integer representing the most recent score earned by player one.
            Defaults to 0.
        playerTwoScore: An integer representing the most recent score earned by player two.
            Defaults to 0.
        playerThreeScore: An integer representing the most recent score earned by player three.
            Defaults to 0.
        playerFourScore: An integer representing the most recent score earned by player four.
            Defaults to 0.
    """
    highScore = getHighScore()
    titleImageOne = TitleTextSprite()
    titleImageTwo = TitleTextSprite(False)
    subtitleImage = TitleBoxSprite()

    subtitleText = c.FONT.render("SECRETS OF OLD CLU CLU LAND", False, c.WHITE)
    playText = c.FONT.render("PLAY GAME", False, c.CYAN)
    changeText = c.FONT.render("CHANGE CONTROLS", False, c.CYAN)
    cursorText = c.FONT.render(">", False, c.ORANGE)
    highScoreText = c.FONT.render("TOP,{:06d}".format(highScore), False, c.PINK)
    playerScoreTexts = [c.FONT.render("I,{:06d}".format(playerOneScore), False, c.WHITE),
                        c.FONT.render("~,{:06d}".format(playerTwoScore), False, c.WHITE),
                        c.FONT.render("{{,{:06d}".format(playerThreeScore), False, c.WHITE),
                        c.FONT.render("}},{:06d}".format(playerFourScore), False, c.WHITE)]
    scoreTextCoordinates = [(62, 400), (307, 400), (62, 425), (307, 425)]

    while True:
        # If the player does not select an option within 740 frames, the demo is animated. After the demo, or after the
        # player has made a selection, looping is set to False so this loop resets the music, frameCount, cursor
        # location, and title images

        pg.mixer.music.load(c.TITLE_MUSIC)
        pg.mixer.music.play()
        cursorLocation = (150, 310)
        titleImageOne.setTitleImageBackwards()
        titleImageTwo.setTitleImageBackwards()
        subtitleImage.setTitleImage()
        frameCount = 0
        looping = True

        while looping:
            frameCount += 1
            checkQuitGame()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == controlsDicts[0]["pause"] or event.key == pg.K_RETURN:
                        if cursorLocation == (150, 310):
                            numberOfPlayers = chooseNumberOfPlayers(titleImageOne, titleImageTwo, subtitleImage,
                                                                    "GAME")
                            startGame(numberOfPlayers, highScore)
                        else:
                            numberOfPlayers = chooseNumberOfPlayers(subtitleImage, titleImageOne, titleImageTwo,
                                                                    "CONTROLS")
                            displayChangeControlMenu(subtitleImage, titleImageOne, titleImageTwo, numberOfPlayers)
                        looping = False
                    elif event.key in [controlsDicts[0]["up"], controlsDicts[0]["down"]]:
                        if cursorLocation == (150, 310):
                            cursorLocation = (100, 335)
                        else:
                            cursorLocation = (150, 310)
            c.SCREEN.fill(c.BLACK)
            c.SCREEN.blit(subtitleText, (42, 275))
            c.SCREEN.blit(playText, (180, 310))
            c.SCREEN.blit(changeText, (130, 335))
            c.SCREEN.blit(cursorText, cursorLocation)
            c.SCREEN.blit(highScoreText, (172, 375))
            for text, coords in zip(playerScoreTexts, scoreTextCoordinates):
                c.SCREEN.blit(text, coords)
            for sprite in [titleImageOne, titleImageTwo, subtitleImage]:
                sprite.update()
                c.SCREEN.blit(sprite.image, sprite.coordinates)
            if frameCount == 740:
                animateDemo()
                looping = False
            pg.display.update()
            c.CLOCK.tick(c.FPS)


def startGame(numberOfPlayers, highScore):
    """Choose how many players will play the game. A random (cycling) order of levels is chosen and played until
    all players are out of lives.

    Args:
        numberOfPlayers: An integer showing how many players will play the game.
        highScore: An integer showing the current high score.
    Returns:
        playerScoresList: A list of the most recent score for each of the four players, set to 0 if that player
            didn't play this game.
    """
    pg.mixer.music.stop()
    playerList = [PlayerSprite(num + 1) for num in range(numberOfPlayers)]
    playerArmList = [PlayerArmSprite(player) for player in playerList]
    gameOverTextStates = [c.TextStates.NOT_REVEALED for _ in range(numberOfPlayers)]
    levelOrder = getLevelOrder()
    levelIndex = 0
    while any(player.playerState != c.PlayerStates.DEAD for player in playerList):
        # This loop continues until all players have run out of lives.
        # If levelIndex is greater than the levelOrder list, it resets to index 1
        # Note that this means the level at index 0 is never replayed, while every other level is played in a repeating
        # pattern.

        playLevel(playerList, playerArmList, levelOrder[levelIndex], 0, gameOverTextStates, highScore)
        levelIndex += 1
        if levelIndex == len(levelOrder):
            levelIndex = 1
    playerScoresList = [player.score for player in playerList]
    while len(playerScoresList) < 4:
        playerScoresList.append(0)
    return playerScoresList
