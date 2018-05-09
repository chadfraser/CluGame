import pygame as pg

import game.tools.constants as c
from game.sprites.player import PlayerSprite
from game.tools.asset_cache import playSound


class PlayerArmSprite(pg.sprite.Sprite):
    """Create a sprite of the player's arm.

    Attributes:
        playerBody: An instance of the PlayerSprite class that this arm belongs to.
    """

    def __init__(self, playerBody):
        """Init PlayerArmSprite using the PlayerSprite instance playerBody.

        Instance variables:
            coordinates: A tuple location to blit the sprite on the screen.
            swingingCoordinates: A tuple location storing the sprite's coordinates when it grabs a post.
            armState: An ArmStates Enum instance of the current state of the sprite.
                Used to determine which methods get called and when.
            extendedDirection: A Directions Enum instance of the current direction in which the sprite is
                extended.
                Used to determine how the sprite moves and whether its image is flipped.
                Should only be one of the four cardinal directions. Setting this to CLOCKWISE or COUNTER will
                cause unexpected and undesired results.
            currentAngleOctant: An integer indicating in which octant of the circle around this sprite's center
                point the playerBody object is currently located, with 0 being the octant from -22.5 degrees to
                22.5 degrees.
            emptyImage: A Surface object, showing a fully-transparent blank image.
                Used when the sprite should not be visibly drawn onscreen.
            image: The current image to be drawn for the sprite.
                Defaults to the emptyImage.
            rect: A rect object for the sprite.
            collisionRect: A smaller rect object used for checking collision between this sprite and others.
                This creates a better visual for collision than using the main rect object.
            wallCollisionRect: A smaller rect object used for checking collision between this sprite and the
                level boundary's rects.
                This rect is larger than collisionRect to ensure that it overlaps the level boundary's rects
                properly.
        """
        super().__init__(c.armGroup)
        self.playerBody = playerBody
        self.coordinates = (0, 0)
        self.swingingCoordinates = (0, 0)
        self.armState = c.ArmStates.OFF_SCREEN
        self.extendedDirection = c.Directions.RIGHT
        self.currentAngleOctant = 0

        self.emptyImage = self.playerBody.emptyImage
        self.image = self.emptyImage
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pg.rect.Rect((0, 0), (12, 12))
        self.wallCollisionRect = pg.rect.Rect((0, 0), (40, 40))

    def setCoordinates(self, x, y):
        """Set the sprite's coordinates using the passed arguments.

        This also adjusts the location of rect, collisionRect, and wallCollisionRect.
        Because this sprite should appear in the proper location on the playerBody PlayerSprite instance, the
        exact coordinates are offset by a specific amount based on the direction the playerBody object is facing
        and based on this sprite's extendedDirection.

        Args:
            x: An integer x coordinate to draw the sprite.
            y: An integer y coordinate to draw the sprite.
        """
        horizontalOffset = 14
        verticalOffset = 16
        if self.playerBody.facingDirection == c.Directions.LEFT:
            horizontalOffset -= 10
        elif self.playerBody.facingDirection == c.Directions.UP:
            verticalOffset -= 10

        if self.extendedDirection == c.Directions.UP:
            self.coordinates = (x + horizontalOffset, y - 12)
            self.collisionRect = pg.rect.Rect((self.coordinates[0] + 2, self.coordinates[1]), (12, 12))
        elif self.extendedDirection == c.Directions.DOWN:
            self.coordinates = (x + horizontalOffset, y + 32)
            self.collisionRect = pg.rect.Rect((self.coordinates[0] + 2, self.coordinates[1] + 4), (12, 12))
        elif self.extendedDirection == c.Directions.LEFT:
            self.coordinates = (x - 14, y + verticalOffset)
            self.collisionRect = pg.rect.Rect((self.coordinates[0], self.coordinates[1] + 2), (12, 12))
        else:
            self.coordinates = (x + 30, y + verticalOffset)
            self.collisionRect = pg.rect.Rect((self.coordinates[0] + 4, self.coordinates[1] + 2), (12, 12))
        self.rect.topleft = self.coordinates
        self.wallCollisionRect = pg.rect.Rect((self.coordinates[0] - 14, self.coordinates[1] - 14), (40, 40))

    def offsetGrabCoordinates(self, x, y):
        """Adjust the sprite's coordinates using the passed arguments.

        This also adjusts the location of rect, collisionRect, and wallCollisionRect.
        This is to be called when the sprite grabs onto a post, to ensure that it is centered on the post.

        Args:
            x: An integer x to show how many pixels to move the sprite to the left.
            y: An integer y to show how many pixels to move the sprite upwards.
        """
        self.coordinates = (self.coordinates[0] - x, self.coordinates[1] - y)
        self.rect.topleft = self.coordinates
        self.collisionRect = pg.rect.Rect((self.collisionRect[0] - x, self.collisionRect[1] - y), (12, 12))
        self.swingingCoordinates = (self.coordinates[0], self.coordinates[1])
        self.wallCollisionRect = pg.rect.Rect((self.coordinates[0] - 14, self.coordinates[1] - 14), (40, 40))

    def rotateImage(self):
        """Rotate the sprite's image either 0, 90, 180, or 270 degrees to the left, then flip it."""
        rotationDegrees = 90 * c.directionList.index(self.extendedDirection)
        self.image = pg.transform.rotate(self.image, rotationDegrees)
        self.flipImage()

    def flipImage(self):
        """Flip the sprite's image horizontally or vertically based on its extendedDirection and the direction
        that playerBody is facing.

        If the sprite is in the SWINGING state, it is further flipped based on which sixteenth of the circle
        around this sprite's center point the playerBody object is currently located.
        """
        if self.extendedDirection == c.Directions.UP:
            self.image = pg.transform.flip(self.image, True, False)
        if self.extendedDirection == c.Directions.RIGHT:
            self.image = pg.transform.flip(self.image, False, True)
        if self.armState == c.ArmStates.EXTENDED:
            if self.playerBody.facingDirection == c.Directions.LEFT:
                self.image = pg.transform.flip(self.image, True, False)
            if self.playerBody.facingDirection == c.Directions.UP:
                self.image = c.pg.transform.flip(self.image, False, True)
        else:
            playerAngleSixteenth = (self.playerBody.currentAngle % 360) // 22.5
            if self.playerBody.swingingDirection == c.Directions.CLOCKWISE:
                if playerAngleSixteenth in [5, 6, 7, 8]:
                    self.image = c.pg.transform.flip(self.image, False, True)
                if playerAngleSixteenth in [1, 2, 3, 4]:
                    self.image = pg.transform.flip(self.image, True, False)
            else:
                if playerAngleSixteenth in [0, 1, 2, 15]:
                    self.image = pg.transform.flip(self.image, False, True)
                if playerAngleSixteenth in [11, 12, 13, 14]:
                    self.image = pg.transform.flip(self.image, True, False)

    def flipDiagonalImage(self):
        """Flip and rotate the sprite's image based on its swingingDirection and which sixteenth of the circle
        around this sprite's center point the playerBody object is currently located.

        This method should only be called when the sprite is extended diagonally.
        """
        playerAngleSixteenth = (self.playerBody.currentAngle % 360) // 22.5
        if self.playerBody.swingingDirection == c.Directions.CLOCKWISE:
            if playerAngleSixteenth in [1, 2, 5, 6, 9, 10]:
                self.image = pg.transform.flip(self.image, True, False)
            if playerAngleSixteenth in [1, 2, 9, 10, 13, 14]:
                self.image = pg.transform.flip(self.image, False, True)
            if playerAngleSixteenth in [9, 10]:
                self.image = pg.transform.rotate(self.image, 90)
            if playerAngleSixteenth in [1, 2]:
                self.image = pg.transform.rotate(self.image, 270)
        else:
            if playerAngleSixteenth in [5, 6, 9, 10, 13, 14]:
                self.image = pg.transform.flip(self.image, True, False)
            if playerAngleSixteenth in [9, 10]:
                self.image = pg.transform.flip(self.image, False, True)
            if playerAngleSixteenth in [13, 14]:
                self.image = pg.transform.rotate(self.image, 90)
            if playerAngleSixteenth in [5, 6]:
                self.image = pg.transform.rotate(self.image, 270)

    def update(self):
        """Depending on the sprite's state and playerBody's state, determine which methods to call."""
        if self.playerBody.playerState in [c.PlayerStates.BALL, c.PlayerStates.FALLING, c.PlayerStates.HITTING_WALL,
                                           c.PlayerStates.EXPLODING, c.PlayerStates.OFF_SCREEN, c.PlayerStates.DEAD]:
            self.armState = c.ArmStates.OFF_SCREEN
        elif self.armState == c.ArmStates.EXTENDED:
            self.setCoordinates(self.playerBody.coordinates[0], self.playerBody.coordinates[1])
            self.checkGrabPost()
            self.image = self.playerBody.imageDict["arm"][0]
            self.rotateImage()
        elif self.armState == c.ArmStates.SWINGING:
            self.swing()
        if self.armState == c.ArmStates.OFF_SCREEN:
            self.image = self.emptyImage
        self.image.set_colorkey(c.BLACK)

    def extendArm(self, direction):
        """Make the sprite visible in its EXTENDED state if the direction passed is perpendicular to the
        playerBody's current direction.

        For safety's sake, this sets the sprite's state to OFF_SCREEN before checking whether or not to set it to
        EXTENDED.

        Args:
            direction: A string representation of which direction key the player has held.
                Note that if direction is not in "up", "down", "left", or "right", this will have no effect.
        """
        self.armState = c.ArmStates.OFF_SCREEN
        if self.playerBody.isFacingHorizontally() and direction in ["up", "down"]:
            self.extendedDirection = c.directionsDict[direction]
            self.armState = c.ArmStates.EXTENDED
        elif not self.playerBody.isFacingHorizontally() and direction in ["left", "right"]:
            self.extendedDirection = c.directionsDict[direction]
            self.armState = c.ArmStates.EXTENDED

    def checkGrabPost(self):
        """Set the sprite's state to SWINGING if it is over a post on the level image.

        To check if the sprite is over a post on the level image, it initially checks if the sprite is
        overlapping any of the level boundary's rects or a revealed rubber trap, as those cover up posts. It also
        checks if the playerBody object is overlapping with a trap or is frozen, as it cannot grab a post in
        either of those situations.
        If none of the above occurs, it checks if it is within 2 frames of (36 + 48x, 36 + 48y) in either
        direction, since every post on the level image is on those coordinates. This gives it a range where it
        can grab the post despite being a couple of pixels before or after the post's location.
        Note that because of this, if the player's speed is set to more than 5 pixels per frame, the arm may pass
        through posts it should grab.

        If the sprite meets the above criteria and grabs a post, its state and the playerBody's state are set to
        SWINGING, and the currentAngleOctant and the player's currentAngle are set based on the sprite's current
        extendedDirection.
        """
        if not any(self.wallCollisionRect.colliderect(levelRect) for levelRect in
                   PlayerSprite.currentLevel.levelBorderRects) and not \
                any(self.wallCollisionRect.colliderect(trap.collisionRect) for trap in c.rubberGroup if
                    trap.trapState in [c.OtherStates.REVEALED, c.OtherStates.TRIGGERED]) and not \
                any(self.playerBody.rect.colliderect(trap.collisionRect) for trap in c.rubberGroup) and not \
                self.playerBody.isFrozen:
            if self.collisionRect[0] % 48 in range(34, 39) and self.collisionRect[1] % 48 in range(34, 39) and \
                                    30 < self.collisionRect[0] < 500 and 20 < self.collisionRect[1] < 500:
                """CHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANG"""
                playSound("grab_post_move_end.wav")
                self.armState = c.ArmStates.SWINGING
                self.playerBody.playerState = c.PlayerStates.SWINGING
                self.setSwingDirection()

                if self.extendedDirection == c.Directions.LEFT:
                    self.playerBody.currentAngle = 0
                    self.currentAngleOctant = 0
                    self.coordinates = (self.coordinates[0] - 2, self.coordinates[1] - 2)
                elif self.extendedDirection == c.Directions.UP:
                    self.playerBody.currentAngle = 90
                    self.currentAngleOctant = 2
                    self.coordinates = (self.coordinates[0], self.coordinates[1] - 4)
                elif self.extendedDirection == c.Directions.RIGHT:
                    self.playerBody.currentAngle = 180
                    self.currentAngleOctant = 4
                    self.coordinates = (self.coordinates[0] + 2, self.coordinates[1] - 2)
                else:
                    self.playerBody.currentAngle = 270
                    self.currentAngleOctant = 6

                self.offsetGrabCoordinates(self.collisionRect[0] % 48 - 34, self.collisionRect[1] % 48 - 36)
                self.playerBody.swingingArmCoordinates = self.collisionRect.center

    def reverseDirection(self):
        """Set the sprite's facingDirection to the opposite of its current extendedDirection."""
        if self.extendedDirection == c.Directions.UP:
            self.extendedDirection = c.Directions.DOWN
        elif self.extendedDirection == c.Directions.DOWN:
            self.extendedDirection = c.Directions.UP
        elif self.extendedDirection == c.Directions.LEFT:
            self.extendedDirection = c.Directions.RIGHT
        else:
            self.extendedDirection = c.Directions.LEFT

    def setSwingDirection(self):
        """Set the playerBody's swingingDirection based on the current directions as it grabs the post, and
        stores its current direction as its initialSwingDirection."""
        if any(((self.extendedDirection == c.Directions.UP and self.playerBody.facingDirection == c.Directions.LEFT),
                (self.extendedDirection == c.Directions.DOWN and
                 self.playerBody.facingDirection == c.Directions.RIGHT),
                (self.extendedDirection == c.Directions.RIGHT and self.playerBody.facingDirection == c.Directions.UP),
                (self.extendedDirection == c.Directions.LEFT and
                 self.playerBody.facingDirection == c.Directions.DOWN))):
            self.playerBody.swingingDirection = c.Directions.CLOCKWISE
        else:
            self.playerBody.swingingDirection = c.Directions.COUNTER
        self.playerBody.initialSwingDirection = self.playerBody.facingDirection

    def changeSwingDirection(self):
        """Set the sprite's facingDirection based on its playerBody's currentAngle."""
        if 29 < self.playerBody.currentAngle < 120:
            self.extendedDirection = c.Directions.UP
        elif 119 < self.playerBody.currentAngle < 210:
            self.extendedDirection = c.Directions.RIGHT
        elif 209 < self.playerBody.currentAngle < 300:
            self.extendedDirection = c.Directions.DOWN
        else:
            self.extendedDirection = c.Directions.LEFT
        self.rotateImage()

    def swing(self):
        """Change the sprite's image based on its swingingDirection and its playerBody's currentAngle.

        If the playerBody state is no longer swinging, this sprite's state is set to OFF_SCREEN and the method is
        returned.
        Otherwise, the sprite's image is set to the orthogonal image if the playerBody is moving orthogonally, or
        to one of its diagonal images based on which of the quadrants the playerBody is in.
        """
        if self.playerBody.playerState not in [c.PlayerStates.SWINGING, c.PlayerStates.HITTING_PLAYER_SWINGING]:
            self.armState = c.ArmStates.OFF_SCREEN
            return
        if self.playerBody.isTurningOrthogonally():
            self.image = self.playerBody.imageDict["arm"][0]
            self.changeSwingDirection()
        else:
            playerAngleSixteenth = (self.playerBody.currentAngle % 360) // 22.5
            if (playerAngleSixteenth in [1, 2, 9, 10]) == (self.playerBody.swingingDirection
                                                           == c.Directions.CLOCKWISE):
                self.image = self.playerBody.imageDict["arm"][1]
            else:
                self.image = self.playerBody.imageDict["arm"][2]
            self.flipDiagonalImage()
        self.adjustPosition()

    def adjustPosition(self):
        """Slightly alter the sprite's coordinates and currentAngleOctant whenever it enters a new octant.

        Whenever the sprite enters a new octant, its coordinates are set to its initial swinging coordinates,
        then adjusted slightly by what octant it is in.
        This ensures that the visible part of the sprite's hand is always centered on the post, and that it does
        not end up off-centered should the sprite's swinging direction suddenly change from clockwise to
        counter-clockwise (or vice versa).
        """
        offsets = self.swingingCoordinates
        if self.playerBody.swingingDirection == c.Directions.CLOCKWISE:
            horizontalOffsets = [2, 0, 0, -2, -2, 0, 2, 2]
            verticalOffsets = [4, 4, 2, 2, 0, 0, 4, 2]
            if (self.currentAngleOctant * 45 + 22.5) < self.playerBody.currentAngle < \
                    (self.currentAngleOctant * 45 + 45):
                offsets = (offsets[0] + horizontalOffsets[self.currentAngleOctant],
                           offsets[1] + verticalOffsets[self.currentAngleOctant])
                self.currentAngleOctant = (self.currentAngleOctant + 1) % 8
                self.coordinates = (offsets[0], offsets[1])
        else:
            horizontalOffsets = [2, 2, 2, 0, -2, -2, 0, 0]
            verticalOffsets = [0, 2, 2, 4, 4, 2, 4, 0]
            if ((self.currentAngleOctant - 1) * 45) % 360 < self.playerBody.currentAngle < \
                    ((self.currentAngleOctant - 1) * 45 % 360 + 22.5):
                offsets = (offsets[0] + horizontalOffsets[self.currentAngleOctant],
                           offsets[1] + verticalOffsets[self.currentAngleOctant])
                self.currentAngleOctant = (self.currentAngleOctant - 1) % 8
                self.coordinates = (offsets[0], offsets[1])
