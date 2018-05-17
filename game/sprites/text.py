import pygame as pg

from game.sprites.sprite_sheet import SpriteSheet
import game.tools.constants as c


class PointsSprite(pg.sprite.Sprite):
    """Create a sprite of the 100 points text.

    Attributes:
        pointsImage: A Surface object to be used as the sprite's image.
        passingDirection: A Directions Enum instance of the direction the player was facing upon colliding with
            this sprite.
            Should only be one of the four cardinal directions. Setting this to CLOCKWISE or COUNTER will cause
            unexpected and undesired results.
    """

    def __init__(self, pointsImage, passingDirection=c.Directions.RIGHT):
        """Init PointsSprite using the Surface pointsImage and the Directions Enum passingDirection.

        Instance variables:
            coordinates: A tuple location to blit the sprite on the screen.
            isHorizontal: A boolean storing whether or not passingDirection is horizontal.
            frameCount: An integer that increases whenever the update method is called.
                Used to control when other methods should be called.
        """
        super().__init__(c.textGroup)
        self.image = pointsImage
        self.image.set_colorkey(c.BLACK)
        self.coordinates = (0, 0)
        self.passingDirection = passingDirection
        self.isHorizontal = False
        self.frameCount = 0

    def update(self):
        """Increase frameCount. Moves the sprite two pixels forward for the first six frames, and disappears
        once frameCount is 40.
        """
        self.frameCount += 1
        positionOffset = 2
        if self.passingDirection in [c.Directions.UP, c.Directions.LEFT]:
            positionOffset = -2
        if self.frameCount < 7:
            if self.isHorizontal:
                self.coordinates = (self.coordinates[0], self.coordinates[1] + positionOffset)
            else:
                self.coordinates = (self.coordinates[0] + positionOffset, self.coordinates[1])
        if self.frameCount == 40:
            self.kill()


class GameOverTextSprite(pg.sprite.Sprite):
    """Create a sprite of the game over text.

    Attributes:
        playerNumber: An integer representing whether the object represent player 1, 2, 3, or 4.
    """

    def __init__(self, playerNumber=1):
        """Init GameOverTextSprite using the integer playerNumber.

        Instance variables:
            spriteSheet: The SpriteSheet object for the display sprite sheet image.
            image: The current image to be drawn for the sprite. Always is the one image from spriteSheet.
            coordinates: A tuple location to blit the sprite on the screen.
            frameCount: An integer that increases whenever the update method is called.
                Used to control when other methods should be called.
        """
        super().__init__(c.textGroup)
        spriteSheet = SpriteSheet("display.png")
        self.image = spriteSheet.getSheetImage(404, 536, 62, 32)
        self.image.set_colorkey(c.RED)
        self.coordinates = (20, 478)
        self.playerNumber = playerNumber
        self.frameCount = 0

    def initialize(self):
        """Set the base coordinates of the sprite.

        If playerNumber is 1, or the total number of players is at least 3 and playerNumber is 2, the coordinates
        are set near the left edge of the screen. Otherwise, they are set near the right edge of the screen.
        This ensures that the first half of the players' list (rounded down) have their game over text spawn on
        the left edge of the screen, and the second half have it spawn on the right edge.
        """
        if self.playerNumber == 1 or self.playerNumber == 2 and len(c.playerGroup) > 2:
            self.coordinates = (20, 478)
        else:
            self.coordinates = (430, 478)

    def update(self):
        """Increase frameCount. Moves the sprite four pixels up for the first 37 frames, and disappears once
        once frameCount is 300.
        """
        self.frameCount += 1
        if self.coordinates[1] > 38:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 4)
        if self.frameCount == 300:
            self.kill()
