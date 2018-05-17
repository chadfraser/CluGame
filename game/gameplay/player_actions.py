import pygame as pg

from game.gameplay.state import checkQuitGame
from game.sprites.sonic_wave import SonicWaveSprite
import game.tools.constants as c
from game.tools.asset_cache import playSound
from game.tools.controls import controlsDicts


def pauseGame(pausingPlayerIndex):
    """Stop all onscreen action until the same player to pause the game unpauses it.

    This function will do nothing if any of the other players attempt to unpause the game. Only the pause button
    from the player who paused the game will have an effect.

    Args:
        pausingPlayerIndex: An integer representing which of the players initially paused the game.
    """
    while True:
        checkQuitGame()
        for event in pg.event.get():

            # After unpausing, the queue is cleared to ensure that no keys pressed during the game preparing to unpause
            # take effect.
            if event.type == pg.KEYDOWN:
                if event.key == controlsDicts[pausingPlayerIndex]["pause"]:
                    playSound("pause_unpause.wav")
                    pg.time.delay(1000)
                    pg.mixer.music.unpause()
                    pg.event.clear()
                    return


def shootWave(player):
    """Create a sonic wave sprite in front of the player who pressed the shoot button, assuming that player does
    not already have two sonic wave sprites active.

    Args:
        player: The PlayerSprite object for the player who is shooting a sonic wave.
    """
    sonicWavesFromPlayer = [sprite for sprite in c.attackGroup if sprite.firingPlayerNumber == player.playerNumber]
    if len(sonicWavesFromPlayer) < 2 and player.playerState in [c.PlayerStates.MOVING, c.PlayerStates.SWINGING,
                                                                c.PlayerStates.FINISHED_SWINGING]:
        waveCoordinates = player.coordinates

        # In order to keep the sonic wave sprite centered on its row or column, its initial coordinates are adjusted
        # by mod 48.
        # This is done because the player's coordinates are not necessarily centered on the row or column while they
        # are swinging.
        if player.isFacingHorizontally():
            if 0 < player.coordinates[1] % 48 < 24:
                waveCoordinates = (int(player.coordinates[0]),
                                   int(player.coordinates[1] - (player.coordinates[1] % 48)))
            elif player.coordinates[1] % 48 > 23:
                waveCoordinates = (int(player.coordinates[0]),
                                   int(player.coordinates[1] + (48 - player.coordinates[1] % 48)))
        else:
            if 0 < player.coordinates[0] % 48 < 24:
                waveCoordinates = (int(player.coordinates[0] - (player.coordinates[0] % 48)),
                                   int(player.coordinates[1]))
            elif player.coordinates[0] % 48 > 23:
                waveCoordinates = (int(player.coordinates[0] + (48 - player.coordinates[0] % 48)),
                                   int(player.coordinates[1]))
        playSound("shoot_wave.wav")
        newWave = SonicWaveSprite(player.facingDirection, player.playerNumber)
        newWave.setInitialCoordinates(waveCoordinates[0], waveCoordinates[1])
        c.attackGroup.add(newWave)
