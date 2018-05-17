import pygame as pg

from game.gameplay.level import BonusLevel
from game.sprites.sprite_sheet import SpriteSheet
from game.sprites.player import PlayerSprite
from game.sprites.text import PointsSprite
from game.tools.asset_cache import playSound
import game.tools.constants as c


class GoldSprite(pg.sprite.Sprite):
    """Create a sprite of the gold item.

    Class variables:
        levelCount: An integer storing how many levels the player has currently played.
            Once levelCount reaches 22, the below methods change slightly.
        globalFrameCount: An integer storing a frame count common to all gold sprites.
    """

    levelCount = 0
    globalFrameCount = 0

    def __init__(self):
        """Init GoldSprite.

        Instance variables:
            spriteSheet: The SpriteSheet object for the gold sprite sheet image.
                If the current level is an instance of the BonusLevel class, uses the bonus sprite sheet image.
            animationFrames: A list of 8 Surface objects from the SpriteSheet object.
            coordinates: A tuple location to blit the sprite on the screen.
            goldState: An OtherStates Enum instance of the current state of the sprite.
                Used to determine which methods get called and when.
            passingDirection: A Directions Enum instance of the direction the player was facing upon colliding
                with this sprite.
                Should only be one of the four cardinal directions. Setting this to CLOCKWISE or COUNTER will
                cause unexpected and undesired results.
            isHorizontal: A boolean indicating if the sprite should be rotated 270 degrees or not.
            alreadyRevealed: A boolean indicating if the sprite has already been revealed by a player.
                Players only earn points from colliding with gold sprites that have not already been revealed.
            frameCount: An integer that increases whenever the update method is called.
            animationCount: An integer tracking from where in animationFrame the sprite should take its next
                image.
            flashImage: A Surface object, showing the gold flashing brightly.
            pointsImage: A Surface object, showing the 100 points earned from first revealing a gold sprite.
                The GoldSprite class never uses this image directly, but passes it to the PointsSprite class
                when creating a new instance of the latter.
            emptyImage: A Surface object, showing a fully-transparent blank image.
                Used when the sprite should not be visibly drawn onscreen.
            image: The current image to be drawn for the sprite.
                Defaults to the emptyImage.
            rect: A rect object for the sprite.
            collisionRect: A smaller rect object used for checking collision between this sprite and others.
                This creates a better visual for collision than using the main rect object.
        """
        super().__init__(c.goldGroup)
        if isinstance(PlayerSprite.currentLevel, BonusLevel):
            spriteSheet = SpriteSheet("gold_bonus.png")
        else:
            spriteSheet = SpriteSheet("gold.png")
        self.animationFrames = []

        self.coordinates = (0, 0)
        self.goldState = c.OtherStates.OFF_SCREEN
        self.passingDirection = c.Directions.RIGHT
        self.isHorizontal = self.alreadyRevealed = False
        self.frameCount = self.animationCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 34, 34))
        self.animationFrames.extend(spriteSheet.getStripImages(0, 34, 34, 34))
        self.flashImage = spriteSheet.getSheetImage(0, 68, 34, 34)
        self.pointsImage = spriteSheet.getSheetImage(34, 68, 34, 34)
        self.emptyImage = spriteSheet.getSheetImage(34, 102, 34, 34)

        self.image = self.emptyImage
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pg.rect.Rect((0, 0), (16, 32))

    def setCoordinates(self, x, y):
        """Set the sprite's coordinates to the passed arguments.

        This also adjusts the location of rect and collisionRect.
        Because collisionRect is a rectangle, its exact coordinates, width, and height depend on whether or not
        this sprite is facing horizontally.

        Args:
            x: An integer x coordinate to draw the sprite.
            y: An integer y coordinate to draw the sprite.
        """
        self.coordinates = x, y
        self.rect.topleft = x, y
        if self.isHorizontal:
            self.collisionRect = pg.rect.Rect((x + 1, y + 9), (32, 16))
        else:
            self.collisionRect = pg.rect.Rect((x + 9, y + 1), (16, 32))

    def rotateImage(self):
        """Rotate the sprite's image 270 degrees to the left and flip it if it is horizontal."""
        if self.isHorizontal:
            self.image = pg.transform.rotate(self.image, 270)
            self.image = pg.transform.flip(self.image, True, False)

    def update(self):
        """Increase frameCount. Depending on frameCount and playerState, determines which methods to call."""
        self.frameCount += 1

        # If the sprite's state is REVEALED, it flashes every 6 frames.
        # This uses the globalFrameCount so the revealed gold sprites all flash in sync.
        # It sets its default image to its fourth animation frame.
        if self.goldState == c.OtherStates.REVEALED:
            if GoldSprite.globalFrameCount % 12 < 6:
                self.image = self.animationFrames[3]
            else:
                self.image = self.flashImage
            self.animationCount = 3

        # If the sprite's state is UPSIDE_DOWN, sets its default image is its eighth animation frame.
        elif self.goldState == c.OtherStates.UPSIDE_DOWN:
            self.image = self.animationFrames[7]
            self.animationCount = 7
        elif self.goldState == c.OtherStates.FLIPPING_UP:
            self.flipUp()
        elif self.goldState == c.OtherStates.FLIPPING_DOWN:
            self.flipDown()
        elif self.goldState == c.OtherStates.OFF_SCREEN:
            self.image = self.emptyImage
        elif self.goldState == c.OtherStates.DELAYED_UP:
            if GoldSprite.globalFrameCount % 12 < 6:
                self.image = self.animationFrames[3]
            else:
                self.image = self.flashImage
            self.animationCount = 3

            # Gold stays in the delayed state for 10 frames after being flipped to prevent it from flipping again too
            # quickly
            if self.frameCount % 10 == 0:
                self.goldState = c.OtherStates.REVEALED
        elif self.goldState == c.OtherStates.DELAYED_DOWN:
            self.image = self.animationFrames[7]
            if self.frameCount % 10 == 0:
                self.goldState = c.OtherStates.UPSIDE_DOWN

        # All methods that rely on frameCount do so in factors of 360. To keep frameCount from increasing without
        # bounds, it resets to 0 every 360 frames.
        if self.frameCount % 360 == 0:
            self.frameCount = 0

        # Because the globalFrameCount is only relevant in terms of its value mod 12, its resets every 12 frames to
        # keep it from increasing without bounds.
        if GoldSprite.globalFrameCount % 12 == 0:
            GoldSprite.globalFrameCount = 0
        self.rotateImage()
        self.image.set_colorkey(c.BLACK)

    def startFlipAnimation(self):
        """Set the sprite's state as it is passed over.

        If the sprite has already been revealed, frameCount is set to 12 instead of 0 to account for the fact
        that its image is already in the middle of its flipping animation.
        Gold sprites cannot enter the FLIPPING_DOWN state while in a bonus level, or before level 22.
        """
        self.frameCount = 0
        playSound("pass_over_gold.wav")
        if self.goldState == c.OtherStates.REVEALED and GoldSprite.levelCount > 21 and not\
                isinstance(PlayerSprite.currentLevel, BonusLevel):
            self.goldState = c.OtherStates.FLIPPING_DOWN
        elif self.goldState in [c.OtherStates.UPSIDE_DOWN, c.OtherStates.OFF_SCREEN, c.OtherStates.REVEALED]:
            if self.alreadyRevealed:
                self.frameCount = 12
            self.goldState = c.OtherStates.FLIPPING_UP

    def flipUp(self):
        """Change the sprite's image based on its animationCount, until it is facing up. Create a new instance of
        the PointsSprite class if this sprite has not already been revealed.

        If passingDirection is down or left, the image cycles through animationFrames in the negative direction.
        Otherwise, it cycles through them in the positive direction.
        """
        if self.frameCount % 3 == 0:
            if self.passingDirection in [c.Directions.UP, c.Directions.LEFT]:
                if self.animationCount == 0:
                    self.animationCount = 7
                else:
                    self.animationCount -= 1
            else:
                if self.animationCount == 7:
                    self.animationCount = 0
                else:
                    self.animationCount += 1
        self.image = self.animationFrames[self.animationCount]
        if self.frameCount % 36 == 0:
            self.goldState = c.OtherStates.DELAYED_UP
            if not self.alreadyRevealed:
                points100 = PointsSprite(self.pointsImage, self.passingDirection)
                positionOffset = 10
                if self.passingDirection in [c.Directions.UP, c.Directions.LEFT]:
                    positionOffset = -10
                if self.isHorizontal:
                    points100.coordinates = (self.coordinates[0], self.coordinates[1] + positionOffset)
                    points100.isHorizontal = True
                else:
                    points100.coordinates = (self.coordinates[0] + positionOffset, self.coordinates[1])
                self.alreadyRevealed = True
            self.frameCount = 0

    def flipDown(self):
        """Change the sprite's image based on its animationCount, until it is facing down.

        If passingDirection is down or left, the image cycles through animationFrames in the negative direction.
        Otherwise, it cycles through them in the positive direction.
        """
        if self.frameCount % 3 == 0:
            if self.passingDirection in [c.Directions.UP, c.Directions.LEFT]:
                if self.animationCount == 0:
                    self.animationCount = 7
                else:
                    self.animationCount -= 1
            else:
                if self.animationCount == 7:
                    self.animationCount = 0
                else:
                    self.animationCount += 1
        self.image = self.animationFrames[self.animationCount]
        if self.frameCount % 36 == 0:
            self.goldState = c.OtherStates.DELAYED_DOWN
            self.frameCount = 0
