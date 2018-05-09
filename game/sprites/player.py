import math
import pygame as pg
import sys

from game.sprites.sprite_sheet import SpriteSheet
import game.tools.constants as c
from game.tools.asset_cache import playSound


class PlayerSprite(pg.sprite.Sprite):
    """Create a sprite of the player character.

    Attributes:
        playerNumber: An integer representing whether the object represent player 1, 2, 3, or 4.
            If playerNumber is greater than 4, getImage will end the program as the SpriteSheet class will be
            unable to find the image file (For example, "player5.png" does not exist.)
            This is used to set the sprite's coordinates during the animateLevelEnd method.
    Class variables:
        currentLevel: A Level class instance for the current level being played.
            Tracks the rect objects of the level's boundaries for collision detection, and is used in the
            GoldSprite and ItemClock classes as a shortcut for accessing attributes of the current level.
        movementSpeed: A float representation of how many pixels per frame the players travel while moving.
        rotationSpeed: A float representation of how many degrees per frame the players rotate while swinging.
    """

    currentLevel = None
    movementSpeed = 2.12
    rotationSpeed = 4.24

    def __init__(self, playerNumber=1):
        """Init PlayerSprite using the integer playerNumber.

        Instance variables:
            spriteSheet: The SpriteSheet object for the player sprite sheet image.
            lives: An integer representing the player's current remaining number of lives.
            baseCoordinates: A tuple location to blit the sprite upon starting a level or after losing a life.
                This should be updated whenever the player begins a new level, and at no other point.
            coordinates: A tuple location to blit the sprite on the screen.
            swingingArmCoordinates: A tuple location of the center point of the player's arm sprite when it grabs
                onto a post.
                This should be updated whenever the arm sprite grabs onto a new post, and at no other point.
            playerState: A PlayerStates Enum instance of the current state of the sprite.
                Used to determine which methods get called and when.
            facingDirection: A Directions Enum instance of the current direction the sprite is facing.
                Used to determine which direction the sprite moves and whether its image is flipped.
                Should only be one of the four cardinal directions. Setting this to CLOCKWISE or COUNTER will
                cause unexpected and undesired results.
            initialSwingDirection: A Directions Enum instance of which direction the sprite was facing
                immediately before entering the SWINGING PlayerStates Enum.
                Used to determine if a player should fall into a black hole sprite if they finish swinging while
                their rects overlap.
                Should only be one of the four cardinal directions. Setting this to CLOCKWISE or COUNTER will
                cause unexpected and undesired results.
            swingingDirection: A Directions Enum instance indicating if the sprite is swinging clockwise or
                counter-clockwise.
                Should only be one of the two rotation directions. Setting this to a cardinal direction will
                cause unexpected and undesired results.
            bouncingOffWall: A boolean indicating if the sprite is currently colliding with any of the level
                boundary's rect objects.
            bouncingOffPlayer: A boolean indicating if the sprite is currently colliding with any other Player
                sprites.
            isFrozen: A boolean indicating if the sprite is currently unable to move due to the methods of an
                ItemClock sprite.
            killedUrchinCount: An integer tracking how many Urchin sprites the player has killed in the current
                level.
            goldCollectedCount: An integer tracking how many Gold sprites the player has revealed in the current
                level.
            self.score: An integer tracking the player's total cumulative score.
            frameCount: An integer that increases whenever the update method is called.
                Used to control when other methods should be called.
            currentAngle: A float that tracks the current angle between the player sprite's center point and
                swingingArmCoordinates.
                Should only be updated or referenced while the player is swinging.
            imageDict: A dict associating keys with lists of Surface objects from the SpriteSheet object.
                As the player's image appears different when moving or squishing based on if they are moving
                horizontally or vertically, those keys take dicts of Surface objects instead of lists.
            emptyImage: A Surface object, showing a fully-transparent blank image.
                Used when the sprite should not be visibly drawn onscreen.
            image: The current image to be drawn for the sprite.
                Defaults to the emptyImage.
            rect: A rect object for the sprite.
            collisionRect: A smaller rect object used for checking collision between this sprite and others.
                This creates a better visual for collision than using the main rect object.
        """
        super().__init__(c.playerGroup)
        spriteSheet = SpriteSheet("player{}.png".format(playerNumber))
        self.playerNumber = playerNumber
        self.lives = 5
        self.baseCoordinates = (0, 0)
        self.coordinates = (0, 0)
        self.swingingArmCoordinates = (0, 0)
        self.playerState = c.PlayerStates.OFF_SCREEN
        self.facingDirection = c.Directions.RIGHT
        self.initialSwingDirection = c.Directions.RIGHT
        self.swingingDirection = c.Directions.CLOCKWISE
        self.bouncingOffWall = self.bouncingOffPlayer = self.isFrozen = False
        self.killedUrchinCount = self.goldCollectedCount = self.score = self.frameCount = 0
        self.currentAngle = 0.0

        self.imageDict = {"arm": [], "ball": [], "end": [], "death": [], "turn": [], "fall": [],  # #######
                          "move": {}, "squish": {}}
        armImageList = spriteSheet.getStripImages(152, 0, 16, 16, 2)
        armImageList.append(spriteSheet.getSheetImage(184, 0, 14, 14))
        self.imageDict["arm"] = armImageList
        self.imageDict["ball"] = spriteSheet.getStripImages(0, 0, 34, 34, 2)
        self.imageDict["end"] = spriteSheet.getStripImages(68, 0, 42, 32, 2)
        self.imageDict["death"] = spriteSheet.getStripImages(0, 34, 34, 34, 4)
        self.imageDict["turn"] = spriteSheet.getStripImages(136, 34, 34, 34)
        self.imageDict["fall"] = spriteSheet.getStripImages(0, 68, 34, 34, 4)
        self.imageDict["move"]["vertical"] = spriteSheet.getStripImages(0, 102, 32, 38, 4)
        self.imageDict["squish"]["vertical"] = spriteSheet.getStripImages(128, 102, 48, 38)
        self.imageDict["move"]["horizontal"] = spriteSheet.getStripImages(0, 140, 34, 34, 4)
        self.imageDict["squish"]["horizontal"] = spriteSheet.getStripImages(136, 140, 30, 52, 3)
        self.emptyImage = spriteSheet.getSheetImage(136, 68, 34, 34)

        self.image = self.emptyImage
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pg.rect.Rect((0, 0), (16, 16))

    def initialize(self, x, y):
        """Reset some of the sprite's attributes to its proper initial values.

        This should be called whenever the player begins a new level, and at no other point.
        Note that this only updates the attributes which should be reset upon starting a new level, and does not
        update attributes that should carry between levels such as lives and score.
        """
        self.baseCoordinates = (x, y)
        self.setCoordinates(x, y)
        self.facingDirection = c.Directions.RIGHT
        self.bouncingOffWall = self.bouncingOffPlayer = self.isFrozen = False
        self.killedUrchinCount = self.goldCollectedCount = 0
        if not self.playerState == c.PlayerStates.DEAD:
            self.putSpriteInBall()
        else:
            self.image = self.emptyImage

    def setCoordinates(self, x, y):
        """Set the sprite's coordinates to the passed arguments.

        This also adjusts the location of rect and collisionRect.

        Args:
            x: An integer x coordinate to draw the sprite.
            y: An integer y coordinate to draw the sprite.
        """
        self.coordinates = x, y
        self.rect.topleft = x, y
        self.collisionRect = pg.rect.Rect((x + 8, y + 8), (16, 16))

    def isFacingHorizontally(self):
        """Check if the player is currently facing one of the horizontal directions.

        Returns:
            A boolean representing whether the player is in fact facing right or left, or not.
        """
        return self.facingDirection in [c.Directions.RIGHT, c.Directions.LEFT]

    def getDirectionKey(self):
        """Get the imageKey string of the player's current orientation.

        Returns:
             A string representing if the player is currently facing a horizontal or a vertical direction.
        """
        if self.isFacingHorizontally():
            return "horizontal"
        else:
            return "vertical"

    def flipImage(self):
        """Flip the sprite's image horizontally if it is currently facing left, or vertically if it is currently
        facing up.

        If the player is currently swinging, this method is ignored if isTurningOrthogonally is False (i.e., if
        the player currently appears to be facing diagonally).
        """
        if self.playerState not in [c.PlayerStates.SWINGING, c.PlayerStates.HITTING_PLAYER_SWINGING] or\
                self.isTurningOrthogonally():
            if self.facingDirection == c.Directions.LEFT:
                self.image = pg.transform.flip(self.image, True, False)
            elif self.facingDirection == c.Directions.UP:
                self.image = pg.transform.flip(self.image, False, True)

    def flipDiagonalImage(self):
        """Flip the sprite's image as needed, based on where in its circular swinging movement the sprite is
        located, and whether or not it is swinging clockwise.

        currentAngleOctant stores which octant of the circle around swingingArmCoordinates the sprite's center
        point is currently located in, with 0 degrees being the rightmost edge of the circle.
        """
        currentAngleSixteenth = (self.currentAngle % 360) // 22.5
        if self.swingingDirection == c.Directions.CLOCKWISE:
            if currentAngleSixteenth in [1, 2, 13, 14]:
                self.image = pg.transform.flip(self.image, False, True)
            if currentAngleSixteenth in [1, 2, 5, 6]:
                self.image = pg.transform.flip(self.image, True, False)
        else:
            if currentAngleSixteenth in [5, 6, 9, 10]:
                self.image = pg.transform.flip(self.image, False, True)
            if currentAngleSixteenth in [9, 10, 13, 14]:
                self.image = pg.transform.flip(self.image, True, False)

    def changeImage(self, imageKey, imageIndex):
        """Change the current image of the sprite.

        If imageKey is "move" or "squish", since those are sub-dictionaries within imageDict instead of lists,
        this method must also call on getDirectionKey to determine if the player is moving horizontally or
        vertically.
        If either the imageKey does not exist in the imageDict, or else the imageIndex does not exist in the list
        that is the value of imageDict[imageKey], the program will end with an error message.

        Args:
            imageKey: A string representing from which key in the imageDict we wish to get the Surface object.
            imageIndex: An integer representing which index in the imageKey list is the Surface object we want.
        """
        try:
            if imageKey in ["move", "squish"]:
                self.image = self.imageDict[imageKey][self.getDirectionKey()][imageIndex]
            else:
                self.image = self.imageDict[imageKey][imageIndex]
        except KeyError:
            print("ERROR: The PlayerSprite class does not have a key of '{}' in its imageDict.".format(imageKey))
            pg.quit()
            sys.exit()
        except IndexError:
            print("ERROR: The PlayerSprite class does not have an image at position {} in its imageDict, under the "
                  "key '{}'.".format(imageIndex, imageKey))
            pg.quit()
            sys.exit()

    def update(self):
        """Increase frameCount. Depending on frameCount and playerState, determines which methods to call.

        The sprite always checks collision with other objects each frame that it updates.
        The priority of these collision checks are:
          1. Objects that kill the player.
          2. Collision rects for the level boundaries, if the player is not colliding with an object that kills it.
          3. Other player sprites, if the player is not colliding with any of the above objects.
        """
        self.checkEnemyCollision()
        self.checkBlackHoleCollision()
        self.checkWallCollision()
        self.checkOtherPlayerCollision()
        self.frameCount += 1

        if self.playerState == c.PlayerStates.BALL:
            # If the player is in a ball state, it flashes every 8 frames (unless it is frozen).

            if self.frameCount % 16 < 8 and not self.isFrozen:
                self.changeImage("ball", 0)
            else:
                self.changeImage("ball", 1)
        elif self.playerState == c.PlayerStates.MOVING:
            self.moveSprite()
            self.animateMovement()
        elif self.playerState == c.PlayerStates.FINISHED_SWINGING:
            # If the player has finished swinging within the past 16 frames without being frozen, and is not facing the
            # same direction as when they began moving, they are put in the FINISHED_SWINGING state.
            # This is identical to the MOVING state, except that they ignore collision with black hole sprites while in
            # this state.

            self.moveSprite()
            self.animateMovement()
            if self.frameCount % 10 == 0 and not self.isFrozen:
                self.frameCount = 0
                self.playerState = c.PlayerStates.MOVING
        elif self.playerState == c.PlayerStates.SWINGING:
            self.swing()
        elif self.playerState == c.PlayerStates.HITTING_PLAYER_MOVING or\
                self.playerState == c.PlayerStates.HITTING_PLAYER_SWINGING:
            self.bounceOffOfPlayer()
        elif self.playerState == c.PlayerStates.HITTING_WALL:
            # The player sprite spends 9 frames animating being squished against the wall.
            # It rebounds afterwards, changing direction and then begins to move.
            # After 9 frames, if it not frozen, it checks if it is no longer colliding with any of the level boundary's
            # rects. If not, it enters the MOVING state again.

            if self.frameCount == 4:
                self.changeImage("squish", 1)
            elif 4 < self.frameCount < 9:
                self.changeImage("squish", 2)
            elif self.frameCount == 9:
                self.rebound()
            elif self.frameCount > 9:
                self.moveSprite()
                self.animateMovement()
                if not self.isFrozen and not any(self.rect.colliderect(levelRect) for levelRect in
                                                 PlayerSprite.currentLevel.levelBorderRects):
                    self.frameCount = 0
                    self.playerState = c.PlayerStates.MOVING
                    self.bouncingOffWall = False
        elif self.playerState in [c.PlayerStates.FALLING, c.PlayerStates.EXPLODING]:
            # The sprite's image changes every 8 frames.
            # It uses the "death" imageKey if the player is in the EXPLODING state, and the "fall" imageKey if the
            # player is in the FALLING state.
            # After 40 total frames, the player enters the OFF_SCREEN state and their image is replaced with the
            # emptyImage.

            imageKey = "death"
            if self.playerState == c.PlayerStates.FALLING:
                imageKey = "fall"
            if 7 < self.frameCount % 40 < 33:
                self.changeImage(imageKey, (self.frameCount - 7) // 8)
            if self.frameCount % 40 == 0:
                self.frameCount = 0
                self.playerState = c.PlayerStates.OFF_SCREEN
                self.image = self.emptyImage
        elif self.playerState == c.PlayerStates.OFF_SCREEN:
            # After 160 frames of being off-screen, the player is respawned at its baseCoordinates location, at the
            # cost of one life.
            # If the player has no lives left, they permanently enter the DEAD state.
            # A sprite in the DEAD state never meaningfully updates, except during the end-of-level animations.

            if self.lives > 0 and self.frameCount % 160 == 0:
                self.setCoordinates(self.baseCoordinates[0], self.baseCoordinates[1])
                self.putSpriteInBall()
                self.frameCount = 0
            elif self.lives == 0:
                self.playerState = c.PlayerStates.DEAD
        elif self.playerState == c.PlayerStates.LEVEL_END:
            self.animateLevelEnd()

        if self.bouncingOffPlayer:
            # Every time the sprite updates, if it is currently bouncing off of another player, it checks whether or
            # not these sprites are still colliding. If not, it sets the bouncingOffPlayer boolean to False.
            # Below, it also does runs the same check if it is currently bouncing off of any of the level boundary's
            # rects.

            # otherPlayers is all other player sprites that are in one of the three moving states.
            # Players in any other states are ignored, as either not considered to be 'active' (Such as BALL, FALLING,
            # or DEAD) or else are already in the process of bouncing off of an object (Such as HITTING_WALL).

            otherPlayers = [player for player in c.playerGroup if (player != self and
                            player.playerState in [c.PlayerStates.MOVING, c.PlayerStates.SWINGING,
                                                   c.PlayerStates.FINISHED_SWINGING])]
            if not any(player.collisionRect.colliderect(self.collisionRect) for player in otherPlayers):
                self.bouncingOffPlayer = False
        if self.bouncingOffWall:
            if not any(self.rect.colliderect(levelRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects):
                self.bouncingOffWall = False

        if self.frameCount % 240 == 0:
            # All methods that rely on frameCount do so in factors of 240. To keep frameCount from increasing without
            # bounds, it resets to 0 every 240 frames.

            self.frameCount = 0
        self.flipImage()
        self.image.set_colorkey(c.BLACK)

    def putSpriteInBall(self):
        """Set the sprite's facingDirection, playerState, and image to their default for the player's BALL state.

        Even though this method should never be called if the lives is not positive, this includes a sanity check
        by setting lives to 0 at a minimum.
        """
        self.facingDirection = c.Directions.RIGHT
        self.playerState = c.PlayerStates.BALL
        self.changeImage("ball", 0)
        if self.isFrozen:
            self.changeImage("ball", 1)
        self.lives = max(0, self.lives - 1)
        self.frameCount = 0

    def startMoving(self, direction):
        """Set the sprite's facingDirection and image, and puts them in the MOVING state.

        If the sprite is not currently in the BALL state, this method is ignored.

        Args:
             direction: A string representation of which direction key the player has begun moving.
                Note that if direction is not in "up", "down", "left", or "right", this will cause the program to
                end with an error message.
        """
        if self.playerState == c.PlayerStates.BALL:
            playSound("move_out_of_ball.wav")
            try:
                self.facingDirection = c.directionsDict[direction]
            except KeyError:
                print("ERROR: '{}' is not a valid cardinal direction.".format(direction))
                pg.quit()
                sys.exit()
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - 1)
            self.changeImage("move", 0)
            if self.isFrozen:
                self.changeImage("move", 2)
            self.playerState = c.PlayerStates.MOVING
            self.frameCount = 0

    def moveSprite(self):
        """Move the sprite's coordinates according to movementSpeed, in the direction they are facing.

        If the sprite passes over a gold sprite, it causes that sprite to run its startFlipAnimation method.
        If that gold sprite has not yet been revealed, it adds one to the player's goldCollectedCount.

        If the sprite crosses over the left or right edge of the screen, they reappear at the opposite edge.
        Crossing over the upper or lower edge of the screen should not be possible. If it were to happen, the
        player's coordinates would be reset once the timer reaches 0 and they lose a life, preventing the game
        from locking up.
        """
        if not self.isFrozen:
            if self.facingDirection == c.Directions.UP:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - PlayerSprite.movementSpeed)
            elif self.facingDirection == c.Directions.DOWN:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + PlayerSprite.movementSpeed)
            elif self.facingDirection == c.Directions.LEFT:
                self.setCoordinates(self.coordinates[0] - PlayerSprite.movementSpeed, self.coordinates[1])
                if self.rect.right < 0:
                    self.setCoordinates(512, self.coordinates[1])
            elif self.facingDirection == c.Directions.RIGHT:
                self.setCoordinates(self.coordinates[0] + PlayerSprite.movementSpeed, self.coordinates[1])
                if self.rect.left > 512:
                    self.setCoordinates(-48, self.coordinates[1])
            for gold in c.goldGroup:
                # This does not call the startFlipAnimation method if the gold sprite is currently flipping up or down.

                if gold.collisionRect.collidepoint(self.rect.center) and gold.goldState in\
                        [c.OtherStates.OFF_SCREEN, c.OtherStates.REVEALED, c.OtherStates.UPSIDE_DOWN]:
                    gold.passingDirection = self.facingDirection
                    if not gold.alreadyRevealed:
                        self.goldCollectedCount += 1
                    gold.startFlipAnimation()

    def animateMovement(self):
        """Change the sprite's image every 4 frames to create the illusion of animation."""
        if self.frameCount % 8 < 4:
            self.changeImage("move", 1)
            if self.isFrozen:
                self.changeImage("move", 3)
        else:
            self.changeImage("move", 0)
            if self.isFrozen:
                self.changeImage("move", 2)

    def hitWall(self):
        """Change the sprite's image to appear squished, and sets their state to HITTING_WALL."""
        self.frameCount = 0
        playSound("bounce_wall.wav")
        self.playerState = c.PlayerStates.HITTING_WALL
        self.image = self.imageDict["squish"][self.getDirectionKey()][0]

    def rebound(self):
        """Reverse the sprite's direction and change its image to appear to be moving."""
        self.reverseDirection()
        self.image = self.imageDict["move"][self.getDirectionKey()][0]
        if self.isFrozen:
            self.image = self.imageDict["move"][self.getDirectionKey()][2]

    def bounceOffOfPlayer(self):
        """Change the sprite's image, coordinates, and swinging angle as it bounces off of another player.

        As bouncing off of a wall takes priority over bouncing off of a player, it first runs a check to see if
        the sprite is also bouncing off of a wall. If so, it sets the sprite's state to HITTING_WALL, and the
        rest of the method is ignored.
        Otherwise, the sprite remains in position for 12 frames, changing its image every 6 frames to create the
        illusion of animation.
        At the twelfth frame, the sprite either reverses its cardinal direction or reverses its rotation
        direction depending on whether it is moving or swinging.
        Every 16 frames, if the sprite is not frozen, it restores the sprite to either the MOVING or SWINGING
        state that it was in before colliding with another player.
        """
        imageKey = "move"
        if self.playerState == c.PlayerStates.HITTING_PLAYER_SWINGING and not self.isTurningOrthogonally():
            imageKey = "turn"
        if any(self.rect.colliderect(levelRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects):
            self.frameCount = 0
            self.playerState = c.PlayerStates.HITTING_WALL
            self.bouncingOffWall = True
        else:
            if self.frameCount == 12:
                if self.playerState == c.PlayerStates.HITTING_PLAYER_MOVING:
                    self.rebound()
                elif self.swingingDirection == c.Directions.CLOCKWISE:
                    self.swingingDirection = c.Directions.COUNTER
                else:
                    self.swingingDirection = c.Directions.CLOCKWISE
            elif self.frameCount % 16 < 6:
                self.changeImage(imageKey, 2)
            elif self.frameCount % 16 < 12:
                self.changeImage(imageKey, 3)
            else:
                if self.playerState == c.PlayerStates.HITTING_PLAYER_MOVING:
                    self.moveSprite()
                    self.animateMovement()
                else:
                    self.swing()
            if self.frameCount % 16 == 0 and not self.isFrozen:
                if self.playerState == c.PlayerStates.HITTING_PLAYER_MOVING:
                    self.moveSprite()
                    self.animateMovement()
                    self.playerState = c.PlayerStates.MOVING
                else:
                    self.swing()
                    self.playerState = c.PlayerStates.SWINGING
                self.frameCount = 0
                self.bouncingOffPlayer = False

    def reverseDirection(self):
        """Set the sprite's facingDirection to the opposite of its current facingDirection."""
        if self.facingDirection == c.Directions.UP:
            self.facingDirection = c.Directions.DOWN
        elif self.facingDirection == c.Directions.DOWN:
            self.facingDirection = c.Directions.UP
        elif self.facingDirection == c.Directions.LEFT:
            self.facingDirection = c.Directions.RIGHT
        else:
            self.facingDirection = c.Directions.LEFT

    def changeSwingingDirection(self):
        """Set the sprite's facingDirection based on its currentAngle.

        If the sprite is swinging counter-clockwise, the direction they should be facing is reversed.
        """
        if 29 < self.currentAngle < 120:
            self.facingDirection = c.Directions.LEFT
        elif 119 < self.currentAngle < 210:
            self.facingDirection = c.Directions.UP
        elif 209 < self.currentAngle < 300:
            self.facingDirection = c.Directions.RIGHT
        else:
            self.facingDirection = c.Directions.DOWN
        if self.swingingDirection == c.Directions.COUNTER:
            self.reverseDirection()

    def isTurningOrthogonally(self):
        """Check if the player's current coordinates put it in the orthogonal segments of the circle around
        swingingArmCoordinates.

        Returns:
            A boolean representing if the sprite's center point is in any of the eight sixteenths of the circle
            around swingingArmCoordinates that would cause it to move orthogonally.
        """
        currentAngleSixteenth = (self.currentAngle % 360) // 22.5
        return currentAngleSixteenth in [0, 3, 4, 7, 8, 11, 12, 15]

    def rotateImageAroundPoint(self):
        """Rotate the sprite around its swingingArmCoordinates.

        The sprite's rect's new center point is first calculated based on its current angle and on its
        swingingArmCoordinates, with a constant radius of 23.
        That rect is then used to set the coordinates of the sprite and its collisionRect.
        """
        radius = 23
        radianAngle = math.radians(self.currentAngle)
        horizontalValue = self.swingingArmCoordinates[0] + radius * math.cos(radianAngle)
        verticalValue = self.swingingArmCoordinates[1] + radius * math.sin(radianAngle)
        self.rect.center = horizontalValue, verticalValue
        self.setCoordinates(self.rect.topleft[0], self.rect.topleft[1])

    def swing(self):
        """Change the sprite's image and coordinates based on its rotationSpeed and currentAngle.

        If the sprite is frozen, its image changes to give the illusion of animation, but its coordinates do not
        change.
        Otherwise, every time this function is called, the sprite's currentAngle is incremented by its
        rotationSpeed (or decremented if the sprite is swinging counter-clockwise).
        Then its new coordinates are calculated, followed by its facingDirection, a check if it is colliding with
        any gold sprites, and finally a change in its image to give the illusion of animation.
        """
        if not self.isFrozen:
            if self.swingingDirection == c.Directions.CLOCKWISE:
                self.currentAngle += PlayerSprite.rotationSpeed
            else:
                self.currentAngle -= PlayerSprite.rotationSpeed
            self.currentAngle %= 360
            self.rotateImageAroundPoint()
            self.changeSwingingDirection()
            for gold in c.goldGroup:
                if gold.collisionRect.collidepoint(self.rect.center) and gold.goldState in [c.OtherStates.OFF_SCREEN,
                                                                                            c.OtherStates.REVEALED,
                                                                                            c.OtherStates.UPSIDE_DOWN]:
                    gold.passingDirection = self.facingDirection
                    if not gold.alreadyRevealed:
                        self.goldCollectedCount += 1
                    gold.startFlipAnimation()
        if self.isTurningOrthogonally():
            self.animateMovement()
        elif self.frameCount % 8 < 4:
            self.image = self.imageDict["turn"][0]
            self.flipDiagonalImage()
        else:
            self.image = self.imageDict["turn"][1]
            self.flipDiagonalImage()

    def checkEnemyCollision(self):
        """Check if the sprite is currently colliding with an enemy sprite, and run the appropriate method if so.

        If the player is in any 'inactive' states (Such as BALL, FALLING, or OFF_SCREEN), this method is ignored.
        Otherwise, if the player collides with a blue (i.e., active) enemy sprite, they enter the EXPLODING
        state.
        If they collide with a yellow enemy sprite, the enemy sprite is pushed.
        """
        if self.playerState in [c.PlayerStates.MOVING, c.PlayerStates.SWINGING, c.PlayerStates.FINISHED_SWINGING,
                                c.PlayerStates.HITTING_WALL, c.PlayerStates.HITTING_PLAYER_MOVING,
                                c.PlayerStates.HITTING_PLAYER_SWINGING]:
            if any(enemy.collisionRect.colliderect(self.collisionRect) and enemy.enemyState == c.EnemyStates.MOVING
                   and enemy.color == c.BLUE for enemy in c.enemyGroup):
                playSound("death.wav")
                self.frameCount = 0
                self.facingDirection = c.Directions.RIGHT
                self.playerState = c.PlayerStates.EXPLODING
                self.image = self.imageDict["death"][0]
            else:
                pushedEnemies = [enemy for enemy in c.enemyGroup if enemy.collisionRect.colliderect(self.rect)
                                 and enemy.color == c.YELLOW]
                for enemy in pushedEnemies:
                    enemy.push(self)

    def checkBlackHoleCollision(self):
        """Check if the sprite is currently moving and its center point overlaps with a black hole sprite.

        If they are colliding, the player's coordinates are set to the black hole sprite's coordinates, for
        improved animation. The player is then put into the FALLING state.
        This method is ignored unless the player is in the MOVING state.
        """
        if self.playerState == c.PlayerStates.MOVING:
            for hole in c.blackHoleGroup:
                if hole.rect.collidepoint(self.rect.center):
                    self.coordinates = hole.coordinates
                    self.rect.topleft = hole.coordinates
                    playSound("death.wav")
                    self.frameCount = 0
                    self.facingDirection = c.Directions.RIGHT
                    self.playerState = c.PlayerStates.FALLING
                    self.image = self.imageDict["fall"][0]

    def checkWallCollision(self):
        """Check if the sprite is colliding with any of the level boundary's rects.

        If the player is in any 'inactive' states (Such as BALL, FALLING, or OFF_SCREEN) or is already in the
        HITTING_WALL state, this method is ignored.
        Otherwise, if the player collides with any of the level boundary's rects, they bounce off and
        bouncingOffWall is set to True.
        """
        if self.playerState in [c.PlayerStates.MOVING, c.PlayerStates.FINISHED_SWINGING,
                                c.PlayerStates.HITTING_PLAYER_MOVING, c.PlayerStates.HITTING_PLAYER_SWINGING] and not\
                self.bouncingOffWall:
            if any(self.rect.colliderect(levelRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects):
                self.hitWall()
                self.bouncingOffWall = True

    def checkOtherPlayerCollision(self):
        """Check if the sprite is colliding with any of the other player sprites.

        If they are colliding, the sprite's image is changed to the appropriate colliding image, and the sprite's
        state is set to either HITTING_PLAYER_MOVING or HITTING_PLAYER_SWINGING.
        This method is ignored unless the player is currently in a moving or swinging state, and is not already
        colliding with another wall or player.
        """
        if self.playerState in [c.PlayerStates.MOVING, c.PlayerStates.SWINGING, c.PlayerStates.FINISHED_SWINGING]\
                and not self.bouncingOffWall and not self.bouncingOffPlayer:
            otherPlayers = [player for player in c.playerGroup if (player != self and
                            player.playerState in [c.PlayerStates.MOVING, c.PlayerStates.SWINGING,
                                                   c.PlayerStates.FINISHED_SWINGING, c.PlayerStates.HITTING_WALL])]
            for player in otherPlayers:
                if player.collisionRect.colliderect(self.collisionRect):
                    playSound("bounce_rubber_or_player.wav")
                    self.frameCount = 0
                    self.bouncingOffPlayer = True
                    player.checkOtherPlayerCollision()
                    if self.playerState in [c.PlayerStates.MOVING, c.PlayerStates.FINISHED_SWINGING]:
                        self.playerState = c.PlayerStates.HITTING_PLAYER_MOVING
                        self.image = self.imageDict["move"][self.getDirectionKey()][2]
                    else:
                        self.playerState = c.PlayerStates.HITTING_PLAYER_SWINGING
                        if self.isTurningOrthogonally():
                            self.image = self.imageDict["move"][self.getDirectionKey()][2]
                        elif self.frameCount % 8 < 4:
                            self.image = self.imageDict["turn"][2]
                            self.flipDiagonalImage()
                        else:
                            self.image = self.imageDict["turn"][3]
                            self.flipDiagonalImage()
                    player.checkOtherPlayerCollision()

    def adjustPosition(self):
        """Set the sprite's coordinates to be centered along the current row/column it is moving through."""
        if self.isFacingHorizontally():
            if 0 < self.coordinates[1] % 48 < 24:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - (self.coordinates[1] % 48))
            elif self.coordinates[1] % 48 > 23:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + (48 - self.coordinates[1] % 48))
        else:
            if 0 < self.coordinates[0] % 48 < 24:
                self.setCoordinates(self.coordinates[0] - (self.coordinates[0] % 48), self.coordinates[1])
            elif self.coordinates[0] % 48 > 23:
                self.setCoordinates(self.coordinates[0] + (48 - self.coordinates[0] % 48), self.coordinates[1])

    def animateLevelEnd(self):
        """Change the sprite's image to the end-of-level image, and flip it every 16 frames."""
        self.facingDirection = c.Directions.LEFT
        self.image = self.imageDict["end"][0]
        if (self.frameCount - 1) % 32 > 15:
            self.flipImage()
        if self.frameCount % 16 == 1 and self.playerNumber == 1:
            # Only player one makes noise during the level end, to prevent overlapping sound effects

            playSound("grab_post_move_end.wav")

    def setLevelEndCountImage(self):
        """Set the sprite's image to look towards the score box as the score counts up."""
        self.image = self.imageDict["end"][1]
