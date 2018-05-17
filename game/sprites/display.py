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
        """
        super().__init__(c.displayGroup)
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
            self.coordinates = (50, 487)
        else:
            self.coordinates = (50, 711)
        self.image.set_colorkey(c.RED)


class HalfDisplaySprite(pg.sprite.Sprite):
    """Create a sprite of the small end-of-level display, for when there are more than two characters.

    Attributes:
        playerNumber: An integer representing the player that this display is displaying.
    """

    def __init__(self, playerNumber=1):
        """Init HalfDisplaySprite.

        Instance variables:
            spriteSheet: The SpriteSheet object for the display sprite sheet image.he bonus sprite sheet image.
            image: The current image to be drawn for the sprite. Always is the one image from spriteSheet.
            coordinates: A tuple location to blit the sprite on the screen.
        """
        super().__init__(c.displayGroup)
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
            self.coordinates = (4, 484)
        elif playerNumber == 2:
            self.coordinates = (260, 484)
        elif playerNumber == 3:
            self.coordinates = (4, 708)
        else:
            self.coordinates = (260, 708)
        self.image.set_colorkey(c.RED)


class DisplayIconSprite(pg.sprite.Sprite):
    """Create a sprite of the small scoring icon that appears during the end-of-level display.

    Attributes:
        playerNumber: An integer representing the player that this display is displaying.
        numberOfPlayers: An integer representing how many players are currently playing the game.
    """

    def __init__(self, playerNumber=1, numberOfPlayers=1):
        """Init HalfDisplaySprite.

        Instance variables:
            emptyImage: A Surface object, showing a fully-transparent blank image.
                Used when the sprite should not be visibly drawn onscreen.
            urchinImage: A Surface object, showing an urchin enemy.
                Used when the sprite is counting how many enemies the player has killed.
            goldImage: A Surface object, showing a gold sprite.
                Used when the sprite is counting how many gold sprites the player has collected.
                Is rotated and flipped in order to appear horizontally.
            image: The current image to be drawn for the sprite. Always is the one image from spriteSheet.
            coordinates: A tuple location to blit the sprite on the screen.
            frameCount: An integer that increases whenever the update method is called.
        """
        super().__init__(c.textGroup)
        self.animationCount = 0
        self.emptyImage = SpriteSheet("gold.png").getSheetImage(68, 68, 34, 34)
        self.urchinImage = SpriteSheet("urchin.png").getSheetImage(68, 34, 34, 34)
        self.goldImage = SpriteSheet("gold.png").getSheetImage(0, 68, 34, 34)
        self.goldImage = pg.transform.rotate(self.goldImage, 270)
        self.goldImage = pg.transform.flip(self.goldImage, True, False)
        self.image = self.emptyImage

        if playerNumber == 1:
            self.coordinates = (21, 137)
            if numberOfPlayers < 3:
                self.coordinates = (91, 132)
        elif playerNumber == 2:
            self.coordinates = (277, 137)
            if numberOfPlayers < 3:
                self.coordinates = (91, 356)
        elif playerNumber == 3:
            self.coordinates = (21, 361)
        else:
            self.coordinates = (277, 361)
        self.frameCount = 0
        self.image.set_colorkey(c.BLACK)

    def setIconImage(self):
        """Change the sprite's image based on animationCount, then increment animationCount by 1."""
        if self.animationCount == 0:
            self.image = self.urchinImage
        elif self.animationCount == 1:
            self.image = self.goldImage
        else:
            self.image = self.emptyImage
        self.animationCount += 1
