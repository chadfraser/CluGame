import pygame as pg

from game.gameplay.level import BonusLevel
from game.gameplay.score_level import scoreLevel, checkScoreBonusPoints, checkHighScore
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
    # count (Also in a different location from the standard gold count location)    .

    if isinstance(level, BonusLevel):
        bonusTextWord = c.FONT.render("BONUS!", False, c.WHITE)
        c.SCREEN.blit(bonusTextWord, (210, 210))
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

    for fontData, coords in zip(playerLivesData, livesDataCoordinates):
        for num, text in enumerate(fontData):
            # Because the < > symbols should be slightly closer to the number of lives than the standard text width
            # would allow, the life count is placed 13 pixels after the <, and the > is placed 15 frames after the
            # life count.

            c.SCREEN.blit(text, coords)
            coords = (coords[0] + 13, coords[1]) if num == 0 else (coords[0] + 15, coords[1])


def scrollLevelData(playerList, level, goldCount, time, levelCount, highScore):
    playerLivesData = []
    for num, player in enumerate(playerList):
        playerLivesData.append([c.FONT.render("<", False, playerFontColors[num]),
                                c.FONT.render("{}".format(min(player.lives, 9)), False, c.WHITE),
                                c.FONT.render(">", False, playerFontColors[num])])
    timeText = c.FONT.render("TIME,{:03d}".format(time), False, c.WHITE)

    if len(playerList) < 3:
        livesDataCoordinates = [(42, 16), (428, 16)]
    else:
        livesDataCoordinates = [(5, 16), (62, 16), (408, 16), (467, 16)]

    playerText = []
    scoreText = []
    scrollCount = 0
    level.initialize()

    highScore = checkHighScore(playerList, highScore)
    highScoreText = c.FONT.render("TOP,{:06d}".format(highScore), False, c.WHITE)
    levelText = c.FONT.render("<<<<< CLU,CLU,LAND,,{:02d} >>>>>".format(levelCount % 100), False, c.WHITE)

    if len(playerList) < 3:
        playerTextCoordinates = [(162, 497), (162, 721)]
        scoreDataCoordinates = [(240, 545), (240, 769)]
    else:
        playerTextCoordinates = [(37, 496), (292, 496), (37, 721), (292, 721)]
        scoreDataCoordinates = [(55, 524), (309, 524), (55, 748), (309, 748)]

    for num, player in enumerate(playerList):
        playerText.append(c.FONT.render("< PLAYER {} >".format(num + 1), False, c.WHITE))
        scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
        # Which displays are used in the end-of-level animation depends on the number of players.
        # If there are one or two players, the full-sized displays are used, with player one on top and player two
        # on the bottom.
        # If there are three or four players, the half-sized displays are used, with player one on the top-left, player
        # two on the top-right, player three on the bottom-left, and player four on the bottom-right.

        if len(playerList) < 3:
            FullDisplaySprite(num + 1)
        else:
            HalfDisplaySprite(num + 1)

    while scrollCount < 448:
        c.SCREEN.fill(level.backgroundColor)
        checkQuitGame()
        checkPauseGameWithInput(playerList)
        # All of the level data scrolls up off-screen six pixels every frame until t is all completely off-screen.
        # The gold and black hole sprites still update every frame to continue to animate them, as the main
        # playLevel function is not called during this loop.

        c.SCREEN.blit(level.image, (0, 0 - scrollCount))
        GoldSprite.globalFrameCount += 1
        if isinstance(level, BonusLevel):
            bonusTextWord = c.FONT.render("BONUS!", False, c.WHITE)
            c.SCREEN.blit(bonusTextWord, (210, 210 - scrollCount))
            c.SCREEN.blit(timeText, (192, 242 - scrollCount))
        else:
            goldText = c.FONT.render("LAST,{:02d}".format(goldCount), False, c.WHITE)
            c.SCREEN.blit(goldText, (132, 16 - scrollCount))
            c.SCREEN.blit(timeText, (262, 16 - scrollCount))
            c.SCREEN.blit(highScoreText, (254, 674 - scrollCount))
            c.SCREEN.blit(timeText, (82, 674 - scrollCount))
            c.SCREEN.blit(levelText, (38, 642 - scrollCount))
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
        for fontData, coords in zip(playerLivesData, livesDataCoordinates):
            for num, text in enumerate(fontData):
                c.SCREEN.blit(text, (coords[0], coords[1] - scrollCount))
                coords = (coords[0] + 13, coords[1] - scrollCount) if num == 0 else\
                    (coords[0] + 15, coords[1] - scrollCount)
        for text, coords in zip(playerText, playerTextCoordinates):
            c.SCREEN.blit(text, (coords[0], coords[1] - scrollCount))
        for text, coords in zip(scoreText, scoreDataCoordinates):
            c.SCREEN.blit(text, (coords[0], coords[1] - scrollCount))
        scrollCount += 6
        pg.display.update()
        c.CLOCK.tick(c.FPS)


def blitLevelEndData(playerList, level, time, levelCount, highScore, scoreBonus):
    playerText = []
    scoreText = []
    playerLivesEndData = []
    displayIcons = []
    iconCountText = []
    frameCount = 0

    levelText = c.FONT.render("<<<<< CLU,CLU,LAND,,{:02d} >>>>>".format(levelCount % 100), False, c.WHITE)
    timeText = c.FONT.render("TIME,{:03d}".format(time), False, c.WHITE)

    if len(playerList) < 3:
        playerTextCoordinates = [(162, 47), (162, 271)]
        scoreDataCoordinates = [(240, 95), (240, 319)]
        livesEndDataCoordinates = [(140, 95), (140, 319)]
        playerEndCoordinates = [(88, 79), (88, 303)]
        scoreIconCountCoordinates = [(140, 143), (140, 367)]
        bonusTextCoordinates = [(236, 143), (236, 367)]
        bonusScoreCoordinates = [(340, 143), (340, 367)]
        bonusCompletionTextCoordinates = [(220, 127), (220, 351)]
        bonusCompletionScoreCoordinates = [(340, 127), (340, 351)]
    else:
        playerTextCoordinates = [(37, 46), (292, 46), (37, 271), (292, 271)]
        scoreDataCoordinates = [(55, 74), (309, 74), (55, 298), (309, 298)]
        livesEndDataCoordinates = [(70, 111), (327, 111), (70, 335), (327, 335)]
        playerEndCoordinates = [(17, 99), (273, 99), (17, 323), (273, 323)]
        scoreIconCountCoordinates = [(64, 147), (320, 147), (64, 371), (320, 371)]
        bonusTextCoordinates = [(150, 135), (407, 135), (150, 358), (407, 358)]
        bonusScoreCoordinates = [(150, 151), (407, 151), (150, 374), (407, 374)]
        bonusCompletionTextCoordinates = [(134, 103), (391, 103), (134, 327), (391, 327)]
        bonusCompletionScoreCoordinates = [(150, 119), (407, 119), (150, 343), (407, 343)]

    bonusText = bonusScoreText = bonusCompletionText = bonusCompletionScore = c.FONT.render("", False, c.WHITE)
    doesScoreBonus, bonusScoringIndex = checkScoreBonusPoints(playerList, scoreBonus)
    if isinstance(level, BonusLevel) and sum([player.goldCollectedCount for player in playerList]) == 66:
        doesScoreBonusCompletion = True
    else:
        doesScoreBonusCompletion = False

    for num, player in enumerate(playerList):
        displayIcons.append(DisplayIconSprite(num + 1, len(playerList)))
        playerText.append(c.FONT.render("< PLAYER {} >".format(num + 1), False, c.WHITE))
        scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
        playerLivesEndData.append([c.FONT.render("<", False, c.WHITE),
                                   c.FONT.render("{}".format(min(player.lives, 9)), False, c.WHITE),
                                   c.FONT.render(">", False, c.WHITE)])
        player.coordinates = playerEndCoordinates[num]

        if len(playerList) < 3:
            FullDisplaySprite(num + 1)
        else:
            HalfDisplaySprite(num + 1)

    while True:
        frameCount += 1
        if any(player.lives > 0 for player in playerList):
            if frameCount == 32:
                highScore, iconCount = scoreLevel(playerList, level, time, highScore, stepToScore=0)
                timeText = c.FONT.render("TIME,000", False, c.WHITE)
            elif frameCount == 64 and not isinstance(level, BonusLevel):
                for icon in displayIcons:
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
                for icon in displayIcons:
                    icon.setIconImage()
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
                    bonusText = c.FONT.render("BONUS", False, c.WHITE)
                    bonusScoreText = c.FONT.render("2000!", False, c.WHITE)
                if doesScoreBonusCompletion:
                    for player in playerList:
                        if player.lives > 0:
                            player.score += 3000
                    if not doesScoreBonus:
                        playSound("earn_bonus.wav")
                    bonusCompletionText = c.FONT.render("PERFECT", False, c.WHITE)
                    bonusCompletionScore = c.FONT.render("3000!", False, c.WHITE)
        if frameCount == 442:
            return

        scoreText = []
        for player in playerList:
            scoreText.append(c.FONT.render("{:06d}PTS.".format(player.score % 1000000), False, c.WHITE))
        highScore = checkHighScore(playerList, highScore)
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
        for fontData, coords in zip(playerLivesEndData, livesEndDataCoordinates):
            for num, text in enumerate(fontData):
                c.SCREEN.blit(text, (coords[0], coords[1]))
                coords = (coords[0] + 13, coords[1]) if num == 0 else (coords[0] + 15, coords[1])
        for text, coords in zip(playerText, playerTextCoordinates):
            c.SCREEN.blit(text, (coords[0], coords[1]))
        for text, coords in zip(scoreText, scoreDataCoordinates):
            c.SCREEN.blit(text, (coords[0], coords[1]))

        if (frameCount > 74 and not isinstance(level, BonusLevel)) or frameCount > 138:
            for text, coords in zip(iconCountText, scoreIconCountCoordinates):
                c.SCREEN.blit(text, (coords[0], coords[1]))
        if frameCount > 188:
            c.SCREEN.blit(bonusText, bonusTextCoordinates[bonusScoringIndex])
            c.SCREEN.blit(bonusScoreText, bonusScoreCoordinates[bonusScoringIndex])
            for (coords, player) in zip(bonusCompletionTextCoordinates, playerList):
                if player.lives > 0:
                    c.SCREEN.blit(bonusCompletionText, (coords[0], coords[1]))
            for (coords, player) in zip(bonusCompletionScoreCoordinates, playerList):
                if player.lives > 0:
                    c.SCREEN.blit(bonusCompletionScore, (coords[0], coords[1]))

        pg.display.update()
        c.CLOCK.tick(c.FPS)
