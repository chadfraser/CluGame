import pygame
import os
import sys
import CluSprites
import CluLevels


gameFolder = os.path.dirname(__file__)
spriteFolder = os.path.join(gameFolder, "Sprites")
backgroundFolder = os.path.join(gameFolder, "Backgrounds")
titleFolder = os.path.join(gameFolder, "Titles")
musicFolder = os.path.join(gameFolder, "Music")

_imageLibrary = {}
_soundLibrary = {}


def getImage(folder, imagePath):
    global _imageLibrary
    image = _imageLibrary.get(imagePath)
    if image is None:
        fullPath = os.path.join(folder, imagePath)
        image = pygame.image.load(fullPath).convert()
        _imageLibrary[imagePath] = image
    return image


def playSound(soundPath):
    global _soundLibrary
    sound = _soundLibrary.get(soundPath)
    if sound is None:
        fullPath = os.path.join(musicFolder, soundPath)
        sound = pygame.mixer.Sound(fullPath)
        _soundLibrary[soundPath] = sound
    sound.play()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (250, 115, 180)
ORANGE = (250, 150, 55)
CYAN = (60, 180, 250)

pygame.init()
pygame.font.init()

FONT = pygame.font.Font("Nintendo NES.ttf", 16)

gameIcon = getImage(spriteFolder, "game_display_icon.png")
gameIcon.set_colorkey(WHITE)

pygame.display.set_caption("Clu Clu Land Special")
pygame.display.set_icon(gameIcon)
SCREEN_SIZE = (512, 448)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CLOCK = pygame.time.Clock()
FPS = 60

TITLE_MUSIC = os.path.join(musicFolder, "music_title.mp3")
LEVEL_START_MUSIC = os.path.join(musicFolder, "music_level_start.mp3")
LEVEL_MUSIC = os.path.join(musicFolder, "music_level.mp3")
LOW_TIME_MUSIC = os.path.join(musicFolder, "music_low_time.mp3")
LEVEL_END_MUSIC = os.path.join(musicFolder, "music_level_end.mp3")
BONUS_LEVEL_MUSIC = os.path.join(musicFolder, "music_bonus.mp3")
GAME_OVER_MUSIC = os.path.join(musicFolder, "music_game_over.mp3")


controlsDicts = [{"shoot": "z", "pause": "return", "up": "up", "down": "down", "left": "left", "right": "right"},
                 {"shoot": "[0]", "pause": "enter", "up": "[8]", "down": "[2]", "left": "[4]", "right": "[6]"}]


def getHighScore():
    try:
        with open(os.path.join(gameFolder, "clu_high_score.txt"), "r") as highScoreFile:
            highScore = int(highScoreFile.read()[-6:])
    except ValueError:
        highScore = 0
    except FileNotFoundError:
        open(os.path.join(gameFolder, "clu_high_score.txt"), "w")
        highScore = 0
    return highScore


def setHighScore(highScore):
    with open(os.path.join(gameFolder, "clu_high_score.txt"), "w") as highScoreFile:
        highScoreFile.write(str(highScore))


def blitLevelData(playerList, level, time):
    livesText = FONT.render("<", False, ORANGE)
    livesTextTwo = FONT.render("{}".format(min(playerList[0].lives, 9)), False, WHITE)
    livesTextThree = FONT.render(">", False, ORANGE)
    goldText = FONT.render("LAST,{:02d}".format(level.goldCount), False, WHITE)
    timeText = FONT.render("TIME,{:03d}".format(time), False, WHITE)
    SCREEN.blit(level.image, (0, 0))
    SCREEN.blit(livesText, (42, 16))
    SCREEN.blit(livesTextTwo, (55, 16))
    SCREEN.blit(livesTextThree, (70, 16))
    SCREEN.blit(goldText, (132, 16))
    SCREEN.blit(timeText, (262, 16))
    for hole in CluSprites.blackHoleGroup:
        SCREEN.blit(hole.image, hole.coordinates)
    if len(playerList) > 1:
        livesTextFour = FONT.render("<", False, GREEN)
        livesTextFive = FONT.render("{}".format(min(playerList[1].lives, 9)), False, WHITE)
        livesTextSix = FONT.render(">", False, GREEN)
        SCREEN.blit(livesTextFour, (428, 16))
        SCREEN.blit(livesTextFive, (441, 16))
        SCREEN.blit(livesTextSix, (456, 16))


def displayTitleScreen(playerOneScore=0, playerTwoScore=0):
    highScore = getHighScore()
    titleImageOne = CluSprites.TitleSprite("title_01.png")
    titleImageTwo = CluSprites.TitleSprite("title_01.png", "right")
    subtitleImage = getImage(titleFolder, "title_main_1.png")
    lightTitleImage = getImage(titleFolder, "title_main_2.png")
    subtitleImage.set_colorkey(BLACK)
    lightTitleImage.set_colorkey(BLACK)
    subtitleText = FONT.render("SECRETS OF OLD CLU CLU LAND", False, WHITE)
    playText = FONT.render("PLAY GAME", False, CYAN)
    changeText = FONT.render("CHANGE CONTROLS", False, CYAN)
    cursorText = FONT.render(">", False, ORANGE)
    highScoreText = FONT.render("TOP,{:06d}".format(highScore), False, PINK)
    playerOneScoreText = FONT.render("I,{:06d}".format(playerOneScore), False, WHITE)
    playerTwoScoreText = FONT.render("~,{:06d}".format(playerTwoScore), False, WHITE)

    while True:
        pygame.mixer.music.load(TITLE_MUSIC)
        pygame.mixer.music.play()
        frameCount = 0
        titleImageOne.setTitleImageBackwards()
        titleImageTwo.setTitleImageBackwards()
        cursorLocation = (150, 310)
        looping = True

        while looping:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == controlsDicts[0]["pause"] and cursorLocation == (150, 310):
                        numberOfPlayers = chooseOneOrTwoPlayers(subtitleImage, titleImageOne, titleImageTwo, "GAME")
                        pygame.mixer.music.stop()
                        playerList = [CluSprites.PlayerSprite()]
                        playerArmList = [CluSprites.PlayerArmSprite()]
                        playerArmList[0].playerBody = playerList[0]
                        if numberOfPlayers == 2:
                            playerList.append(CluSprites.PlayerSprite(2))
                            playerArmList.append(CluSprites.PlayerArmSprite(2))
                            playerArmList[1].playerBody = playerList[1]
                        playLevel(playerList, playerArmList, CluLevels.HOUSE, 0)  ################
                    elif pygame.key.name(event.key) == controlsDicts[0]["pause"]:
                        numberOfPlayers = chooseOneOrTwoPlayers(subtitleImage, titleImageOne, titleImageTwo,
                                                                "CONTROLS")
                        displayChangeControlMenu(subtitleImage, titleImageOne, titleImageTwo, numberOfPlayers)
                        looping = False
                    if pygame.key.name(event.key) == controlsDicts[0]["up"] or \
                       pygame.key.name(event.key) == controlsDicts[0]["down"]:
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
            SCREEN.blit(playerOneScoreText, (62, 400))
            SCREEN.blit(playerTwoScoreText, (307, 400))

            for sprite in [titleImageOne, titleImageTwo]:
                sprite.update()
            if 500 > frameCount or frameCount % 10 > 4:
                SCREEN.blit(subtitleImage, (50, 22))
                SCREEN.blit(titleImageOne.image, (98, 54))
                SCREEN.blit(titleImageTwo.image, (274, 54))
            if 499 < frameCount and frameCount % 10 < 5:
                SCREEN.blit(lightTitleImage, (50, 22))
            if 740 < frameCount:
                animateDemo()
            pygame.display.update()
            frameCount += 1
            CLOCK.tick(FPS)


def animateDemo():
    SCREEN.fill(BLACK)
    frameCount = 0
    playerListDemo = [CluSprites.PlayerSprite(), CluSprites.PlayerSprite(2)]
    playerListDemo[0].lives = 1
    playerListDemo[1].lives = 1
    levelDemo = CluLevels.HOUSE
    blackHoleDemo = [CluSprites.BlackHoleSprite()]
    blitLevelData(playerListDemo, levelDemo, 800)
    for num, player in enumerate(playerListDemo):
        player.initialize(-49 + 48 * levelDemo.playerStartPosition[num][0],
                          49 + 48 * levelDemo.playerStartPosition[num][1])

    while True:
        pygame.display.update()
        pass


def playLevel(playerList, playerArmList, level, levelCount):
    CluSprites.blackHoleGroup.empty()
    CluSprites.enemyGroup.empty()

    levelCount += 1
    setUpLevel(level)
    pausedPlayerNumber = 0
    levelComplete = False
    alreadyLoadedLevelEnd = False
    playingLowTimeMusic = False
    timeReachedZero = False
    gameOverTextActive = [0 for __ in range(len(playerList))]
    frameCount = 0
    timeCount = 800

    SCREEN.fill(BLACK)
    blitLevelData(playerList, level, timeCount)
    pygame.display.update()
    pygame.mixer.music.load(LEVEL_START_MUSIC)
    pygame.mixer.music.play()

    # pygame.time.delay(6000)
    pygame.event.clear()
    pygame.mixer.music.load(LEVEL_MUSIC)
    pygame.mixer.music.play(-1)

    for num, player in enumerate(playerList):
        player.initialize(-49 + 48 * level.playerStartPosition[num][0],
                          49 + 48 * level.playerStartPosition[num][1])
        CluSprites.PlayerSprite.currentLevel = level
        CluSprites.GoldSprite.levelCount = levelCount
        player.lives = 0

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
                    if pygame.key.name(event.key) == controlsDicts[0]["pause"]:
                        pygame.mixer.music.pause()
                        playSound("pause_unpause.wav")
                        pausedPlayerNumber = 1
                        pygame.time.delay(1000)
                        pygame.event.clear()
                    elif pygame.key.name(event.key) in [controlsDicts[0]["up"], controlsDicts[0]["down"],
                                                        controlsDicts[0]["left"], controlsDicts[0]["right"]]:
                        if playerList[0].playerState == CluSprites.PlayerStates.BALL:
                            directionChosen = [key for key, val in controlsDicts[0].items()
                                               if val == pygame.key.name(event.key)][0]
                            playerList[0].startMoving(directionChosen)
                        elif playerList[0].playerState in [CluSprites.PlayerStates.MOVING,
                                                           CluSprites.PlayerStates.SWINGING,
                                                           CluSprites.PlayerStates.FROZEN]:
                            directionChosen = [key for key, val in controlsDicts[0].items()
                                               if val == pygame.key.name(event.key)][0]
                            playerArmList[0].extendArm(directionChosen)
                    if pygame.key.name(event.key) == controlsDicts[0]["shoot"]:
                        shootWave(playerList[0])
                    if len(playerList) > 1:
                        if pygame.key.name(event.key) == controlsDicts[1]["pause"]:
                            pygame.mixer.music.pause()
                            playSound("pause_unpause.wav")
                            pausedPlayerNumber = 2
                            pygame.time.delay(1000)
                            pygame.event.clear()
                        if pygame.key.name(event.key) in [controlsDicts[1]["up"], controlsDicts[1]["down"],
                                                          controlsDicts[1]["left"], controlsDicts[1]["right"]]:
                            if playerList[1].playerState == CluSprites.PlayerStates.BALL:
                                directionChosen = [key for key, val in controlsDicts[1].items()
                                                   if val == pygame.key.name(event.key)][0]
                                playerList[1].startMoving(directionChosen)
                            elif playerList[1].playerState in [CluSprites.PlayerStates.MOVING,
                                                               CluSprites.PlayerStates.SWINGING,
                                                               CluSprites.PlayerStates.FROZEN]:
                                directionChosen = [key for key, val in controlsDicts[1].items()
                                                   if val == pygame.key.name(event.key)][0]
                                playerArmList[1].extendArm(directionChosen)
                        if pygame.key.name(event.key) == controlsDicts[1]["shoot"]:
                            shootWave(playerList[1])
                heldKeys = pygame.key.get_pressed()
                if not any((heldKeys[pygame.K_UP], heldKeys[pygame.K_DOWN], heldKeys[pygame.K_LEFT],
                           heldKeys[pygame.K_RIGHT])):
                    playerArmList[0].armState = CluSprites.ArmStates.OFF_SCREEN
                    if playerList[0].playerState in [CluSprites.PlayerStates.SWINGING,
                                                     CluSprites.PlayerStates.HITTING_PLAYER_SWINGING]:
                        playerList[0].playerState = CluSprites.PlayerStates.MOVING
                    playerList[0].adjustPosition()
                if len(playerList) > 1:
                    if not any((heldKeys[pygame.K_KP8], heldKeys[pygame.K_KP2], heldKeys[pygame.K_KP4],
                                heldKeys[pygame.K_KP6])):
                        playerArmList[1].armState = CluSprites.ArmStates.OFF_SCREEN
                        if playerList[1].playerState in [CluSprites.PlayerStates.SWINGING,
                                                         CluSprites.PlayerStates.HITTING_PLAYER_SWINGING]:
                            playerList[1].playerState = CluSprites.PlayerStates.MOVING
                        playerList[1].adjustPosition()
            SCREEN.fill(BLACK)
            blitLevelData(playerList, level, timeCount)
            if not levelComplete:
                for group in CluSprites.allGroups:
                    for sprite in group:
                        SCREEN.blit(sprite.image, sprite.coordinates)
                # for sprite in CluSprites.armGroup:
                #     pygame.draw.rect(SCREEN, WHITE, sprite.wallCollisionRect)
                # for sprite in CluSprites.goldGroup:
                #     pygame.draw.rect(SCREEN, WHITE, sprite.collisionRect)
                for sprite in level.levelBorderRects:
                     pygame.draw.rect(SCREEN, WHITE, sprite)
                if pausedPlayerNumber == 0:
                    if frameCount % 5 == 0:
                        timeCount = max(0, timeCount - 1)
                    for group in CluSprites.allGroups:
                        group.update()
                    if timeCount > 200 and playingLowTimeMusic:
                        playingLowTimeMusic = False
                        pygame.mixer.music.load(LEVEL_MUSIC)
                        pygame.mixer.music.stop()
                        pygame.mixer.music.play(-1)
                    if timeCount == 200 and all(value < 1 for value in gameOverTextActive):
                        playingLowTimeMusic = True
                        pygame.mixer.music.load(LOW_TIME_MUSIC)
                        pygame.mixer.music.stop()
                        pygame.mixer.music.play(-1)
                    if timeCount == 0:
                        if not timeReachedZero:
                            frameCount = 0
                            timeReachedZero = True
                            playSound("death.wav")
                            for player in playerList:
                                player.playerState = CluSprites.PlayerStates.EXPLODING
                                pygame.mixer.music.stop()
                                player.frameCount = 0
                        if frameCount == 170 and any(player.lives > 0 for player in playerList):
                            timeReachedZero = False
                            timeCount = 400
                            pygame.mixer.music.load(LEVEL_MUSIC)
                            pygame.mixer.music.play(-1)
                    for player in playerList:
                        if player.playerState == CluSprites.PlayerStates.DEAD:
                            if gameOverTextActive[player.playerNumber - 1] == 0 and not\
                                    any(value == 1 for value in gameOverTextActive):
                                frameCount = 0
                                gameOverTextSprite = CluSprites.GameOverTextSprite(player.playerNumber)
                                gameOverTextSprite.initialize()
                                pygame.mixer.music.stop()
                                pygame.mixer.music.load(GAME_OVER_MUSIC)
                                pygame.mixer.music.play()
                                gameOverTextActive[player.playerNumber - 1] = 1
                            if gameOverTextActive[player.playerNumber - 1] == 1 and frameCount == 300:
                                gameOverTextActive[player.playerNumber - 1] = -1
                                pygame.mixer.music.stop()
                                if all(value == -1 for value in gameOverTextActive):
                                    pygame.mixer.music.load(LEVEL_END_MUSIC)
                                else:
                                    if timeCount > 200:
                                        pygame.mixer.music.load(LEVEL_MUSIC)
                                    else:
                                        pygame.mixer.music.load(LOW_TIME_MUSIC)
                                CluSprites.textGroup.empty()
                                pygame.mixer.music.play()

            # elif pausedPlayerNumber == 0:
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
                                                                CluSprites.PlayerStates.SWINGING]:
        playSound("shoot_wave.wav")
        newWave = CluSprites.SonicWaveSprite(player.facingDirection, player.playerNumber)
        newWave.setInitialCoordinates(player.coordinates[0], player.coordinates[1])
        CluSprites.attackGroup.add(newWave)


def setUpLevel(level):
    level.initialize()
    goldList = []
    rubberList = []
    for (x, y) in level.goldTilesVertical:
        goldList.append(CluSprites.GoldSprite())
        goldList[-1].initialize(-25 + 48 * x, 49 + 48 * y)
    for (x, y) in level.goldTilesHorizontal:
        goldList.append(CluSprites.GoldSprite())
        goldList[-1].isHorizontal = True
        goldList[-1].initialize(-1 + 48 * x, 25 + 48 * y)
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


def setTextCoordinates(value, numberOfPlayers):
    if numberOfPlayers == 1:
        textCoordinates = (90 + value, 345)
    else:
        textCoordinates = (122 + value, 345)
    return textCoordinates


def displayChangeControlMenu(subtitle, titleImageOne, titleImageTwo, numberOfPlayers):
    titleImageOne.setTitleImage()
    titleImageTwo.setTitleImage()
    controlToChange = "SHOOT"
    frameCount = 0
    playerNumber = 1
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
                controlToChange = changeControlInput(controlToChange, event, playerNumber, numberOfPlayers)
                frameCount = 0
        if controlToChange == "NONE":
            if playerNumber == numberOfPlayers:
                return
            else:
                playerNumber += 1
                controlToChange = "SHOOT"

        SCREEN.fill(BLACK)
        subtitleText = FONT.render("SECRETS OF OLD CLU CLU LAND", False, WHITE)
        SCREEN.blit(subtitleText, (42, 275))
        SCREEN.blit(subtitle, (50, 22))
        SCREEN.blit(titleImageOne.image, (98, 54))
        SCREEN.blit(titleImageTwo.image, (274, 54))
        if controlToChange == "UP":
            textCoordinates = setTextCoordinates(23, numberOfPlayers)
        elif controlToChange == "DOWN":
            textCoordinates = setTextCoordinates(5, numberOfPlayers)
        elif controlToChange == "RIGHT":
            textCoordinates = setTextCoordinates(0, numberOfPlayers)
        if numberOfPlayers == 1:
            controlInputText = FONT.render("SELECT '{}' BUTTON".format(controlToChange), False, WHITE)
        elif playerNumber == 1:
            controlInputText = FONT.render("P1 '{}' BUTTON".format(controlToChange), False, WHITE)
        else:
            controlInputText = FONT.render("P2 '{}' BUTTON".format(controlToChange), False, WHITE)
        if frameCount % 60 < 30:
            SCREEN.blit(controlInputText, textCoordinates)
        pygame.display.update()
        frameCount += 1
        CLOCK.tick(FPS)


def changeControlInput(controlToChange, event, playerNumber, numberOfPlayers):
    global controlsDicts
    currentIndex = playerNumber - 1
    if controlToChange == "SHOOT":
        if currentIndex == 0:
            for listIndex, controls in enumerate(controlsDicts):
                controlsDicts[listIndex] = controlsDicts[currentIndex].fromkeys(controlsDicts[currentIndex], "None")
        if not any(pygame.key.name(event.key) in controlValue.values() for controlValue in controlsDicts):
            controlsDicts[currentIndex]["shoot"] = pygame.key.name(event.key)
            controlToChange = "PAUSE"
    elif not any(pygame.key.name(event.key) in controlValue.values() for controlValue in controlsDicts):
        if controlToChange == "PAUSE":
            controlsDicts[currentIndex]["pause"] = pygame.key.name(event.key)
            controlToChange = "UP"
        elif controlToChange == "UP":
            controlsDicts[currentIndex]["up"] = pygame.key.name(event.key)
            controlToChange = "DOWN"
        elif controlToChange == "DOWN":
            controlsDicts[currentIndex]["down"] = pygame.key.name(event.key)
            controlToChange = "LEFT"
        elif controlToChange == "LEFT":
            controlsDicts[currentIndex]["left"] = pygame.key.name(event.key)
            controlToChange = "RIGHT"
        elif controlToChange == "RIGHT":
            controlsDicts[currentIndex]["right"] = pygame.key.name(event.key)
            controlToChange = "NONE"
            if playerNumber == numberOfPlayers:
                pygame.mixer.music.stop()
                pygame.time.delay(500)
    return controlToChange


def chooseOneOrTwoPlayers(subtitle, titleImageOne, titleImageTwo, textToDisplay):
    titleImageOne.setTitleImage()
    titleImageTwo.setTitleImage()
    subtitleText = FONT.render("SECRETS OF OLD CLU CLU LAND", False, WHITE)
    onePlayerText = FONT.render("1 PLAYER", False, CYAN)
    twoPlayerText = FONT.render("2 PLAYER", False, CYAN)
    optionText = FONT.render(textToDisplay, False, CYAN)
    cursorText = FONT.render(">", False, ORANGE)
    cursorLocation = (40, 330)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == controlsDicts[0]["pause"] and cursorLocation == (300, 330):
                    return 2
                elif pygame.key.name(event.key) == controlsDicts[0]["pause"]:
                    return 1
                elif pygame.key.name(event.key) == controlsDicts[0]["left"] or \
                     pygame.key.name(event.key) == controlsDicts[0]["right"]:
                    if cursorLocation == (40, 330):
                        cursorLocation = (300, 330)
                    else:
                        cursorLocation = (40, 330)
        SCREEN.fill(BLACK)
        SCREEN.blit(subtitleText, (42, 275))
        SCREEN.blit(subtitle, (50, 22))
        SCREEN.blit(titleImageOne.image, (98, 54))
        SCREEN.blit(titleImageTwo.image, (274, 54))
        SCREEN.blit(onePlayerText, (60, 330))
        SCREEN.blit(twoPlayerText, (320, 330))
        if textToDisplay == "CONTROLS":
            SCREEN.blit(optionText, (60, 350))
            SCREEN.blit(optionText, (320, 350))
        else:
            SCREEN.blit(optionText, (90, 350))
            SCREEN.blit(optionText, (350, 350))
        SCREEN.blit(cursorText, cursorLocation)

        pygame.display.update()
        CLOCK.tick(FPS)


def main():
    playerOneCurrentScore = 0
    playerTwoCurrentScore = 0

    while True:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # SCREEN.blit(pygame.image.load(os.path.join(backgroundFolder, "background_5A.png")), (0, 0))
        # goldIcon = pygame.image.load(os.path.join(spriteFolder, "gold_1.png")).convert()
        # goldIcon.set_colorkey(BLACK)
        # goldRotate = pygame.transform.flip(pygame.transform.rotate(goldIcon, 90), False, True)
        # for level in [CluLevels.BOX_PLUS]:
        #     level.setGoldCount()
        #     print(level, level.goldCount, len(level.goldTilesHorizontal), len(level.goldTilesVertical))
        #     SCREEN.blit(level.image, (0, 0))
        #     for (x, y) in level.goldTilesVertical:
        #         SCREEN.blit(goldIcon, (-25 + 48 * x, 49 + 48 * y))
        #     for (x, y) in level.goldTilesHorizontal:
        #         SCREEN.blit(goldRotate, (-1 + 48 * x, 25 + 48 * y))
        #     pygame.display.update()
        #     pygame.time.delay(60000)
        #     SCREEN.fill(BLACK)
        for group in CluSprites.allGroups:
            group.empty()
        displayTitleScreen(playerOneCurrentScore, playerTwoCurrentScore)
        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
