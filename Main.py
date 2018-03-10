import pygame
import os
import sys
import math
import CluLevels
import CluSprites
import DemoSprites
from CluGlobals import getImage, playSound


gameFolder = os.path.dirname(__file__)
spriteFolder = os.path.join(gameFolder, "Sprites")
backgroundFolder = os.path.join(gameFolder, "Backgrounds")
titleFolder = os.path.join(gameFolder, "Titles")
musicFolder = os.path.join(gameFolder, "Music")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 200, 15)
HOT_PINK = (255, 0, 95)
ORANGE = (250, 150, 55)
PINK = (250, 115, 180)
CYAN = (60, 180, 250)
PURPLE = (168, 0, 16)

pygame.mixer.pre_init(frequency=44100, buffer=512)
pygame.init()
pygame.font.init()

FONT = pygame.font.Font("Nintendo NES.ttf", 16)
DEMO_FONT = pygame.font.Font("Nintendo NES.ttf", 48)

# gameIcon = getImage(spriteFolder, "game_display_icon.png")
# gameIcon.set_colorkey(WHITE)

pygame.display.set_caption("Clu Clu Land Special")
# pygame.display.set_icon(gameIcon)
SCREEN_SIZE = (512, 448)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CLOCK = pygame.time.Clock()
FPS = 60

TITLE_MUSIC = os.path.join(musicFolder, "music_title.mp3")
DEMO_MUSIC = os.path.join(musicFolder, "music_demo.mp3")
LEVEL_START_MUSIC = os.path.join(musicFolder, "music_level_start.mp3")
LEVEL_MUSIC = os.path.join(musicFolder, "music_level.mp3")
LOW_TIME_MUSIC = os.path.join(musicFolder, "music_low_time.mp3")
LEVEL_END_MUSIC = os.path.join(musicFolder, "music_level_end.mp3")
BONUS_LEVEL_MUSIC = os.path.join(musicFolder, "music_bonus.mp3")
GAME_OVER_MUSIC = os.path.join(musicFolder, "music_game_over.mp3")


controlsDicts = [{"shoot": "z", "pause": "return", "up": "up", "down": "down", "left": "left", "right": "right"},
                 {"shoot": "[0]", "pause": "enter", "up": "[8]", "down": "[2]", "left": "[4]", "right": "[6]"},
                 {"shoot": "q", "pause": "e", "up": "w", "down": "s", "left": "a", "right": "d"},
                 {"shoot": "u", "pause": "o", "up": "i", "down": "k", "left": "j", "right": "l"}]


def getHighScore():
    try:
        with open(os.path.join(gameFolder, "clu_high_score.txt"), "r") as highScoreFile:
            highScore = int(highScoreFile.read()[-6:])
    except ValueError:
        highScore = 0
    except FileNotFoundError:
        highScore = 0
        setHighScore(highScore)
    return highScore


def setHighScore(highScore):
    with open(os.path.join(gameFolder, "clu_high_score.txt"), "w") as highScoreFile:
        highScoreFile.write(str(highScore))


def blitLevelData(playerList, level, time):
    colors = [HOT_PINK, GREEN, BLUE, YELLOW]
    playerLivesData = []
    goldCount = len([gold for gold in CluSprites.goldGroup if gold.goldState in [CluSprites.OtherState.UPSIDE_DOWN,
                                                                                 CluSprites.OtherState.FLIPPING_DOWN,
                                                                                 CluSprites.OtherState.OFF_SCREEN]])
    for num, player in enumerate(playerList):
        playerLivesData.append([FONT.render("<", False, colors[num]),
                                FONT.render("{}".format(min(player.lives, 9)), False, WHITE),
                                FONT.render(">", False, colors[num])])
    goldText = FONT.render("LAST,{:02d}".format(goldCount), False, WHITE)
    timeText = FONT.render("TIME,{:03d}".format(time), False, WHITE)
    SCREEN.blit(level.image, (0, 0))
    SCREEN.blit(goldText, (132, 16))
    SCREEN.blit(timeText, (262, 16))
    for hole in CluSprites.blackHoleGroup:
        SCREEN.blit(hole.image, hole.coordinates)
    if len(playerList) < 3:
        livesDataCoordinates = [(42, 16), (428, 16)]
    else:
        livesDataCoordinates = [(5, 16), (62, 16), (408, 16), (467, 16)]
    for fontData, coords in zip(playerLivesData, livesDataCoordinates):
        for num, text in enumerate(fontData):
            SCREEN.blit(text, coords)
            coords = (coords[0] + 13, coords[1]) if num == 0 else (coords[0] + 15, coords[1])
    return goldCount


def displayTitleScreen(playerOneScore=0, playerTwoScore=0, playerThreeScore=0, playerFourScore=0):
    highScore = getHighScore()
    titleImageOne = CluSprites.TitleSprite()
    titleImageTwo = CluSprites.TitleSprite("right")
    titleImageTwo.coordinates = (274, 54)
    subtitleImage = CluSprites.SubtitleSprite()

    subtitleText = FONT.render("SECRETS OF OLD CLU CLU LAND", False, WHITE)
    playText = FONT.render("PLAY GAME", False, CYAN)
    changeText = FONT.render("CHANGE CONTROLS", False, CYAN)
    cursorText = FONT.render(">", False, ORANGE)
    highScoreText = FONT.render("TOP,{:06d}".format(highScore), False, PINK)
    playerScoreTexts = [FONT.render("I,{:06d}".format(playerOneScore), False, WHITE),
                        FONT.render("~,{:06d}".format(playerTwoScore), False, WHITE),
                        FONT.render("{{,{:06d}".format(playerThreeScore), False, WHITE),
                        FONT.render("}},{:06d}".format(playerFourScore), False, WHITE)]
    scoreTextCoordinates = [(62, 400), (307, 400), (62, 425), (307, 425)]

    while True:
        pygame.mixer.music.load(TITLE_MUSIC)
        pygame.mixer.music.play()
        cursorLocation = (150, 310)
        titleImageOne.setTitleImageBackwards()
        titleImageTwo.setTitleImageBackwards()
        subtitleImage.frameCount = 0
        frameCount = 0
        looping = True

        while looping:
            frameCount += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == controlsDicts[0]["pause"] or event.key == pygame.K_RETURN:
                        if cursorLocation == (150, 310):
                            numberOfPlayers = chooseNumberOfPlayers(subtitleImage, titleImageOne, titleImageTwo, "GAME")
                            pygame.mixer.music.stop()
                            playerList = [CluSprites.PlayerSprite(num + 1) for num in range(numberOfPlayers)]
                            playerArmList = [CluSprites.PlayerArmSprite(player) for player in playerList]
                            while any(player.playerState != CluSprites.PlayerStates.DEAD for player in playerList):
                                playLevel(playerList, playerArmList, CluLevels.HOUSE, 0)  # ###############
                            playerScoresList = [player.score for player in playerList]
                            return playerScoresList
                        else:
                            numberOfPlayers = chooseNumberOfPlayers(subtitleImage, titleImageOne, titleImageTwo,
                                                                    "CONTROLS")
                            displayChangeControlMenu(subtitleImage, titleImageOne, titleImageTwo, numberOfPlayers)
                            looping = False
                    elif pygame.key.name(event.key) in [controlsDicts[0]["up"], controlsDicts[0]["down"]]:
                        if cursorLocation == (150, 310):
                            cursorLocation = (100, 335)
                        else:
                            cursorLocation = (150, 310)
            SCREEN.fill(BLACK)
            SCREEN.blit(subtitleText, (42, 275))
            SCREEN.blit(playText, (180, 310))
            SCREEN.blit(changeText, (130, 335))
            SCREEN.blit(cursorText, cursorLocation)
            SCREEN.blit(highScoreText, (172, 375))
            for text, coords in zip(playerScoreTexts, scoreTextCoordinates):
                SCREEN.blit(text, coords)
            for sprite in [titleImageOne, titleImageTwo, subtitleImage]:
                sprite.update()
                SCREEN.blit(sprite.image, sprite.coordinates)
            if frameCount == 740:
                animateDemo()
                looping = False
            pygame.display.update()
            CLOCK.tick(FPS)


def animateDemo():
    pygame.mixer.music.load(DEMO_MUSIC)
    pygame.mixer.music.play()
    playerNames = [DEMO_FONT.render("BUBBLES", False, RED), DEMO_FONT.render("GLOOPY", False, GREEN),
                   DEMO_FONT.render("NEMO", False, BLUE), DEMO_FONT.render("DIZZY", False, YELLOW)]
    playerNameCoordinates = [(103, 61), (127, 61), (145, 337), (122, 337)]

    displayRects = [pygame.Rect(20, -260, 380, 260), pygame.Rect(480, 180, 380, 260), pygame.Rect(120, 444, 380, 260),
                    pygame.Rect(-380, 20, 380, 260)]
    coverRect = pygame.Rect(20, -260, 380, 260)
    nameRects = [pygame.Rect(86, 47, 540, 100), pygame.Rect(86, 46, 540, 100), pygame.Rect(57, 324, 540, 100),
                 pygame.Rect(57, 324, 540, 100)]
    spriteCoords = [(0, 4), (-4, 0), (0, -4), (4, 0)]

    for demoNum in range(4):
        frameCount = 0
        DemoSprites.demoGroup.empty()
        DemoSprites.initialize()
        SCREEN.fill(GREY)
        pygame.display.update()

        if demoNum == 0:
            for num in range(4):
                DemoSprites.DemoGoldSprite((458 + 96 * (num + num // 2), -164))
            for num in range(14):
                for postNum in range(2):
                    DemoSprites.PostSprite((-196 + 96 * num, -194 + 96 * postNum))
            DemoSprites.DemoWallSprite(0, (668 + 96 * 3, -294))
            DemoSprites.DemoPlayerSprite(0, (180, -182))
        elif demoNum == 1:
            for num in range(10):
                for postNum in range(6):
                    DemoSprites.PostSprite((1474 - 96 * num, 246 + 96 * postNum))
            DemoSprites.DemoArmSprite(1, (1430 - 96 * 8, 242 + 96 * 1))
            DemoSprites.DemoPlayerSprite(1, (638, 274))
        elif demoNum == 2:
            for num in range(12):
                for postNum in range(2):
                    DemoSprites.PostSprite((734 - 96 * num, 510 + 96 * postNum))
            DemoSprites.DemoWallSprite(2, (-452, 222))
            DemoSprites.DemoHoleSprite((474, 540))
            DemoSprites.DemoUrchinSprite((474 - 96 * 5, 540))
            DemoSprites.DemoWaveSprite((174, 540))
            DemoSprites.DemoPlayerSprite(2, (290, 522))
            DemoSprites.DemoPlayerSprite.facingDirection = DemoSprites.Directions.LEFT
        else:
            for num in range(2):
                for postNum in range(2):
                    DemoSprites.PostSprite((-448 + 384 * num, 86 + 96 * postNum))
                    DemoSprites.PostSprite((-352 + 384 * num, 86 + 96 * postNum))
            for num in range(2):
                DemoSprites.DemoRubberTrapSprite(num, (-276 + 96 * num, 86))
            DemoSprites.DemoArmSprite(3, (-200, 90), True)
            DemoSprites.DemoPlayerSprite(3, (-224, 112))
        DemoSprites.DemoDisplay(demoNum, displayRects[demoNum].topleft)
        alphaKey = 255

        while frameCount < 600:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == controlsDicts[0]["pause"] or event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        SCREEN.fill(BLACK)
                        return
            frameCount += 1

            if frameCount < 105:
                displayRects[demoNum].topleft = [displayRects[demoNum].topleft[0] + spriteCoords[demoNum][0],
                                                 displayRects[demoNum].topleft[1] + spriteCoords[demoNum][1]]
                if demoNum == 0:
                    coverRect.bottomleft = displayRects[demoNum].topleft
                elif demoNum == 1:
                    coverRect.topleft = displayRects[demoNum].topright
                elif demoNum == 2:
                    coverRect.topleft = displayRects[demoNum].bottomleft
                else:
                    coverRect.topright = displayRects[demoNum].topleft
                for sprite in DemoSprites.demoGroup:
                    sprite.coordinates = (sprite.coordinates[0] + spriteCoords[demoNum][0],
                                          sprite.coordinates[1] + spriteCoords[demoNum][1])

            if frameCount < 328:
                pygame.draw.rect(SCREEN, BLACK, displayRects[demoNum])
                for sprite in DemoSprites.demoGroup:
                    sprite.setCoordinates()
                    sprite.update()
                    SCREEN.blit(sprite.image, sprite.coordinates)
                pygame.draw.rect(SCREEN, GREY, coverRect)
                pygame.display.update(coverRect)
                pygame.display.update(displayRects[demoNum])
            elif frameCount == 328:
                playSound("item_appears_or_collected.wav")
                demoNameBlock = DemoSprites.DemoNameDisplay(demoNum, (nameRects[demoNum].left, nameRects[demoNum].top))
                for sprite in DemoSprites.demoGroup:
                    sprite.setMonochromeImage()
            else:
                SCREEN.fill(GREY)
                pygame.draw.rect(SCREEN, BLACK, displayRects[demoNum])
                for sprite in DemoSprites.demoGroup:
                    SCREEN.blit(sprite.image, sprite.coordinates)
                pygame.draw.rect(SCREEN, GREY, (displayRects[demoNum].right, 0,
                                                SCREEN_SIZE[0] - displayRects[demoNum].right, SCREEN_SIZE[1]))
                pygame.draw.rect(SCREEN, GREY, (0, 0, displayRects[demoNum].left, SCREEN_SIZE[1]))
                pygame.draw.rect(SCREEN, GREY, (0, 0, SCREEN_SIZE[0], displayRects[demoNum].top))
                pygame.draw.rect(SCREEN, BLACK, (nameRects[demoNum].left, nameRects[demoNum].top, 365, 65))
                SCREEN.blit(demoNameBlock.image, demoNameBlock.coordinates)
                SCREEN.blit(playerNames[demoNum], playerNameCoordinates[demoNum])
                alphaKey = flashScreen(frameCount, alphaKey)
                pygame.display.update()
            CLOCK.tick(FPS)


def flashScreen(frameCount, alphaKey):
    frameCount -= 325
    screenCovering = pygame.Surface(SCREEN_SIZE)
    screenCovering.fill(WHITE)
    screenCovering.set_alpha(alphaKey)
    if 39 < frameCount:
        alphaKey = max(0, alphaKey - 3)
    SCREEN.blit(screenCovering, (0, 0))
    pygame.display.update()
    return alphaKey


def playLevel(playerList, playerArmList, level, levelCount):
    CluSprites.blackHoleGroup.empty()
    CluSprites.enemyGroup.empty()

    levelCount += 1
    setUpLevel(level)
    pausedPlayerNumber = 0
    levelComplete = alreadyLoadedLevelEnd = playingLowTimeMusic = timeReachedZero = False  # # # # # # # # # #
    gameOverTextActive = [0 for _ in range(len(playerList))]
    frameCount = 0
    timeCount = 800
    if isinstance(level, CluLevels.BonusLevel):
        timeCount = 200
    elif levelCount in range(5, 11) or (levelCount > 21 and (levelCount - 1) % 20 in range(6, 10)):
        timeCount = 700
    elif levelCount in range(12, 16) or (levelCount > 21 and (levelCount - 1) % 20 in range(11, 17)):
        timeCount = 600
    elif levelCount in range(17, 21) or (levelCount > 21 and (levelCount - 1) % 20 > 16):
        timeCount = 500
    initialTimeCount = timeCount

    SCREEN.fill(BLACK)
    blitLevelData(playerList, level, timeCount)
    pygame.display.update()
    pygame.mixer.music.load(LEVEL_START_MUSIC)
    pygame.mixer.music.play()

    pygame.time.delay(6000)
    pygame.event.clear()
    pygame.mixer.music.load(LEVEL_MUSIC)
    pygame.mixer.music.play(-1)

    for num, player in enumerate(playerList):
        player.initialize(48 * level.playerStartPosition[num][0], 49 + 48 * level.playerStartPosition[num][1])
    CluSprites.PlayerSprite.currentLevel = level
    CluSprites.GoldSprite.levelCount = levelCount

    while True:
        while pausedPlayerNumber != 0:
            pauseGame(pausedPlayerNumber - 1)
            pausedPlayerNumber = 0
        while pausedPlayerNumber == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.KEYUP:
                #     if pygame.key.name(event.key) in [controlsDicts[0]["up"], controlsDicts[0]["down"],
                #                                       controlsDicts[0]["left"], controlsDicts[0]["right"]]:
                #         playerArmList[0].armState = CluSprites.ArmStates.OFF_SCREEN
                #         if playerList[0].playerState in [CluSprites.PlayerStates.SWINGING,
                #                                          CluSprites.PlayerStates.HITTING_PLAYER_SWINGING]:
                #             playerList[0].playerState = CluSprites.PlayerStates.MOVING
                #     if len(playerList) > 1:
                #         if pygame.key.name(event.key) in [controlsDicts[1]["up"], controlsDicts[1]["down"],
                #                                           controlsDicts[1]["left"], controlsDicts[1]["right"]]:
                #             playerArmList[1].armState = CluSprites.ArmStates.OFF_SCREEN
                #             if playerList[1].playerState in [CluSprites.PlayerStates.SWINGING,
                #                                              CluSprites.PlayerStates.HITTING_PLAYER_SWINGING]:
                #                 playerList[1].playerState = CluSprites.PlayerStates.MOVING
                if event.type == pygame.KEYDOWN:
                    for num, player in enumerate(playerList):
                        if pygame.key.name(event.key) == controlsDicts[num]["pause"] and\
                                        player.playerState != CluSprites.PlayerStates.DEAD:
                            pygame.mixer.music.pause()
                            playSound("pause_unpause.wav")
                            pausedPlayerNumber = num + 1
                            pygame.time.delay(1000)
                            pygame.event.clear()
                        elif pygame.key.name(event.key) in [controlsDicts[num]["up"], controlsDicts[num]["down"],
                                                            controlsDicts[num]["left"], controlsDicts[num]["right"]]:
                            if player.playerState == CluSprites.PlayerStates.BALL:
                                directionChosen = [key for key, val in controlsDicts[num].items()
                                                   if val == pygame.key.name(event.key)][0]
                                player.startMoving(directionChosen)
                            elif player.playerState in [CluSprites.PlayerStates.MOVING,
                                                        CluSprites.PlayerStates.SWINGING,
                                                        CluSprites.PlayerStates.FINISHED_SWINGING]:
                                directionChosen = [key for key, val in controlsDicts[num].items()
                                                   if val == pygame.key.name(event.key)][0]
                                playerArmList[num].extendArm(directionChosen)
                        if pygame.key.name(event.key) == controlsDicts[num]["shoot"] and not player.isFrozen:
                            shootWave(player)
                heldKeys = pygame.key.get_pressed()
                if not any((heldKeys[pygame.K_UP], heldKeys[pygame.K_DOWN], heldKeys[pygame.K_LEFT],
                           heldKeys[pygame.K_RIGHT])):
                    playerArmList[0].armState = CluSprites.ArmStates.OFF_SCREEN
                    if playerList[0].playerState in [CluSprites.PlayerStates.SWINGING,
                                                     CluSprites.PlayerStates.HITTING_PLAYER_SWINGING]:
                        playerList[0].playerState = CluSprites.PlayerStates.FINISHED_SWINGING
                        playerList[0].swingFrameCount = playerList[0].frameCount = 0
                        playerList[0].adjustPosition()
                if len(playerList) > 1:
                    if not any((heldKeys[pygame.K_KP8], heldKeys[pygame.K_KP2], heldKeys[pygame.K_KP4],
                                heldKeys[pygame.K_KP6])):
                        playerArmList[1].armState = CluSprites.ArmStates.OFF_SCREEN
                        if playerList[1].playerState in [CluSprites.PlayerStates.SWINGING,
                                                         CluSprites.PlayerStates.HITTING_PLAYER_SWINGING]:
                            playerList[1].playerState = CluSprites.PlayerStates.FINISHED_SWINGING
                            playerList[1].swingFrameCount = 0
                            playerList[1].adjustPosition()  # ###############
            SCREEN.fill(BLACK)
            goldCount = blitLevelData(playerList, level, timeCount)
            if not levelComplete:
                if pausedPlayerNumber == 0:
                    CluSprites.GoldSprite.globalFrameCount += 1
                    for group in CluSprites.allGroups:
                        group.update()
                        for sprite in group:
                            SCREEN.blit(sprite.image, (math.floor(sprite.coordinates[0]),
                                                       math.floor(sprite.coordinates[1])))
                    if frameCount % 5 == 0:
                        timeCount = max(0, timeCount - 1)
                    if timeCount > 200 and playingLowTimeMusic:
                        playingLowTimeMusic = False
                        pygame.mixer.music.load(LEVEL_MUSIC)
                        pygame.mixer.music.stop()
                        pygame.mixer.music.play(-1)
                    if timeCount < 200 and all(value < 1 for value in gameOverTextActive):
                        playingLowTimeMusic = True
                        pygame.mixer.music.load(LOW_TIME_MUSIC)
                        pygame.mixer.music.stop()
                        pygame.mixer.music.play(-1)
                    if timeCount == 0:
                        if not timeReachedZero:
                            frameCount = 0
                            timeReachedZero = True
                            playSound("death.wav")
                            pygame.mixer.music.stop()
                            for player in playerList:
                                if player.playerState not in [CluSprites.PlayerStates.DEAD,
                                                              CluSprites.PlayerStates.OFF_SCREEN,
                                                              CluSprites.PlayerStates.FALLING,
                                                              CluSprites.PlayerStates.EXPLODING]:
                                    player.playerState = CluSprites.PlayerStates.EXPLODING
                                    player.frameCount = 0
                        if frameCount == 170 and any(0 < player.lives for player in playerList):
                            timeReachedZero = False
                            timeCount = 400
                            pygame.mixer.music.load(LEVEL_MUSIC)
                            pygame.mixer.music.play(-1)
                    for num, player in enumerate(playerList):
                        if player.playerState == CluSprites.PlayerStates.DEAD:
                            gameOverTextActive, frameCount, timeCount = initializeGameOverSprite(gameOverTextActive,
                                                                                                 num, frameCount,
                                                                                                 timeCount)
                else:
                    for group in CluSprites.allGroups:
                        for sprite in group:
                            SCREEN.blit(sprite.image, (math.floor(sprite.coordinates[0]),
                                                       math.floor(sprite.coordinates[1])))
            #     if not alreadyLoadedLevelEnd:
            #         frameCount = 0
            #         pygame.mixer.music.load(LEVEL_END_MUSIC)
            #         pygame.mixer.music.stop()
            #         pygame.mixer.music.play()
            #         alreadyLoadedLevelEnd = True
            #         level.isFlashing = True
            #     elif frameCount > 330:
            #         # Add level end
            #         pygame.display.update()
            #         pygame.time.delay(10000)
            pygame.display.update()
            frameCount += 1
            CLOCK.tick(FPS)

            # pygame.mixer.music.stop()
            # pygame.mixer.music.play()
            # pygame.time.delay(6000)
            # pygame.mixer.music.load(LEVEL_END_MUSIC)
            # pygame.mixer.music.play()
            # pygame.time.delay(6000)
            # pygame.mixer.music.stop()
            # pygame.event.clear()
            # return


def pauseGame(pausingPlayerIndex):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == controlsDicts[pausingPlayerIndex]["pause"]:
                    playSound("pause_unpause.wav")
                    pygame.time.delay(1000)
                    pygame.mixer.music.unpause()
                    pygame.event.clear()
                    return


def shootWave(player):
    sonicWavesFromPlayer = [sprite for sprite in CluSprites.attackGroup if
                            sprite.firingPlayerNumber == player.playerNumber]
    if len(sonicWavesFromPlayer) < 2 and player.playerState in [CluSprites.PlayerStates.MOVING,
                                                                CluSprites.PlayerStates.SWINGING,
                                                                CluSprites.PlayerStates.FINISHED_SWINGING]:
        waveCoordinates = player.coordinates
        if player.isFacingHorizontally():
            if 0 < player.coordinates[1] % 48 < 24:
                waveCoordinates = (math.floor(player.coordinates[0]),
                                   math.floor(player.coordinates[1] - (player.coordinates[1] % 48)))
            elif player.coordinates[1] % 48 > 23:
                waveCoordinates = (math.floor(player.coordinates[0]),
                                   math.floor(player.coordinates[1] + (48 - player.coordinates[1] % 48)))
        else:
            if 0 < player.coordinates[0] % 48 < 24:
                waveCoordinates = (math.floor(player.coordinates[0] - (player.coordinates[0] % 48)),
                                   math.floor(player.coordinates[1]))
            elif player.coordinates[0] % 48 > 23:
                waveCoordinates = (math.floor(player.coordinates[0] + (48 - player.coordinates[0] % 48)),
                                   math.floor(player.coordinates[1]))
        playSound("shoot_wave.wav")
        newWave = CluSprites.SonicWaveSprite(player.facingDirection, player.playerNumber)
        newWave.setInitialCoordinates(waveCoordinates[0], waveCoordinates[1])
        CluSprites.attackGroup.add(newWave)


def setUpLevel(level):
    level.initialize()
    CluSprites.initializeLevelItems(level)
    goldList = []
    rubberList = []
    for (x, y) in level.goldTilesVertical:
        goldList.append(CluSprites.GoldSprite())
        goldList[-1].setCoordinates(-25 + 48 * x, 49 + 48 * y)
    for (x, y) in level.goldTilesHorizontal:
        goldList.append(CluSprites.GoldSprite())
        goldList[-1].isHorizontal = True
        goldList[-1].setCoordinates(-1 + 48 * x, 25 + 48 * y)
    for (x, y) in level.rubberTilesVertical:
        rubberList.append(CluSprites.RubberTrapSprite())
        rubberList[-1].setCoordinates(-36 + 48 * x, 36 + 48 * y)
    for (x, y) in level.rubberTilesHorizontal:
        rubberList.append(CluSprites.RubberTrapSprite())
        rubberList[-1].isHorizontal = True
        rubberList[-1].setCoordinates(-14 + 48 * x, 14 + 48 * y)
    CluSprites.blackHoleGroup.add(CluSprites.BlackHoleSprite() for _ in range(len(level.blackHolePositions)))
    for (x, y), hole in zip(level.blackHolePositions, CluSprites.blackHoleGroup):
        hole.initialize(-1 + 48 * x, 49 + 48 * y)


def initializeGameOverSprite(gameOverTextActive, index, frameCount, timeCount):
    if gameOverTextActive[index] == 0 and not any(value == 1 for value in gameOverTextActive):
        frameCount = 0
        gameOverTextSprite = CluSprites.GameOverTextSprite(index)
        gameOverTextSprite.initialize()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(GAME_OVER_MUSIC)
        pygame.mixer.music.play()
        gameOverTextActive[index] = 1
    if gameOverTextActive[index] == 1 and frameCount == 300:
        gameOverTextActive[index] = -1
        pygame.mixer.music.stop()
        if all(value == -1 for value in gameOverTextActive):
            pygame.mixer.music.load(LEVEL_END_MUSIC)
        else:
            if timeCount > 200:
                pygame.mixer.music.load(LEVEL_MUSIC)
            else:
                pygame.mixer.music.load(LOW_TIME_MUSIC)
        pygame.mixer.music.play()
    return gameOverTextActive, frameCount, timeCount


def setTextCoordinates(value, numberOfPlayers):
    if numberOfPlayers == 1:
        textCoordinates = (90 + value, 345)
    else:
        textCoordinates = (122 + value, 345)
    return textCoordinates


def displayChangeControlMenu(subtitleImage, titleImageOne, titleImageTwo, numberOfPlayers):
    for sprite in [subtitleImage, titleImageOne, titleImageTwo]:
        sprite.setTitleImage()
    frameCount = controlChangeIndex = currentPlayerIndex = 0
    if numberOfPlayers == 1:
        textCoordinates = (90, 345)
    else:
        textCoordinates = (122, 345)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                controlChangeIndex = changeControlInput(controlChangeIndex, event, currentPlayerIndex, numberOfPlayers)
                frameCount = 0
        if controlChangeIndex == 6:
            if currentPlayerIndex == numberOfPlayers:
                return
            else:
                currentPlayerIndex += 1
                controlChangeIndex = 0

        controlsList = ["shoot", "pause", "up", "down", "left", "right", "none"]
        controlToChange = controlsList[controlChangeIndex]
        SCREEN.fill(BLACK)
        subtitleText = FONT.render("SECRETS OF OLD CLU CLU LAND", False, WHITE)
        SCREEN.blit(subtitleText, (42, 275))
        for sprite in [titleImageOne, titleImageTwo, subtitleImage]:
            SCREEN.blit(sprite.image, sprite.coordinates)
        if controlChangeIndex == 2:
            textCoordinates = setTextCoordinates(23, numberOfPlayers)
        elif controlChangeIndex == 3:
            textCoordinates = setTextCoordinates(5, numberOfPlayers)
        elif controlChangeIndex == 5:
            textCoordinates = setTextCoordinates(0, numberOfPlayers)
        if numberOfPlayers == 1:
            controlInputText = FONT.render("SELECT '{}' BUTTON".format(controlToChange.upper()), False, WHITE)
        else:
            controlInputText = FONT.render("P{} '{}' BUTTON".format(currentPlayerIndex, controlToChange.upper()),
                                           False, WHITE)
        if frameCount % 60 < 30:
            SCREEN.blit(controlInputText, textCoordinates)
        pygame.display.update()
        frameCount += 1
        CLOCK.tick(FPS)


def changeControlInput(controlChangeIndex, event, currentIndex, numberOfPlayers):
    controlsList = ["shoot", "pause", "up", "down", "left", "right", "none"]
    if controlChangeIndex == 0 and currentIndex == 0:
        for listIndex, controls in enumerate(controlsDicts):
            if numberOfPlayers <= listIndex:
                break
            controlsDicts[listIndex] = controlsDicts[currentIndex].fromkeys(controlsDicts[currentIndex], "None")
    if not any(pygame.key.name(event.key) in controlValue.values() for controlValue in controlsDicts):
        if controlChangeIndex == 6:
            if currentIndex + 1 == numberOfPlayers:
                pygame.mixer.music.stop()
                pygame.time.delay(500)
        else:
            controlsDicts[currentIndex][controlsList[controlChangeIndex]] = pygame.key.name(event.key)
            controlChangeIndex += 1
    return controlChangeIndex


def chooseNumberOfPlayers(subtitleImage, titleImageOne, titleImageTwo, textToDisplay):
    for sprite in [subtitleImage, titleImageOne, titleImageTwo]:
        sprite.setTitleImage()
    subtitleText = FONT.render("SECRETS OF OLD CLU CLU LAND", False, WHITE)
    playerNumbersText = [FONT.render("1 PLAYER", False, CYAN),
                         FONT.render("2 PLAYER", False, CYAN),
                         FONT.render("3 PLAYER", False, CYAN),
                         FONT.render("4 PLAYER", False, CYAN)]
    playerTextCoordinates = [(60, 310), (320, 310), (60, 370), (320, 370)]
    optionText = FONT.render(textToDisplay, False, CYAN)
    cursorText = FONT.render(">", False, ORANGE)
    cursorLocation = (40, 310)
    optionTextCoordinates = [(60, 330), (320, 330), (60, 390), (320, 390)]
    if textToDisplay == "GAME":
        optionTextCoordinates = [(90, 330), (350, 330), (90, 390), (350, 390)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == controlsDicts[0]["pause"] or event.key == pygame.K_RETURN:
                    coordinatesIndex = [(), (40, 310), (300, 310), (40, 370), (300, 370)]
                    return coordinatesIndex.index(cursorLocation)
                elif pygame.key.name(event.key) == controlsDicts[0]["left"] or\
                                pygame.key.name(event.key) == controlsDicts[0]["right"]:
                    if cursorLocation[0] == 40:
                        cursorLocation = (300, cursorLocation[1])
                    else:
                        cursorLocation = (40, cursorLocation[1])
                elif pygame.key.name(event.key) == controlsDicts[0]["up"] or\
                                pygame.key.name(event.key) == controlsDicts[0]["down"]:
                    if cursorLocation[1] == 310:
                        cursorLocation = (cursorLocation[0], 370)
                    else:
                        cursorLocation = (cursorLocation[0], 310)
        SCREEN.fill(BLACK)
        SCREEN.blit(subtitleText, (42, 275))
        for sprite in [titleImageOne, titleImageTwo, subtitleImage]:
                SCREEN.blit(sprite.image, sprite.coordinates)
        for text, coords in zip(playerNumbersText, playerTextCoordinates):
            SCREEN.blit(text, coords)
        for coords in optionTextCoordinates:
            SCREEN.blit(optionText, coords)
        SCREEN.blit(cursorText, cursorLocation)
        pygame.display.update()
        CLOCK.tick(FPS)


def main():
    currentScores = [0, 0, 0, 0]

    while True:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for group in CluSprites.allGroups:
            if group is not CluSprites.itemGroup:
                group.empty()
        playerScores = displayTitleScreen(currentScores[0], currentScores[1], currentScores[2], currentScores[3])
        for num, score in enumerate(playerScores):
            currentScores[num] += score
        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
