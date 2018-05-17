import pygame as pg

import game.tools.constants as c
from game.sprites.sprite_sheet import SpriteSheet
from game.tools.asset_cache import playSound


class DemoSprite(pg.sprite.Sprite):
    """Create an instance of a sprite for the demo.

    This class should not be called directly. Only call its subclasses.

    Attributes:
        coordinates: A tuple location to blit the sprite on the screen.
    """

    def __init__(self, coordinates=(0, 0)):
        """Init DemoSprite using the tuple coordinates.

        Instance variables:
            spriteSheet: The SpriteSheet object for the demo sprite sheet image.
            animationFrames: An empty list. Subclasses replace this with a list of Surface objects from the
                SpriteSheet object.
            frameCount: An integer that increases whenever the update method is called in the subclasses.
                Used to control when other methods should be called.
            emptyImage: A Surface object, showing a fully-transparent blank image.
                Used when the sprite should not be visibly drawn onscreen.
            image: The current image to be drawn for the sprite.
                Defaults to the emptyImage.
            rect: A rect object for the sprite.
        """
        super().__init__(c.demoGroup)
        self.spriteSheet = SpriteSheet("demo.png")
        self.animationFrames = []
        self.coordinates = coordinates
        self.frameCount = 0
        self.emptyImage = self.spriteSheet.getSheetImage(546, 416, 32, 32)
        self.image = self.emptyImage
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        """Not to be called directly, but inherited by subclasses."""
        pass

    def setCoordinates(self):
        """Change the sprite's coordinates.

        If the demo player sprite is currently swinging, this sprite's coordinates change based on how they are
        swinging.
        Otherwise, it changes based on which direction the demo player sprite is facing.
        """
        if DemoPlayerSprite.swingValue != (0, 0):
            self.coordinates = (self.coordinates[0] + DemoPlayerSprite.swingValue[0],
                                self.coordinates[1] + DemoPlayerSprite.swingValue[1])
        elif not DemoPlayerSprite.paused:
            if DemoPlayerSprite.facingDirection == c.Directions.UP:
                offsets = (0, 4)
            elif DemoPlayerSprite.facingDirection == c.Directions.DOWN:
                offsets = (0, -4)
            elif DemoPlayerSprite.facingDirection == c.Directions.LEFT:
                offsets = (4, 0)
            else:
                offsets = (-4, 0)
            self.coordinates = (self.coordinates[0] + offsets[0], self.coordinates[1] + offsets[1])
        self.rect.topleft = self.coordinates

    def setMonochromeImage(self):
        """Not to be called directly, but inherited by subclasses."""
        pass


class PostSprite(DemoSprite):
    """Create an instance of a post sprite for the demo.

    Attributes:
        coordinates: A tuple location to blit the sprite on the screen.
    """

    def __init__(self, coordinates=(0, 0)):
        """Init PostSprite using the tuple coordinates.

        Instance variables:
            animationFrames: A list of 2 Surface objects from the SpriteSheet object.
            image: The current image to be drawn for the sprite.
                Defaults to the first image in animationFrames.
        """
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(0, 0, 32, 32, 2)
        self.image = self.animationFrames[0]

    def setMonochromeImage(self):
        """Set the sprite's image to its monochrome variant."""
        self.image = self.animationFrames[1]


class DemoPlayerSprite(DemoSprite):
    """Create an instance of a player sprite for the demo.

    Attributes:
        demoNumber: An integer determining whether this sprite belongs to the first, second, third, or fourth
            demo animation.
        coordinates: A tuple location to blit the sprite on the screen.
    Class variables:
        facingDirection: A Directions Enum instance of the current direction the sprite is facing.
            Used to determine which direction the sprite moves and whether its image is flipped.
            Should only be one of the four cardinal directions. Setting this to CLOCKWISE or COUNTER will cause
            unexpected and undesired results.
        swingValue: A tuple of two integers, indicating the horizontal and vertical value each other sprite's
            coordinates should change if this sprite is swinging.
        paused: A boolean indicating if this sprite should remain stationary, and thus no other sprite's
            coordinates should change.
    """

    facingDirection = c.Directions.RIGHT
    swingValue = (0, 0)
    paused = False

    def __init__(self, demoNumber=0, coordinates=(0, 0)):
        """Init DemoPlayerSprite using the integer demoNumber and the tuple coordinates.

        Instance variables:
            playerNumber: An integer one greater than demoNumber. Used over demoNumber for the sake of clarity in
                in methods.
            animationFrames: A list of multiple Surface objects from the SpriteSheet object.
                Which Surface objects are included depends on playerNumber.
            image: The current image to be drawn for the sprite.
                Defaults to the emptyImage.
            rect: A rect object for the sprite.
            animated: A boolean indicating whether or not the sprite is currently going through a non-movement
                based animation.
            clockwise: A boolean indicating whether or not the sprite is moving clockwise when it swings.
            swingFrameCount: An integer determining which frame of animation the sprite is moving while swinging.
        """
        super().__init__(coordinates)
        self.playerNumber = demoNumber + 1
        if self.playerNumber == 1:
            self.animationFrames = self.spriteSheet.getStripImages(0, 236, 68, 104, 5)
        elif self.playerNumber == 2:
            self.animationFrames = self.spriteSheet.getStripImages(0, 340, 68, 76, 6)
        elif self.playerNumber == 3:
            self.animationFrames = self.spriteSheet.getStripImages(0, 416, 68, 104, 9)
        else:
            self.animationFrames = self.spriteSheet.getStripImages(408, 340, 68, 76, 2)
        self.image = self.animationFrames[0]
        self.rect = self.image.get_rect()
        self.animated = False
        self.clockwise = True
        self.swingFrameCount = 0

    def update(self):
        """Increase frameCount. Depending on frameCount and playerNumber, determine which methods to call."""
        self.frameCount += 1

        # The sprite's image changes every 4 frames to create the illusion of animation.
        # This is overshadowed if one of the below methods changes the sprite's image on the same frame.
        if self.facingDirection in [c.Directions.LEFT, c.Directions.RIGHT]:
            if self.frameCount % 8 < 4:
                self.image = self.animationFrames[0]
            else:
                self.image = self.animationFrames[1]
        else:
            if self.frameCount % 8 < 4:
                self.image = self.animationFrames[4]
            else:
                self.image = self.animationFrames[5]

        if self.playerNumber == 1:
            self.playerOneUpdate()
        elif self.playerNumber == 2:
            self.playerTwoUpdate()
        elif self.playerNumber == 3:
            self.playerThreeUpdate()
        else:
            self.playerFourUpdate()

        # The sprite's image flips horizontally if it is facing left, or vertically if it is facing upwards.
        # This is not triggered if frameCount is 0, since all sprites start on the same coordinates when the demo
        # animation begins.
        if DemoPlayerSprite.facingDirection == c.Directions.LEFT and 0 < self.frameCount:
            self.image = pg.transform.flip(self.image, True, False)
        elif DemoPlayerSprite.facingDirection == c.Directions.UP and 0 < self.frameCount:
            self.image = pg.transform.flip(self.image, False, True)

    def playerOneUpdate(self):
        """Change the sprite's image and coordinates based on frameCount, if it strikes a wall demo sprite.

        Is only to be called if playerNumber is 1.
        """
        if DemoPlayerSprite.paused:
            if self.frameCount == 1:
                self.coordinates = (self.coordinates[0] + 18, self.coordinates[1])
            if self.frameCount < 6:
                self.image = self.animationFrames[2]
            elif self.frameCount < 8:
                self.image = self.animationFrames[3]
            elif self.frameCount < 11:
                self.image = self.animationFrames[4]
            elif self.frameCount == 11:
                DemoPlayerSprite.paused = False
                DemoPlayerSprite.facingDirection = c.Directions.LEFT
                self.coordinates = (self.coordinates[0] - 16, self.coordinates[1])

    def playerTwoUpdate(self):
        """Change the sprite's image and coordinates based on frameCount and swingFrameCount, if it is in a
        position where its swinging should be animated.

        Is only to be called if playerNumber is 2.
        """
        if 106 < self.frameCount < 147 or 170 < self.frameCount < 211 or 232 < self.frameCount:
            self.swing()
            if 5 < self.swingFrameCount < 15 or 23 < self.swingFrameCount < 35 or 44 < self.swingFrameCount < 54 or\
                    62 < self.swingFrameCount < 73:
                if self.frameCount % 8 < 4:
                    self.image = self.animationFrames[2]
                else:
                    self.image = self.animationFrames[3]
                if 23 < self.swingFrameCount < 35 and not self.clockwise:
                    self.image = pg.transform.flip(self.image, False, True)
            elif 14 < self.swingFrameCount < 24 or 53 < self.swingFrameCount < 63:
                if self.frameCount % 8 < 4:
                    self.image = self.animationFrames[4]
                else:
                    self.image = self.animationFrames[5]

        if self.swingFrameCount == 6:
            if self.clockwise:
                DemoPlayerSprite.facingDirection = c.Directions.DOWN
            else:
                DemoPlayerSprite.facingDirection = c.Directions.UP
        elif self.swingFrameCount == 24 or self.swingFrameCount == 45:
            DemoPlayerSprite.facingDirection = c.Directions.LEFT
        elif self.swingFrameCount == 63:
            DemoPlayerSprite.facingDirection = c.Directions.RIGHT

        if self.frameCount == 112 or self.frameCount == 176:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 4)
        elif self.frameCount == 129 or self.frameCount == 193:
            self.coordinates = (self.coordinates[0], self.coordinates[1] + 4)
        elif self.frameCount == 147:
            DemoPlayerSprite.swingValue = (0, 0)
            self.swingFrameCount = 39
            DemoPlayerSprite.paused = False
            self.clockwise = False
        elif self.frameCount == 211:
            DemoPlayerSprite.swingValue = (0, 0)
            self.swingFrameCount = 0
            DemoPlayerSprite.paused = False

    def swing(self):
        """Change the swingValue tuple based on if the sprite is swinging clockwise and its swingFrameCount.

        This sets paused to True to prevent all other sprites from moving automatically, as their movement should
        be completely governed by swingValue while this method is called.
        Is only to be called if playerNumber is 2.
        """
        DemoPlayerSprite.paused = True
        self.swingFrameCount = (self.swingFrameCount + 1) % 76
        swingOffsets = (0, 0)
        if self.swingFrameCount % 76 in (0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 14, 15, 16, 64, 65, 67, 68, 70, 71, 72,
                                         75):
            swingOffsets = (swingOffsets[0] - 4, swingOffsets[1])
        if self.swingFrameCount % 76 in (22, 25, 27, 29, 31, 32, 33, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
                                         48, 50, 55):
            swingOffsets = (swingOffsets[0] + 4, swingOffsets[1])
        if self.swingFrameCount % 76 in (4, 7, 9, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 26, 27, 28, 30, 32,
                                         34, 37, 6, 15):
            swingOffsets = (swingOffsets[0], swingOffsets[1] - 4)
        if self.swingFrameCount % 76 in (43, 45, 47, 48, 49, 51, 52, 54, 56, 57, 58, 59, 60, 61, 62, 64, 65, 66, 68,
                                         69, 71, 74, 53, 44):
            swingOffsets = (swingOffsets[0], swingOffsets[1] + 4)
        if self.clockwise:
            DemoPlayerSprite.swingValue = (swingOffsets[0], swingOffsets[1])
        else:
            DemoPlayerSprite.swingValue = (swingOffsets[0], -swingOffsets[1])

    def playerThreeUpdate(self):
        """Change the sprite's image and coordinates based on frameCount, if it strikes a wall demo sprite or
        strikes a black home demo sprite.

        Is only to be called if playerNumber is 3.
        """
        if self.animated:
            if self.frameCount == 9:
                playSound("death.wav")
                DemoPlayerSprite.paused = True
                self.image = self.animationFrames[5]
            elif 15 < self.frameCount:
                animationNumber = min(3, (self.frameCount - 14) // 8)
                self.image = self.animationFrames[5 + animationNumber]
        elif DemoPlayerSprite.paused:
            if self.frameCount == 1:
                self.coordinates = (self.coordinates[0] - 18, self.coordinates[1])
            if self.frameCount < 4:
                self.image = self.animationFrames[2]
            elif self.frameCount < 6:
                self.image = self.animationFrames[3]
            elif self.frameCount < 11:
                self.image = self.animationFrames[4]
            elif self.frameCount == 11:
                DemoPlayerSprite.paused = False
                DemoPlayerSprite.facingDirection = c.Directions.RIGHT
                self.coordinates = (self.coordinates[0] + 18, self.coordinates[1])

    def playerFourUpdate(self):
        """Change the sprite's image and coordinates based on frameCount and the animated boolean, if it collides
        with a rubber trap demo sprite.

        Is only to be called if playerNumber is 4.
        """
        if self.animated:
            if self.frameCount == 8:
                self.animated = False
                if DemoPlayerSprite.facingDirection == c.Directions.RIGHT:
                    DemoPlayerSprite.facingDirection = c.Directions.LEFT
                else:
                    DemoPlayerSprite.facingDirection = c.Directions.RIGHT
                self.frameCount = 0

                for sprite in c.demoGroup:
                    if isinstance(sprite, DemoArmSprite):
                        if DemoPlayerSprite.facingDirection == c.Directions.RIGHT:
                            sprite.coordinates = (sprite.coordinates[0] + 12, sprite.coordinates[1])
                        else:
                            sprite.coordinates = (sprite.coordinates[0] - 12, sprite.coordinates[1])

    def setCoordinates(self):
        """Set the sprite's rect to match its coordinates."""
        self.rect.topleft = self.coordinates


class DemoArmSprite(DemoSprite):
    """Create an instance of a player's arm sprite for the demo.

    Attributes:
        demoNumber: An integer determining whether this sprite belongs to the first, second, third, or fourth
            demo animation.
        coordinates: A tuple location to blit the sprite on the screen.
        flipped: A boolean indicating if this sprite should be flipped horizontally.
    """

    def __init__(self, demoNumber=1, coordinates=(0, 0), flipped=False):
        """Init DemoArmSprite using the integer demoNumber and the tuple coordinates.

        Instance variables:
            animationFrames: A list of multiple Surface objects from the SpriteSheet object.
                Which Surface objects are included depends on playerNumber.
            extendedDirection: A Directions Enum instance of the current direction in which the sprite is
                extended.
                Used to determine how the sprite moves and whether its image is flipped.
                Should only be one of the four cardinal directions. Setting this to CLOCKWISE or COUNTER will
                cause unexpected and undesired results.
        """
        super().__init__(coordinates)
        self.demoNumber = demoNumber
        self.animationFrames = self.spriteSheet.getStripImages(64, 0, 32, 32, 4)
        self.flipped = flipped
        self.extendedDirection = c.Directions.RIGHT

    def update(self):
        """Increase frameCount. Depending on frameCount and playerNumber, determine which methods to call.

        For safety's sake, this sets the sprite's image to the emptyImage before running any other methods, which
        may or may not change its image again.
        """
        self.frameCount += 1
        self.image = self.emptyImage
        if self.demoNumber == 1:
            # If demoNumber is 1, this sprite's image will rotate, flip, and change based on frameCount to create
            # the illusion of animation.

            if 100 < self.frameCount < 147 or 164 < self.frameCount < 211 or 226 < self.frameCount:
                self.image = self.animationFrames[0]
                if 120 < self.frameCount < 130 or 183 < self.frameCount < 193 or 246 < self.frameCount < 256 or\
                        285 < self.frameCount < 296 or 324 < self.frameCount:
                    self.image = pg.transform.rotate(self.image, 270)
                if 129 < self.frameCount < 141 or 192 < self.frameCount < 204 or 255 < self.frameCount < 267 or\
                        295 < self.frameCount < 306:
                    self.image = self.animationFrames[1]
                    self.image = pg.transform.rotate(self.image, 90)
                elif 111 < self.frameCount < 121 or 174 < self.frameCount < 184 or 237 < self.frameCount < 247 or\
                        276 < self.frameCount < 286 or 315 < self.frameCount < 325:
                    self.image = self.animationFrames[2]
            else:
                self.image = self.emptyImage
            self.adjustPosition()
            if self.extendedDirection == c.Directions.LEFT:
                self.image = pg.transform.flip(self.image, True, False)
            if self.frameCount in [107, 171, 233]:
                playSound("grab_post_move_end.wav")

        # If demoNumber is 1, this sprite's and coordinates will flip and change based on frameCount to create the
        # illusion of animation.
        else:
            if 50 < self.frameCount < 150 or 180 < self.frameCount < 215 or 280 < self.frameCount:
                self.image = self.animationFrames[3]
            elif self.frameCount == 180:
                self.flipped = False
                self.coordinates = (self.coordinates[0], self.coordinates[1] + 88)
            elif self.frameCount == 215:
                self.flipped = True
                self.coordinates = (self.coordinates[0], self.coordinates[1] - 88)
            if DemoPlayerSprite.facingDirection == c.Directions.LEFT:
                self.image = pg.transform.flip(self.image, True, False)
        if self.flipped:
            self.image = pg.transform.flip(self.image, False, True)

    def setCoordinates(self):
        """Change the coordinates if the demo player sprite is paused (i.e., if it is swinging)."""
        if DemoPlayerSprite.paused:
            self.coordinates = (self.coordinates[0] + DemoPlayerSprite.swingValue[0],
                                self.coordinates[1] + DemoPlayerSprite.swingValue[1])
        self.rect.topleft = self.coordinates

    def adjustPosition(self):
        """Offset the arm's coordinates based on frameCount to ensure it stays overlapping with the post.

        Is only to be called if playerNumber is 2.
        """
        horizontalOffset = 0
        verticalOffset = 0
        if self.frameCount in [141, 184, 267, 286]:
            horizontalOffset = -4
        if self.frameCount in [121, 204, 247, 306, 325]:
            horizontalOffset = 4
        if self.frameCount in [238, 267, 325]:
            verticalOffset = -4
        if self.frameCount in [112, 141, 175, 204, 277, 307]:
            verticalOffset = 4
        if self.frameCount == 147:
            verticalOffset = 88
        if self.frameCount == 211:
            horizontalOffset = 8
        self.coordinates = (self.coordinates[0] + horizontalOffset, self.coordinates[1] + verticalOffset)

        if self.frameCount in [130, 193, 296]:
            self.flipped = True
        if self.frameCount == 147 or self.frameCount == 256:
            self.flipped = False
        if self.frameCount == 130 or self.frameCount == 256:
            self.extendedDirection = c.Directions.LEFT
        if self.frameCount == 193 or self.frameCount == 296:
            self.extendedDirection = c.Directions.RIGHT


class DemoGoldSprite(DemoSprite):
    """Create an instance of a gold sprite for the demo.

    Attributes:
        coordinates: A tuple location to blit the sprite on the screen.
    """

    def __init__(self, coordinates=(0, 0)):
        """Init DemoGoldSprite using the tuple coordinates.

        Instance variables:
            animationFrames: A list of 11 Surface objects from the SpriteSheet object.
            animationCount: An integer tracking from where in animationFrame the sprite should take its next
                image.
            timesFlipped: An integer tracking how many times this sprite has started its flip animation.
            flipping: A boolean indicating if the sprite is currently in its flip animation.
            rect: A rect object for the sprite.
        """
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(0, 32, 68, 68, 10)
        self.animationCount = 0
        self.timesFlipped = 0
        self.flipping = False
        self.rect = self.image.get_rect()

    def update(self):
        """Increase frameCount. Depending on frameCount and timesFlipped, determine which methods to call."""
        self.frameCount += 1
        if self.flipping and 9 < self.frameCount:
            self.flipUp()
        elif self.timesFlipped:
            if self.frameCount % 12 < 6:
                self.image = self.animationFrames[3]
            else:
                self.image = self.animationFrames[8]

        # If the demo player sprite collides with this sprite, it sets flipping to True.
        # timesFlipped should always be either 0 or 1 during the demo animation, and thus frameCount will be set to
        # either 0 or 9 (To account for the fact that its image is already in the middle of its flipping animation).
        # This is not triggered if frameCount is 0, since all sprites start on the same coordinates when the demo
        # animation begins.
        for sprite in c.demoGroup:
            if isinstance(sprite, DemoPlayerSprite) and self.rect.colliderect(sprite.rect) and\
                    0 < self.frameCount and not self.flipping:
                playSound("pass_over_gold.wav")
                self.flipping = True
                self.frameCount = 9 * self.timesFlipped

    def flipUp(self):
        """Change the sprite's image based on its animationCount, until it is facing up after 36 frames."""
        if self.timesFlipped == 0:
            if self.frameCount % 3 == 0:
                if self.animationCount == 7:
                    self.animationCount = 0
                else:
                    self.animationCount += 1
        else:
            if self.frameCount % 3 == 0:
                if self.animationCount == 0:
                    self.animationCount = 7
                else:
                    self.animationCount -= 1
        self.image = self.animationFrames[self.animationCount]
        if self.frameCount == 36:
            self.timesFlipped += 1
            self.frameCount = 0
            self.flipping = False

    def setMonochromeImage(self):
        """Set the sprite's image to its monochrome variant."""
        self.image = self.animationFrames[9]


class DemoHoleSprite(DemoSprite):
    """Create an instance of a black hole sprite for the demo.

    Attributes:
        coordinates: A tuple location to blit the sprite on the screen.
    """

    def __init__(self, coordinates=(0, 0)):
        """Init DemoHoleSprite using the tuple coordinates.

        Instance variables:
            animationFrames: A list of 11 Surface objects from the SpriteSheet object.
            animationCount: An integer tracking from where in animationFrame the sprite should take its next
                image.
            image: The current image to be drawn for the sprite.
            rect: A rect object for the sprite.
        """
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(0, 100, 68, 68, 5)
        self.animationCount = 0
        self.image = self.animationFrames[0]
        self.rect = self.image.get_rect()

    def update(self):
        """Increase frameCount. Depending on frameCount, determine which Surface object to use as its image.

        The sprite's image changes every 6 frames, cycling through the animationFrames list.
        """
        self.frameCount += 1
        if self.frameCount % 6 == 0:
            self.animationCount += 1
            if self.animationCount == 4:
                self.animationCount = 0
            self.image = self.animationFrames[self.animationCount]

        for sprite in c.demoGroup:
            if isinstance(sprite, DemoPlayerSprite) and self.rect.collidepoint(sprite.rect.center) and\
                            self.frameCount and not sprite.animated:
                sprite.animated = True
                sprite.frameCount = 0

    def setMonochromeImage(self):
        """Set the sprite's image to its monochrome variant."""
        self.image = self.animationFrames[4]


class DemoUrchinSprite(DemoSprite):
    """Create an instance of an urchin sprite for the demo.

    Attributes:
        coordinates: A tuple location to blit the sprite on the screen.
    """

    def __init__(self, coordinates=(0, 0)):
        """Init DemoUrchinSprite using the tuple coordinates.

        Instance variables:
            animationFrames: A list of 11 Surface objects from the SpriteSheet object.
            animationCount: An integer tracking the current state of the sprite's animation.
            image: The current image to be drawn for the sprite.
            rect: A rect object for the sprite.
        """
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(136, 168, 68, 68, 7)
        self.animationCount = 0
        self.audioCount = 1
        self.image = self.animationFrames[0]
        self.rect = self.image.get_rect()

    def update(self):
        """Increase frameCount. Depending on frameCount and animationCount, determine which methods to call.

        The sprite's image changes every 5th and 8th frame in an 8 frame cycle until it is crushed against a demo
        wall sprite.
        """
        self.frameCount += 1
        if self.animationCount == 0:
            if self.frameCount % 8 < 5:
                self.image = self.animationFrames[0]
            else:
                self.image = self.animationFrames[1]
            for sprite in c.demoGroup:
                if isinstance(sprite, DemoWaveSprite) and self.rect.collidepoint(sprite.rect.center) and\
                        0 < self.frameCount:
                    playSound("push_or_shoot_enemy.wav")
                    self.animationCount = 1
                    self.frameCount = 0
        elif self.animationCount == 1:
            if self.frameCount < 3:
                self.image = self.animationFrames[2]
            elif self.frameCount % 8 < 5:
                self.image = self.animationFrames[3]
            else:
                self.image = self.animationFrames[4]
            for sprite in c.demoGroup:
                if isinstance(sprite, DemoPlayerSprite) and self.rect.colliderect(sprite.rect) and\
                        self.animationCount == 1:
                    self.animationCount = 2
                    self.frameCount = 0
        elif self.animationCount == 2:
            if self.frameCount > 3:
                self.coordinates = (self.coordinates[0] - 4, self.coordinates[1])
                self.audioCount += 1
            if self.audioCount % 10 == 0:
                    playSound("push_or_shoot_enemy.wav")
        else:
            if self.frameCount < 5:
                self.image = self.animationFrames[5]
            elif self.frameCount < 10:
                self.image = self.animationFrames[6]
            else:
                self.kill()


class DemoWaveSprite(DemoSprite):
    """Create an instance of a sonic wave sprite for the demo.

    Attributes:
        coordinates: A tuple location to blit the sprite on the screen.
    """

    def __init__(self, coordinates=(0, 0)):
        """Init DemoWaveSprite using the tuple coordinates.

        Instance variables:
            animationFrames: A list of 11 Surface objects from the SpriteSheet object.
            rect: A rect object for the sprite.
        """
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(0, 168, 68, 68, 2)
        self.rect = self.image.get_rect()

    def update(self):
        """Increase frameCount. After 28 frames, the sprite appears and then moves forward eight pixels every
        frame.
        """
        self.frameCount += 1
        if self.frameCount == 28:
            playSound("shoot_wave.wav")
        if 28 < self.frameCount:
            self.coordinates = (self.coordinates[0] - 8, self.coordinates[1])
            self.image = self.animationFrames[0]
            if self.frameCount % 2 == 0:
                self.image = self.animationFrames[1]


class DemoRubberTrapSprite(DemoSprite):
    """Create an instance of a rubber trap sprite for the demo.

    Attributes:
        demoNumber: An integer determining whether this sprite belongs to the first, second, third, or fourth
            demo animation.
        coordinates: A tuple location to blit the sprite on the screen.
    """

    def __init__(self, demoNumber=0, coordinates=(0, 0)):
        """Init DemoRubberTrapSprite using the integer demoNumber and the tuple coordinates.

        Instance variables:
            animationFrames: A list of 11 Surface objects from the SpriteSheet object.
            animated: A boolean indicating whether or not the sprite is currently going through an animation.
            image: The current image to be drawn for the sprite.
        """
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(0, 520, 96, 120, 6)
        self.demoNumber = demoNumber
        self.animated = False
        self.image = self.animationFrames[0]

    def update(self):
        """Increase frameCount. Depending on frameCount, determine which methods to call if animated is True."""
        self.frameCount += 1
        self.rect = pg.Rect(self.coordinates[0] + 20, self.coordinates[1], 50, 120)
        if self.animated:
            if self.frameCount % 33 // 3 in (0, 4, 6, 8, 10):
                self.image = self.animationFrames[1]
            elif self.frameCount % 33 // 3 in (1, 3, 7):
                self.image = self.animationFrames[2]
            elif self.frameCount % 33 // 3 == 2:
                self.image = self.animationFrames[3]

            else:
                self.image = self.animationFrames[0]
            if 18 < self.frameCount < 30:
                self.image = pg.transform.flip(self.image, True, False)
            elif self.frameCount % 33 == 0:
                self.frameCount = 0
                self.animated = False
            if self.demoNumber == 0:
                self.image = pg.transform.flip(self.image, True, False)
        else:
            self.image = self.animationFrames[0]

        for sprite in c.demoGroup:
            if isinstance(sprite, DemoPlayerSprite) and self.rect.collidepoint(sprite.rect.center) and\
                            not self.animated:
                playSound("bounce_rubber_or_player.wav")
                self.frameCount = sprite.frameCount = 0
                self.animated = True
                sprite.animated = True

    def setMonochromeImage(self):
        """Set the sprite's image to its monochrome variant, depending on demoNumber."""
        self.image = self.animationFrames[4]
        if self.demoNumber == 1:
            self.image = self.animationFrames[5]
            self.image = pg.transform.flip(self.image, True, False)


class DemoWallSprite(DemoSprite):
    """Create an instance of a the level's boundary wall sprite for the demo.

    Attributes:
        demoNumber: An integer determining whether this sprite belongs to the first, second, third, or fourth
            demo animation.
        coordinates: A tuple location to blit the sprite on the screen.
    """

    def __init__(self, demoNumber=0, coordinates=(0, 0)):
        """Init DemoWallSprite using the integer demoNumber and the tuple coordinates.

        Instance variables:
            animationFrames: A list of 11 Surface objects from the SpriteSheet object.
            animated: A boolean indicating whether or not the sprite is currently going through an animation.
            image: The current image to be drawn for the sprite.
                The image to be drawn depends on demoNumber.
            rect: A rect object for the sprite.
        """
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(680, 0, 255, 564)
        self.demoNumber = demoNumber
        self.image = self.animationFrames[0]
        if demoNumber == 2:
            self.image = self.animationFrames[1]
        self.rect = self.image.get_rect()

    def update(self):
        """Increase frameCount and set the sprite's image.

        If the player collides with the sprite, frameCount is set to -100 to ensure that it doesn't collide with
        the sprite again before bouncing off.
        """
        self.frameCount += 1
        if self.demoNumber == 2:
            self.image = self.animationFrames[1]
            self.image = pg.transform.flip(self.image, True, False)

        for sprite in c.demoGroup:
            if isinstance(sprite, DemoPlayerSprite) and self.rect.colliderect(sprite.rect) and 0 < self.frameCount\
                    and not DemoPlayerSprite.paused:
                playSound("bounce_wall.wav")
                DemoPlayerSprite.paused = True
                self.frameCount = -100
                sprite.frameCount = 0
            elif isinstance(sprite, DemoUrchinSprite) and self.rect.collidepoint(sprite.rect.center) and\
                    sprite.animationCount == 2:
                playSound("crush_enemy.wav")
                sprite.animationCount = 3
                sprite.frameCount = 0


class DemoDisplay(pg.sprite.Sprite):
    """Create an instance of the display box surrounding the demo.

    Attributes:
        demoNumber: An integer determining whether this sprite belongs to the first, second, third, or fourth
            demo animation.
        coordinates: A tuple location to blit the sprite on the screen.
    """

    def __init__(self, demoNumber=0, coordinates=(0, 0)):
        """Init DemoSprite using the integer demoNumber and the tuple coordinates.

        Instance variables:
            spriteSheet: The SpriteSheet object for the demo display sprite sheet image.
            animationFrames: A list of 4 Surface objects from the SpriteSheet object.
            image: The image to be drawn for this display.
            rect: A rect object for the sprite.
        """
        super().__init__(c.demoGroup)
        self.spriteSheet = SpriteSheet("demo_display.png")
        self.animationFrames = []
        self.demoNumber = demoNumber
        self.coordinates = coordinates

        self.animationFrames.extend(self.spriteSheet.getStripImages(0, 0, 380, 260))
        self.animationFrames.extend(self.spriteSheet.getStripImages(0, 260, 380, 260))

        self.image = self.animationFrames[self.demoNumber]
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        """Not to be called directly, but inherited by subclasses."""
        pass

    def setCoordinates(self):
        """Set the display's rect to match its coordinates."""
        self.rect.topleft = self.coordinates

    def setMonochromeImage(self):
        """Not to be called directly, but inherited by subclasses."""
        pass


class DemoNameDisplay(DemoDisplay):
    """Create an instance of a the display box surrounding the player's name in the demo.

    Attributes:
        demoNumber: An integer determining whether this sprite belongs to the first, second, third, or fourth
            demo animation.
        coordinates: A tuple location to blit the sprite on the screen.
    """

    def __init__(self, demoNumber=0, coordinates=(0, 0)):
        """Init DemoSprite using the integer demoNumber and the tuple coordinates.

        Instance variables:
            image: The image to be drawn for this display.
            rect: A rect object for the sprite.
        """
        super().__init__(demoNumber, coordinates)
        self.image = self.spriteSheet.getSheetImage(0, 520, 365, 70)
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()


def initialize():
    """Reset the DemoPlayerSprite class' class variables to their base values."""
    DemoPlayerSprite.facingDirection = c.Directions.RIGHT
    DemoPlayerSprite.paused = False
    DemoPlayerSprite.swingValue = (0, 0)
