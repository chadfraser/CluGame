import pygame as pg
import random
import sys

from game.sprites.player import PlayerSprite
from game.sprites.sprite_sheet import SpriteSheet
import game.tools.constants as c
from game.tools.asset_cache import playSound


class UrchinSprite(pg.sprite.Sprite):
    """Create a sprite of the urchin enemy.

    Class variables:
        isFrozen: A boolean indicating if the sprite is currently unable to move due to the methods of an
            ItemClock sprite.
    """

    isFrozen = False

    def __init__(self):
        """Init UrchinSprite.

        Instance variables:
            spriteSheet: The SpriteSheet object for the urchin sprite sheet image.
            coordinates: A tuple location to blit the sprite on the screen.
            enemyState: An EnemyStates Enum instance of the current state of the sprite.
                Used to determine which methods get called and when.
            color: A tuple representing the urchin's current color.
                Blue urchins are active, whereas yellow urchins are stunned.
            facingDirection: A Directions Enum instance of the current direction the sprite is facing.
                Used to determine which direction the sprite moves and whether its image is flipped.
                Should only be one of the four cardinal directions. Setting this to CLOCKWISE or COUNTER will
                cause unexpected and undesired results.
            bouncingOff: A boolean indicating if the sprite is currently colliding with any objects that would
                prevent it from moving forwards.
            running: A boolean indicating if the sprite is currently moving at double speed.
            frameCount: An integer that increases whenever the update method is called.
            animationCount: An integer that increases whenever the sprite changes its animation image under
                specific circumstances.
                This is tracked for the purposes of controlling when to change the enemyState.
            delayCount: An integer representing how long the sprite must wait at an intersection before it can
                move.
            imageDict: A dict associating the keys BLUE and YELLOW with sub-dictionaries. These sub-dictionaries
                associate keywords with lists of Surface objects from the SpriteSheet object.
            emptyImage: A Surface object, showing a fully-transparent blank image.
                Used when the sprite should not be visibly drawn onscreen.
            image: The current image to be drawn for the sprite.
                Defaults to the emptyImage.
            rect: A rect object for the sprite.
            collisionRect: A smaller rect object used for checking collision between this sprite and others.
                This creates a better visual for collision than using the main rect object.
        """
        super().__init__(c.enemyGroup)
        spriteSheet = SpriteSheet("urchin.png")
        self.coordinates = (0, 0)
        self.enemyState = c.EnemyStates.SMALL_BALL
        self.color = c.BLUE
        self.facingDirection = c.Directions.RIGHT
        self.bouncingOff = self.running = False
        self.frameCount = self.animationCount = self.delayCount = 0

        self.imageDict = {c.BLUE: {}, c.YELLOW: {}}
        self.imageDictKeys = ["horizontal", "vertical", "ball"]

        # xValue is used to prevent repetition, as we need to call getStripImages three times in total with very
        # similar arguments, differing only by xValue each time, and only by 34 each time.
        # In this case, we want (0, 0, 34, 34); (0, 34, 34, 34); (0, 68, 34, 34)

        xValue = 0
        for key in self.imageDictKeys:
            stripImages = spriteSheet.getStripImages(0, xValue, 34, 34)
            self.imageDict[c.BLUE][key] = [stripImages[0], stripImages[1]]
            self.imageDict[c.YELLOW][key] = [stripImages[2], stripImages[3]]
            xValue += 34
        self.imageDict[c.BLUE]["death"] = self.imageDict[c.YELLOW]["death"]\
            = spriteSheet.getStripImages(0, 102, 34, 34)
        self.emptyImage = spriteSheet.getSheetImage(0, 136, 34, 34)

        self.image = self.emptyImage
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pg.rect.Rect((0, 0), (18, 18))

    def setCoordinates(self, x, y):
        """Set the sprite's coordinates to the passed arguments.

        This also adjusts the location of rect and collisionRect.

        Args:
            x: An integer x coordinate to draw the sprite.
            y: An integer y coordinate to draw the sprite.
        """
        self.coordinates = x, y
        self.rect.topleft = x, y
        self.collisionRect = pg.rect.Rect((x + 8, y + 8), (18, 18))

    def isFacingHorizontally(self):
        """Check if the sprite is currently facing one of the horizontal directions.

        Returns:
            A boolean representing whether the player is in fact facing right or left, or not.
        """
        return self.facingDirection in [c.Directions.RIGHT, c.Directions.LEFT]

    def flipImage(self):
        """Flip the sprite's image horizontally if it is currently facing left, or vertically if it is currently
        facing up.
        """
        if self.facingDirection == c.Directions.LEFT:
            self.image = pg.transform.flip(self.image, True, False)
        elif self.facingDirection == c.Directions.UP:
            self.image = pg.transform.flip(self.image, False, True)

    def changeImage(self, imageKey, imageIndex):
        """Change the current image of the sprite.

        Note that "move" is not actually a key in imageDict. Instead, if imageKey is "move", we use "horizontal"
        or "vertical" as our imageKey. This is to cut down on repetition, so we can just check
        isFacingHorizontally here in this function instead of every time we call changeImage.
        If either the imageKey does not exist in the imageDict, or else the imageIndex does not exist in the list
        that is the value of imageDict[imageKey], the program will end with an error message.

        Args:
            imageKey: A string representing from which key in the imageDict we wish to get the Surface object.
            imageIndex: An integer representing which index in the imageKey list is the Surface object we want.
        """
        if imageKey == "move":
            if self.isFacingHorizontally():
                imageKey = "horizontal"
            else:
                imageKey = "vertical"
        try:
            self.image = self.imageDict[self.color][imageKey][imageIndex]
        except KeyError:
            print("ERROR: The UrchinSprite class does not have a key of '{}' in its imageDict.".format(imageKey))
            pg.quit()
            sys.exit()
        except IndexError:
            print("ERROR: The UrchinSprite class does not have an image at position {} in its imageDict, under the "
                  "key '{}'.".format(imageIndex, imageKey))
            pg.quit()
            sys.exit()

    def update(self):
        """Increase frameCount. Depending on frameCount and playerState, determines which methods to call."""
        self.frameCount += 1
        # The sprite always checks collision with other objects each frame that it updates.
        # The priority of these collision checks are:
        #   1. Sonic wave sprites.
        #   2. Other urchin sprites, if the urchin's color is BLUE (i.e., active).

        self.checkSonicWaveCollision()
        self.checkOtherUrchinCollision()

        if self.enemyState == c.EnemyStates.SMALL_BALL:
            # If the urchin is in a small ball state and BLUE, it changes to a regular ball state after 5 frames.
            # After doing this 8 times total, it changes to a moving state.
            # If the urchin is YELLOW, it spends 32 frames fully in this state, then changes to a regular ball state
            # after 5 frames.
            # After changing states on this 84 times total, it changes its color to BLUE.

            if self.color == c.BLUE and self.frameCount % 5 == 0:
                if self.animationCount < 8:
                    self.changeImage("ball", 0)
                    self.enemyState = c.EnemyStates.BALL
                    self.frameCount = 0
                    self.animationCount += 1
                else:
                    self.changeImage("move", 0)
                    self.enemyState = c.EnemyStates.MOVING
                    self.frameCount = self.animationCount = 0
            elif self.color == c.YELLOW:
                if self.animationCount == 84:
                    self.color = c.BLUE
                    self.changeImage("ball", 0)
                    self.enemyState = c.EnemyStates.BALL
                    self.animationCount = 0
                    self.frameCount = 0
                elif (self.frameCount > 32 or 0 < self.animationCount) and self.frameCount % 5 == 0:
                    self.changeImage("ball", 0)
                    self.enemyState = c.EnemyStates.BALL
                    self.frameCount = 0
                    self.animationCount += 1
        elif self.enemyState == c.EnemyStates.BALL:
            # The urchin's BALL state is almost identical to SMALL_BALL, except it spends less time in this state.
            # It spends only 3 frames in this state, as opposed to the 5 frames spent in the small ball state.

            if self.color == c.BLUE and self.frameCount % 3 == 0:
                self.changeImage("ball", 1)
                self.enemyState = c.EnemyStates.SMALL_BALL
                self.frameCount = 0
            elif self.color == c.YELLOW:
                if self.animationCount == 84:
                    self.color = c.BLUE
                    self.changeImage("ball", 1)
                    self.enemyState = c.EnemyStates.SMALL_BALL
                    self.animationCount = 0
                    self.frameCount = 0
                elif (self.frameCount > 32 or self.animationCount > 0) and self.frameCount % 3 == 0:
                    self.changeImage("ball", 1)
                    self.enemyState = c.EnemyStates.SMALL_BALL
                    self.frameCount = 0
                    self.animationCount += 1
        elif self.enemyState == c.EnemyStates.MOVING:
            # If the sprite's color is BLUE, first it's checked if the sprite is at an intersection.
            # If so, running is set to False and the sprite randomly chooses its next action.
            # The sprite only moves every second frame. It does not move if the class is currently frozen by an
            # ItemClock sprite.
            # If the sprite is YELLOW, it spends 32 frames in this state before changing to the ball state.
            # Animation count is set to 1 to account for the 32 frames the sprite has already waited.

            if self.color == c.BLUE:
                if self.rect.center[0] % 48 == 16 and self.rect.center[1] % 48 == 18:
                    self.running = False
                    self.getRandomMoveAction()
                self.animateMovement()
                if self.frameCount % 2 == 0 and not UrchinSprite.isFrozen:
                    self.moveSprite()
                if self.frameCount % 480 == 0:
                    # All methods that rely on frameCount do so in factors of 480. To keep frameCount from increasing
                    # without bounds, it resets to 0 every 480 frames.

                    self.frameCount = 0
            elif self.frameCount > 32:
                self.changeImage("ball", 0)
                self.enemyState = c.EnemyStates.BALL
                self.animationCount = 1
        elif self.enemyState == c.EnemyStates.WAITING:
            self.animateMovement()
            if not UrchinSprite.isFrozen:
                self.moveSprite()
        elif self.enemyState == c.EnemyStates.EXPLODING:
            # The sprite's image changes every 5 frames.
            # It uses the "ball" imageKey for the first 10 frames to create the illusion of the sprite getting smaller,
            # then uses the "death" imageKey.
            # On the 25th frame, the sprite's image is replaced with the emptyImage. Then on the 30th frame, it is
            # replaced with the fourth image in the "death" imageKey list, and its state is changed to OFF_SCREEN.

            if self.frameCount % 30 > 24:
                self.image = self.emptyImage
            else:
                if 0 < self.frameCount % 30 < 10:
                    key = "ball"
                    index = (self.frameCount % 30) // 5
                else:
                    key = "death"
                    if self.frameCount % 30 == 0:
                        self.enemyState = c.EnemyStates.OFF_SCREEN
                        self.offsetPointsSpriteCoordinates(self.facingDirection)
                        self.facingDirection = c.Directions.RIGHT
                        index = 3
                        self.frameCount = 0
                    else:
                        index = (self.frameCount % 30 - 10) // 5
                self.changeImage(key, index)
        elif self.enemyState == c.EnemyStates.OFF_SCREEN:
            if self.frameCount % 32 == 0:
                self.kill()
        self.flipImage()
        self.image.set_colorkey(c.BLACK)

    def getRandomMoveAction(self):
        """Randomly select if the sprite will move normally, run, wait, or change its direction.

        If the enemy chooses to wait, there's a 50% chance it will wait for 20 frames, and a 17% chance that it
        will wait for 40, 60, or 80 frames each.
        The sprite will not change its direction while it is frozen."""
        randomValue = random.randint(0, 40)
        if randomValue < 2:
            self.frameCount = 0
            self.delayCount = random.randint(0, 5)
            self.enemyState = c.EnemyStates.WAITING
        elif randomValue < 10 and not UrchinSprite.isFrozen:
            self.setRandomDirection()
        elif randomValue > 38:
            self.running = True

    def moveSprite(self, moveVal=2):
        """Move the sprite's coordinates according to moveVal, in the direction they are facing.

        If the sprite is running, its speed is doubled

        If the sprite crosses over the left or right edge of the screen, they reappear at the opposite edge.
        Crossing over the upper or lower edge of the screen should not be possible. If it were to happen, another
        enemy would not spawn in the urchin's place, but the game would be able to continue.
        If the enemy is in the waiting state, it won't move and will instead wait for 20, 40, 60, or 80 frames
        before moving again, depending on how low delayCount is.
        The sprite will only move every other frame, unless it is not in the moving state (i.e., it is being
        pushed by a player).
        If the sprite's color is BLUE, it will check if it is colliding with a level boundary's rect, a revealed
        gold sprite, a revealed rubber trap sprite, or another urchin. If so, it reverses its direction.

        Args:
            moveVal: An integer showing how many pixels the sprite should move every other frame.
        """
        if moveVal == 2 and self.running:
            moveVal *= 2
        if self.enemyState == c.EnemyStates.WAITING:
            if self.frameCount % 20 == 0:
                if self.delayCount < 3:
                    self.delayCount += 1
                else:
                    self.setRandomDirection()
                    self.enemyState = c.EnemyStates.MOVING
        elif not self.enemyState == c.EnemyStates.MOVING or self.frameCount % 2 == 0:
            if self.facingDirection == c.Directions.UP:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - moveVal)
            elif self.facingDirection == c.Directions.DOWN:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + moveVal)
            elif self.facingDirection == c.Directions.LEFT:
                self.setCoordinates(self.coordinates[0] - moveVal, self.coordinates[1])
                if self.rect.right < 0:
                    self.setCoordinates(512, self.coordinates[1])
            elif self.facingDirection == c.Directions.RIGHT:
                self.setCoordinates(self.coordinates[0] + moveVal, self.coordinates[1])
                if self.rect.left > 512:
                    self.setCoordinates(-48, self.coordinates[1])
            if self.color == c.BLUE:
                if any(self.rect.colliderect(levelRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects) \
                        or any(self.collisionRect.colliderect(gold.collisionRect) for gold in c.goldGroup if
                               gold.goldState != c.OtherStates.OFF_SCREEN) \
                        or any(self.collisionRect.colliderect(rubberTrap.collisionRect) for rubberTrap in c.rubberGroup
                               if rubberTrap.trapState != c.OtherStates.OFF_SCREEN):
                    self.bouncingOff = True
                    self.reverseDirection()
        if self.bouncingOff:
            otherUrchins = [enemy for enemy in c.enemyGroup if
                            (enemy != self and enemy.enemyState not in [c.EnemyStates.OFF_SCREEN])]
            if not any(self.rect.colliderect(enemy) for enemy in otherUrchins) and\
                    not any(self.rect.colliderect(levelRect) for levelRect in
                            PlayerSprite.currentLevel.levelBorderRects) and\
                    not any(self.collisionRect.colliderect(gold.collisionRect) for gold in c.goldGroup if
                            gold.goldState != c.OtherStates.OFF_SCREEN) and\
                    not any(self.collisionRect.colliderect(rubberTrap.collisionRect) for rubberTrap in c.rubberGroup
                            if rubberTrap.trapState != c.OtherStates.OFF_SCREEN):
                self.bouncingOff = False

    def animateMovement(self):
        """Change the sprite's image every 8 frames to create the illusion of animation."""
        if self.frameCount % 16 < 8:
            self.changeImage("move", 1)
        else:
            self.changeImage("move", 0)

    def reverseDirection(self):
        """Set the sprite's facingDirection to the opposite of its current facingDirection."""
        if self.facingDirection == c.Directions.UP:
            self.facingDirection = c.Directions.DOWN
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + 2)
        elif self.facingDirection == c.Directions.DOWN:
            self.facingDirection = c.Directions.UP
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - 2)
        elif self.facingDirection == c.Directions.LEFT:
            self.facingDirection = c.Directions.RIGHT
            self.setCoordinates(self.coordinates[0] + 2, self.coordinates[1])
        elif self.facingDirection == c.Directions.RIGHT:
            self.facingDirection = c.Directions.LEFT
            self.setCoordinates(self.coordinates[0] - 2, self.coordinates[1])

    def checkSonicWaveCollision(self):
        """Check if the sprite is currently colliding with a sonic wave sprite, and change its state and color if
        so.

        The urchin's animation count is set to 0 if it is hit by a sonic wave sprite to reset the amount of time
        that it has spent being stunned.
        If the urchin is in any 'inactive' states, this method is ignored.
        """
        if self.enemyState not in [c.EnemyStates.EXPLODING, c.EnemyStates.OFF_SCREEN]:
            if any(wave.rect.collidepoint(self.rect.center) for wave in c.attackGroup):
                playSound("push_enemy.wav")
                self.color = c.YELLOW
                if self.enemyState == c.EnemyStates.BALL:
                    key = "ball"
                    index = 1
                elif self.enemyState == c.EnemyStates.SMALL_BALL:
                    key = "ball"
                    index = 0
                else:
                    key = "move"
                    index = 0
                self.changeImage(key, index)
                self.frameCount = self.animationCount = 0

    def checkOtherUrchinCollision(self):
        """Check if the sprite is colliding with any of the other urchin sprites.

        If they are colliding, the sprite reverses its direction (unless it is already colliding with an object)
        and moves forwards.
        This method is ignored unless the urchin is currently in a moving state, and its color is BLUE.
        """
        if self.enemyState == c.EnemyStates.MOVING and self.color == c.BLUE:
            otherUrchins = [enemy for enemy in c.enemyGroup if (enemy != self and
                            enemy.enemyState not in [c.EnemyStates.OFF_SCREEN])]
            if any(self.rect.colliderect(enemy) for enemy in otherUrchins):
                self.frameCount = 0
                if not self.bouncingOff:
                    self.reverseDirection()
                    self.bouncingOff = True
                self.moveSprite()

    def push(self, pushingPlayer):
        """Move the sprite in the direction the player pushing it is facing, and check if it has collided with a
        wall.

        The urchin's animation count is set to 0 if it is pushed to reset the amount of time that it has spent
        being stunned.
        When the sprite and the player are both facing horizontally or are both facing vertically, this method
        puts the urchin immediately in front of the player sprite's rect every frame.
        Otherwise, this method just pushes the urchin sprite forward every frame until is it no longer in the
        middle of the intersection.
        """
        self.animationCount = 0
        # if not pygame.mixer.Channel(1).get_busy():
        #     pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(musicFolder, "push_enemy.wav")))
        playSound("push_enemy.wav")
        if any(levelRect.colliderect(self.collisionRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects):
            playSound("crush_enemy.wav")
            self.enemyState = c.EnemyStates.EXPLODING
            self.frameCount = 0
            self.changeImage("death", 0)
            pushingPlayer.killedUrchinCount += 1
        else:
            if self.isFacingHorizontally() == pushingPlayer.isFacingHorizontally():
                self.facingDirection = pushingPlayer.facingDirection
                if self.facingDirection == c.Directions.UP and\
                        self.collisionRect.collidepoint(pushingPlayer.collisionRect.midtop):
                    self.rect.bottom = pushingPlayer.rect.top
                elif self.facingDirection == c.Directions.DOWN and\
                        self.collisionRect.collidepoint(pushingPlayer.collisionRect.midbottom):
                    self.rect.top = pushingPlayer.rect.bottom
                elif self.facingDirection == c.Directions.LEFT and\
                        self.collisionRect.collidepoint(pushingPlayer.collisionRect.midleft):
                    self.rect.right = pushingPlayer.rect.left
                elif self.facingDirection == c.Directions.RIGHT and\
                        self.collisionRect.collidepoint(pushingPlayer.collisionRect.midright):
                    self.rect.left = pushingPlayer.rect.right
                self.setCoordinates(self.rect.topleft[0], self.rect.topleft[1])
                self.moveSprite(int(PlayerSprite.movementSpeed))
            elif 2 < self.rect.center[0] % 48 < 30 and 4 < self.rect.center[1] % 48 < 32:
                self.moveSprite(int(PlayerSprite.movementSpeed))

    def offsetPointsSpriteCoordinates(self, offsetDirection):
        """Move the sprite's coordinates in one direction.

        To be called when the sprite's state changes to OFF_SCREEN, as at that point its image changes to a 500
        representing its value in points. This method exists to move the 500 away from the wall, to make it more
        visible.
        """
        if offsetDirection == c.Directions.UP:
            self.setCoordinates(self.coordinates[0] - 2, self.coordinates[1] + 20)
        elif offsetDirection == c.Directions.DOWN:
            self.setCoordinates(self.coordinates[0] - 2, self.coordinates[1] - 20)
        elif offsetDirection == c.Directions.LEFT:
            self.setCoordinates(self.coordinates[0] + 18, self.coordinates[1])
        else:
            self.setCoordinates(self.coordinates[0] - 22, self.coordinates[1])

    def setRandomDirection(self):
        """Randomly choose one of the four cardinal directions to be the sprite's new facingDirection."""
        self.facingDirection = random.choice(c.directionList)
