import pygame as pg

import game.gameplay.level as lvl
from game.sprites.sprite_sheet import SpriteSheet
from game.sprites.player import PlayerSprite
import game.tools.constants as c


class FullDisplaySprite(pg.sprite.Sprite):
    """Create a sprite of the large end-of-level display.

    Attributes:
        playerNumber: An integer representing the player that this display is displaying.
    """

    def __init__(self, playerNumber=1):
        """Init FullDisplaySprite.

        Instance variables:
            spriteSheet: The SpriteSheet object for the display sprite sheet image.he bonus sprite sheet image.
            image: The current image to be drawn for the sprite. Always is the one image from spriteSheet.
            coordinates: A tuple location to blit the sprite on the screen.
            frameCount: An integer that increases whenever the update method is called.
        """
        super().__init__(c.textGroup)
        spriteSheet = SpriteSheet("display.png")
        if isinstance(PlayerSprite.currentLevel, lvl.BoardTwoLevel):
            self.image = spriteSheet.getSheetImage(402, 242, 402, 146)
        elif isinstance(PlayerSprite.currentLevel, lvl.BoardThreeLevel):
            self.image = spriteSheet.getSheetImage(0, 388, 402, 146)
        elif isinstance(PlayerSprite.currentLevel, lvl.BoardFourLevel):
            self.image = spriteSheet.getSheetImage(402, 388, 402, 146)
        elif isinstance(PlayerSprite.currentLevel, lvl.BoardFiveLevel):
            self.image = spriteSheet.getSheetImage(0, 534, 402, 146)
        else:
            self.image = spriteSheet.getSheetImage(0, 242, 402, 146)

        if playerNumber == 1:
            self.coordinates = (56, 570)
        else:
            self.coordinates = (56, 794)
        self.frameCount = 0
        self.image.set_colorkey(c.RED)

    def update(self):
        """Increase frameCount. Depending on frameCount, change the sprite's coordinates."""
        self.frameCount += 1
        if self.frameCount < 88:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 6)


class HalfDisplaySprite(pg.sprite.Sprite):
    """Create a sprite of the small end-of-level display, for when there are more than two characters.

    Attributes:
        level: A Level instance of the level that was just completed.
        playerNumber: An integer representing the player that this display is displaying.
    """

    def __init__(self, level, playerNumber=1):
        """Init HalfDisplaySprite.

        Instance variables:
            spriteSheet: The SpriteSheet object for the display sprite sheet image.he bonus sprite sheet image.
            image: The current image to be drawn for the sprite. Always is the one image from spriteSheet.
            coordinates: A tuple location to blit the sprite on the screen.
            frameCount: An integer that increases whenever the update method is called.
        """
        super().__init__(c.textGroup)
        spriteSheet = SpriteSheet("display.png")
        if isinstance(PlayerSprite.currentLevel, lvl.BoardTwoLevel):
            self.image = spriteSheet.getSheetImage(250, 680, 250, 146)
        elif isinstance(PlayerSprite.currentLevel, lvl.BoardThreeLevel):
            self.image = spriteSheet.getSheetImage(500, 680, 250, 146)
        elif isinstance(PlayerSprite.currentLevel, lvl.BoardFourLevel):
            self.image = spriteSheet.getSheetImage(0, 826, 250, 146)
        elif isinstance(PlayerSprite.currentLevel, lvl.BoardFiveLevel):
            self.image = spriteSheet.getSheetImage(250, 826, 250, 146)
        else:
            self.image = spriteSheet.getSheetImage(0, 680, 250, 146)

        if playerNumber == 1:
            self.coordinates = (6, 570)
        elif playerNumber == 2:
            self.coordinates = (260, 570)
        elif playerNumber == 3:
            self.coordinates = (6, 794)
        else:
            self.coordinates = (260, 794)
        self.frameCount = 0
        self.image.set_colorkey(c.RED)

    def update(self):
        """Increase frameCount. Depending on frameCount, change the sprite's coordinates."""
        self.frameCount += 1
        if self.frameCount < 88:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 6)
