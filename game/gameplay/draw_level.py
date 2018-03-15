import pygame as pg
import sys

from game.gameplay.level import BonusLevel
from game.gameplay.state import checkPauseGame, checkQuitGame
from game.sprites.gold import GoldSprite
from game.sprites.display import FullDisplaySprite, HalfDisplaySprite
from game.tools.asset_cache import playSound
import game.tools.constants as c
from game.tools.controls import controlsDicts


playerFontColors = [c.HOT_PINK, c.GREEN, c.BLUE, c.YELLOW]


def blitLevelData(playerList, level, goldCount, time, levelCount, highScore, animate=False, scrolling=False):
    """Draw the level data to the screen. If scrolling is True, gradually scroll the level data off-screen.

    This includes the time remaining, gold remaining, players' lives, black hole sprites, and the level image.
    Black hole sprites are included, as they are the only sprites drawn before the level begins.
    If scrolling is True, this also includes all gold sprites.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        level: A Level object representing the current level being played.
        goldCount: An integer representing how many gold sprites are not yet revealed.
        time: An integer representing the time the players have remaining to complete the level.
        levelCount: An integer storing the current number of levels played this game.
        highScore: An integer showing the current high score.
        animate: A boolean indicating if this function should update the gold and black hole sprites, causing
            them to be animated.
            This is only to be set to True when the level is completed or all players have run out of lives, as
            the main playLevel function automatically updates all sprites on its own in all other cases.
        scrolling: A boolean indicating if the screen should scroll upwards.
    """
    playerLivesData = []
    for num, player in enumerate(playerList):
        playerLivesData.append([c.FONT.render("<", False, playerFontColors[num]),
                                c.FONT.render("{}".format(min(player.lives, 9)), False, c.WHITE),
                                c.FONT.render(">", False, playerFontColors[num])])
    # The gold count is written with two digits. The time remaining is written with three digits.

    bonusText = c.FONT.render("BONUS!", False, c.WHITE)
    goldText = c.FONT.render("LAST,{:02d}".format(goldCount), False, c.WHITE)
    timeText = c.FONT.render("TIME,{:03d}".format(time), False, c.WHITE)
    # The location of where the players' lives are shown depends on the number of players.
    # If there are one or two players, player one's lives are displayed on the left and player two's on the right
    # If there are three or four players, player one's lives are displayed on the far left, player two's on the
    # mid-left, player three's on the mid-right, and player four's on the far right.

    if len(playerList) < 3:
        livesDataCoordinates = [(42, 16), (428, 16)]
    else:
        livesDataCoordinates = [(5, 16), (62, 16), (408, 16), (467, 16)]

    if not scrolling:
        c.SCREEN.blit(level.image, (0, 0))
        # Bonus levels blit the time count in a different location, and blit the word 'BONUS!' instead of the gold
        # count (Also in a different location from the standard gold count location)    .

        if isinstance(level, BonusLevel):
            c.SCREEN.blit(bonusText, (198, 210))
            c.SCREEN.blit(timeText, (188, 242))
        else:
            c.SCREEN.blit(goldText, (132, 16))
            c.SCREEN.blit(timeText, (262, 16))
            if animate:
                GoldSprite.globalFrameCount += 1
                for hole in c.blackHoleGroup:
                    hole.update()
                for gold in c.goldGroup:
                    gold.update()
                    c.SCREEN.blit(gold.image, gold.coordinates)
            for hole in c.blackHoleGroup:
                c.SCREEN.blit(hole.image, hole.coordinates)

        for fontData, coords in zip(playerLivesData, livesDataCoordinates):
            for num, text in enumerate(fontData):
                # Because the < > symbols should be slightly closer to the number of lives than the standard text width
                # would allow, the life count is placed 13 pixels after the <, and the > is placed 15 frames after the
                # life count.

                c.SCREEN.blit(text, coords)
                coords = (coords[0] + 13, coords[1]) if num == 0 else (coords[0] + 15, coords[1])

    else:
        playerText = []
        scoreText = []
        scrollCount = pausedPlayerNumber = 0
        level.isFlashing = False
        level.image = level.standardImage

        highScoreText = c.FONT.render("TOP,{:06d}".format(highScore), False, c.WHITE)
        levelText = c.FONT.render("<<<<< CLU,CLU,LAND,,{:02d} >>>>>".format(levelCount % 100), False, c.WHITE)

        for num, player in enumerate(playerList):
            playerText.append(c.FONT.render("< PLAYER {} >".format(num), False, c.WHITE))
            scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
            if len(playerList) < 3:
                FullDisplaySprite(num + 1)
            else:
                HalfDisplaySprite(num + 1)

        if len(playerList) < 3:
            playerTextCoordinates = [(162, 50), (162, 274)]
            scoreDataCoordinates = [(240, 626), (240, 850)]
        else:
            playerTextCoordinates = [(38, 52), (292, 52), (38, 276), (292, 276)]
            scoreDataCoordinates = [(50, 608), (304, 608), (50, 832), (304, 832)]

        while scrollCount < 448:
            pausedPlayerNumber = checkPauseGame(pausedPlayerNumber)
            checkQuitGame()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    for num, player in enumerate(playerList):
                        if event.key == controlsDicts[num]["pause"] and player.playerState != c.PlayerStates.DEAD:
                            # Players who have run out of lives cannot pause the game.
                            # After pausing, the queue is cleared to ensure that no keys pressed during the game
                            # preparing to pause take effect while paused.

                            pg.mixer.music.pause()
                            playSound("pause_unpause.wav")
                            pausedPlayerNumber = num + 1
                            pg.time.delay(1000)
                            pg.event.clear()

            # If scrolling is True, then all of the level data scrolls up off-screen six pixels every frame until
            # it is all completely off-screen.
            # The gold and black hole sprites still update every frame to continue to animate them, as the main
            # playLevel function is not called during this loop.

            c.SCREEN.blit(level.image, (0, 0 - scrollCount))
            GoldSprite.globalFrameCount += 1
            if isinstance(level, BonusLevel):
                c.SCREEN.blit(bonusText, (198, 210 - scrollCount))
                c.SCREEN.blit(timeText, (188, 242 - scrollCount))
            else:
                c.SCREEN.blit(goldText, (132, 16 - scrollCount))
                c.SCREEN.blit(timeText, (262, 16 - scrollCount))
                c.SCREEN.blit(highScoreText, (262, 674 - scrollCount))
                c.SCREEN.blit(timeText, (74, 674 - scrollCount))
                c.SCREEN.blit(levelText, (234, 642 - scrollCount))
                for hole in c.blackHoleGroup:
                    hole.update()
                    c.SCREEN.blit(hole.image, (hole.coordinates[0], hole.coordinates[1] - scrollCount))
            for gold in c.goldGroup:
                gold.update()
                c.SCREEN.blit(gold.image, (gold.coordinates[0], gold.coordinates[1] - scrollCount))
            for display in c.textGroup:
                display.update()
            for fontData, coords in zip(playerLivesData, livesDataCoordinates):
                for num, text in enumerate(fontData):
                    c.SCREEN.blit(text, (coords[0], coords[1] - scrollCount))
                    coords = (coords[0] + 13, coords[1] - scrollCount) if num == 0 else\
                        (coords[0] + 15, coords[1] - scrollCount)
            for fontData, coords in zip(playerText, playerTextCoordinates):
                c.SCREEN.blit(text, (coords[0], coords[1] - scrollCount))
            for fontData, coords in zip(scoreText, scoreDataCoordinates):
                c.SCREEN.blit(text, (coords[0], coords[1] - scrollCount))
            scrollCount += 6
            pg.display.update()
            c.CLOCK.tick(c.FPS)


# def drawLevelEnd(playerList, level, levelCount, time, score):
#     frameCount = pausedPlayerNumber = 0
#     playerLivesEndData = []
#     for num, player in enumerate(playerList):
#         playerLivesEndData.append([c.FONT.render("<", False, c.WHITE),
#                                    c.FONT.render("{}".format(min(player.lives, 9)), False, c.WHITE),
#                                    c.FONT.render(">", False, c.WHITE)])
#         if len(playerList) < 3:
#             player.coordinates = (0, 0)
#         else:
#             player.coordinates = (0, 0)
#     if len(playerList) < 3:
#         playerTextCoords = [(162, 50), (162, 274)]
#         scoreCoords = [(240, 98), (240, 322)]
#         livesCoords = [(146, 98), (146, 322)]
#         iconCoords = [(96, 134), (96, 358)]
#         iconTextCoords = [(146, 148), (146, 372)]
#         bonusTextCoords = [(240, 148), (240, 372)]
#         bonusScoreCoords = [(362, 148), (362, 372)]
#     else:
#         playerTextCoords = [(38, 52), (292, 52), (38, 276), (292, 276)]
#         scoreCoords = [(50, 80), (304, 80), (50, 304), (304, 304)]
#         livesCoords = [(70, 116), (324, 116), (70, 340), (324, 340)]
#         iconCoords = [(16, 144), (270, 144), (16, 368), (270, 368)]
#         iconTextCoords = [(70, 156), (324, 156), (70, 380), (324, 380)]
#         bonusTextCoords = [(134, 116), (388, 116), (134, 340), (388, 340)]
#         bonusScoreCoords = [(154, 156), (408, 156), (154, 380), (408, 380)]
#
#     # time - 10 every 4 frames
#     playerText = []
#     for num in range(len(playerList)):
#         playerText.append(c.FONT.render("< PLAYER {} >".format(num), False, c.WHITE))
#     timeText = c.FONT.render("TIME,{:03d}".format(time), False, c.WHITE)
#     highScoreText = c.FONT.render("TOP,{:06d}".format(score), False, c.WHITE)
#     levelText = c.FONT.render("<<<<< CLU,CLU,LAND,,{:02d} >>>>>".format(levelCount % 100), False, c.WHITE)
#     while True:
#         pausedPlayerNumber = checkPauseGame(pausedPlayerNumber)
#         checkQuitGame()
#         for event in pg.event.get():
#             if event.type == pg.KEYDOWN:
#                 for num, player in enumerate(playerList):
#                     if event.key == controlsDicts[num]["pause"] and player.playerState != c.PlayerStates.DEAD:
#                         # Players who have run out of lives cannot pause the game.
#                         # After pausing, the queue is cleared to ensure that no keys pressed during the game
#                         # preparing to pause take effect while paused.
#
#                         pg.mixer.music.pause()
#                         playSound("pause_unpause.wav")
#                         pausedPlayerNumber = num + 1
#                         pg.time.delay(1000)
#                         pg.event.clear()
#
#         # If scrolling is True, then all of the level data scrolls up off-screen six pixels every frame until
#         # it is all completely off-screen.
#         # The gold and black hole sprites still update every frame to continue to animate them, as the main
#         # playLevel function is not called during this loop.
#
#         # if isinstance(level, BonusLevel):
#         #     c.SCREEN.blit(bonusText, (198, 210 - scrollCount))
#         #     c.SCREEN.blit(timeText, (188, 242 - scrollCount))
#         else:
#             c.SCREEN.blit(goldText, (132, 16 - scrollCount))
#             c.SCREEN.blit(timeText, (262, 16 - scrollCount))
#             for hole in c.blackHoleGroup:
#                 hole.update()
#                 c.SCREEN.blit(hole.image, (hole.coordinates[0], hole.coordinates[1] - scrollCount))
#         for gold in c.goldGroup:
#             gold.update()
#             c.SCREEN.blit(gold.image, (gold.coordinates[0], gold.coordinates[1] - scrollCount))
#         for fontData, coords in zip(playerLivesData, livesDataCoordinates):
#             for num, text in enumerate(fontData):
#                 c.SCREEN.blit(text, (coords[0], coords[1] - scrollCount))
#                 coords = (coords[0] + 13, coords[1] - scrollCount) if num == 0 else \
#                     (coords[0] + 15, coords[1] - scrollCount)
#         frameCount += 6
#         pg.display.update()
#         c.CLOCK.tick(c.FPS)

