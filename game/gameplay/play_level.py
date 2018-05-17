import pygame as pg

from game.gameplay.draw_level import blitLevelData, blitLevelEndData, scrollLevelData
from game.gameplay.level import BonusLevel
from game.gameplay.player_actions import shootWave
from game.gameplay.setup_level import setLevelConstants, setLevelSprites, setLevelTime
from game.gameplay.state import checkPauseGame, checkQuitGame
from game.sprites.gold import GoldSprite
from game.sprites.player import PlayerSprite
from game.sprites.text import GameOverTextSprite
from game.sprites.urchin import UrchinSprite
from game.tools.asset_cache import playSound
import game.tools.constants as c
from game.tools.controls import controlsDicts


def playLevel(playerList, playerArmList, level, levelCount, gameOverTextStates, highScore):
    """Play the current level. Update and draw all sprites every frame, count down the timer, and control the
    state of the players and game depending on which keys are pressed.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        playerArmList: A list of all PlayerArmSprite objects in the game.
        level: A Level object representing the current level being played.
        levelCount: An integer storing the current number of levels played this game.
        gameOverTextStates: A list of four TextStates Enum instances, representing whether the gameOverTextSprite
            instances have been created for the player corresponding to that index.
        highScore: An integer showing the current high score.

    Returns:
        playerList: A list of all PlayerSprite objects in the game.
        highScore: An integer showing the current high score.
    """
    PlayerSprite.currentLevel = level
    setLevelSprites(level)
    setLevelConstants(levelCount)
    timeCount = setLevelTime(level, levelCount)
    targetTimeCount = max(1, timeCount - 300)
    pausedPlayerNumber = frameCount = 0

    # If any of the game over text sprites are still set to the ONSCREEN state from a previous level, change their
    # state to OFF_SCREEN to prevent a bug where new game over sprites would never become visible.
    for index, value in enumerate(gameOverTextStates):
        if value == c.TextStates.ONSCREEN:
            gameOverTextStates[index] = c.TextStates.OFF_SCREEN

    # scoreBonus tracks if the player should earn bonus points for completing the level quickly. If they complete the
    # level before the timer reaches targetTimeCount, the bonus is earned. If the timer ever reaches targetTimeCount,
    # scoringBonus is set to False for the current level.
    # playingLowTime music tracks if the music being played is the 'low time' music. If the timer increases above 200
    # while it's playing the 'low time' music, it loads and plays the standard music instead.
    # timeReachedZero tracks if the timer has already reached 0, so it only kills all players once at that point.
    # gameOverStarted tracks if the code to intialize a game over has begun. Initializing a game over takes
    scoreBonus = True
    playingLowTimeMusic = timeReachedZero = gameOverStarted = False
    c.SCREEN.fill(level.backgroundColor)
    goldCount = len(c.goldGroup)
    blitLevelData(playerList, level, goldCount, timeCount)
    pg.display.update()
    pg.mixer.music.load(c.LEVEL_START_MUSIC)
    pg.mixer.music.play()

    # There is a delay of 360 frames before the level is playable, to allow the level start music to finish playing.
    while frameCount < 360:
        checkQuitGame()
        frameCount += 1
        c.CLOCK.tick(c.FPS)

    # The event queue is cleared after the delay to ensure that no keys pressed as the level loads take effect
    # afterwards.
    pg.event.clear()

    if isinstance(level, BonusLevel):
        pg.mixer.music.load(c.BONUS_LEVEL_MUSIC)
    else:
        pg.mixer.music.load(c.LEVEL_MUSIC)
    pg.mixer.music.play(-1)
    for num, player in enumerate(playerList):
        player.initialize(48 * level.playerStartPosition[num][0], 49 + 48 * level.playerStartPosition[num][1])

    # This loop continues until either all players have run out of lives, or the level is completed.
    while True:
        pausedPlayerNumber = checkPauseGame(pausedPlayerNumber)
        checkQuitGame()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                for num, player in enumerate(playerList):

                    # Players who have run out of lives cannot pause the game.
                    # After pausing, the queue is cleared to ensure that no keys pressed while the game prepares to
                    # pause will take effect while paused.
                    if event.key == controlsDicts[num]["pause"] and player.playerState != c.PlayerStates.DEAD:
                        pg.mixer.music.pause()
                        playSound("pause_unpause.wav")
                        pausedPlayerNumber = num + 1
                        pg.time.delay(1000)
                        pg.event.clear()

                    # If the player presses a direction key while in the BALL state, the move in the direction pressed.
                    # If they are in an 'active' state, the player's arm is extended.
                    if event.key in [controlsDicts[num]["up"], controlsDicts[num]["down"],
                                     controlsDicts[num]["left"], controlsDicts[num]["right"]]:
                        if player.playerState == c.PlayerStates.BALL:
                            directionChosen = [key for key, val in controlsDicts[num].items()
                                               if val == event.key][0]
                            player.startMoving(directionChosen)
                        elif player.playerState in [c.PlayerStates.MOVING, c.PlayerStates.SWINGING,
                                                    c.PlayerStates.FINISHED_SWINGING]:
                            directionChosen = [key for key, val in controlsDicts[num].items()
                                               if val == event.key][0]
                            playerArmList[num].extendArm(directionChosen)
                    if event.key == controlsDicts[num]["shoot"] and not player.isFrozen:
                        shootWave(player)
        heldKeys = pg.key.get_pressed()

        # Every frame, check if each player is pressing any direction keys.
        # If the player is not and they are in a swinging state, they stop swinging.
        for num, player in enumerate(playerList):
            if not any((heldKeys[keyType] for keyType in [controlsDicts[num]["up"],
                                                          controlsDicts[num]["down"],
                                                          controlsDicts[num]["left"],
                                                          controlsDicts[num]["right"]])):
                playerArmList[num].armState = c.ArmStates.OFF_SCREEN

                # The player's state is set to MOVING if they are still facing the same direction as when they began
                # swinging.
                # Otherwise, it is set to FINISHED_SWINGING, so they have a brief period to pass over a black hole
                # sprite that may be beneath them.
                if player.playerState in [c.PlayerStates.SWINGING, c.PlayerStates.HITTING_PLAYER_SWINGING]:
                    if player.facingDirection == player.initialSwingDirection:
                        player.playerState = c.PlayerStates.MOVING
                    else:
                        player.playerState = c.PlayerStates.FINISHED_SWINGING
                    player.frameCount = 0
                    player.adjustPosition()

        goldCount = len([gold for gold in c.goldGroup if gold.goldState in [c.OtherStates.UPSIDE_DOWN,
                                                                            c.OtherStates.FLIPPING_DOWN,
                                                                            c.OtherStates.DELAYED_DOWN,
                                                                            c.OtherStates.OFF_SCREEN]])

        if pausedPlayerNumber == 0:

            # Standard gameplay updates every frame until all gold sprites have been revealed or all players have run
            # out of lives (And their game over text has moved off-screen), unless the game is paused.
            # If the current level is a bonus level, standard gameplay instead updates either either all gold sprites
            # have been revealed or the timer reaches 0.
            if goldCount > 0 and ((isinstance(level, BonusLevel) and timeCount > 0) or\
                                  (not isinstance(level, BonusLevel) and not all(value == c.TextStates.OFF_SCREEN for
                                                                                 value in gameOverTextStates))):
                blitLevelData(playerList, level, goldCount, timeCount)
                if pausedPlayerNumber == 0:
                    GoldSprite.globalFrameCount += 1
                    for group in c.allGroups:
                        group.update()
                        # Sprite coordinates are casted to integers before drawing them to the screen, as player
                        # sprites' coordinates are measured in sub-pixels.
                        for sprite in group:
                            c.SCREEN.blit(sprite.image, (int(sprite.coordinates[0]), int(sprite.coordinates[1])))

                    # Every 5 frames, the timer decreases by 1 (To a minimum of 0).
                    # The timer will not decrease if an ItemClock's effect is active.
                    if frameCount % 5 == 0 and not UrchinSprite.isFrozen:
                        timeCount = max(0, timeCount - 1)

                    # Scoring bonus points from targetTimeCount, playing the low time music, playing the regular music,
                    # or losing a life from the time reaching 0 all only happen during regular levels.
                    if not isinstance(level, BonusLevel):
                        if timeCount < targetTimeCount:
                            scoreBonus = False
                        if timeCount > 200 and playingLowTimeMusic:
                            playingLowTimeMusic = False
                            pg.mixer.music.load(c.LEVEL_MUSIC)
                            pg.mixer.music.stop()
                            pg.mixer.music.play(-1)

                        # Low time music does not play if any game over text sprites are currently onscreen.
                        if timeCount < 200 and not any(value == c.TextStates.ONSCREEN for value in gameOverTextStates)\
                                and not playingLowTimeMusic:
                            playingLowTimeMusic = True
                            pg.mixer.music.load(c.LOW_TIME_MUSIC)
                            pg.mixer.music.stop()
                            pg.mixer.music.play(-1)

                        if timeCount == 0:
                            if not timeReachedZero:
                                frameCount = 0
                                timeReachedZero = True
                                playSound("death.wav")
                                pg.mixer.music.stop()

                                # When the timer reaches 0, all players onscreen lose a life.
                                for player in playerList:
                                    if player.playerState not in [c.PlayerStates.DEAD, c.PlayerStates.OFF_SCREEN,
                                                                  c.PlayerStates.FALLING, c.PlayerStates.EXPLODING]:
                                        player.playerState = c.PlayerStates.EXPLODING
                                        player.frameCount = 0

                            # After 170 frames, the timer is increased if any players are still alive.
                            if frameCount == 170 and any(player.playerState != c.PlayerStates.DEAD for player in
                                                         playerList):
                                timeReachedZero = False
                                timeCount = 400
                                pg.mixer.music.load(c.LEVEL_MUSIC)
                                pg.mixer.music.play(-1)

                    for num, player in enumerate(playerList):
                        if player.playerState == c.PlayerStates.DEAD:
                            gameOverTextStates, frameCount = initializeGameOverSprite(gameOverTextStates, num,
                                                                                      frameCount, timeCount)

                # The only game logic that happens while the game is paused is drawing the sprites to the screen in the
                # same location they were in prior to the game being paused.
                else:
                    for group in c.allGroups:
                        for sprite in group:
                            c.SCREEN.blit(sprite.image, (int(sprite.coordinates[0]), int(sprite.coordinates[1])))

            # If all players have run out of lives and their game over text has moved off-screen, the level continues
            # to be animated for 330 frames to let the level end music finish playing, then scrolls off-screen.
            elif all(value == c.TextStates.OFF_SCREEN for value in gameOverTextStates):
                if not gameOverStarted:
                    pg.mixer.music.load(c.LEVEL_END_MUSIC)
                    pg.mixer.music.stop()
                    pg.mixer.music.play()
                    gameOverStarted = True
                    frameCount = 0
                elif frameCount < 330:
                    blitLevelData(playerList, level, goldCount, timeCount, animate=True)
                    pg.display.update()
                else:
                    scrollLevelData(playerList, level, goldCount, timeCount, levelCount, highScore)
                    for player in playerList:
                        player.frameCount = 0
                        player.playerState = c.PlayerStates.LEVEL_END
                    blitLevelEndData(playerList, level, timeCount, levelCount, highScore, scoreBonus)
                    for player in playerList:
                        player.playerState = c.PlayerStates.DEAD
                    return playerList, highScore

            # isFlashing is only set to True once all of the gold sprites are revealed and the level ends.
            # After 330 frames, the level scrolls off-screen and the next level can begin.
            elif not level.isFlashing:
                pg.mixer.music.load(c.LEVEL_END_MUSIC)
                pg.mixer.music.stop()
                pg.mixer.music.play()
                level.isFlashing = True
                for player in playerList:
                    if player.playerState != c.PlayerStates.DEAD:
                        player.playerState = c.PlayerStates.LEVEL_END
                frameCount = 0
            elif level.frameCount < 330:
                level.flashBoard()
                blitLevelData(playerList, level, 0, timeCount, animate=True)
                pg.display.update()
            else:
                scrollLevelData(playerList, level, 0, timeCount, levelCount, highScore)
                for player in playerList:
                    player.frameCount = 0

                    # Players already set to the LEVEL_END state (i.e., players who were not in the DEAD state) gain a
                    # life as the level ends.
                    # Then, all players are set to the LEVEL_END state for the end-of-level animations.
                    # This implicitly keeps dead players' lives at 0, while living players now have a minimum of 1
                    # life.
                    if player.playerState == c.PlayerStates.LEVEL_END:
                        player.lives += 1
                    player.playerState = c.PlayerStates.LEVEL_END
                blitLevelEndData(playerList, level, timeCount, levelCount, highScore, scoreBonus)

                # After the end-of-level scoring and animation, any player whose life count is still 0 is set to the
                # DEAD state.
                # Other players will be put in the BALL state by the program at the start of the next level.
                for player in playerList:
                    if player.lives == 0:
                        player.playerState = c.PlayerStates.DEAD
                return playerList, highScore

        pg.display.update()
        frameCount += 1

        # All methods that rely on frameCount do so in factors of 56100. To keep frameCount from increasing without
        # bounds, it resets to 0 every 56100 frames.
        # Realistically, frameCount will never reach this value in normal gameplay. This is only included as a
        # potential safeguard.
        if frameCount % 56100 == 0:
            frameCount = 0
        c.CLOCK.tick(c.FPS)


def initializeGameOverSprite(gameOverTextStates, index, frameCount, timeCount):
    """Adjust the values of the gameOverTextStates list.

    In the gameOverTextStates list, a value of NOT_REVEALED for a particular index represents that the game over
    text sprite has not yet been created for that index's player (i.e., that player still has lives, or has run
    out of lives, but another game over text sprite is currently onscreen).
    A value of ONSCREEN represents that the game over text sprite is currently onscreen for that index's player.
    It stays onscreen for 300 frames before disappearing, and only one can be onscreen at a time.
    A value of OFF_SCREEN represents that the game over text sprite has been created, but has been onscreen for
    300 frames, and is now off-screen.
    If all indexes have a value of OFF_SCREEN, that means that all players have run out of lives and received a
    game over.

    Args:
        gameOverTextStates: A list of four TextStates Enum instances, representing whether the gameOverTextSprite
            instances have been created for the player corresponding to that index.
        index: An integer corresponding to the player who has run out of lives that this function is checking.
        frameCount: An integer that increases by 1 every frame of gameplay.
                Used to control when other methods should be called.
        timeCount: An integer representing the time the players have remaining to complete the level.

    Returns:
        gameOverTextStates: A list of four TextStates Enum instances, representing whether the gameOverTextSprite
            instances have been created for the player corresponding to that index.
        frameCount: An integer that increases by 1 every frame of gameplay.
                Used to control when other methods should be called.
    """

    # If the player's game over text sprite has not yet been created, but none are currently visible onscreen, it sets
    # the appropriate index of gameOverTextStates to 'ONSCREEN' and creates a new gameOverTextSprite object.
    if gameOverTextStates[index] == c.TextStates.NOT_REVEALED and not any(value == c.TextStates.ONSCREEN for value in
                                                                          gameOverTextStates):
        frameCount = 0
        gameOverTextSprite = GameOverTextSprite(index + 1)
        gameOverTextSprite.initialize()
        pg.mixer.music.stop()
        pg.mixer.music.load(c.GAME_OVER_MUSIC)
        pg.mixer.music.play()
        gameOverTextStates[index] = c.TextStates.ONSCREEN

    # After 300 frames of being onscreen, the appropriate index of gameOverTextStates is set to OFF_SCREEN.
    # The gameOverTextSprite object is automatically deleted after 300 frames.
    if gameOverTextStates[index] == c.TextStates.ONSCREEN and frameCount == 300:
        gameOverTextStates[index] = c.TextStates.OFF_SCREEN
        pg.mixer.music.stop()

        # If no other players have lives remaining, and all gameOverTextSprite objects have been created, the game over
        # music plays.
        if all(value == c.TextStates.OFF_SCREEN for value in gameOverTextStates):
            pg.mixer.music.load(c.LEVEL_END_MUSIC)

        else:
            if timeCount > 200:
                pg.mixer.music.load(c.LEVEL_MUSIC)
            else:
                pg.mixer.music.load(c.LOW_TIME_MUSIC)
        pg.mixer.music.play()
    return gameOverTextStates, frameCount
