import pygame as pg

from game.sprites.sprite_sheet import SpriteSheet
import game.tools.constants as c


class SonicWaveSprite(pg.sprite.Sprite):
    """Create a sprite of the sonic wave fired by a player character.

    Attributes:
        direction: A string representation of which direction the firing player was facing when this sprite was
            created.
            Note that if direction is not in "up", "down", "left", or "right", this direction defaults to acting
            as though it were "right".
        firingPlayerNumber: A integer representing the number of the player that shot the sonic wave.
            Though none of this class' methods rely on this attribute, other functions do.
    """

    def __init__(self, direction, firingPlayerNumber=1):
        """Init SonicWaveSprite using the string direction and the integer firingPlayerNumber.

        Instance variables:
            spriteSheet: The SpriteSheet object for the wave sprite sheet image.
            animationFrames: A list of 2 Surface objects from the SpriteSheet object
            coordinates: A tuple location to blit the sprite on the screen.
            frameCount: An integer that increases whenever the update method is called.
                Used to control when other methods should be called.
            image: The current image to be drawn for the sprite.
                Defaults to the emptyImage.
            rect: A rect object for the sprite.
            collisionRect: A smaller rect object used for checking collision between this sprite and others.
                This creates a better visual for collision than using the main rect object.
        """
        super().__init__(c.attackGroup)
        spriteSheet = SpriteSheet("wave.png")
        self.animationFrames = []
        self.coordinates = (0, 0)
        self.direction = direction
        self.firingPlayerNumber = firingPlayerNumber
        self.frameCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 34, 34))
        self.image = self.animationFrames[0]
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pg.rect.Rect((0, 0), (16, 32))

    def setInitialCoordinates(self, x, y):
        """Set the sprite's initial coordinates based on the passed arguments.

        Because this sprite should appear a distance in front of the firing player sprite, the exact coordinates
        are offset by 20 pixels in this sprite's direction.

        Args:
            x: An integer x coordinate to draw the sprite.
            y: An integer y coordinate to draw the sprite.
        """
        if self.direction == c.Directions.UP:
            self.setCoordinates(x, y - 20)
        elif self.direction == c.Directions.DOWN:
            self.setCoordinates(x, y + 20)
        elif self.direction == c.Directions.LEFT:
            self.setCoordinates(x - 20, y)
        else:
            self.setCoordinates(x + 20, y)

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
        if self.isFacingHorizontally():
            self.collisionRect = pg.rect.Rect((x + 9, y + 1), (16, 32))
        else:
            self.collisionRect = pg.rect.Rect((x + 1, y + 9), (32, 16))

    def isFacingHorizontally(self):
        """Check if the sprite is currently facing one of the horizontal directions.

        Returns:
            A boolean representing whether the sprite is in fact facing right or left, or not.
        """
        return self.direction in [c.Directions.RIGHT, c.Directions.LEFT]

    def rotateImage(self):
        """Rotate the sprite's image either 0, 90, 180, or 270 degrees to the left."""
        rotationDegrees = 90 * c.directionList.index(self.direction)
        self.image = pg.transform.rotate(self.image, rotationDegrees)

    def update(self):
        """Increase frameCount. Moves the sprite six pixels forward, changes its image every frame, and
        disappears once frameCount is 32. When frameCount is 1, the sprite is moved 20 pixels forward.

        This prevents a glitch where the wave could not shoot an urchin that was too close to the player.

        If the sprite crosses over the left or right edge of the screen, they reappear at the opposite edge.
        This does not happen if the sprite crosses over the upper or lower edge of the screen.
        """
        self.frameCount += 1
        if self.direction == c.Directions.UP:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - 6)
        elif self.direction == c.Directions.DOWN:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + 6)
        elif self.direction == c.Directions.LEFT:
            self.setCoordinates(self.coordinates[0] - 6, self.coordinates[1])
        else:
            self.setCoordinates(self.coordinates[0] + 6, self.coordinates[1])
        if self.rect.right < 0:
            self.setCoordinates(512, self.coordinates[1])
        elif self.rect.left > 512:
            self.setCoordinates(-34, self.coordinates[1])

        if self.frameCount % 2 == 1:
            self.image = self.animationFrames[0]
        else:
            self.image = self.animationFrames[1]

        if self.frameCount == 1:
            self.setInitialCoordinates(self.coordinates[0], self.coordinates[1])
        elif self.frameCount == 32:
            self.kill()
        self.rotateImage()
        self.image.set_colorkey(c.BLACK)
