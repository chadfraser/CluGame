import pygame as pg

from game.sprites.sprite_sheet import SpriteSheet
from game.tools.asset_cache import playSound
import game.tools.constants as c


class RubberTrapSprite(pg.sprite.Sprite):
    """Create a sprite of the player character."""

    def __init__(self):
        """Init RubberTrapSprite.

        Instance variables:
            spriteSheet: The SpriteSheet object for the trap sprite sheet image.
            animationFrames: A list of 4 Surface objects from the SpriteSheet object
            coordinates: A tuple location to blit the sprite on the screen.
            trapState: An OtherStates Enum instance of the current state of the sprite.
                Used to determine which methods get called and when.
            collidingPlayer: An instance of the PlayerSprite class that collides with this sprite.
                Is a None type variable until the trap sprite overlaps with a player sprite.
            isHorizontal: A boolean indicating if the sprite should be rotated 90 degrees or not.
            flipTrigger: A boolean indicating if the trap is in a step in its animation where it is triggered and
                its image should be flipped.
            frameCount: An integer that increases whenever the animateTrap method is called.
            emptyImage: A Surface object, showing a fully-transparent blank image.
                Used when the sprite should not be visibly drawn onscreen.
            image: The current image to be drawn for the sprite.
                Defaults to the emptyImage.
            rect: A rect object for the sprite.
            collisionRect: A smaller rect object used for checking collision between this sprite and others.
                This creates a better visual for collision than using the main rect object.
        """
        super().__init__(c.rubberGroup)
        spriteSheet = SpriteSheet("trap.png")
        self.animationFrames = []

        self.coordinates = (0, 0)
        self.trapState = c.OtherStates.OFF_SCREEN
        self.collidingPlayer = None
        self.isHorizontal = self.flipTrigger = False
        self.frameCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 60, 56, 4, key=c.RED))
        self.emptyImage = spriteSheet.getSheetImage(0, 240, 60, 56, key=c.RED)

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
        horizontalOffsets = (6, 44)
        verticalOffsets = (24, 8)
        if self.isHorizontal:
            self.collisionRect = pg.rect.Rect((x + horizontalOffsets[0], y + verticalOffsets[0]),
                                              (horizontalOffsets[1], verticalOffsets[1]))
        else:
            self.collisionRect = pg.rect.Rect((x + verticalOffsets[0], y + horizontalOffsets[0]),
                                              (verticalOffsets[1], horizontalOffsets[1]))

    def rotateImage(self):
        """Rotate the sprite's image 90 degrees to the left if it is vertical."""
        if not self.isHorizontal:
            self.image = pg.transform.rotate(self.image, 90)

    def flipImage(self):
        """Flip the image vertically."""
        self.image = pg.transform.flip(self.image, False, True)

    def update(self):
        """Depending on trapState, determine which method to call, then check if the trap if colliding with any
        players.
        """
        if self.trapState == c.OtherStates.REVEALED:
            self.image = self.animationFrames[0]
        elif self.trapState == c.OtherStates.TRIGGERED:
            self.animateTrap()
        else:
            self.image = self.emptyImage
        self.checkPlayerCollision()
        self.rotateImage()

    def checkPlayerCollision(self):
        """Check if the sprite's rects are colliding with any of the player sprites.

        If the item sprite is not in the TRIGGERED state and collides with a player sprite, its state becomes the
        TRIGGERED state.
        The flipTrigger boolean is set to True if the colliding player is moving left or upwards, so the trap
        appears to be contorting around the player (As opposed to doing so in the direction opposite the player).
        """
        if self.trapState != c.OtherStates.TRIGGERED:
            for player in c.playerGroup:
                if self.collisionRect.colliderect(player.collisionRect) and\
                                player.playerState == c.PlayerStates.MOVING:
                    if self.trapState == c.OtherStates.OFF_SCREEN:
                        self.image.set_colorkey(c.RED)
                        playSound("bounce_rubber_or_player.wav")
                    else:
                        playSound("bounce_wall.wav")
                    self.collidingPlayer = player
                    self.trapState = c.OtherStates.TRIGGERED
                    if self.collidingPlayer.facingDirection == c.Directions.LEFT or \
                            self.collidingPlayer.facingDirection == c.Directions.UP:
                        self.flipTrigger = True
                    else:
                        self.flipTrigger = False

    def animateTrap(self):
        """Increase frameCount. Depending on frameCount, determines which methods to call.

        The sprite's image depends on frameCount to give the illusion of animation. If flipTrigger is True or if
        frameCount is in a certain range, the image is flipped vertically (If both these cases occur, then the
        flips cancel each other out).
        The colliding player bounces off of the sprite after 8 frames.
        To keep frameCount from increasing without bounds, it resets to 0 after 33 frames.
        """
        self.frameCount += 1
        animationIndex = self.getTrapAnimationStep()
        self.image = self.animationFrames[animationIndex]
        if self.flipTrigger:
            self.flipImage()
        if 18 < self.frameCount % 33 < 30:
            self.flipImage()
        if self.frameCount % 33 == 8:
            self.collidingPlayer.rebound()
        if self.frameCount % 33 == 0:
            self.frameCount = 0
            self.trapState = c.OtherStates.REVEALED

    def getTrapAnimationStep(self):
        """Get the index of the desired image the sprite should use, based on its frameCount. This gives the
        illusion of animation.

        Returns:
            An integer representing which index of animationFrames the sprite should use as its image.
        """
        if self.frameCount % 33 // 3 in (0, 4, 6, 8, 10):
            return 1
        elif self.frameCount % 33 // 3 in (1, 3, 7):
            return 2
        elif self.frameCount % 33 // 3 == 2:
            return 3
        else:
            return 0
