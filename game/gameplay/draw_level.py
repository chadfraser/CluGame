import pygame as pg

from game.gameplay.level import BonusLevel
from game.gameplay.score_level import scoreLevel, checkIfScoresBonusPoints, compareHighScore
from game.gameplay.state import checkPauseGameWithInput, checkQuitGame
from game.sprites.gold import GoldSprite
from game.sprites.display import DisplayIconSprite, FullDisplaySprite, HalfDisplaySprite
from game.tools.asset_cache import playSound
import game.tools.constants as c


playerFontColors = [c.HOT_PINK, c.GREEN, c.BLUE, c.YELLOW]


def blitLevelData(playerList, level, goldCount, time, animate=False):
    """Draw the level data to the screen.

    This includes the time remaining, gold remaining, players' lives, black hole sprites, and the level image.
    Black hole sprites are included, as they are the only sprites drawn before the level begins.
    If animate is True, this also includes all gold sprites.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        level: A Level object representing the current level being played.
        goldCount: An integer representing how many gold sprites are currently unrevealed (either invisible or
            face-down).
        time: An integer representing the time the players have remaining to complete the level.
        animate: A boolean indicating if this function should update the gold and black hole sprites, causing
            them to be animated.
            This is only to be set to True when the level is completed or all players have run out of lives, as
            the main playLevel function automatically updates all sprites on its own in all other cases.
    """
    playerLivesData = []
    for num, player in enumerate(playerList):
        playerLivesData.append([c.FONT.render("<", False, playerFontColors[num]),
                                c.FONT.render("{}".format(min(player.lives, 9)), False, c.WHITE),
                                c.FONT.render(">", False, playerFontColors[num])])
    timeText = c.FONT.render("TIME,{:03d}".format(time), False, c.WHITE)

    # The location of where the players' lives are shown depends on the number of players.
    # If there are one or two players, player one's lives are displayed on the left and player two's on the right
    # If there are three or four players, player one's lives are displayed on the far left, player two's on the
    # mid-left, player three's on the mid-right, and player four's on the far right.
    if len(playerList) < 3:
        livesDataCoordinates = [(42, 16), (428, 16)]
    else:
        livesDataCoordinates = [(5, 16), (62, 16), (408, 16), (467, 16)]

    c.SCREEN.blit(level.image, (0, 0))

    # Bonus levels blit the time count in a different location, and blit the word 'BONUS!' instead of the gold
    # count (Also in a different location from the standard gold count location).
    if isinstance(level, BonusLevel):
        bonusWordText = c.FONT.render("BONUS!", False, c.WHITE)
        c.SCREEN.blit(bonusWordText, (210, 210))
        c.SCREEN.blit(timeText, (192, 242))
    else:
        goldText = c.FONT.render("LAST,{:02d}".format(goldCount), False, c.WHITE)
        c.SCREEN.blit(goldText, (132, 16))
        c.SCREEN.blit(timeText, (262, 16))
    if animate:
        GoldSprite.globalFrameCount += 1
        for hole in c.blackHoleGroup:
            hole.update()
        for gold in c.goldGroup:
            gold.update()
            c.SCREEN.blit(gold.image, gold.coordinates)
        for textSprite in c.textGroup:
            textSprite.update()
            c.SCREEN.blit(textSprite.image, textSprite.coordinates)
    for hole in c.blackHoleGroup:
        c.SCREEN.blit(hole.image, hole.coordinates)
    for trap in c.rubberGroup:
        c.SCREEN.blit(trap.image, trap.coordinates)

    # Because the < > symbols should be slightly closer to the number of lives than the standard text width would
    # allow, the life count is placed 13 pixels after the <, and the > is placed 15 frames after the life count.
    for fontData, coords in zip(playerLivesData, livesDataCoordinates):
        for num, text in enumerate(fontData):
            c.SCREEN.blit(text, coords)
            coords = (coords[0] + 13, coords[1]) if num == 0 else (coords[0] + 15, coords[1])


def scrollLevelData(playerList, level, goldCount, time, levelCount, highScore):
    """Draw the level data to the screen as it scrolls off-screen.

    This includes the time remaining, gold remaining, players' lives, black hole sprites, gold sprites, text
    sprites, trap sprites, and the level image.
    After the level scrolls off-screen, the end-of-level data is drawn to the screen, which includes the current
    high score and level count.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        level: A Level object representing the current level being played.
        goldCount: An integer representing how many gold sprites are currently unrevealed (either invisible or
            face-down).
        time: An integer representing the time the players have remaining to complete the level.
                levelCount: An integer storing how many levels the player has currently played.
        levelCount: An integer storing how many levels the player has currently played.
        highScore: An integer showing the current high score.
    """
    playerLivesData = []
    playerTextData = []
    playerScoreData = []
    scrollCount = 0
    level.initialize()

    for num, player in enumerate(playerList):
        playerLivesData.append([c.FONT.render("<", False, playerFontColors[num]),
                                c.FONT.render("{}".format(min(player.lives, 9)), False, c.WHITE),
                                c.FONT.render(">", False, playerFontColors[num])])
    timeText = c.FONT.render("TIME,{:03d}".format(time), False, c.WHITE)

    # The location of where the players' lives are shown depends on the number of players.
    # If there are one or two players, player one's lives are displayed on the left and player two's on the right
    # If there are three or four players, player one's lives are displayed on the far left, player two's on the
    # mid-left, player three's on the mid-right, and player four's on the far right.
    if len(playerList) < 3:
        livesDataCoordinates = [(42, 16), (428, 16)]
    else:
        livesDataCoordinates = [(5, 16), (62, 16), (408, 16), (467, 16)]

    highScore = compareHighScore(playerList, highScore)
    highScoreText = c.FONT.render("TOP,{:06d}".format(highScore), False, c.WHITE)
    levelText = c.FONT.render("<<<<< CLU,CLU,LAND,,{:02d} >>>>>".format(levelCount % 100), False, c.WHITE)

    if len(playerList) < 3:
        playerTextCoordinates = [(162, 497), (162, 721)]
        scoreDataCoordinates = [(240, 545), (240, 769)]
    else:
        playerTextCoordinates = [(37, 496), (292, 496), (37, 721), (292, 721)]
        scoreDataCoordinates = [(55, 524), (309, 524), (55, 748), (309, 748)]

    for num, player in enumerate(playerList):
        playerTextData.append(c.FONT.render("< PLAYER {} >".format(num + 1), False, c.WHITE))
        playerScoreData.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))

        # Which displays are used in the end-of-level animation depends on the number of players.
        # If there are one or two players, the full-sized displays are used, with player one on top and player two
        # on the bottom.
        # If there are three or four players, the half-sized displays are used, with player one on the top-left, player
        # two on the top-right, player three on the bottom-left, and player four on the bottom-right.
        if len(playerList) < 3:
            FullDisplaySprite(num + 1)
        else:
            HalfDisplaySprite(num + 1)

    # Every sprite scrolls upwards 6 pixels per frame until it is all completely off-screen.
    # This takes 75 frames in total.
    while scrollCount < 448:
        c.SCREEN.fill(level.backgroundColor)
        checkQuitGame()
        checkPauseGameWithInput(playerList)

        c.SCREEN.blit(level.image, (0, 0 - scrollCount))
        GoldSprite.globalFrameCount += 1

        # Bonus levels blit the time count in a different location, and blit the word 'BONUS!' instead of the gold
        # count (Also in a different location from the standard gold count location).
        if isinstance(level, BonusLevel):
            bonusWordText = c.FONT.render("BONUS!", False, c.WHITE)
            c.SCREEN.blit(bonusWordText, (210, 210 - scrollCount))
            c.SCREEN.blit(timeText, (192, 242 - scrollCount))
        else:
            goldText = c.FONT.render("LAST,{:02d}".format(goldCount), False, c.WHITE)
            c.SCREEN.blit(goldText, (132, 16 - scrollCount))
            c.SCREEN.blit(timeText, (262, 16 - scrollCount))

            # The highScoreText, levelText, and another copy of timeText begin in the proper location off-screen so
            # that they scroll up to the proper location in the end-of-level screen.
            c.SCREEN.blit(highScoreText, (254, 674 - scrollCount))
            c.SCREEN.blit(timeText, (82, 674 - scrollCount))
            c.SCREEN.blit(levelText, (38, 642 - scrollCount))

            # The gold, black hole, and text sprites still update every frame as they scroll, so they continue being
            # animated, as the main playLevel function is not called during this loop.
            for hole in c.blackHoleGroup:
                hole.update()
                c.SCREEN.blit(hole.image, (hole.coordinates[0], hole.coordinates[1] - scrollCount))
        for gold in c.goldGroup:
            gold.update()
            c.SCREEN.blit(gold.image, (gold.coordinates[0], gold.coordinates[1] - scrollCount))
        for textSprite in c.textGroup:
            textSprite.update()
            c.SCREEN.blit(textSprite.image, (textSprite.coordinates[0], textSprite.coordinates[1] - scrollCount))
        for display in c.displayGroup:
            c.SCREEN.blit(display.image, (display.coordinates[0], display.coordinates[1] - scrollCount))
        for trap in c.rubberGroup:
            c.SCREEN.blit(trap.image, trap.coordinates)

        # Because the < > symbols should be slightly closer to the number of lives than the standard text width would
        # allow, the life count is placed 13 pixels after the <, and the > is placed 15 frames after the life count.
        for fontData, coords in zip(playerLivesData, livesDataCoordinates):
            for num, text in enumerate(fontData):
                c.SCREEN.blit(text, (coords[0], coords[1] - scrollCount))
                coords = (coords[0] + 13, coords[1] - scrollCount) if num == 0 else\
                    (coords[0] + 15, coords[1] - scrollCount)
        for text, coords in zip(playerTextData, playerTextCoordinates):
            c.SCREEN.blit(text, (coords[0], coords[1] - scrollCount))
        for text, coords in zip(playerScoreData, scoreDataCoordinates):
            c.SCREEN.blit(text, (coords[0], coords[1] - scrollCount))

        scrollCount += 6
        pg.display.update()
        c.CLOCK.tick(c.FPS)


def blitLevelEndData(playerList, level, time, levelCount, highScore, scoreBonus):
    """Draw the end-of-level data to the screen, while calling the functions to increase the players' scores as
    required.

    This includes the players' displays and sprites, their lives, their scores, the time remaining, level count,
    and the current high score.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        level: A Level object representing the current level being played.
        time: An integer representing the time the players have remaining to complete the level.
                levelCount: An integer storing how many levels the player has currently played.
        levelCount: An integer storing how many levels the player has currently played.
        highScore: An integer showing the current high score.
        scoreBonus: A boolean indicating if the level has been completed within 300 counts of the timer.
    """
    playerTextData = []
    playerScoreData = []
    playerLivesData = []
    playerDisplayIcons = []
    iconCountText = []
    frameCount = 0

    levelText = c.FONT.render("<<<<< CLU,CLU,LAND,,{:02d} >>>>>".format(levelCount % 100), False, c.WHITE)
    timeText = c.FONT.render("TIME,{:03d}".format(time), False, c.WHITE)

    if len(playerList) < 3:
        playerTextCoordinates = [(162, 47), (162, 271)]
        scoreDataCoordinates = [(240, 95), (240, 319)]
        livesDataCoordinates = [(140, 95), (140, 319)]
        playerSpriteCoordinates = [(88, 79), (88, 303)]
        displayIconTextCoordinates = [(140, 143), (140, 367)]
        bonusTextCoordinates = [(236, 143), (236, 367)]
        bonusScoreCoordinates = [(340, 143), (340, 367)]
        bonusLevelCompletionTextCoordinates = [(220, 127), (220, 351)]
        bonusLevelCompletionScoreCoordinates = [(340, 127), (340, 351)]
    else:
        playerTextCoordinates = [(37, 46), (292, 46), (37, 271), (292, 271)]
        scoreDataCoordinates = [(55, 74), (309, 74), (55, 298), (309, 298)]
        livesDataCoordinates = [(70, 111), (327, 111), (70, 335), (327, 335)]
        playerSpriteCoordinates = [(17, 99), (273, 99), (17, 323), (273, 323)]
        displayIconTextCoordinates = [(64, 147), (320, 147), (64, 371), (320, 371)]
        bonusTextCoordinates = [(150, 135), (407, 135), (150, 358), (407, 358)]
        bonusScoreCoordinates = [(150, 151), (407, 151), (150, 374), (407, 374)]
        bonusLevelCompletionTextCoordinates = [(134, 103), (391, 103), (134, 327), (391, 327)]
        bonusLevelCompletionScoreCoordinates = [(150, 119), (407, 119), (150, 343), (407, 343)]

    # All of the bonus font objects default to an empty string. They are only updated as a relevant string if the
    # appropriate bonus is earned.
    bonusEarnedText = bonusScoreText = bonusLevelCompletionText = bonusLevelCompletionScore =\
        c.FONT.render("", False, c.WHITE)
    doesScoreBonus, bonusScoringIndex = checkIfScoresBonusPoints(playerList, scoreBonus)

    # The bonus completion points are only earned if the players collect all 66 gold bars on the bonus stage.
    if isinstance(level, BonusLevel) and sum([player.goldCollectedCount for player in playerList]) == 66:
        doesScoreBonusCompletion = True
    else:
        doesScoreBonusCompletion = False

    for num, player in enumerate(playerList):
        playerDisplayIcons.append(DisplayIconSprite(num + 1, len(playerList)))
        playerTextData.append(c.FONT.render("< PLAYER {} >".format(num + 1), False, c.WHITE))
        playerScoreData.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
        playerLivesData.append([c.FONT.render("<", False, c.WHITE),
                                c.FONT.render("{}".format(min(player.lives, 9)), False, c.WHITE),
                                c.FONT.render(">", False, c.WHITE)])
        player.coordinates = playerSpriteCoordinates[num]

        # Which displays are used in the end-of-level animation depends on the number of players.
        # If there are one or two players, the full-sized displays are used, with player one on top and player two
        # on the bottom.
        # If there are three or four players, the half-sized displays are used, with player one on the top-left, player
        # two on the top-right, player three on the bottom-left, and player four on the bottom-right.
        if len(playerList) < 3:
            FullDisplaySprite(num + 1)
        else:
            HalfDisplaySprite(num + 1)

    while True:
        frameCount += 1

        # If none of the players have any lives remaining, do not score or animate their sprites in the end-of-level
        # screen.
        if any(player.lives > 0 for player in playerList):
            if frameCount == 32:
                highScore, iconCount = scoreLevel(playerList, level, time, highScore, stepToScore=0)
                timeText = c.FONT.render("TIME,000", False, c.WHITE)

            # These steps are skipped during bonus levels, as there are no enemies to score.
            elif frameCount == 64 and not isinstance(level, BonusLevel):
                for icon in playerDisplayIcons:
                    icon.setIconImage()
                iconCountText = [c.FONT.render("+00", False, c.WHITE) for _ in playerList]
            elif frameCount == 96 and not isinstance(level, BonusLevel):
                highScore, iconCount = scoreLevel(playerList, level, time, highScore, stepToScore=1)
                iconCountText = []
                for num, player in enumerate(playerList):
                    iconCountText.append(c.FONT.render("+{:02d}".format(iconCount[num] % 100), False,
                                                       c.WHITE))

            elif frameCount == 128:
                iconCountText = [c.FONT.render("+00", False, c.WHITE) for _ in playerList]
                for icon in playerDisplayIcons:
                    icon.setIconImage()

                    # This method is called again during a bonus level, to skip the urchin icon and move directly to
                    # the gold icon.
                    if isinstance(level, BonusLevel):
                        icon.setIconImage()
            elif frameCount == 160:
                highScore, iconCount = scoreLevel(playerList, level, time, highScore, stepToScore=2)
                iconCountText = []
                for player in playerList:
                    iconCountText.append(c.FONT.render("+{:02d}".format(player.goldCollectedCount % 100), False,
                                                       c.WHITE))

            elif frameCount == 188:
                for player in playerList:
                    player.setLevelEndCountImage()
                if doesScoreBonus:
                    playerList[bonusScoringIndex].score += 2000
                    if playerList[bonusScoringIndex].score > highScore:
                        highScore = playerList[bonusScoringIndex].score
                    playSound("earn_bonus.wav")
                    bonusEarnedText = c.FONT.render("BONUS", False, c.WHITE)
                    bonusScoreText = c.FONT.render("2000!", False, c.WHITE)
                if doesScoreBonusCompletion:
                    for player in playerList:
                        if player.lives > 0:
                            player.score += 3000

                    # To prevent the earn_bonus sound from playing multiple times at once, it only plays here if the
                    # doesScoreBonus is False (since it should already be playing from the above block of code if it is
                    # True).
                    if not doesScoreBonus:
                        playSound("earn_bonus.wav")
                    bonusLevelCompletionText = c.FONT.render("PERFECT", False, c.WHITE)
                    bonusLevelCompletionScore = c.FONT.render("3000!", False, c.WHITE)
        if frameCount == 442:
            return

        scoreText = []

        # Every frame, update the text displaying the players' scores and the high score, in case these values have
        # changed since the previous frame.
        for player in playerList:
            scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
        highScore = compareHighScore(playerList, highScore)
        highScoreText = c.FONT.render("TOP,{:06d}".format(highScore), False, c.WHITE)

        c.SCREEN.fill(level.backgroundColor)
        checkQuitGame()
        checkPauseGameWithInput(playerList)

        c.SCREEN.blit(highScoreText, (254, 224))
        c.SCREEN.blit(timeText, (82, 224))
        c.SCREEN.blit(levelText, (38, 192))
        for display in c.displayGroup:
            c.SCREEN.blit(display.image, (display.coordinates[0], display.coordinates[1] - 450))
        for textSprite in c.textGroup:
            c.SCREEN.blit(textSprite.image, (textSprite.coordinates[0], textSprite.coordinates[1]))
        for player in c.playerGroup:
            if frameCount < 188:
                player.update()
            c.SCREEN.blit(player.image, player.coordinates)

        # Because the < > symbols should be slightly closer to the number of lives than the standard text width would
        # allow, the life count is placed 13 pixels after the <, and the > is placed 15 frames after the life count.
        for fontData, coords in zip(playerLivesData, livesDataCoordinates):
            for num, text in enumerate(fontData):
                c.SCREEN.blit(text, (coords[0], coords[1]))
                coords = (coords[0] + 13, coords[1]) if num == 0 else (coords[0] + 15, coords[1])

        for text, coords in zip(playerTextData, playerTextCoordinates):
            c.SCREEN.blit(text, (coords[0], coords[1]))
        for text, coords in zip(scoreText, scoreDataCoordinates):
            c.SCREEN.blit(text, (coords[0], coords[1]))

        # During regular levels, the score icon and its text should be visible from frame 75 onwards, when enemies are
        # scored.
        # During bonus levels, the score icon and its text should be visible from frame 139 onwards, when gold is
        # scored.
        if (frameCount > 74 and not isinstance(level, BonusLevel)) or frameCount > 138:
            for text, coords in zip(iconCountText, displayIconTextCoordinates):
                c.SCREEN.blit(text, (coords[0], coords[1]))

        if frameCount > 188:
            c.SCREEN.blit(bonusEarnedText, bonusTextCoordinates[bonusScoringIndex])
            c.SCREEN.blit(bonusScoreText, bonusScoreCoordinates[bonusScoringIndex])
            for (coords, player) in zip(bonusLevelCompletionTextCoordinates, playerList):
                if player.lives > 0:
                    c.SCREEN.blit(bonusLevelCompletionText, (coords[0], coords[1]))
            for (coords, player) in zip(bonusLevelCompletionScoreCoordinates, playerList):
                if player.lives > 0:
                    c.SCREEN.blit(bonusLevelCompletionScore, (coords[0], coords[1]))

        pg.display.update()
        c.CLOCK.tick(c.FPS)
