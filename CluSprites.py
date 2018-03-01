import pygame
import os
import sys
import random
from enum import Enum
from CluLevels import BonusLevel


"""Enemies: Pushing sound effect
   Gold: Level complete
   Gameplay: Random item locations
             Random level order
             Spawning items
             Level complete (Tally points, animate, sound effects, bonus)
             Game over screen
   Bonus level differences"""

"""Fix pushing urchin sound effect"""
"""Fix window icon"""
"""Fix urchin push locations, wall hitboxes, hit while spinning"""

"""Finish player end screen animation"""
"""Adjusting player coordinates"""

"""apple banana  cherry  melon   pineapple
bag      clock   flag
pts800   pts1500
count_points    earn_bonus

Sonic wave, points, text, player, player arm"""

"""Collect clock: Change color of ..."""


SCREEN_SIZE = (512, 448)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 200, 15)

gameFolder = os.path.dirname(__file__)
spriteFolder = os.path.join(gameFolder, "Sprites")
spriteSheetFolder = os.path.join(gameFolder, "Sprites", "SpriteSheets")
backgroundFolder = os.path.join(gameFolder, "Backgrounds")
titleFolder = os.path.join(gameFolder, "Titles")
musicFolder = os.path.join(gameFolder, "Music")

_imageLibrary = {}
_soundLibrary = {}


def getImage(folder, imageFile):
    global _imageLibrary
    image = _imageLibrary.get(imageFile)
    if image is None:
        fullPath = os.path.join(folder, imageFile)
        try:
            image = pygame.image.load(fullPath).convert()
            _imageLibrary[imageFile] = image
        except pygame.error:
            print("ERROR: Cannot find image '{}'".format(imageFile))
            pygame.quit()
            sys.exit()
    return image


def playSound(soundFile):
    global _soundLibrary
    sound = _soundLibrary.get(soundFile)
    if sound is None:
        fullPath = os.path.join(musicFolder, soundFile)
        try:
            sound = pygame.mixer.Sound(fullPath)
            _soundLibrary[soundFile] = sound
        except pygame.error:
            print("ERROR: Cannot find sound '{}'".format(soundFile))
            pygame.quit()
            sys.exit()
        # if soundFile == "push_or_shoot_enemy.wav":
        #     sound.set_volume(0.5)
    sound.play()


class SpriteSheet:
    def __init__(self, imagePath):
        self.sheet = getImage(spriteSheetFolder, imagePath)

    def getSheetImage(self, x, y, width, height, key=BLACK):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(key)
        return image

    def getStripImages(self, x, y, width, height, numberOfImages=0, key=BLACK):
        spriteSheetWidth = self.sheet.get_size()[0]
        if numberOfImages != 0:
            spriteSheetWidth = width * numberOfImages + x
        imageList = []
        while x + width <= spriteSheetWidth:
            image = self.getSheetImage(x, y, width, height, key)
            imageList.append(image)
            x += width
        return imageList


class PlayerStates(Enum):
    BALL = "ball"
    MOVING = "moving"
    SWINGING = "swinging"
    FINISHED_SWINGING = "finished swinging"
    HITTING_WALL = "hitting wall"
    HITTING_PLAYER_MOVING = "hitting player moving"
    HITTING_PLAYER_SWINGING = "hitting player swinging"
    FALLING = "falling"
    EXPLODING = "exploding"
    OFF_SCREEN = "off screen"
    FROZEN = "frozen"
    LEVEL_END = "level end"
    DEAD = "dead"


class ArmStates(Enum):
    EXTENDED = "extended"
    SWINGING = "swinging"
    OFF_SCREEN = "off screen"


class EnemyState(Enum):
    MOVING = "moving"
    BALL = "ball"
    SMALL_BALL = "small ball"
    WAITING = "waiting"
    EXPLODING = "exploding"
    OFF_SCREEN = "off screen"
    DEAD = "dead"


class OtherState(Enum):
    REVEALED = "revealed"
    UPSIDE_DOWN = "flipped over"
    FLIPPING_UP = "flipping up"
    FLIPPING_DOWN = "flipping down"
    OFF_SCREEN = "off screen"
    TRIGGERED = "triggered"


class Directions(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


playerGroup = pygame.sprite.Group()
armGroup = pygame.sprite.Group()
attackGroup = pygame.sprite.Group()
blackHoleGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
itemGroup = pygame.sprite.Group()
goldGroup = pygame.sprite.Group()
rubberGroup = pygame.sprite.Group()
textGroup = pygame.sprite.Group()
allGroups = (itemGroup, blackHoleGroup, enemyGroup, goldGroup, rubberGroup, armGroup, playerGroup, attackGroup,
             textGroup)

directionsDict = {"up": Directions.UP, "down": Directions.DOWN, "left": Directions.LEFT, "right": Directions.RIGHT}


class TitleSprite(pygame.sprite.Sprite):
    def __init__(self, position="left"):
        super().__init__()
        spriteSheet = SpriteSheet("title.png")
        self.animationFrames = []
        self.position = position
        self.rotationCount = self.frameCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 144, 82))
        self.animationFrames.extend(spriteSheet.getStripImages(0, 82, 144, 82))
        self.animationFrames.extend(spriteSheet.getStripImages(0, 164, 144, 82, 3))
        self.image = self.animationFrames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        self.frameCount += 1
        if self.position == "left":
            if (20 < self.frameCount < 132 and self.frameCount % 2 == 1) or 289 < self.frameCount < 394:
                self.rotateAnimationLeft()
        else:
            if (150 < self.frameCount < 272 and self.frameCount % 2 == 1) or 289 < self.frameCount < 394:
                self.rotateAnimationRight()
        self.image.set_colorkey(BLACK)

    def rotateAnimationLeft(self):
        self.rotationCount += 1
        if self.rotationCount < len(self.animationFrames):
            self.image = self.animationFrames[self.rotationCount]
        else:
            self.rotationCount = 0
            self.image = self.animationFrames[0]

    def rotateAnimationRight(self):
        self.rotationCount += 1
        if self.rotationCount < len(self.animationFrames):
            self.image = self.animationFrames[-self.rotationCount]
        else:
            self.rotationCount = 0
            self.image = self.animationFrames[-1]

    def setTitleImage(self):
        self.image = self.animationFrames[4]
        self.image.set_colorkey(BLACK)

    def setTitleImageBackwards(self):
        self.image = self.animationFrames[0]
        self.frameCount = self.rotationCount = 0
        self.image.set_colorkey(BLACK)


class PlayerSprite(pygame.sprite.Sprite):
    directionList = [Directions.RIGHT, Directions.UP, Directions.LEFT, Directions.DOWN]
    currentLevel = None
    movementSpeed = 2

    def __init__(self, playerNumber=1):
        super().__init__(playerGroup)
        spriteSheet = SpriteSheet("player{}.png".format(playerNumber))
        self.playerNumber = playerNumber
        self.lives = 5
        self.baseCoordinates = (0, 0)
        self.coordinates = (0, 0)
        self.playerState = OtherState.OFF_SCREEN
        self.facingDirection = Directions.RIGHT
        self.swingingClockwise = self.bouncingOff = False
        self.killedUrchinCount = self.goldCollectedCount = self.score = 0
        self.swingFrameCount = self.frameCount = 0

        self.imageDict = {"arm": [], "ball": [], "end": [], "death": [], "turn": [], "fall": [],
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
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (12, 12))

    def flipImage(self):
        if self.facingDirection == Directions.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.facingDirection == Directions.UP:
            self.image = pygame.transform.flip(self.image, False, True)

    def rotateImage(self):
        if self.swingFrameCount % 85 < 17 and self.swingingClockwise:
            self.image = pygame.transform.rotate(self.image, 270)
        elif 26 < self.swingFrameCount % 85 < 47:
            self.image = pygame.transform.rotate(self.image, 270)
            if not self.isFacingHorizontally():
                self.image = pygame.transform.flip(self.image, True, False)
            elif not self.swingingClockwise:
                self.image = pygame.transform.flip(self.image, False, True)
        elif 46 < self.swingFrameCount % 85 < 67:
            if self.swingingClockwise:
                self.image = pygame.transform.rotate(self.image, 90)
                self.flipImage()
            elif self.facingDirection == Directions.DOWN:
                self.image = pygame.transform.rotate(self.image, 90)
                self.image = pygame.transform.flip(self.image, False, True)
            else:
                self.image = pygame.transform.rotate(self.image, 270)
        else:
            self.image = pygame.transform.rotate(self.image, 270)
            if self.facingDirection == Directions.RIGHT:
                self.image = pygame.transform.flip(self.image, False, True)
            if not self.swingingClockwise and self.swingFrameCount > 71:
                self.image = pygame.transform.flip(self.image, False, True)

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y
        self.collisionRect = pygame.rect.Rect((x + 12, y + 12), (12, 12))

    def initialize(self, x, y):
        self.baseCoordinates = (x, y)
        self.setCoordinates(x, y)
        self.killedUrchinCount = self.goldCollectedCount = 0
        if not self.playerState == PlayerStates.DEAD:
            self.putSpriteInBall()

    def isFacingHorizontally(self):
        return self.facingDirection in [Directions.RIGHT, Directions.LEFT]

    def changeImage(self, imageKey, imageIndex):
        if imageKey in ["move", "squish"]:
            self.image = self.imageDict[imageKey][self.getDirectionKey()][imageIndex]
        else:
            self.image = self.imageDict[imageKey][imageIndex]

    def getDirectionKey(self):
        if self.isFacingHorizontally():
            return "horizontal"
        else:
            return "vertical"

    def putSpriteInBall(self):
        self.facingDirection = Directions.RIGHT
        self.playerState = PlayerStates.BALL
        self.changeImage("ball", 0)
        self.lives = max(0, self.lives - 1)
        self.frameCount = 0

    def update(self):
        self.checkEnemyCollision()
        self.checkBlackHoleCollision()
        self.checkOtherPlayerCollision()
        self.frameCount += 1

        if self.playerState == PlayerStates.BALL:
            if self.frameCount % 16 < 8:
                self.changeImage("ball", 0)
            else:
                self.changeImage("ball", 1)
            if self.frameCount % 16 == 0:
                self.frameCount = 0
        elif self.playerState == PlayerStates.MOVING:
            self.moveSprite()
            self.moveAnimation()
            if self.frameCount % 8 == 0:
                self.frameCount = 0
        elif self.playerState == PlayerStates.FINISHED_SWINGING:
            self.moveSprite()
            self.moveAnimation()
            if self.frameCount % 16 == 0:
                self.playerState = PlayerStates.MOVING
        elif self.playerState == PlayerStates.HITTING_WALL:
            if self.frameCount % 9 == 4:
                self.changeImage("squish", 1)
            elif self.frameCount % 9 > 4:
                self.changeImage("squish", 2)
            if self.frameCount % 9 == 0:
                self.frameCount = 0
                self.rebound()
        elif self.playerState == PlayerStates.FALLING:
            if 7 < self.frameCount % 40 < 17:
                self.changeImage("fall", 1)
            elif 16 < self.frameCount % 40 < 25:
                self.changeImage("fall", 2)
            elif 24 < self.frameCount % 40 < 33:
                self.changeImage("fall", 3)
            if self.frameCount % 40 == 0:
                self.playerState = PlayerStates.OFF_SCREEN
                self.image = self.emptyImage
                self.frameCount = 0
        elif self.playerState == PlayerStates.EXPLODING:
            if 7 < self.frameCount % 40 < 17:
                self.changeImage("death", 1)
            elif 16 < self.frameCount % 40 < 25:
                self.changeImage("death", 2)
            elif 24 < self.frameCount % 40 < 33:
                self.changeImage("death", 3)
            if self.frameCount % 40 == 0:
                self.playerState = PlayerStates.OFF_SCREEN
                self.image = self.emptyImage
                self.frameCount = 0
        elif self.playerState == PlayerStates.OFF_SCREEN:
            if self.lives > 0 and self.frameCount % 160 == 0:
                self.setCoordinates(self.baseCoordinates[0], self.baseCoordinates[1])
                self.putSpriteInBall()
                self.frameCount = 0
            elif self.lives == 0:
                self.playerState = PlayerStates.DEAD
        elif self.playerState == PlayerStates.SWINGING:
            self.swingFrameCount += 1
            self.swing()
        elif self.playerState == PlayerStates.HITTING_PLAYER_MOVING:
            if self.frameCount % 8 < 4:
                self.changeImage("move", 2)
            else:
                self.changeImage("move", 3)
            if self.frameCount % 8 == 0:
                self.moveSprite()
                self.frameCount = 0
                self.playerState = PlayerStates.MOVING
        elif self.playerState == PlayerStates.HITTING_PLAYER_SWINGING:
            if self.getOrthogonalTurnState():
                imageKey = "move"
            else:
                imageKey = "turn"
            if self.frameCount % 8 < 4:
                self.changeImage(imageKey, 2)
            else:
                self.changeImage(imageKey, 3)
            if self.frameCount % 8 == 1:
                self.swingingClockwise = not self.swingingClockwise
            if self.frameCount % 8 == 0:
                # self.swingFrameCount = 85 - self.swingFrameCount
                self.moveSprite()
                self.frameCount = 0
                self.playerState = PlayerStates.SWINGING
        elif self.playerState == PlayerStates.LEVEL_END:
            self.animateLevelEnd()

        if self.bouncingOff:
            otherPlayers = [player for player in playerGroup if (player != self and
                            player.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING,
                                                   PlayerStates.HITTING_PLAYER_MOVING,
                                                   PlayerStates.HITTING_PLAYER_SWINGING,
                                                   PlayerStates.FINISHED_SWINGING,
                                                   PlayerStates.FROZEN])]
            if not any(player.collisionRect.colliderect(self.collisionRect) for player in otherPlayers):
                self.bouncingOff = False
        self.flipImage()
        self.image.set_colorkey(BLACK)

    def startMoving(self, direction):
        if self.playerState == PlayerStates.BALL:
            playSound("move_out_of_ball.wav")
            self.facingDirection = directionsDict[direction]
            self.changeImage("move", 0)
            self.playerState = PlayerStates.MOVING
            self.frameCount = 0

    def moveSprite(self):
        if self.facingDirection == Directions.UP:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - PlayerSprite.movementSpeed)
        elif self.facingDirection == Directions.DOWN:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + PlayerSprite.movementSpeed)
        elif self.facingDirection == Directions.LEFT:
            self.setCoordinates(self.coordinates[0] - PlayerSprite.movementSpeed, self.coordinates[1])
            if self.rect.right < 0:
                self.setCoordinates(512, self.coordinates[1])
        elif self.facingDirection == Directions.RIGHT:
            self.setCoordinates(self.coordinates[0] + PlayerSprite.movementSpeed, self.coordinates[1])
            if self.rect.left > 512:
                self.setCoordinates(-48, self.coordinates[1])
        if any(self.rect.colliderect(levelRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects):
            self.hitWall()
            self.bouncingOff = True
        for gold in goldGroup:
            if gold.collisionRect.collidepoint(self.rect.center) and gold.goldState in\
                    [OtherState.OFF_SCREEN, OtherState.REVEALED, OtherState.UPSIDE_DOWN]:
                gold.passingDirection = self.facingDirection
                if not gold.alreadyRevealed:
                    self.goldCollectedCount += 1
                gold.startFlipAnimation()

    def hitWall(self):
        self.frameCount = 0
        playSound("bounce_wall.wav")
        self.playerState = PlayerStates.HITTING_WALL
        self.image = self.imageDict["squish"][self.getDirectionKey()][0]

    def rebound(self):
        self.changeDirection()
        self.image = self.imageDict["move"][self.getDirectionKey()][0]
        self.playerState = PlayerStates.MOVING

    def changeDirection(self):
        if self.facingDirection == Directions.UP:
            self.facingDirection = Directions.DOWN
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + (PlayerSprite.movementSpeed + 2))
        elif self.facingDirection == Directions.DOWN:
            self.facingDirection = Directions.UP
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - (PlayerSprite.movementSpeed + 2))
        elif self.facingDirection == Directions.LEFT:
            self.facingDirection = Directions.RIGHT
            self.setCoordinates(self.coordinates[0] + (PlayerSprite.movementSpeed + 2), self.coordinates[1])
        elif self.facingDirection == Directions.RIGHT:
            self.facingDirection = Directions.LEFT
            self.setCoordinates(self.coordinates[0] - (PlayerSprite.movementSpeed + 2), self.coordinates[1])

    def moveAnimation(self):
        if self.frameCount % 8 < 4:
            self.changeImage("move", 1)
        else:
            self.changeImage("move", 0)

    def getOrthogonalTurnState(self):
        if self.swingingClockwise:
            if self.swingFrameCount % 85 < 6 or 16 < self.swingFrameCount % 85 < 28 or\
                                    38 < self.swingFrameCount % 85 < 50 or 59 < self.swingFrameCount % 85 < 71 or\
                                    self.swingFrameCount % 85 > 81:
                return True
        else:
            if self.swingFrameCount % 85 < 6 or 15 < self.swingFrameCount % 85 < 27 or\
                                    37 < self.swingFrameCount % 85 < 48 or 58 < self.swingFrameCount % 85 < 70 or\
                                    self.swingFrameCount % 85 > 79:
                return True
        return False

    def swing(self):
        if self.swingingClockwise:
            if self.swingFrameCount % 85 == 8:
                self.facingDirection = Directions.DOWN
            elif self.swingFrameCount % 85 == 30:
                self.facingDirection = Directions.LEFT
            elif self.swingFrameCount % 85 == 52:
                self.facingDirection = Directions.UP
            elif self.swingFrameCount % 85 == 74:
                self.facingDirection = Directions.RIGHT
        else:
            if self.swingFrameCount % 85 == 8:
                self.facingDirection = Directions.UP
            elif self.swingFrameCount % 85 == 29:
                self.facingDirection = Directions.LEFT
            elif self.swingFrameCount % 85 == 50:
                self.facingDirection = Directions.DOWN
            elif self.swingFrameCount % 85 == 72:
                self.facingDirection = Directions.RIGHT
        if self.getOrthogonalTurnState():
            self.moveAnimation()
        elif (self.swingingClockwise and self.frameCount % 12 < 6) or\
                (not self.swingingClockwise and (self.frameCount - 6) % 12 < 6):
            self.image = self.imageDict["turn"][0]
            self.rotateImage()
        else:
            self.image = self.imageDict["turn"][1]
            self.rotateImage()

        if self.swingFrameCount % 85 == 0:
            self.swingFrameCount = 0
        if self.frameCount % 96 == 0:
            self.frameCount = 0
        self.moveSwingSprite()
        for gold in goldGroup:
            if gold.collisionRect.collidepoint(self.rect.center) and gold.goldState in\
                    [OtherState.OFF_SCREEN, OtherState.REVEALED, OtherState.UPSIDE_DOWN]:
                gold.passingDirection = self.facingDirection
                if not gold.alreadyRevealed:
                    self.goldCollectedCount += 1
                gold.startFlipAnimation()
        # if self.swingFrameCount > 55:
        #     pygame.time.delay(200)

    def moveSwingSprite(self):
        if self.swingingClockwise:
            if self.swingFrameCount % 85 in (17, 48, 50, 51, 53, 55, 56, 58, 59, 60, 61, 63, 64, 65, 66, 68, 69, 70,
                                             71, 72, 74, 75, 77, 78, 79, 80, 83):
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - 2)
            if self.swingFrameCount % 85 in (4, 7, 9, 11, 13, 14, 15, 18, 19, 20, 21, 23, 24, 25, 26, 30, 31, 32, 34,
                                             36, 38, 41):
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + 2)
            if self.swingFrameCount % 85 in (25, 29, 31, 33, 35, 36, 37, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 51,
                                             52, 53, 55, 57, 59, 62, 71, 83):
                self.setCoordinates(self.coordinates[0] - 2, self.coordinates[1])
            if self.swingFrameCount % 85 in (0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 13, 15, 17, 18, 69, 72, 74, 76, 77, 79,
                                             80, 81, 84):
                self.setCoordinates(self.coordinates[0] + 2, self.coordinates[1])
            if self.swingFrameCount % 85 == 6:
                self.setCoordinates(self.coordinates[0] + 2, self.coordinates[1] - 1)
            elif self.swingFrameCount % 85 == 28:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + 6)
            elif self.swingFrameCount % 85 == 39:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + 1)
            elif self.swingFrameCount % 85 == 50:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + 3)
            elif self.swingFrameCount % 85 == 82:
                self.setCoordinates(self.coordinates[0] + 2, self.coordinates[1] + 1)
            elif self.swingFrameCount % 85 == 83:
                self.setCoordinates(self.coordinates[0] + 2, self.coordinates[1])
        else:
            if self.swingFrameCount % 85 in (4, 7, 9, 11, 12, 14, 15, 17, 19, 20, 21, 22, 24, 25, 26, 27, 28, 30, 31,
                                             33, 34, 36, 39, 59):
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - 2)
            if self.swingFrameCount % 85 in (47, 50, 52, 53, 55, 56, 58, 60, 61, 62, 64, 65, 66, 67, 69, 71, 72, 74,
                                             75, 77, 79, 82):
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + 2)
            if self.swingFrameCount % 85 in (26, 29, 31, 32, 34, 35, 37, 39, 40, 41, 43, 44, 45, 46, 48, 49, 50,
                                             51, 53, 54, 56, 58, 59, 61, 69, 80):
                self.setCoordinates(self.coordinates[0] - 2, self.coordinates[1])
            if self.swingFrameCount % 85 in (0, 1, 3, 4, 5, 6, 7, 9, 10, 12, 13, 15, 16, 18, 68, 71, 73, 75, 77, 78,
                                             79, 81, 82, 83, 84):
                self.setCoordinates(self.coordinates[0] + 2, self.coordinates[1])
            if self.swingFrameCount % 85 == 6:
                self.setCoordinates(self.coordinates[0] + 2, self.coordinates[1] + 1)
            elif self.swingFrameCount % 85 == 16:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - 2)
            elif self.swingFrameCount % 85 == 37:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - 1)
            elif self.swingFrameCount % 85 == 47:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - 1)
            elif self.swingFrameCount % 85 == 70:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + 6)
            elif self.swingFrameCount % 85 == 80:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + 1)

    def checkBlackHoleCollision(self):
        if self.playerState == PlayerStates.MOVING:
            for hole in blackHoleGroup:
                if hole.rect.collidepoint(self.rect.center):
                    self.coordinates = hole.coordinates
                    self.rect.topleft = hole.coordinates
                    playSound("death.wav")
                    self.frameCount = 0
                    self.facingDirection = Directions.RIGHT
                    self.playerState = PlayerStates.FALLING
                    self.image = self.imageDict["fall"][0]

    def checkEnemyCollision(self):
        if self.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING, PlayerStates.FINISHED_SWINGING,
                                PlayerStates.HITTING_WALL, PlayerStates.HITTING_PLAYER_MOVING,
                                PlayerStates.HITTING_PLAYER_SWINGING]:
            if any(enemy.collisionRect.colliderect(self.collisionRect) and enemy.enemyState == EnemyState.MOVING
                   and enemy.color == BLUE for enemy in enemyGroup):
                playSound("death.wav")
                self.frameCount = 0
                self.facingDirection = Directions.RIGHT
                self.playerState = PlayerStates.EXPLODING
                self.image = self.imageDict["death"][0]
            else:
                pushedEnemies = [enemy for enemy in enemyGroup if enemy.collisionRect.colliderect(self.rect)
                                 and enemy.color == YELLOW]
                for enemy in pushedEnemies:
                    enemy.push(self)

    def checkOtherPlayerCollision(self):
        if self.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING, PlayerStates.FINISHED_SWINGING,
                                PlayerStates.FROZEN] and not self.bouncingOff:
            otherPlayers = [player for player in playerGroup if (player != self and
                            player.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING,
                                                   PlayerStates.FINISHED_SWINGING, PlayerStates.FROZEN,
                                                   PlayerStates.HITTING_PLAYER_MOVING,
                                                   PlayerStates.HITTING_PLAYER_SWINGING])]
            for player in otherPlayers:
                if player.collisionRect.colliderect(self.collisionRect):
                    playSound("bounce_rubber_or_player.wav")
                    self.frameCount = 0
                    self.bouncingOff = True
                    if self.playerState in [PlayerStates.MOVING, PlayerStates.FINISHED_SWINGING, PlayerStates.FROZEN]:
                        self.playerState = PlayerStates.HITTING_PLAYER_MOVING
                    else:
                        self.playerState = PlayerStates.HITTING_PLAYER_SWINGING
                    self.image = self.imageDict["move"][self.getDirectionKey()][2]
                    if player.playerState not in [PlayerStates.HITTING_PLAYER_MOVING,
                                                  PlayerStates.HITTING_PLAYER_SWINGING]:
                        player.checkOtherPlayerCollision()

    def adjustPosition(self):  # TEST MORE
        if self.isFacingHorizontally():
            if 0 < (self.coordinates[1] - 1) % 48 < 24:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - (self.coordinates[1] % 48 - 1))
            elif self.coordinates[1] % 48 > 23:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + (48 - self.coordinates[1] % 48 + 1))
        else:
            if 0 < self.coordinates[0] % 48 < 24:
                self.setCoordinates(self.coordinates[0] - (self.coordinates[0] % 48), self.coordinates[1])
            elif self.coordinates[0] % 48 > 23:
                self.setCoordinates(self.coordinates[0] + (48 - self.coordinates[0] % 48), self.coordinates[1])

    def animateLevelEnd(self):
        if self.playerNumber == 1:
            self.setCoordinates(88, 80)
            if self.frameCount in (32, 160, 192):
                self.image = self.imageDict["end"][1]
            else:
                self.image = self.imageDict["end"][0]
                if self.frameCount % 32 > 15:
                    self.flipImage()
                if self.frameCount % 16 == 0:
                    playSound("grab_post_move_end.wav")
            # REMEMBER TO COUNT DOWN TIME


class PlayerArmSprite(pygame.sprite.Sprite):
    directionList = [Directions.RIGHT, Directions.UP, Directions.LEFT, Directions.DOWN]

    def __init__(self, playerBody=None):
        super().__init__(armGroup)
        self.playerBody = playerBody
        self.coordinates = (0, 0)
        self.armState = ArmStates.OFF_SCREEN
        self.extendedDirection = Directions.RIGHT
        self.swingingClockwise = False
        self.swingFrameCount = 0

        self.emptyImage = self.playerBody.emptyImage
        self.image = self.emptyImage
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (12, 12))
        self.wallCollisionRect = pygame.rect.Rect((0, 0), (40, 40))

    def setCoordinates(self, x, y):
        horizontalOffset = 14
        verticalOffset = 16
        if self.playerBody.facingDirection == Directions.LEFT:
            horizontalOffset -= 10
        elif self.playerBody.facingDirection == Directions.UP:
            verticalOffset -= 10

        if self.extendedDirection == Directions.UP:
            self.coordinates = (x + horizontalOffset, y - 13)
            self.collisionRect = pygame.rect.Rect((self.coordinates[0] + 2, self.coordinates[1]), (12, 12))
        elif self.extendedDirection == Directions.DOWN:
            self.coordinates = (x + horizontalOffset, y + 31)
            self.collisionRect = pygame.rect.Rect((self.coordinates[0] + 2, self.coordinates[1] + 4), (12, 12))
        elif self.extendedDirection == Directions.LEFT:
            self.coordinates = (x - 14, y + verticalOffset)
            self.collisionRect = pygame.rect.Rect((self.coordinates[0], self.coordinates[1] + 2), (12, 12))
        else:
            self.coordinates = (x + 30, y + verticalOffset)
            self.collisionRect = pygame.rect.Rect((self.coordinates[0] + 4, self.coordinates[1] + 2), (12, 12))
        self.rect.topleft = self.coordinates
        self.wallCollisionRect = pygame.rect.Rect((self.coordinates[0] - 14, self.coordinates[1] - 14), (40, 40))

    def offsetCoordinates(self, x, y):
        self.coordinates = (self.coordinates[0] - x, self.coordinates[1] - y)
        self.rect.topleft = self.coordinates
        self.collisionRect = pygame.rect.Rect((self.collisionRect[0] - x, self.collisionRect[1] - y), (12, 12))
        self.wallCollisionRect = pygame.rect.Rect((self.coordinates[0] - 14, self.coordinates[1] - 14), (40, 40))

    def rotateImage(self):
        if self.extendedDirection in PlayerArmSprite.directionList:
            rotationDegrees = 90 * PlayerArmSprite.directionList.index(self.extendedDirection)
            self.image = pygame.transform.rotate(self.image, rotationDegrees)
        self.flipImage()

    def flipImage(self):
        if self.extendedDirection == Directions.UP:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.extendedDirection == Directions.RIGHT:
            self.image = pygame.transform.flip(self.image, False, True)
        if self.armState == ArmStates.EXTENDED:
            if self.playerBody.facingDirection == Directions.LEFT:
                self.image = pygame.transform.flip(self.image, True, False)
            if self.playerBody.facingDirection == Directions.UP:
                self.image = pygame.transform.flip(self.image, False, True)

    def update(self):
        if self.playerBody.playerState in [PlayerStates.BALL, PlayerStates.FALLING, PlayerStates.EXPLODING,
                                           PlayerStates.HITTING_WALL, PlayerStates.OFF_SCREEN, PlayerStates.DEAD]:
            self.armState = ArmStates.OFF_SCREEN
        elif self.armState == ArmStates.EXTENDED:
            self.setCoordinates(self.playerBody.coordinates[0], self.playerBody.coordinates[1])
            self.checkGrabPost()
            self.image = self.playerBody.imageDict["arm"][0]
        elif self.armState == ArmStates.SWINGING:
            self.swingFrameCount += 1
            self.swing()
        if self.armState == ArmStates.OFF_SCREEN:
            self.image = self.emptyImage
        self.rotateImage()
        self.image.set_colorkey(BLACK)

    def extendArm(self, direction):
        self.armState = ArmStates.OFF_SCREEN
        if self.playerBody.isFacingHorizontally() and direction in ["up", "down"]:
            self.extendedDirection = directionsDict[direction]
            self.armState = ArmStates.EXTENDED
        elif not self.playerBody.isFacingHorizontally() and direction in ["left", "right"]:
            self.extendedDirection = directionsDict[direction]
            self.armState = ArmStates.EXTENDED

    def checkGrabPost(self):
        if not any(self.wallCollisionRect.colliderect(levelRect) for levelRect in
                   PlayerSprite.currentLevel.levelBorderRects) and not\
                any(self.wallCollisionRect.colliderect(trap.collisionRect) for trap in rubberGroup if
                    trap.trapState in [OtherState.REVEALED, OtherState.TRIGGERED]) and not\
                any(self.playerBody.rect.colliderect(trap.collisionRect) for trap in rubberGroup):
            if self.collisionRect[0] % 48 in range(34, 39) and self.collisionRect[1] % 48 in range(34, 39) and\
                                    70 < self.collisionRect[0] < 400 and 20 < self.collisionRect[1] < 500:
                playSound("grab_post_move_end.wav")
                self.armState = ArmStates.SWINGING
                self.playerBody.playerState = PlayerStates.SWINGING
                if any(((self.extendedDirection == Directions.UP and
                         self.playerBody.facingDirection == Directions.LEFT),
                        (self.extendedDirection == Directions.DOWN and
                         self.playerBody.facingDirection == Directions.RIGHT),
                        (self.extendedDirection == Directions.RIGHT and
                         self.playerBody.facingDirection == Directions.UP),
                        (self.extendedDirection == Directions.LEFT and
                         self.playerBody.facingDirection == Directions.DOWN))):
                    self.swingingClockwise = True
                    self.playerBody.swingingClockwise = True
                else:
                    self.swingingClockwise = False
                    self.playerBody.swingingClockwise = False
                # print(self.extendedDirection, self.playerBody.facingDirection, self.swingingClockwise)
                offsets = (self.collisionRect[0] % 48 - 34, self.collisionRect[1] % 48 - 36)
                # print(self.coordinates[0] % 48, self.coordinates[1] % 48, self.rect.topleft,
                #       self.collisionRect.topleft, self.wallCollisionRect.topleft)
                self.offsetCoordinates(offsets[0], offsets[1])
                # print(self.coordinates[0] % 48, self.coordinates[1] % 48, self.rect.topleft,
                #       self.collisionRect.topleft, self.wallCollisionRect.topleft)
                if self.swingingClockwise:
                    if self.extendedDirection == Directions.DOWN:
                        self.swingFrameCount = self.playerBody.swingFrameCount = 84
                        self.playerBody.setCoordinates(self.playerBody.coordinates[0] - offsets[0],
                                                       self.playerBody.coordinates[1] - offsets[1])
                    elif self.extendedDirection == Directions.LEFT:
                        self.swingFrameCount = self.playerBody.swingFrameCount = 22
                        self.playerBody.setCoordinates(self.playerBody.coordinates[0] - offsets[0],
                                                       self.playerBody.coordinates[1] - offsets[1] + 2)
                    elif self.extendedDirection == Directions.UP:
                        self.swingFrameCount = self.playerBody.swingFrameCount = 43
                        self.playerBody.setCoordinates(self.playerBody.coordinates[0] - offsets[0],
                                                       self.playerBody.coordinates[1] - offsets[1])
                    else:
                        self.swingFrameCount = self.playerBody.swingFrameCount = 65
                        self.playerBody.setCoordinates(self.playerBody.coordinates[0] - offsets[0],
                                                       self.playerBody.coordinates[1] - offsets[1] - 1)
                else:
                    if self.extendedDirection == Directions.LEFT:
                        self.swingFrameCount = self.playerBody.swingFrameCount = 20
                        self.playerBody.setCoordinates(self.playerBody.coordinates[0] - offsets[0],
                                                       self.playerBody.coordinates[1] - offsets[1])
                    elif self.extendedDirection == Directions.DOWN:
                        self.swingFrameCount = self.playerBody.swingFrameCount = 41
                        self.playerBody.setCoordinates(self.playerBody.coordinates[0] - offsets[0],
                                                       self.playerBody.coordinates[1] - offsets[1])
                    elif self.extendedDirection == Directions.RIGHT:
                        self.swingFrameCount = self.playerBody.swingFrameCount = 63
                        self.playerBody.setCoordinates(self.playerBody.coordinates[0] - offsets[0] + 2,
                                                       self.playerBody.coordinates[1] - offsets[1])
                    else:
                        self.swingFrameCount = self.playerBody.swingFrameCount = 84
                        self.playerBody.setCoordinates(self.playerBody.coordinates[0] - offsets[0],
                                                       self.playerBody.coordinates[1] - offsets[1])

    def swing(self):
        if self.swingingClockwise:
            if self.swingFrameCount % 85 == 6:
                self.extendedDirection = Directions.LEFT
            elif self.swingFrameCount % 85 == 28:
                self.extendedDirection = Directions.UP
            elif self.swingFrameCount % 85 == 50:
                self.extendedDirection = Directions.RIGHT
            elif self.swingFrameCount % 85 == 71:
                self.extendedDirection = Directions.DOWN
        else:
            if self.swingFrameCount % 85 == 16:
                self.extendedDirection = Directions.LEFT
            elif self.swingFrameCount % 85 == 80:
                self.extendedDirection = Directions.UP
            elif self.swingFrameCount % 85 == 59:
                self.extendedDirection = Directions.RIGHT
            elif self.swingFrameCount % 85 == 38:
                self.extendedDirection = Directions.DOWN
        if self.swingingClockwise:
            if self.swingFrameCount % 85 < 6 or 16 < self.swingFrameCount % 85 < 28 or\
                                    38 < self.swingFrameCount % 85 < 50 or 59 < self.swingFrameCount % 85 < 71 or\
                                    self.swingFrameCount % 85 > 80:
                self.image = self.playerBody.imageDict["arm"][0]
                if self.extendedDirection in [Directions.UP, Directions.RIGHT]:
                    self.image = pygame.transform.flip(self.image, False, True)
            else:
                if self.extendedDirection in [Directions.UP, Directions.DOWN]:
                    self.image = self.playerBody.imageDict["arm"][1]
                    if self.extendedDirection == Directions.DOWN:
                        self.image = pygame.transform.flip(self.image, True, True)
                else:
                    self.image = self.playerBody.imageDict["arm"][2]
                self.flipImage()
        else:
            if self.swingFrameCount % 85 < 6 or 15 < self.swingFrameCount % 85 < 27 or\
                                    37 < self.swingFrameCount % 85 < 48 or 58 < self.swingFrameCount % 85 < 70 or\
                                    self.swingFrameCount % 85 > 79:
                self.image = self.playerBody.imageDict["arm"][0]
                if self.extendedDirection in [Directions.DOWN, Directions.LEFT]:
                    self.image = pygame.transform.flip(self.image, False, True)
            else:
                if self.extendedDirection in [Directions.LEFT, Directions.RIGHT]:
                    self.image = self.playerBody.imageDict["arm"][1]
                    self.image = pygame.transform.rotate(self.image, 90)
                    if self.extendedDirection == Directions.RIGHT:
                        self.flipImage()
                else:
                    self.image = self.playerBody.imageDict["arm"][2]
                    self.rotateImage()
                self.image = pygame.transform.flip(self.image, False, True)
        self.adjustPosition()
        if self.swingFrameCount % 85 == 0:
            self.swingFrameCount = 0

    def adjustPosition(self):
        if self.swingingClockwise:
            if self.swingFrameCount % 85 == 6:
                self.coordinates = (self.coordinates[0] + 2, self.coordinates[1] + 4)
            elif self.swingFrameCount % 85 == 17:
                self.coordinates = (self.coordinates[0], self.coordinates[1] - 2)
            elif self.swingFrameCount % 85 == 28:
                self.coordinates = (self.coordinates[0], self.coordinates[1] + 2)
            elif self.swingFrameCount % 85 == 39:
                self.coordinates = (self.coordinates[0] - 2, self.coordinates[1])
            elif self.swingFrameCount % 85 == 50:
                self.coordinates = (self.coordinates[0], self.coordinates[1] - 2)
            elif self.swingFrameCount % 85 == 60:
                self.coordinates = (self.coordinates[0] - 2, self.coordinates[1])
            elif self.swingFrameCount % 85 == 71:
                self.coordinates = (self.coordinates[0], self.coordinates[1] - 2)
            elif self.swingFrameCount % 85 == 81:
                self.coordinates = (self.coordinates[0] + 2, self.coordinates[1])
        else:
            if self.swingFrameCount % 85 == 6:
                self.coordinates = (self.coordinates[0] + 2, self.coordinates[1] - 2)
            elif self.swingFrameCount % 85 == 27:
                self.coordinates = (self.coordinates[0], self.coordinates[1] - 2)
            elif self.swingFrameCount % 85 == 38:
                self.coordinates = (self.coordinates[0] - 2, self.coordinates[1])
            elif self.swingFrameCount % 85 == 48:
                self.coordinates = (self.coordinates[0], self.coordinates[1] + 4)
            elif self.swingFrameCount % 85 == 59:
                self.coordinates = (self.coordinates[0] - 2, self.coordinates[1] - 2)
            elif self.swingFrameCount % 85 == 70:
                self.coordinates = (self.coordinates[0], self.coordinates[1] + 2)
            elif self.swingFrameCount % 85 == 80:
                self.coordinates = (self.coordinates[0] + 2, self.coordinates[1])
        self.rect.topleft = self.coordinates


class SonicWaveSprite(pygame.sprite.Sprite):
    directionList = [Directions.RIGHT, Directions.UP, Directions.LEFT, Directions.DOWN]

    def __init__(self, direction, firingPlayerNumber=1):
        super().__init__(attackGroup)
        self.image = getImage(spriteFolder, "wave_1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (16, 32))
        self.coordinates = (0, 0)
        self.direction = direction
        self.firingPlayerNumber = firingPlayerNumber
        self.frameCount = 0

    def setInitialCoordinates(self, x, y):
        if self.direction == Directions.UP:
            self.setCoordinates(x, y - 20)
        elif self.direction == Directions.DOWN:
            self.setCoordinates(x, y + 20)
        elif self.direction == Directions.LEFT:
            self.setCoordinates(x - 20, y)
        elif self.direction == Directions.RIGHT:
            self.setCoordinates(x + 20, y)

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y
        if self.isFacingHorizontally():
            self.collisionRect = pygame.rect.Rect((x + 9, y + 1), (16, 32))
        else:
            self.collisionRect = pygame.rect.Rect((x + 1, y + 9), (32, 16))

    def isFacingHorizontally(self):
        return self.direction in [Directions.RIGHT, Directions.LEFT]

    def rotateImage(self):
        if self.direction in SonicWaveSprite.directionList:
            rotationDegrees = 90 * SonicWaveSprite.directionList.index(self.direction)
            self.image = pygame.transform.rotate(self.image, rotationDegrees)

    def update(self):
        self.frameCount += 1
        if self.direction == Directions.UP:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - 6)
        elif self.direction == Directions.DOWN:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + 6)
        elif self.direction == Directions.LEFT:
            self.setCoordinates(self.coordinates[0] - 6, self.coordinates[1])
        elif self.direction == Directions.RIGHT:
            self.setCoordinates(self.coordinates[0] + 6, self.coordinates[1])
        if self.rect.right < 0:
            self.setCoordinates(512, self.coordinates[1])
        elif self.rect.left > 512:
            self.setCoordinates(-34, self.coordinates[1])

        if self.frameCount % 2 == 1:
            self.image = getImage(spriteFolder, "wave_1.png")
        else:
            self.image = getImage(spriteFolder, "wave_2.png")

        if self.frameCount == 32:
            self.kill()
        self.rotateImage()
        self.image.set_colorkey(BLACK)


class BlackHoleSprite(pygame.sprite.Sprite):
    maxEnemies, initialEnemies = 2, 0
    blackHoleToSpawnList = []
    blackHoleToSpawn = None
    spawnedInitialEnemies = False
    onCooldown = False

    def __init__(self):
        super().__init__(blackHoleGroup)
        spriteSheet = SpriteSheet("hole.png")
        self.animationFrames = []
        self.coordinates = (0, 0)
        self.animationCount = self.frameCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 34, 34))
        self.image = self.animationFrames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def initialize(self, x, y):
        self.setCoordinates(x, y)
        BlackHoleSprite.blackHoleToSpawnList.append(self)
        BlackHoleSprite.spawnedInitialEnemies = False
        if BlackHoleSprite.blackHoleToSpawn is None:
            BlackHoleSprite.blackHoleToSpawn = BlackHoleSprite.blackHoleToSpawnList[0]

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y

    def update(self):
        self.frameCount += 1
        if len(enemyGroup) < BlackHoleSprite.maxEnemies and not BlackHoleSprite.onCooldown and\
                        BlackHoleSprite.blackHoleToSpawn == self:
            self.spawnEnemy()
        if BlackHoleSprite.onCooldown and self.frameCount % 216 == 0 and BlackHoleSprite.blackHoleToSpawn == self:
            BlackHoleSprite.onCooldown = False
            BlackHoleSprite.chooseNextBlackHoleToSpawn()
            self.frameCount = 0
        if self.frameCount % 6 == 0:
            self.animationCount += 1
            if self.animationCount >= len(self.animationFrames):
                self.animationCount = 0
            self.image = self.animationFrames[self.animationCount]
        if self.frameCount % 450 == 0:
            self.frameCount = 0
        self.image.set_colorkey(BLACK)

    def spawnEnemy(self):
        if (not BlackHoleSprite.spawnedInitialEnemies and self.frameCount % 36 == 0) or \
                (BlackHoleSprite.spawnedInitialEnemies and self.frameCount % 450 == 0):
            newUrchin = UrchinSprite()
            newUrchin.setCoordinates(self.coordinates[0], self.coordinates[1])
            newUrchin.setRandomDirection()
            self.frameCount = 1
            BlackHoleSprite.onCooldown = True
            if not BlackHoleSprite.spawnedInitialEnemies:
                BlackHoleSprite.initialEnemies += 1
            if BlackHoleSprite.initialEnemies == BlackHoleSprite.maxEnemies:
                BlackHoleSprite.spawnedInitialEnemies = True

    @classmethod
    def chooseNextBlackHoleToSpawn(cls):
        if cls.blackHoleToSpawn == cls.blackHoleToSpawnList[-1]:
            cls.blackHoleToSpawn = cls.blackHoleToSpawnList[0]
        else:
            currentSpawnIndex = cls.blackHoleToSpawnList.index(cls.blackHoleToSpawn)
            cls.blackHoleToSpawn = cls.blackHoleToSpawnList[currentSpawnIndex + 1]


class UrchinSprite(pygame.sprite.Sprite):
    movementSpeed = 2

    def __init__(self):
        super().__init__(enemyGroup)
        spriteSheet = SpriteSheet("urchin.png")
        self.coordinates = (0, 0)
        self.enemyState = EnemyState.SMALL_BALL
        self.color = BLUE
        self.facingDirection = Directions.RIGHT
        self.bouncingOff = self.running = False
        self.animationCount = self.frameCount = self.delayCount = 0

        self.imageDict = {BLUE: {}, YELLOW: {}}
        self.imageDictKeys = ["horizontal", "vertical", "ball"]
        xValue = 0
        for key in self.imageDictKeys:
            stripImages = spriteSheet.getStripImages(0, xValue, 34, 34)
            self.imageDict[BLUE][key] = [stripImages[0], stripImages[1]]
            self.imageDict[YELLOW][key] = [stripImages[2], stripImages[3]]
            xValue += 34
        self.imageDict[BLUE]["death"] = self.imageDict[YELLOW]["death"] = spriteSheet.getStripImages(0, 102, 34, 34)
        self.emptyImage = spriteSheet.getSheetImage(0, 136, 34, 34)

        self.image = self.emptyImage
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (18, 18))

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y
        self.collisionRect = pygame.rect.Rect((x + 8, y + 8), (18, 18))

    def isFacingHorizontally(self):
        return self.facingDirection in [Directions.RIGHT, Directions.LEFT]

    def flipImage(self):
        if self.facingDirection == Directions.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.facingDirection == Directions.UP:
            self.image = pygame.transform.flip(self.image, False, True)

    def changeImage(self, imageKey, imageIndex):
        if imageKey == "move":
            if self.isFacingHorizontally():
                imageKey = "horizontal"
            else:
                imageKey = "vertical"
        self.image = self.imageDict[self.color][imageKey][imageIndex]
        # if self.enemyState == EnemyState.MOVING:
        #     if self.frameCount % 16 < 9:
        #         pass
        # else:
        #     if self.enemyState == EnemyState.BALL or (self.frameCount % 8 < 5 and
        #                                               self.enemyState != EnemyState.SMALL_BALL):
        #         imageIndex = 0
        #     else:
        #         imageIndex = 1

    def update(self):
        self.checkSonicWaveCollision()
        self.checkOtherUrchinCollision()
        self.frameCount += 1

        if self.enemyState == EnemyState.SMALL_BALL:
            if self.color == BLUE and self.frameCount % 5 == 0:
                if self.animationCount < 8:
                    self.changeImage("ball", 0)
                    self.enemyState = EnemyState.BALL
                    self.frameCount = 0
                    self.animationCount += 1
                else:
                    self.changeImage("move", 0)
                    self.enemyState = EnemyState.MOVING
                    self.frameCount = self.animationCount = 0
            elif self.color == YELLOW:
                if self.animationCount == 84:
                    self.color = BLUE
                    self.animationCount = 0
                    self.frameCount = 33
                if (self.frameCount > 32 or self.animationCount > 0) and self.frameCount % 5 == 0:
                    self.changeImage("ball", 0)
                    self.enemyState = EnemyState.BALL
                    self.frameCount = 0
                    self.animationCount += 1
        elif self.enemyState == EnemyState.BALL:
            if self.color == BLUE and self.frameCount % 3 == 0:
                self.changeImage("ball", 1)
                self.enemyState = EnemyState.SMALL_BALL
                self.frameCount = 0
            elif self.color == YELLOW:
                if self.animationCount == 84:
                    self.color = BLUE
                    self.animationCount = 0
                    self.frameCount = 33
                if (self.frameCount > 32 or self.animationCount > 0) and self.frameCount % 3 == 0:
                    self.changeImage("ball", 1)
                    self.enemyState = EnemyState.SMALL_BALL
                    self.frameCount = 0
                    self.animationCount += 1
        elif self.enemyState == EnemyState.MOVING:
            if self.color == BLUE:
                if self.rect.center[0] % 48 == 16 and self.rect.center[1] % 48 == 18:
                    self.running = False
                    self.getRandomMoveAction()
                self.moveAnimation()
                if self.frameCount % 2 == 0:
                    self.moveSprite()
                if self.frameCount % 80 == 0:
                    self.frameCount = 0
            elif self.frameCount > 32:
                self.changeImage("ball", 0)
                self.enemyState = EnemyState.BALL
                self.animationCount = 8
        elif self.enemyState == EnemyState.WAITING:
            self.moveAnimation()
            self.moveSprite()
        elif self.enemyState == EnemyState.EXPLODING:
            if self.frameCount % 30 > 24:
                self.image = self.emptyImage
            else:
                if 0 < self.frameCount % 30 < 10:
                    key = "ball"
                    index = (self.frameCount % 30) // 5
                else:
                    key = "death"
                    if self.frameCount % 30 == 0:
                        self.enemyState = EnemyState.OFF_SCREEN
                        self.offsetPointsCoordinates(self.facingDirection)
                        self.facingDirection = Directions.RIGHT
                        index = 3
                        self.frameCount = 0
                    else:
                        index = (self.frameCount % 30 - 10) // 5
                self.changeImage(key, index)
        elif self.enemyState == EnemyState.OFF_SCREEN:
            if self.frameCount % 32 == 0:
                self.enemyState = EnemyState.DEAD
                self.image = self.emptyImage
                BlackHoleSprite.blackHoleToSpawn.frameCount = 0
                self.kill()
        self.flipImage()
        self.image.set_colorkey(BLACK)

    def getRandomMoveAction(self):
        randomValue = random.randint(0, 40)
        if randomValue < 2:
            self.frameCount = 0
            self.delayCount = random.randint(0, 5)
            self.enemyState = EnemyState.WAITING
        elif randomValue < 10:
            self.setRandomDirection()
        elif randomValue > 38:
            self.running = True

    def moveSprite(self, moveVal=0):
        if moveVal == 0:
            moveVal = UrchinSprite.movementSpeed
            if self.running:
                moveVal *= 2
        if self.enemyState == EnemyState.WAITING:
            if self.frameCount % 20 == 0:
                if self.delayCount < 3:
                    self.delayCount += 1
                else:
                    self.setRandomDirection()
                    self.enemyState = EnemyState.MOVING
        elif not self.enemyState == EnemyState.MOVING or self.frameCount % 2 == 0:
            if self.facingDirection == Directions.UP:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - moveVal)
            elif self.facingDirection == Directions.DOWN:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + moveVal)
            elif self.facingDirection == Directions.LEFT:
                self.setCoordinates(self.coordinates[0] - moveVal, self.coordinates[1])
            elif self.facingDirection == Directions.RIGHT:
                self.setCoordinates(self.coordinates[0] + moveVal, self.coordinates[1])
            if self.color == BLUE:
                if any(self.rect.colliderect(levelRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects) \
                        or any(self.collisionRect.colliderect(gold.collisionRect) for gold in goldGroup if
                               gold.goldState != OtherState.OFF_SCREEN) \
                        or any(self.collisionRect.colliderect(rubberTrap.collisionRect) for rubberTrap in rubberGroup
                               if rubberTrap.trapState != OtherState.OFF_SCREEN):
                    self.bouncingOff = True
                    self.changeDirection()
        if self.bouncingOff:
            otherUrchins = [enemy for enemy in enemyGroup if
                            (enemy != self and enemy.enemyState not in [EnemyState.OFF_SCREEN, EnemyState.DEAD])]
            if not any(self.rect.colliderect(enemy) for enemy in otherUrchins) and\
                    not any(self.rect.colliderect(levelRect) for levelRect in
                            PlayerSprite.currentLevel.levelBorderRects) and\
                    not any(self.collisionRect.colliderect(gold.collisionRect) for gold in goldGroup if
                            gold.goldState != OtherState.OFF_SCREEN) and\
                    not any(self.collisionRect.colliderect(rubberTrap.collisionRect) for rubberTrap in rubberGroup
                            if rubberTrap.trapState != OtherState.OFF_SCREEN):
                self.bouncingOff = False

    def moveAnimation(self):
        if self.frameCount % 16 < 9:
            self.changeImage("move", 1)
        else:
            self.changeImage("move", 0)

    def changeDirection(self):
        if self.facingDirection == Directions.UP:
            self.facingDirection = Directions.DOWN
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + UrchinSprite.movementSpeed)
        elif self.facingDirection == Directions.DOWN:
            self.facingDirection = Directions.UP
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - UrchinSprite.movementSpeed)
        elif self.facingDirection == Directions.LEFT:
            self.facingDirection = Directions.RIGHT
            self.setCoordinates(self.coordinates[0] + UrchinSprite.movementSpeed, self.coordinates[1])
        elif self.facingDirection == Directions.RIGHT:
            self.facingDirection = Directions.LEFT
            self.setCoordinates(self.coordinates[0] - UrchinSprite.movementSpeed, self.coordinates[1])

    def checkSonicWaveCollision(self):
        if self.enemyState not in [EnemyState.EXPLODING, EnemyState.OFF_SCREEN, EnemyState.DEAD]:
            if any(wave.rect.collidepoint(self.rect.center) for wave in attackGroup):
                playSound("push_enemy.wav")
                self.color = YELLOW
                if self.enemyState == EnemyState.BALL:
                    key = "ball"
                    index = 1
                elif self.enemyState == EnemyState.SMALL_BALL:
                    key = "ball"
                    index = 0
                else:
                    key = "move"
                    index = 0
                self.changeImage(key, index)
                self.frameCount = self.animationCount = 0

    def checkOtherUrchinCollision(self):
        if self.enemyState == EnemyState.MOVING:
            otherUrchins = [enemy for enemy in enemyGroup if (enemy != self and
                            enemy.enemyState not in [EnemyState.OFF_SCREEN, EnemyState.DEAD])]
            if any(self.rect.colliderect(enemy) for enemy in otherUrchins):
                self.frameCount = 0
                if not self.bouncingOff:
                    self.changeDirection()
                    self.bouncingOff = True
                self.moveSprite()

    def push(self, pushingPlayer):
        self.animationCount = 0
        # if not pygame.mixer.Channel(1).get_busy():
        #     pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(musicFolder, "push_enemy.wav")))
        playSound("push_enemy.wav")
        if any(levelRect.colliderect(self.collisionRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects):
            playSound("crush_enemy.wav")
            self.enemyState = EnemyState.EXPLODING
            self.frameCount = 0
            self.changeImage("death", 0)
            pushingPlayer.killedUrchinCount += 1
        else:
            if self.isFacingHorizontally() == pushingPlayer.isFacingHorizontally():
                self.facingDirection = pushingPlayer.facingDirection
                if self.facingDirection == Directions.UP:
                    self.rect.bottom = pushingPlayer.rect.top
                elif self.facingDirection == Directions.DOWN:
                    self.rect.top = pushingPlayer.rect.bottom
                elif self.facingDirection == Directions.LEFT:
                    self.rect.right = pushingPlayer.rect.left
                else:
                    self.rect.left = pushingPlayer.rect.right
                print(self.rect, pushingPlayer.rect)
            self.moveSprite(PlayerSprite.movementSpeed)

    def offsetPointsCoordinates(self, offsetDirection):
        if offsetDirection == Directions.UP:
            self.setCoordinates(self.coordinates[0] - 2, self.coordinates[1] + 20)
        elif offsetDirection == Directions.DOWN:
            self.setCoordinates(self.coordinates[0] - 2, self.coordinates[1] - 20)
        elif offsetDirection == Directions.LEFT:
            self.setCoordinates(self.coordinates[0] + 18, self.coordinates[1])
        else:
            self.setCoordinates(self.coordinates[0] - 22, self.coordinates[1])

    def setRandomDirection(self):
        self.facingDirection = random.choice([Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT])


class GoldSprite(pygame.sprite.Sprite):
    levelCount = 0
    globalFrameCount = 0

    def __init__(self):
        super().__init__(goldGroup)
        if isinstance(PlayerSprite.currentLevel, BonusLevel):
            spriteSheet = SpriteSheet("gold_bonus.png")
        else:
            spriteSheet = SpriteSheet("gold.png")
        self.animationFrames = []

        self.coordinates = (0, 0)
        self.goldState = OtherState.OFF_SCREEN
        self.passingDirection = Directions.RIGHT
        self.isHorizontal = self.alreadyRevealed = False
        self.animationPosition = self.frameCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 34, 34))
        self.animationFrames.extend(spriteSheet.getStripImages(0, 34, 34, 34))
        self.flashImage = spriteSheet.getSheetImage(0, 68, 34, 34)
        self.pointsImage = spriteSheet.getSheetImage(34, 68, 34, 34)
        self.emptyImage = spriteSheet.getSheetImage(34, 102, 34, 34)

        self.image = self.emptyImage
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (16, 32))

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y
        if self.isHorizontal:
            self.collisionRect = pygame.rect.Rect((x + 1, y + 9), (32, 16))
        else:
            self.collisionRect = pygame.rect.Rect((x + 9, y + 1), (16, 32))

    def rotateImage(self):
        if self.isHorizontal:
            self.image = pygame.transform.rotate(self.image, 270)
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.frameCount += 1
        if self.goldState == OtherState.REVEALED:
            if GoldSprite.globalFrameCount % 12 < 6:
                self.image = self.animationFrames[3]
            else:
                self.image = self.flashImage
            self.animationPosition = 3
        elif self.goldState == OtherState.UPSIDE_DOWN:
            self.image = self.animationFrames[7]
            self.animationPosition = 7
        elif self.goldState == OtherState.FLIPPING_UP:
            self.flipUp()
        elif self.goldState == OtherState.FLIPPING_DOWN:
            self.flipDown()
        elif self.goldState == OtherState.OFF_SCREEN:
            self.image = self.emptyImage
        if self.frameCount % 48 == 0:
            self.frameCount = 0
        if GoldSprite.globalFrameCount % 12 == 0:
            GoldSprite.globalFrameCount = 0
        self.rotateImage()
        self.image.set_colorkey(BLACK)

    def startFlipAnimation(self):
        self.frameCount = 0
        playSound("pass_over_gold.wav")
        if self.goldState == OtherState.REVEALED and GoldSprite.levelCount > 22 and not\
                isinstance(PlayerSprite.currentLevel, BonusLevel):
            self.goldState = OtherState.FLIPPING_DOWN
        elif self.goldState in [OtherState.UPSIDE_DOWN, OtherState.OFF_SCREEN, OtherState.REVEALED]:
            if self.alreadyRevealed:
                self.frameCount = 12
            self.goldState = OtherState.FLIPPING_UP

    def flipUp(self):
        if self.frameCount % 3 == 0:
            if self.passingDirection in [Directions.DOWN, Directions.LEFT]:
                if self.animationPosition == 0:
                    self.animationPosition = 7
                else:
                    self.animationPosition -= 1
            else:
                if self.animationPosition == 7:
                    self.animationPosition = 0
                else:
                    self.animationPosition += 1
        self.image = self.animationFrames[self.animationPosition]
        if self.frameCount % 36 == 0:
            self.goldState = OtherState.REVEALED
            if not self.alreadyRevealed:
                points100 = PointsSprite(self.pointsImage, self.emptyImage, self.passingDirection)
                positionOffset = 10
                if self.passingDirection in [Directions.UP, Directions.LEFT]:
                    positionOffset = -10
                if self.isHorizontal:
                    points100.coordinates = (self.coordinates[0], self.coordinates[1] + positionOffset)
                    points100.isHorizontal = True
                else:
                    points100.coordinates = (self.coordinates[0] + positionOffset, self.coordinates[1])
                self.alreadyRevealed = True
            self.frameCount = 0

    def flipDown(self):
        if self.frameCount % 3 == 0:
            if self.animationPosition == 7:
                self.animationPosition = 0
            else:
                self.animationPosition += 1
        self.image = self.animationFrames[self.animationPosition]
        if self.frameCount > 36:
            self.goldState = OtherState.UPSIDE_DOWN
            self.frameCount = 0

            if self.passingDirection in [Directions.DOWN, Directions.LEFT]:
                if self.animationPosition == 0:
                    self.animationPosition = 7
                else:
                    self.animationPosition -= 1
            else:
                if self.animationPosition == 7:
                    self.animationPosition = 0
                else:
                    self.animationPosition += 1
        self.image = self.animationFrames[self.animationPosition]


class RubberTrapSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(rubberGroup)
        spriteSheet = SpriteSheet("trap.png")
        self.animationFrames = []

        self.coordinates = (0, 0)
        self.trapState = OtherState.OFF_SCREEN
        self.collidingPlayer = None
        self.isHorizontal = self.flipTrigger = False
        self.frameCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 60, 56, 4, key=RED))
        self.emptyImage = spriteSheet.getSheetImage(0, 240, 60, 56, key=RED)

        self.image = self.emptyImage
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (16, 32))

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y
        horizontalOffsets = (6, 44)
        verticalOffsets = (24, 8)
        if self.isHorizontal:
            self.collisionRect = pygame.rect.Rect((x + horizontalOffsets[0], y + verticalOffsets[0]),
                                                  (horizontalOffsets[1], verticalOffsets[1]))
        else:
            self.collisionRect = pygame.rect.Rect((x + verticalOffsets[0], y + horizontalOffsets[0]),
                                                  (verticalOffsets[1], horizontalOffsets[1]))

    def rotateImage(self):
        if not self.isHorizontal:
            self.image = pygame.transform.rotate(self.image, 90)

    def flipImage(self):
        self.image = pygame.transform.flip(self.image, False, True)

    def update(self):
        if self.trapState == OtherState.REVEALED:
            self.image = self.animationFrames[0]
        elif self.trapState == OtherState.TRIGGERED:
            self.animateTrap()
        else:
            self.image = self.emptyImage
        self.checkPlayerCollision()
        self.rotateImage()
        self.image.set_colorkey(BLACK)

    def checkPlayerCollision(self):
        if self.trapState != OtherState.TRIGGERED:
            for player in playerGroup:
                if self.collisionRect.colliderect(player.collisionRect) and player.playerState == PlayerStates.MOVING:
                    if self.trapState == OtherState.OFF_SCREEN:
                        playSound("bounce_rubber_or_player.wav")
                    else:
                        playSound("bounce_wall.wav")
                    self.collidingPlayer = player
                    self.trapState = OtherState.TRIGGERED
                    if self.collidingPlayer.facingDirection == Directions.LEFT or \
                            self.collidingPlayer.facingDirection == Directions.UP:
                        self.flipTrigger = True
                    else:
                        self.flipTrigger = False

    def animateTrap(self):
        self.frameCount += 1
        animationIndex = self.getTrapAnimationStep()
        self.image = self.animationFrames[animationIndex]
        if self.flipTrigger:
            self.flipImage()
        if 18 < self.frameCount < 30:
            self.flipImage()
        if self.frameCount == 8:
            self.collidingPlayer.rebound()
        if self.frameCount % 33 == 0:
            self.frameCount = 0
            self.trapState = OtherState.REVEALED

    def getTrapAnimationStep(self):
        if self.frameCount % 33 // 3 in (0, 4, 6, 8, 10):
            return 1
        elif self.frameCount % 33 // 3 in (1, 3, 7):
            return 2
        elif self.frameCount % 33 // 3 == 2:
            return 3
        else:
            return 0


class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(itemGroup)
        super().__init__(rubberGroup)
        spriteSheet = SpriteSheet("item.png")
        self.animationFrames = []

        self.coordinates = (0, 0)
        self.itemState = OtherState.OFF_SCREEN
        self.frameCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 34, 34))
        self.imageDictKeys = ["apple", "banana", "cherry", "eggplant", "melon", "pineapple", "strawberry",
                              "bag", "clock", "flag", "glasses", "explosion_1", "explosion_2", "empty"]
        self.imageDict = dict(zip(self.imageDictKeys, self.animationFrames))

        self.image = self.imageDict["empty"]
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (18, 28))

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y
        self.collisionRect.topleft = x + 8, y + 4

    def update(self):
        if self.itemState == OtherState.REVEALED:
            pass
        else:
            self.image = self.imageDict["empty"]
        self.checkPlayerCollision()
        self.image.set_colorkey(BLACK)

    def checkPlayerCollision(self):
        # if any(self.rect.collidepoint(player.rect.center) for player in playerGroup) and \
        #                 self.trapState != OtherState.TRIGGERED:
        #     self.collidingPlayer = pygame.sprite.spritecollide(self, playerGroup, False)[0]
        #     self.trapState = OtherState.TRIGGERED
        #     if self.collidingPlayer.facingDirection == Directions.RIGHT or \
        #                     self.collidingPlayer.facingDirection == Directions.UP:
        #         self.flipTrigger = True
        #     else:
        #         self.flipTrigger = False
        #     playSound("item_appears_or_collected.wav")
        pass

    def collectItem(self):
        self.frameCount += 1
        if self.frameCount % 24 < 9:
            self.image = getImage(spriteFolder, "item_collected_1.png")
        else:
            self.image = getImage(spriteFolder, "item_collected_2.png")
        if self.frameCount % 24 == 0:
            self.itemState = OtherState.OFF_SCREEN
            self.frameCount = 0


class PointsSprite(pygame.sprite.Sprite):
    def __init__(self, pointsImage, emptyImage, passingDirection=Directions.RIGHT):
        super().__init__(itemGroup)
        self.emptyImage = emptyImage
        self.image = pointsImage
        self.image.set_colorkey(BLACK)
        self.coordinates = (0, 0)
        self.passingDirection = passingDirection
        self.isHorizontal = False
        self.frameCount = 0

    def update(self):
        self.frameCount += 1
        positionOffset = 2
        if self.passingDirection in [Directions.UP, Directions.LEFT]:
            positionOffset = -2
        if self.frameCount < 7:
            if self.isHorizontal:
                self.coordinates = (self.coordinates[0], self.coordinates[1] + positionOffset)
            else:
                self.coordinates = (self.coordinates[0] + positionOffset, self.coordinates[1])
        if self.frameCount == 40:
            self.kill()
            self.image = self.emptyImage


class GameOverTextSprite(pygame.sprite.Sprite):
    def __init__(self, playerNumber=1):
        super().__init__(textGroup)
        self.image = getImage(spriteFolder, "game_over_text.png")
        self.image.set_colorkey(BLACK)
        self.coordinates = (20, 478)
        self.playerNumber = playerNumber

    def initialize(self):
        if self.playerNumber == 1:
            self.coordinates = (20, 478)
        else:
            self.coordinates = (430, 478)

    def update(self):
        if self.coordinates[1] > 38:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 4)
