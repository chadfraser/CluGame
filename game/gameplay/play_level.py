import pygame as pg
import sys

from game.gameplay.draw_level import blitLevelData
from game.gameplay.player_actions import shootWave
from game.gameplay.setup_level import setLevelSprites, setLevelTime
from game.gameplay.state import checkPauseGame, checkQuitGame
from game.sprites.gold import GoldSprite
from game.sprites.player import PlayerSprite
from game.sprites.text import GameOverTextSprite
from game.sprites.urchin import UrchinSprite
from game.tools.asset_cache import playSound
import game.tools.constants as c
from game.tools.controls import controlsDicts


def playLevel(playerList, playerArmList, level, levelCount, gameOverTextStates, highScore):
    """Increment the level count and play the current level. Update and draw all sprites every frame, count down
    the timer, and control the state of the players and game depending on which keys are pressed.

    Args:
        playerList: A list of all PlayerSprite objects in the game.
        playerArmList: A list of all PlayerArmSprite objects in the game.
        level: A Level object representing the current level being played.
        levelCount: An integer storing the current number of levels played this game.
        gameOverTextStates: A list of four TextStates Enum instances, representing whether the gameOverTextSprite
            instances have been created for the player corresponding to that index.
        highScore: An integer showing the current high score.
    """

    levelCount += 1
    setLevelSprites(level, levelCount)
    timeCount = setLevelTime(level, levelCount)
    targetTimeCount = timeCount - 300
    pausedPlayerNumber = frameCount = 0
    # scoreBonus tracks if the player should earn bonus points for completing the level quickly. If they complete the
    # level before the timer reaches targetTimeCount, the bonus is earned. If the timer ever reaches targetTimeCount,
    # scoringBonus is set to False.
    # playingLowTime music tracks if the music being played is the 'low time' music. If the timer increases above 200
    # while it's playing the 'low time' music, it loads and plays the standard music instead.
    # timeReachedZero tracks if the timer has already reached 0, so it only kills all players once at that point.

    scoreBonus = True
    playingLowTimeMusic = timeReachedZero = False
    c.SCREEN.fill(level.backgroundColor)
    goldCount = len(c.goldGroup)
    blitLevelData(playerList, level, goldCount, timeCount, levelCount, highScore)
    pg.display.update()
    pg.mixer.music.load(c.LEVEL_START_MUSIC)
    pg.mixer.music.play()

    while frameCount < 360:
        checkQuitGame()
        frameCount += 1
        c.CLOCK.tick(c.FPS)
    # The event queue is cleared after the delay to ensure that no keys pressed as the level loads take effect
    # afterwards.

    pg.event.clear()
    pg.mixer.music.load(c.LEVEL_MUSIC)
    pg.mixer.music.play(-1)
    for num, player in enumerate(playerList):
        player.initialize(48 * level.playerStartPosition[num][0], 49 + 48 * level.playerStartPosition[num][1])
    PlayerSprite.currentLevel = level

    while True:
        # This loop continues until either all players have run out of lives, or the level is completed.

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
                    if event.key in [controlsDicts[num]["up"], controlsDicts[num]["down"],
                                     controlsDicts[num]["left"], controlsDicts[num]["right"]]:
                        # If the player presses a direction key while in the BALL state, the move in the direction
                        # pressed.
                        # If they are in an 'active' state, the player's arm is extended.

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
        for num, player in enumerate(playerList):
            # Every frame, check if each player is pressing any direction keys.
            # If not and they are in a swinging state, they stop swinging.

            if not any((heldKeys[keyType] for keyType in [controlsDicts[num]["up"],
                                                          controlsDicts[num]["down"],
                                                          controlsDicts[num]["left"],
                                                          controlsDicts[num]["right"]])):
                playerArmList[num].armState = c.ArmStates.OFF_SCREEN
                if player.playerState in [c.PlayerStates.SWINGING, c.PlayerStates.HITTING_PLAYER_SWINGING]:
                    if player.facingDirection == player.initialSwingDirection:
                        # The player's state is set to MOVING if they are still facing the same direction as when
                        # they began swinging.
                        # Otherwise, it is set to FINISHED_SWINGING, so they have a brief period to pass over a
                        # black hole sprite that may be beneath them.

                        player.playerState = c.PlayerStates.MOVING
                    else:
                        player.playerState = c.PlayerStates.FINISHED_SWINGING
                    player.frameCount = 0
                    player.adjustPosition()

        goldCount = len([gold for gold in c.goldGroup if gold.goldState in [c.OtherStates.UPSIDE_DOWN,
                                                                            c.OtherStates.FLIPPING_DOWN,
                                                                            c.OtherStates.DELAYED_DOWN,
                                                                            c.OtherStates.OFF_SCREEN]])
        if goldCount > 0:
            blitLevelData(playerList, level, goldCount, timeCount, levelCount, highScore)
            if pausedPlayerNumber == 0:
                GoldSprite.globalFrameCount += 1
                for group in c.allGroups:
                    group.update()
                    for sprite in group:
                        # Sprite coordinates are casted to integers before drawing them to the screen, as player
                        # sprites are measured in sub-pixels.

                        c.SCREEN.blit(sprite.image, (int(sprite.coordinates[0]), int(sprite.coordinates[1])))

                if frameCount % 5 == 0 and not UrchinSprite.isFrozen:
                    # Every 5 frames, the timer decreases by 1 (To a minimum of 0).
                    # The timer will not decrease if an ItemClock's effect is active.

                    timeCount = max(0, timeCount - 1)

                if timeCount < targetTimeCount:
                    scoreBonus = False
                if timeCount > 200 and playingLowTimeMusic:
                    playingLowTimeMusic = False
                    pg.mixer.music.load(c.LEVEL_MUSIC)
                    pg.mixer.music.stop()
                    pg.mixer.music.play(-1)
                if timeCount < 200 and not any(value == c.TextStates.ONSCREEN for value in gameOverTextStates):
                    # Low time music does not play if any game over text sprites are currently onscreen.

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
                        for player in playerList:
                            # When the timer reaches 0, all players onscreen lose a life.

                            if player.playerState not in [c.PlayerStates.DEAD, c.PlayerStates.OFF_SCREEN,
                                                          c.PlayerStates.FALLING, c.PlayerStates.EXPLODING]:
                                player.playerState = c.PlayerStates.EXPLODING
                                player.frameCount = 0
                    if frameCount == 170 and any(player.playerState != c.PlayerStates.DEAD for player in
                                                 playerList):
                        # After 170 frames, the timer is increased if any players are still alive.

                        timeReachedZero = False
                        timeCount = 400
                        pg.mixer.music.load(c.LEVEL_MUSIC)
                        pg.mixer.music.play(-1)
                for num, player in enumerate(playerList):
                    if player.playerState == c.PlayerStates.DEAD:
                        gameOverTextStates, frameCount = initializeGameOverSprite(gameOverTextStates, num,
                                                                                  frameCount, timeCount)
            else:
                # The only game logic that happens while the game is paused is drawing the sprites to the screen
                # in the same location they were in prior to the game being paused.

                for group in c.allGroups:
                    for sprite in group:
                        c.SCREEN.blit(sprite.image, (int(sprite.coordinates[0]), int(sprite.coordinates[1])))

        elif not level.isFlashing:
            # isFlashing is only set to True once all of the gold sprites are revealed and the level ends.
            # After 330 frames, the level scrolls off-screen and the next level can begin.

            pg.mixer.music.load(c.LEVEL_END_MUSIC)
            pg.mixer.music.stop()
            pg.mixer.music.play()
            level.isFlashing = True
            frameCount = 0
        elif level.frameCount < 330:
            level.flashBoard()
            blitLevelData(playerList, level, 0, timeCount, levelCount, highScore, animate=True)
            pg.display.update()
        else:
            blitLevelData(playerList, level, 0, timeCount, levelCount, highScore, scrolling=True)
            for player in playerList:
                if player.playerState != c.PlayerStates.DEAD:
                    player.lives += 1
                player.playerState = c.PlayerStates.LEVEL_END
                # getLevelDisplay
            pg.display.update()
            pg.time.delay(10000000)
        #         # Add level end
        #         pg.display.update()
        #         pg.time.delay(10000)
        pg.display.update()
        frameCount += 1
        if frameCount % 56100 == 0:
            # All methods that rely on frameCount do so in factors of 56100. To keep frameCount from increasing
            # without bounds, it resets to 0 every 56100 frames.
            # Realistically, frameCount will never reach this value in normal gameplay. This is only included as
            # a potential safeguard.

            frameCount = 0

        c.CLOCK.tick(c.FPS)

        # pg.mixer.music.stop()
        # pg.mixer.music.play()
        # pg.time.delay(6000)
        # pg.mixer.music.load(LEVEL_END_MUSIC)
        # pg.mixer.music.play()
        # pg.time.delay(6000)
        # pg.mixer.music.stop()
        # pg.event.clear()
        # return


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
    if gameOverTextStates[index] == c.TextStates.NOT_REVEALED and not any(value == c.TextStates.ONSCREEN for value in
                                                                          gameOverTextStates):
        # If the player's game over text sprite has not yet been created, but none are visible onscreen, it sets the
        # appropriate index of gameOverTextStates to 'ONSCREEN' and creates a new gameOverTextSprite object.

        frameCount = 0
        gameOverTextSprite = GameOverTextSprite(index + 1)
        gameOverTextSprite.initialize()
        pg.mixer.music.stop()
        pg.mixer.music.load(c.GAME_OVER_MUSIC)
        pg.mixer.music.play()
        gameOverTextStates[index] = c.TextStates.ONSCREEN

    if gameOverTextStates[index] == c.TextStates.ONSCREEN and frameCount == 300:
        # After 300 frames of being onscreen, the appropriate index of gameOverTextStates is set to OFF_SCREEN.
        # The gameOverTextSprite object is automatically deleted after 300 frames.

        gameOverTextStates[index] = -1
        pg.mixer.music.stop()
        if all(value == c.TextStates.OFF_SCREEN for value in gameOverTextStates):
            # If no other players have lives remaining, and all gameOverTextSprite objects have been created, the game
            # over music plays.

            pg.mixer.music.load(c.LEVEL_END_MUSIC)

        else:
            if timeCount > 200:
                pg.mixer.music.load(c.LEVEL_MUSIC)
            else:
                pg.mixer.music.load(c.LOW_TIME_MUSIC)
        pg.mixer.music.play()
    return gameOverTextStates, frameCount
