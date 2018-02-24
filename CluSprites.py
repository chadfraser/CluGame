import pygame
import os
import random
from enum import Enum
from CluLevels import BonusLevel


"""Spinning: Animating
             Movement
             Moving over black hole
             Sound effect
   Enemies: Pushing sound effect
   Gold: Level complete
   Gameplay: Random item locations
             Random level order
             Spawning items
             Level complete (Tally points, animate, sound effects, bonus)
             Game over screen
   Bonus level differences"""

"""Fix pushing urchin sound effect"""
"""Fix window icon"""

"""Finish player end screen animation"""
"""Adjusting player coordinates"""

"""apple banana  cherry  melon   pineapple
bag      clock   flag
p1turn1 p1turn2
p2turn1 p2turn2
pts800   pts1500
count_points    earn_bonus  grab_post_move_end"""

"""Collect clock: Change color of ..."""


SCREEN_SIZE = (512, 448)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
gameFolder = os.path.dirname(__file__)
spriteFolder = os.path.join(gameFolder, "Sprites")
backgroundFolder = os.path.join(gameFolder, "Backgrounds")
titleFolder = os.path.join(gameFolder, "Titles")
musicFolder = os.path.join(gameFolder, "Music")

_imageLibrary = {}
_soundLibrary = {}


def getImage(folder, imagePath):
    global _imageLibrary
    image = _imageLibrary.get(imagePath)
    if image is None:
        fullPath = os.path.join(folder, imagePath)
        image = pygame.image.load(fullPath).convert()
        _imageLibrary[imagePath] = image
    return image


def playSound(soundPath):
    global _soundLibrary
    sound = _soundLibrary.get(soundPath)
    if sound is None:
        fullPath = os.path.join(musicFolder, soundPath)
        sound = pygame.mixer.Sound(fullPath)
        _soundLibrary[soundPath] = sound
    sound.play()


listOfTitleSprites = ["title_01.png", "title_02.png", "title_03.png", "title_04.png", "title_05.png", "title_06.png",
                      "title_07.png", "title_08.png", "title_09.png", "title_10.png", "title_11.png", "title_12.png",
                      "title_13.png"]
listOfBlackHoleSprites = ["hole_1.png", "hole_2.png", "hole_3.png", "hole_4.png"]
listOfGoldAnimationSprites = ["gold_flash.png", "gold_flip_1.png", "gold_flip_2.png", "gold_flip_3.png",
                              "gold_flip_4.png", "gold_flip_5.png", "gold_flip_6.png", "gold_flip_7.png",
                              "gold_flip_8.png"]
listOfBonusGoldAnimationSprites = ["gold_blue_flash.png", "gold_blue_flip_1.png", "gold_blue_flip_2.png",
                                   "gold_blue_flip_3.png", "gold_blue_flip_4.png", "gold_blue_flip_5.png",
                                   "gold_blue_flip_6.png", "gold_blue_flip_7.png", "gold_blue_flip_8.png"]

player1SpriteDict = {"ball 1": getImage(spriteFolder, "p1_ball_1.png"),
                     "ball 2": getImage(spriteFolder, "p1_ball_2.png"),
                     "arm 1": getImage(spriteFolder, "p1_arm_extend.png"),
                     "arm 2": getImage(spriteFolder, "p1_arm_rotate_1.png"),
                     "arm 3": getImage(spriteFolder, "p1_arm_rotate_2.png"),
                     "death 1": getImage(spriteFolder, "p1_death_1.png"),
                     "death 2": getImage(spriteFolder, "p1_death_2.png"),
                     "death 3": getImage(spriteFolder, "p1_death_3.png"),
                     "death 4": getImage(spriteFolder, "p1_death_4.png"),
                     "fall 1": getImage(spriteFolder, "p1_fall_1.png"),
                     "fall 2": getImage(spriteFolder, "p1_fall_2.png"),
                     "fall 3": getImage(spriteFolder, "p1_fall_3.png"),
                     "fall 4": getImage(spriteFolder, "p1_fall_4.png"),
                     "end screen 1": getImage(spriteFolder, "p1_end_1.png"),
                     "end screen 2": getImage(spriteFolder, "p1_end_2.png"),
                     "move 1": getImage(spriteFolder, "p1_move_1.png"),
                     "move 2": getImage(spriteFolder, "p1_move_2.png"),
                     "move vertical 1": getImage(spriteFolder, "p1_move_3.png"),
                     "move vertical 2": getImage(spriteFolder, "p1_move_4.png"),
                     "flash 1": getImage(spriteFolder, "p1_move_flash_1.png"),
                     "flash 2": getImage(spriteFolder, "p1_move_flash_2.png"),
                     "flash vertical 1": getImage(spriteFolder, "p1_move_flash_3.png"),
                     "flash vertical 2": getImage(spriteFolder, "p1_move_flash_4.png"),
                     "turn 1": getImage(spriteFolder, "p1_turn_1.png"),
                     "turn 2": getImage(spriteFolder, "p1_turn_2.png"),
                     "squish 1": getImage(spriteFolder, "p1_squish_1.png"),
                     "squish 2": getImage(spriteFolder, "p1_squish_2.png"),
                     "squish 3": getImage(spriteFolder, "p1_squish_3.png"),
                     "squish vertical 1": getImage(spriteFolder, "p1_squish_4.png"),
                     "squish vertical 2": getImage(spriteFolder, "p1_squish_5.png"),
                     "squish vertical 3": getImage(spriteFolder, "p1_squish_6.png")
                     }
player2SpriteDict = {"ball 1": getImage(spriteFolder, "p2_ball_1.png"),
                     "ball 2": getImage(spriteFolder, "p2_ball_2.png"),
                     "arm 1": getImage(spriteFolder, "p2_arm_extend.png"),
                     "arm 2": getImage(spriteFolder, "p2_arm_rotate_1.png"),
                     "arm 3": getImage(spriteFolder, "p2_arm_rotate_2.png"),
                     "death 1": getImage(spriteFolder, "p2_death_1.png"),
                     "death 2": getImage(spriteFolder, "p2_death_2.png"),
                     "death 3": getImage(spriteFolder, "p2_death_3.png"),
                     "death 4": getImage(spriteFolder, "p2_death_4.png"),
                     "fall 1": getImage(spriteFolder, "p2_fall_1.png"),
                     "fall 2": getImage(spriteFolder, "p2_fall_2.png"),
                     "fall 3": getImage(spriteFolder, "p2_fall_3.png"),
                     "fall 4": getImage(spriteFolder, "p2_fall_4.png"),
                     "end screen 1": getImage(spriteFolder, "p2_end_1.png"),
                     "end screen 2": getImage(spriteFolder, "p2_end_2.png"),
                     "move 1": getImage(spriteFolder, "p2_move_1.png"),
                     "move 2": getImage(spriteFolder, "p2_move_2.png"),
                     "move vertical 1": getImage(spriteFolder, "p2_move_3.png"),
                     "move vertical 2": getImage(spriteFolder, "p2_move_4.png"),
                     "flash 1": getImage(spriteFolder, "p2_move_flash_1.png"),
                     "flash 2": getImage(spriteFolder, "p2_move_flash_2.png"),
                     "flash vertical 1": getImage(spriteFolder, "p2_move_flash_3.png"),
                     "flash vertical 2": getImage(spriteFolder, "p2_move_flash_4.png"),
                     "turn 1": getImage(spriteFolder, "p2_turn_1.png"),
                     "turn 2": getImage(spriteFolder, "p2_turn_2.png"),
                     "squish 1": getImage(spriteFolder, "p2_squish_1.png"),
                     "squish 2": getImage(spriteFolder, "p2_squish_2.png"),
                     "squish 3": getImage(spriteFolder, "p2_squish_3.png"),
                     "squish vertical 1": getImage(spriteFolder, "p2_squish_4.png"),
                     "squish vertical 2": getImage(spriteFolder, "p2_squish_5.png"),
                     "squish vertical 3": getImage(spriteFolder, "p2_squish_6.png")
                     }


def getImagesFromList(folder, listPath):
    imageList = []
    for tempPath in listPath:
        image = getImage(folder, tempPath)
        image.set_colorkey(BLACK)
        imageList.append(image)
    return imageList


class PlayerStates(Enum):
    BALL = "ball"
    MOVING = "moving"
    SWINGING = "swinging"
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
    STUNNED = "stunned"
    STUNNED_BALL = "stunned ball"
    STUNNED_SMALL_BALL = "stunned small ball"
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
allGroups = (itemGroup, blackHoleGroup, enemyGroup, goldGroup, armGroup, playerGroup, rubberGroup, attackGroup,
             textGroup)


class TitleSprite(pygame.sprite.Sprite):
    titleSpriteAnimations = getImagesFromList(titleFolder, listOfTitleSprites)

    def __init__(self, imageSource, position="left"):
        super().__init__()
        self.image = getImage(titleFolder, imageSource)
        self.image.set_colorkey(BLACK)
        self.position = position
        self.rotationCount = 0
        self.frameCount = 0

    def update(self):
        self.frameCount += 1
        if self.position == "left":
            if (20 < self.frameCount < 132 and self.frameCount % 2 == 1) or 289 < self.frameCount < 394:
                self.rotateAnimationLeft()
        elif self.position == "right":
            if (150 < self.frameCount < 272 and self.frameCount % 2 == 1) or 289 < self.frameCount < 394:
                self.rotateAnimationRight()

    def rotateAnimationLeft(self):
        self.rotationCount += 1
        if self.rotationCount < len(self.titleSpriteAnimations):
            self.image = self.titleSpriteAnimations[self.rotationCount]
        else:
            self.rotationCount = 0
            self.image = self.titleSpriteAnimations[0]

    def rotateAnimationRight(self):
        self.rotationCount += 1
        if self.rotationCount < len(self.titleSpriteAnimations):
            self.image = self.titleSpriteAnimations[-self.rotationCount]
        else:
            self.rotationCount = 0
            self.image = self.titleSpriteAnimations[-1]

    def setTitleImage(self):
        self.image = getImage(titleFolder, "title_05.png")
        self.image.set_colorkey(BLACK)

    def setTitleImageBackwards(self):
        self.image = getImage(titleFolder, "title_01.png")
        self.frameCount = 0
        self.rotationCount = 0
        self.image.set_colorkey(BLACK)


class PlayerSprite(pygame.sprite.Sprite):
    directionList = [Directions.RIGHT, Directions.UP, Directions.LEFT, Directions.DOWN]
    playerSpriteAnimations = player1SpriteDict
    currentLevel = None
    movementSpeed = 2

    def __init__(self, playerNumber=1):
        super().__init__(playerGroup)
        self.playerNumber = playerNumber
        self.lives = 5
        self.image = getImage(spriteFolder, "p1_ball_1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (14, 24))
        self.baseCoordinates = (0, 0)
        self.coordinates = (0, 0)
        self.playerState = PlayerStates.OFF_SCREEN
        self.facingDirection = Directions.RIGHT
        self.armDirection = Directions.RIGHT
        self.bouncingOff = False
        self.frameCount = 0

    def flipImage(self):
        if self.facingDirection == Directions.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.facingDirection == Directions.UP:
            self.image = pygame.transform.flip(self.image, False, True)

    def rotateImage(self):
        if self.facingDirection in PlayerSprite.directionList:
            rotationDegrees = 90 * PlayerSprite.directionList.index(self.facingDirection)
            self.image = pygame.transform.rotate(self.image, rotationDegrees)
            self.flipImage()

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y
        if self.isFacingHorizontally():
            self.collisionRect = pygame.rect.Rect((x + 10, y + 5), (14, 24))
        else:
            self.collisionRect = pygame.rect.Rect((x + 6, y + 10), (20, 20))

    def initialize(self, x, y):
        self.baseCoordinates = (x, y)
        self.setCoordinates(x, y)
        if self.playerNumber == 2:
            self.playerSpriteAnimations = player2SpriteDict
        if not self.playerState == PlayerStates.DEAD:
            self.putSpriteInBall()

    def isFacingHorizontally(self):
        return self.facingDirection in [Directions.RIGHT, Directions.LEFT]

    def putSpriteInBall(self):
        self.facingDirection = Directions.RIGHT
        self.playerState = PlayerStates.BALL
        self.image = self.playerSpriteAnimations["ball 1"]
        self.lives = max(0, self.lives - 1)
        self.frameCount = 0

    def update(self):
        # print(self.playerState, self.coordinates, self.coordinates[0] % 48, self.coordinates[1] % 48,
        #       self.facingDirection, self.frameCount % 88)
        self.checkEnemyCollision()
        self.checkBlackHoleCollision()
        self.checkOtherPlayerCollision()
        self.frameCount += 1

        if self.playerState == PlayerStates.BALL:
            if self.frameCount % 16 < 9:
                self.image = self.playerSpriteAnimations["ball 2"]
            else:
                self.image = self.playerSpriteAnimations["ball 1"]
            if self.frameCount % 16 == 0:
                self.frameCount = 0
        elif self.playerState == PlayerStates.MOVING:
            self.moveSprite()
            self.moveAnimation()
            if self.frameCount % 8 == 0:
                self.frameCount = 0
        elif self.playerState == PlayerStates.HITTING_WALL:
            if self.frameCount % 9 == 3:
                if self.isFacingHorizontally():
                    self.image = self.playerSpriteAnimations["squish 2"]
                else:
                    self.image = self.playerSpriteAnimations["squish vertical 2"]
            elif self.frameCount % 8 < 3:
                if self.isFacingHorizontally():
                    self.image = self.playerSpriteAnimations["squish 3"]
                else:
                    self.image = self.playerSpriteAnimations["squish vertical 3"]
            if self.frameCount % 8 == 0:
                self.frameCount = 0
                self.rebound()
        elif self.playerState == PlayerStates.FALLING:
            if 7 < self.frameCount % 40 < 17:
                self.image = self.playerSpriteAnimations["fall 2"]
            elif 16 < self.frameCount % 40 < 25:
                self.image = self.playerSpriteAnimations["fall 3"]
            elif 24 < self.frameCount % 40 < 33:
                self.image = self.playerSpriteAnimations["fall 4"]
            if self.frameCount % 40 == 0:
                self.playerState = PlayerStates.OFF_SCREEN
                self.image = getImage(spriteFolder, "empty.png")
                self.frameCount = 0
        elif self.playerState == PlayerStates.EXPLODING:
            if 7 < self.frameCount % 40 < 17:
                self.image = self.playerSpriteAnimations["death 2"]
            elif 16 < self.frameCount % 40 < 25:
                self.image = self.playerSpriteAnimations["death 3"]
            elif 24 < self.frameCount % 40 < 33:
                self.image = self.playerSpriteAnimations["death 4"]
            if self.frameCount % 40 == 0:
                self.playerState = PlayerStates.OFF_SCREEN
                self.image = getImage(spriteFolder, "empty.png")
                self.frameCount = 0
        elif self.playerState == PlayerStates.OFF_SCREEN:
            if self.lives > 0 and self.frameCount % 160 == 0:
                self.setCoordinates(self.baseCoordinates[0], self.baseCoordinates[1])
                self.putSpriteInBall()
                self.frameCount = 0
            elif self.lives == 0:
                self.playerState = PlayerStates.DEAD
        elif self.playerState == PlayerStates.SWINGING:
            self.swing()
        elif self.playerState == PlayerStates.HITTING_PLAYER_MOVING:
            if self.frameCount % 8 < 5:
                if self.isFacingHorizontally():
                    self.image = self.playerSpriteAnimations["flash 1"]
                else:
                    self.image = self.playerSpriteAnimations["flash vertical 1"]
            else:
                if self.isFacingHorizontally():
                    self.image = self.playerSpriteAnimations["flash 2"]
                else:
                    self.image = self.playerSpriteAnimations["flash vertical 2"]
            if self.frameCount % 8 == 0:
                self.moveSprite()
                self.frameCount = 0
                self.playerState = PlayerStates.MOVING
        elif self.playerState == PlayerStates.HITTING_PLAYER_SWINGING:
            # if self.frameCount % 8 < 5:
            #     if self.playerNumber == 1:
            #         if self.isFacingHorizontally():
            #             self.image = getImage(spriteFolder, "p1_move_flash_2.png")
            #         else:
            #             self.image = getImage(spriteFolder, "p1_move_flash_4.png")
            #     else:
            #         if self.isFacingHorizontally():
            #             self.image = getImage(spriteFolder, "p2_move_flash_2.png")
            #         else:
            #             self.image = getImage(spriteFolder, "p2_move_flash_4.png")
            # else:
            #     if self.playerNumber == 1:
            #         if self.isFacingHorizontally():
            #             self.image = getImage(spriteFolder, "p1_move_flash.png")
            #         else:
            #             self.image = getImage(spriteFolder, "p1_move_flash_3.png")
            #     else:
            #         if self.isFacingHorizontally():
            #             self.image = getImage(spriteFolder, "p2_move_flash.png")
            #         else:
            #             self.image = getImage(spriteFolder, "p2_move_flash_3.png")
            if self.frameCount % 8 == 0:
                self.moveSprite()
                self.frameCount = 0
                self.playerState = PlayerStates.SWINGING
        elif self.playerState == PlayerStates.LEVEL_END:
            self.animateLevelEnd()

        if self.bouncingOff:
            otherPlayers = [player for player in playerGroup if (player != self and
                            player.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING,
                                                   PlayerStates.HITTING_PLAYER_MOVING,
                                                   PlayerStates.HITTING_PLAYER_SWINGING])]
            if not any(player.collisionRect.colliderect(self.collisionRect) for player in otherPlayers):
                self.bouncingOff = False
        self.flipImage()
        self.image.set_colorkey(BLACK)

    def startMoving(self, direction):
        if self.playerState == PlayerStates.BALL:
            playSound("move_out_of_ball.wav")
            if direction == "up":
                self.facingDirection = Directions.UP
            elif direction == "down":
                self.facingDirection = Directions.DOWN
            elif direction == "left":
                self.facingDirection = Directions.LEFT
            else:
                self.facingDirection = Directions.RIGHT
            if self.isFacingHorizontally():
                self.image = self.playerSpriteAnimations["move 1"]
            else:
                self.image = self.playerSpriteAnimations["move vertical 1"]
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
                gold.startFlipAnimation()

    def hitWall(self):
        self.frameCount = 0
        playSound("bounce_wall.wav")
        self.playerState = PlayerStates.HITTING_WALL
        if self.isFacingHorizontally():
            self.image = self.playerSpriteAnimations["squish 1"]
        else:
            self.image = self.playerSpriteAnimations["squish vertical 1"]
        self.flipImage()
        self.image.set_colorkey(BLACK)

    def rebound(self):
        self.changeDirection()
        if self.isFacingHorizontally():
            self.image = self.playerSpriteAnimations["move 1"]
        else:
            self.image = self.playerSpriteAnimations["move vertical 1"]
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
        if self.frameCount % 8 < 5:
            if self.isFacingHorizontally():
                self.image = self.playerSpriteAnimations["move 2"]
            else:
                self.image = self.playerSpriteAnimations["move vertical 2"]
        else:
            if self.isFacingHorizontally():
                self.image = self.playerSpriteAnimations["move 1"]
            else:
                self.image = self.playerSpriteAnimations["move vertical 1"]

    def swing(self):
        # print(self.coordinates)
        if self.frameCount % 22 == 0:
            if self.facingDirection == Directions.RIGHT:
                self.facingDirection = Directions.DOWN
            else:
                facingDirectionIndex = PlayerSprite.directionList.index(self.facingDirection)
                self.facingDirection = PlayerSprite.directionList[facingDirectionIndex - 1]

        if self.frameCount % 22 < 11:
            self.moveAnimation()
        else:
            if self.frameCount % 8 < 5:
                self.image = self.playerSpriteAnimations["turn 1"]
            else:
                self.image = self.playerSpriteAnimations["turn 2"]
            self.rotateImage()
        if self.frameCount % 88 == 0:
            self.frameCount = 0
        self.moveSwingSprite()

    def moveSwingSprite(self):
        if self.frameCount in (1, 53, 56, 58, 60, 61, 63, 64, 66, 67, 69, 70, 71, 72, 74, 75, 76, 77, 78, 80, 81, 83,
                               84, 86):
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - 2)
        if self.frameCount in (9, 12, 14, 16, 18, 19, 20, 22, 23, 24, 25, 26, 28, 29, 30, 31, 33, 35, 36, 37, 39, 41,
                               43, 46):
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + 2)
        if self.frameCount in (30, 34, 36, 38, 40, 41, 42, 44, 45, 46, 47, 48, 50, 51, 52, 53, 54, 56, 57, 58, 60, 62,
                               64, 68):
            self.setCoordinates(self.coordinates[0] - 2, self.coordinates[1])
        if self.frameCount in (0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 15, 18, 20, 23, 75, 78, 80, 82, 83, 85, 86, 87):
            self.setCoordinates(self.coordinates[0] + 2, self.coordinates[1])

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
                    self.image = self.playerSpriteAnimations["fall 1"]

    def checkEnemyCollision(self):
        if self.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING]:
            if any(enemy.collisionRect.colliderect(self.collisionRect) and enemy.enemyState == EnemyState.MOVING
                   for enemy in enemyGroup):
                playSound("death.wav")
                self.frameCount = 0
                self.facingDirection = Directions.RIGHT
                self.playerState = PlayerStates.EXPLODING
                self.image = self.playerSpriteAnimations["death 1"]
            else:
                pushedEnemies = [enemy for enemy in enemyGroup if enemy.collisionRect.colliderect(self.collisionRect)
                                 and enemy.enemyState in [EnemyState.STUNNED, EnemyState.STUNNED_SMALL_BALL,
                                                          EnemyState.STUNNED_BALL]]
                for enemy in pushedEnemies:
                    enemy.push(self)

    def checkOtherPlayerCollision(self):
        if self.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING]:
            otherPlayers = [player for player in playerGroup if (player != self and
                            player.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING,
                                                   PlayerStates.HITTING_PLAYER_MOVING,
                                                   PlayerStates.HITTING_PLAYER_SWINGING])]
            for player in otherPlayers:
                if player.collisionRect.colliderect(self.collisionRect):
                    playSound("bounce_rubber_or_player.wav")
                    self.frameCount = 0
                    if not self.bouncingOff:
                        self.changeDirection()
                        self.bouncingOff = True
                    if self.playerState == PlayerStates.MOVING:
                        self.playerState = PlayerStates.HITTING_PLAYER_MOVING
                    else:
                        self.playerState = PlayerStates.HITTING_PLAYER_SWINGING
                    if self.isFacingHorizontally():
                        self.image = self.playerSpriteAnimations["flash 1"]
                    else:
                        self.image = self.playerSpriteAnimations["flash vertical 1"]
                    if player.playerState not in [PlayerStates.HITTING_PLAYER_MOVING,
                                                  PlayerStates.HITTING_PLAYER_SWINGING]:
                        player.checkOtherPlayerCollision()

    def adjustPosition(self):  # TEST MORE
        if self.isFacingHorizontally():
            if 0 < (self.coordinates[1] - 1) % 48 < 24:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - (self.coordinates[1] % 48 - 1))
            elif (self.coordinates[1] - 1) % 48 > 23:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + (48 - self.coordinates[1] % 48 + 1))
        else:
            if 0 < (self.coordinates[0] + 1) % 48 < 24:
                self.setCoordinates(self.coordinates[0] - ((self.coordinates[0] - 1) % 48), self.coordinates[1])
            elif (self.coordinates[0] + 1) % 48 > 23:
                self.setCoordinates(self.coordinates[0] + (48 - self.coordinates[0] % 48 + 1), self.coordinates[1])

    def animateLevelEnd(self):
        if self.playerNumber == 1:
            self.setCoordinates(88, 80)
            if self.frameCount in (32, 160, 192):
                self.image = self.playerSpriteAnimations["end screen 2"]
            else:
                self.image = self.playerSpriteAnimations["end screen 1"]
                if self.frameCount % 32 > 15:
                    self.flipImage()
                if self.frameCount % 16 == 0:
                    playSound("grab_post_move_end.wav")
            # REMEMBER TO COUNT DOWN TIME


class PlayerArmSprite(pygame.sprite.Sprite):
    directionList = [Directions.RIGHT, Directions.UP, Directions.LEFT, Directions.DOWN]

    def __init__(self, playerNumber=1):
        super().__init__(armGroup)
        self.playerNumber = playerNumber
        self.playerBody = None
        self.image = getImage(spriteFolder, "empty.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (12, 12))  # 4, 2
        self.wallCollisionRect = pygame.rect.Rect((0, 0), (40, 40))
        self.coordinates = (0, 0)
        self.extendedDirection = Directions.RIGHT
        self.armState = ArmStates.OFF_SCREEN
        self.swingingClockwise = False
        self.frameCount = 0

    # CONTINUE TESTING
    def setCoordinates(self, x, y):
        if isinstance(self.playerBody, PlayerSprite):
            horizontalOffset = 14
            verticalOffset = 16
            if self.playerBody.facingDirection == Directions.LEFT:
                horizontalOffset -= 10
            elif self.playerBody.facingDirection == Directions.UP:
                verticalOffset -= 10

            if self.extendedDirection == Directions.UP:
                self.coordinates = (x + horizontalOffset, y - 13)
            elif self.extendedDirection == Directions.DOWN:
                self.coordinates = (x + horizontalOffset, y + 31)
            elif self.extendedDirection == Directions.LEFT:
                self.coordinates = (x - 13, y + verticalOffset)
            else:
                self.coordinates = (x + 31, y + verticalOffset)
        self.rect.topleft = self.coordinates
        if self.extendedDirection == Directions.UP:
            self.collisionRect = pygame.rect.Rect((self.coordinates[0] + 2, self.coordinates[1]), (12, 12))
        elif self.extendedDirection == Directions.DOWN:
            self.collisionRect = pygame.rect.Rect((self.coordinates[0] + 2, self.coordinates[1] + 4), (12, 12))
        elif self.extendedDirection == Directions.LEFT:
            self.collisionRect = pygame.rect.Rect((self.coordinates[0], self.coordinates[1] + 2), (12, 12))
        else:
            self.collisionRect = pygame.rect.Rect((self.coordinates[0] + 4, self.coordinates[1] + 2), (12, 12))
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
            self.image = self.playerBody.playerSpriteAnimations["arm 1"]
        elif self.armState == ArmStates.SWINGING:
            self.swing()
        if self.armState == ArmStates.OFF_SCREEN:
            self.image = getImage(spriteFolder, "empty.png")
        self.rotateImage()
        self.image.set_colorkey(BLACK)

    def extendArm(self, direction):
        self.armState = ArmStates.OFF_SCREEN
        if self.playerBody.isFacingHorizontally():
            if direction == "up":
                self.extendedDirection = Directions.UP
                self.armState = ArmStates.EXTENDED
            elif direction == "down":
                self.extendedDirection = Directions.DOWN
                self.armState = ArmStates.EXTENDED
        else:
            if direction == "left":
                self.extendedDirection = Directions.LEFT
                self.armState = ArmStates.EXTENDED
            elif direction == "right":
                self.extendedDirection = Directions.RIGHT
                self.armState = ArmStates.EXTENDED

    def checkGrabPost(self):
        if not any(self.wallCollisionRect.colliderect(levelRect) for levelRect in
                   PlayerSprite.currentLevel.levelBorderRects):
            if self.collisionRect[0] % 48 in range(32, 37) and self.collisionRect[1] % 48 in range(34, 39) and\
                                    70 < self.collisionRect[0] < 400 and 20 < self.collisionRect[1] < 500:
                self.playerBody.setCoordinates(self.playerBody.coordinates[0] + (34 - self.collisionRect[0] % 48),
                                               self.playerBody.coordinates[1] + (36 - self.collisionRect[1] % 48))
                self.setCoordinates(self.playerBody.coordinates[0], self.playerBody.coordinates[1])
                self.armState = ArmStates.SWINGING
                self.frameCount = 0
                self.playerBody.playerState = PlayerStates.SWINGING
                self.playerBody.frameCount = 0
                if any(((self.extendedDirection == Directions.UP and
                         self.playerBody.facingDirection == Directions.LEFT),
                        (self.extendedDirection == Directions.DOWN and
                         self.playerBody.facingDirection == Directions.RIGHT),
                        (self.extendedDirection == Directions.RIGHT and
                         self.playerBody.facingDirection == Directions.UP),
                        (self.extendedDirection == Directions.LEFT and
                         self.playerBody.facingDirection == Directions.DOWN))):
                    self.swingingClockwise = True
                else:
                    self.swingingClockwise = False

    def swing(self):
        self.frameCount += 1
        print(self.frameCount)
        if self.frameCount % 22 < 11:
            self.image = self.playerBody.playerSpriteAnimations["arm 1"]
        else:
            if self.extendedDirection in [Directions.UP, Directions.DOWN]:
                self.image = self.playerBody.playerSpriteAnimations["arm 2"]
            else:
                self.image = self.playerBody.playerSpriteAnimations["arm 3"]
        if self.frameCount % 22 == 0:
            if self.swingingClockwise:
                if self.extendedDirection == Directions.RIGHT:
                    self.extendedDirection = Directions.DOWN
                else:
                    extendedDirectionIndex = PlayerArmSprite.directionList.index(self.extendedDirection)
                    self.extendedDirection = PlayerArmSprite.directionList[extendedDirectionIndex - 1]
            else:
                if self.extendedDirection == Directions.DOWN:
                    self.extendedDirection = Directions.RIGHT
                else:
                    extendedDirectionIndex = PlayerArmSprite.directionList.index(self.extendedDirection)
                    self.extendedDirection = PlayerArmSprite.directionList[extendedDirectionIndex + 1]
        self.adjustPosition()
        if self.frameCount % 88 == 0:
            self.frameCount = 0

    def adjustPosition(self):  ############
        if self.frameCount % 88 == 0:
            self.coordinates = (self.coordinates[0] - 2, self.coordinates[1] - 2)
        elif self.frameCount % 88 == 11:
            self.coordinates = (self.coordinates[0] + 2, self.coordinates[1])
        elif self.frameCount % 88 == 22:
            self.coordinates = (self.coordinates[0], self.coordinates[1] + 2)
        elif self.frameCount % 88 == 33:
            self.coordinates = (self.coordinates[0] - 2, self.coordinates[1] + 2)
        elif self.frameCount % 88 == 44:
            self.coordinates = (self.coordinates[0], self.coordinates[1])
        elif self.frameCount % 88 == 55:
            self.coordinates = (self.coordinates[0] - 2, self.coordinates[1] - 2)
        elif self.frameCount % 88 == 66:
            self.coordinates = (self.coordinates[0], self.coordinates[1])
        elif self.frameCount % 88 == 77:
            self.coordinates = (self.coordinates[0] + 4, self.coordinates[1])   #CHECK
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
    blackHoleAnimations = getImagesFromList(spriteFolder, listOfBlackHoleSprites)
    blackHoleToSpawnList = []
    blackHoleToSpawn = None
    spawnedInitialEnemies = False
    onCooldown = False

    def __init__(self):
        super().__init__(blackHoleGroup)
        self.image = getImage(spriteFolder, "hole_1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coordinates = (0, 0)
        self.animationCount = 0
        self.frameCount = 0

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
        if len(enemyGroup) < 2 and not BlackHoleSprite.onCooldown and BlackHoleSprite.blackHoleToSpawn == self:
            if (not BlackHoleSprite.spawnedInitialEnemies and self.frameCount % 36 == 0) or\
                    (BlackHoleSprite.spawnedInitialEnemies and self.frameCount % 450 == 0):   # Set to 2 after testing
                newUrchin = UrchinSprite()
                newUrchin.setCoordinates(self.coordinates[0], self.coordinates[1])
                newUrchin.setRandomDirection()
                self.frameCount = 1
                BlackHoleSprite.onCooldown = True
                if len(enemyGroup) == 2:
                    BlackHoleSprite.spawnedInitialEnemies = True
        if BlackHoleSprite.onCooldown and self.frameCount % 216 == 0 and BlackHoleSprite.blackHoleToSpawn == self:
            BlackHoleSprite.onCooldown = False
            BlackHoleSprite.chooseNextBlackHoleToSpawn()
            self.frameCount = 0
        if self.frameCount % 6 == 0:
            self.animationCount += 1
            if self.animationCount >= len(self.blackHoleAnimations):
                self.animationCount = 0
            self.image = self.blackHoleAnimations[self.animationCount]
        if self.frameCount % 450 == 0:
            self.frameCount = 0

    @classmethod
    def chooseNextBlackHoleToSpawn(cls):
        if cls.blackHoleToSpawn == cls.blackHoleToSpawnList[-1]:
            cls.blackHoleToSpawn = cls.blackHoleToSpawnList[0]
        else:
            currentSpawnIndex = cls.blackHoleToSpawnList.index(cls.blackHoleToSpawn)
            cls.blackHoleToSpawn = cls.blackHoleToSpawnList[currentSpawnIndex + 1]


class UrchinSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(enemyGroup)
        self.image = getImage(spriteFolder, "urchin_ball_2.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (18, 18))
        self.coordinates = (0, 0)
        self.enemyState = EnemyState.SMALL_BALL
        self.facingDirection = Directions.RIGHT
        self.movementSpeed = 2
        self.bouncingOff = False
        self.animationCount = 0
        self.frameCount = 0
        self.delayCount = 0

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

    def update(self):
        self.checkSonicWaveCollision()
        self.checkOtherUrchinCollision()
        self.frameCount += 1

        if self.enemyState == EnemyState.SMALL_BALL:
            if self.frameCount % 5 == 0:
                if self.animationCount < 8:
                    self.image = getImage(spriteFolder, "urchin_ball_1.png")
                    self.enemyState = EnemyState.BALL
                    self.frameCount = 0
                    self.animationCount += 1
                else:
                    self.image = getImage(spriteFolder, "urchin_1.png")
                    self.enemyState = EnemyState.MOVING
                    self.frameCount = 0
                    self.animationCount = 0
        elif self.enemyState == EnemyState.BALL:
            if self.frameCount % 3 == 0:
                self.image = getImage(spriteFolder, "urchin_ball_2.png")
                self.enemyState = EnemyState.SMALL_BALL
                self.frameCount = 0
        elif self.enemyState == EnemyState.MOVING:
            if self.rect.center[0] % 48 == 16 and self.rect.center[1] % 48 == 18:
                randomValue = random.randint(0, 20)
                if randomValue < 1:
                    self.frameCount = 0
                    self.delayCount = random.randint(0, 5)
                    self.enemyState = EnemyState.WAITING
                elif randomValue < 6:
                    self.setRandomDirection()
            self.moveAnimation()
            self.moveSprite()
            if self.frameCount % 80 == 0:
                self.frameCount = 0
        elif self.enemyState == EnemyState.WAITING:
            self.moveAnimation()
            self.moveSprite()
        elif self.enemyState == EnemyState.STUNNED:
            if self.frameCount > 32:
                self.image = getImage(spriteFolder, "urchin_yellow_ball_1.png")
                self.enemyState = EnemyState.STUNNED_BALL
                self.animationCount = 8
        elif self.enemyState == EnemyState.STUNNED_SMALL_BALL:
            if (self.frameCount > 32 or self.animationCount > 0) and self.frameCount % 5 == 0:
                self.image = getImage(spriteFolder, "urchin_yellow_ball_1.png")
                self.enemyState = EnemyState.STUNNED_BALL
                self.frameCount = 0
                self.animationCount += 1
            if self.animationCount == 84:
                self.image = getImage(spriteFolder, "urchin_ball_1.png")
                self.enemyState = EnemyState.BALL
                self.frameCount = 0
                self.animationCount = 0
        elif self.enemyState == EnemyState.STUNNED_BALL:
            if (self.frameCount > 32 or self.animationCount > 0) and self.frameCount % 3 == 0:
                self.image = getImage(spriteFolder, "urchin_yellow_ball_2.png")
                self.enemyState = EnemyState.STUNNED_SMALL_BALL
                self.frameCount = 0
                self.animationCount += 1
            if self.animationCount == 84:
                self.image = getImage(spriteFolder, "urchin_ball_2.png")
                self.enemyState = EnemyState.SMALL_BALL
                self.frameCount = 0
                self.animationCount = 0
        elif self.enemyState == EnemyState.EXPLODING:
            if self.frameCount % 15 < 6:
                self.image = getImage(spriteFolder, "urchin_explosion_2.png")
            elif self.frameCount % 15 < 11:
                self.image = getImage(spriteFolder, "urchin_explosion_3.png")
            if self.frameCount % 15 == 0:
                self.enemyState = EnemyState.OFF_SCREEN
                self.image = getImage(spriteFolder, "points_500.png")
                self.offsetPointsCoordinates(self.facingDirection)
                self.facingDirection = Directions.RIGHT
                self.frameCount = 0
        elif self.enemyState == EnemyState.OFF_SCREEN:
            if self.frameCount % 32 == 0:
                self.enemyState = EnemyState.DEAD
                self.image = getImage(spriteFolder, "empty.png")
                BlackHoleSprite.blackHoleToSpawn.frameCount = 0
                self.kill()
        self.flipImage()
        self.image.set_colorkey(BLACK)

    def moveSprite(self, moveVal=0):
        if moveVal == 0:
            moveVal = self.movementSpeed
        if self.enemyState == EnemyState.WAITING:
            if self.frameCount % 20 == 0:
                if self.delayCount < 3:
                    self.delayCount += 1
                else:
                    self.setRandomDirection()
                    self.enemyState = EnemyState.MOVING
        elif not self.enemyState == EnemyState.MOVING or self.frameCount % 2 == 0:
            if self.facingDirection == Directions.UP:
                # if self.frameCount % 18 == 0:
                #     self.setRandomDirection()
                # elif self.frameCount % 73 == 0\
                #         or any(self.rect.colliderect(levelRect) for levelRect in
                #                PlayerSprite.currentLevel.levelBorderRects) \
                #         or any(self.collisionRect.colliderect(gold.collisionRect) for gold in goldGroup if
                #                gold.goldState != OtherState.OFF_SCREEN) \
                #         or any(self.collisionRect.colliderect(rubberTrap.collisionRect) for rubberTrap in rubberGroup
                #                if rubberTrap.trapState != OtherState.OFF_SCREEN):   # FIX
                #     self.enemyState = EnemyState.MOVING
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - moveVal)
            elif self.facingDirection == Directions.DOWN:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + moveVal)
            elif self.facingDirection == Directions.LEFT:
                self.setCoordinates(self.coordinates[0] - moveVal, self.coordinates[1])
            elif self.facingDirection == Directions.RIGHT:
                self.setCoordinates(self.coordinates[0] + moveVal, self.coordinates[1])
            if self.enemyState not in [EnemyState.STUNNED, EnemyState.STUNNED_BALL, EnemyState.STUNNED_SMALL_BALL]:
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
            if self.isFacingHorizontally():
                self.image = getImage(spriteFolder, "urchin_2.png")
            else:
                self.image = getImage(spriteFolder, "urchin_4.png")
        else:
            if self.isFacingHorizontally():
                self.image = getImage(spriteFolder, "urchin_1.png")
            else:
                self.image = getImage(spriteFolder, "urchin_3.png")

    def changeDirection(self):
        if self.facingDirection == Directions.UP:
            self.facingDirection = Directions.DOWN
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + 2)
        elif self.facingDirection == Directions.DOWN:
            self.facingDirection = Directions.UP
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - 2)
        elif self.facingDirection == Directions.LEFT:
            self.facingDirection = Directions.RIGHT
            self.setCoordinates(self.coordinates[0] + 2, self.coordinates[1])
        elif self.facingDirection == Directions.RIGHT:
            self.facingDirection = Directions.LEFT
            self.setCoordinates(self.coordinates[0] - 2, self.coordinates[1])

    def checkSonicWaveCollision(self):
        if self.enemyState not in [EnemyState.EXPLODING, EnemyState.OFF_SCREEN, EnemyState.DEAD]:
            if any(wave.rect.collidepoint(self.rect.center) for wave in attackGroup):
                playSound("push_enemy.wav")
                if self.enemyState in [EnemyState.BALL, EnemyState.STUNNED_BALL]:
                    self.image = getImage(spriteFolder, "urchin_yellow_ball_1.png")
                    self.enemyState = EnemyState.STUNNED_BALL
                elif self.enemyState in [EnemyState.SMALL_BALL, EnemyState.STUNNED_SMALL_BALL]:
                    self.image = getImage(spriteFolder, "urchin_yellow_ball_2.png")
                    self.enemyState = EnemyState.STUNNED_SMALL_BALL
                elif self.isFacingHorizontally():
                    self.image = getImage(spriteFolder, "urchin_yellow_1.png")
                    self.enemyState = EnemyState.STUNNED
                else:
                    self.image = getImage(spriteFolder, "urchin_yellow_3.png")
                    self.enemyState = EnemyState.STUNNED
                self.frameCount = 0
                self.animationCount = 0

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
        if self.frameCount % 2 == 0:
            playSound("push_enemy.wav")
        if self.isFacingHorizontally() == pushingPlayer.isFacingHorizontally():
            self.facingDirection = pushingPlayer.facingDirection
        self.moveSprite(PlayerSprite.movementSpeed)
        if any(levelRect.colliderect(self.collisionRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects):
            self.enemyState = EnemyState.EXPLODING
            self.image = getImage(spriteFolder, "urchin_explosion_1.png")
            self.frameCount = 0

    def offsetPointsCoordinates(self, offsetDirection):
        if offsetDirection == Directions.UP:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + 20)
        elif offsetDirection == Directions.DOWN:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - 20)
        elif offsetDirection == Directions.LEFT:
            self.setCoordinates(self.coordinates[0] + 20, self.coordinates[1])
        else:
            self.setCoordinates(self.coordinates[0] - 20, self.coordinates[1])

    def setRandomDirection(self):
        self.facingDirection = random.choice([Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT])


class GoldSprite(pygame.sprite.Sprite):
    goldSpriteAnimations = getImagesFromList(spriteFolder, listOfGoldAnimationSprites)
    bonusGoldSpriteAnimations = getImagesFromList(spriteFolder, listOfBonusGoldAnimationSprites)
    levelCount = 0

    def __init__(self):
        super().__init__(goldGroup)
        self.image = getImage(spriteFolder, "empty.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (16, 32))
        self.coordinates = (0, 0)
        self.goldState = OtherState.OFF_SCREEN
        self.animationSprites = GoldSprite.goldSpriteAnimations
        self.passingDirection = Directions.RIGHT
        self.isHorizontal = False
        self.alreadyRevealed = False
        self.animationPosition = 0
        self.frameCount = 0

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y
        if self.isHorizontal:
            self.collisionRect = pygame.rect.Rect((x + 1, y + 9), (32, 16))
        else:
            self.collisionRect = pygame.rect.Rect((x + 9, y + 1), (16, 32))

    def initialize(self, x, y):
        self.setCoordinates(x, y)
        if isinstance(PlayerSprite.currentLevel, BonusLevel):
            self.animationSprites = GoldSprite.bonusGoldSpriteAnimations

    def rotateImage(self):
        if self.isHorizontal:
            self.image = pygame.transform.rotate(self.image, 270)
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.frameCount += 1
        if self.goldState == OtherState.REVEALED:
            if self.frameCount % 12 < 6:
                self.image = self.animationSprites[4]
                self.animationPosition = 4
            else:
                self.image = self.animationSprites[0]
                self.animationPosition = 0
        elif self.goldState == OtherState.UPSIDE_DOWN:
                self.image = self.animationSprites[8]
                self.animationPosition = 8
        elif self.goldState == OtherState.FLIPPING_UP:
            self.flipUp()
        elif self.goldState == OtherState.FLIPPING_DOWN:
            self.flipDown()
        elif self.goldState == OtherState.OFF_SCREEN:
            self.image = getImage(spriteFolder, "empty.png")
        if self.frameCount % 48 == 0:
            self.frameCount = 0
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

        """32187654 Going up        56781234 Going down     123456781234 New down       765432187654 New up
           32187654 Going left        56781234 Going right     123456781234 New down       765432187654 New left"""

    def flipUp(self):
        if self.frameCount % 3 == 0:
            if self.passingDirection in [Directions.DOWN, Directions.LEFT]:
                if self.animationPosition == 1 or self.animationPosition == 0:
                    self.animationPosition = 8
                else:
                    self.animationPosition -= 1
            else:
                if self.animationPosition == 8:
                    self.animationPosition = 1
                elif self.animationPosition == 0:
                    self.animationPosition = 2
                else:
                    self.animationPosition += 1
        self.image = self.animationSprites[self.animationPosition]
        if self.frameCount % 36 == 0:
            self.goldState = OtherState.REVEALED
            if not self.alreadyRevealed:
                points100 = PointsSprite(self.passingDirection)
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

    # FIX AFTER TESTING
    def flipDown(self):
        if self.frameCount % 3 == 0:
            if self.animationPosition == 8:
                self.animationPosition = 1
            elif self.animationPosition == 0:
                self.animationPosition = 2
            else:
                self.animationPosition += 1
        self.image = self.animationSprites[self.animationPosition]
        if self.frameCount > 36:
            self.goldState = OtherState.UPSIDE_DOWN
            self.frameCount = 0

            if self.passingDirection in [Directions.DOWN, Directions.LEFT]:
                if self.animationPosition == 1 or self.animationPosition == 0:
                    self.animationPosition = 8
                else:
                    self.animationPosition -= 1
            else:
                if self.animationPosition == 8:
                    self.animationPosition = 1
                elif self.animationPosition == 0:
                    self.animationPosition = 2
                else:
                    self.animationPosition += 1
        self.image = self.animationSprites[self.animationPosition]


class RubberTrapSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(rubberGroup)
        self.image = getImage(spriteFolder, "empty.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.collisionRect = pygame.rect.Rect((0, 0), (16, 32))
        self.coordinates = (0, 0)
        self.trapState = OtherState.OFF_SCREEN
        self.collidingPlayer = None
        self.isHorizontal = False
        self.flipTrigger = False
        self.frameCount = 0

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y
        horizontalOffsets = 6, 44
        verticalOffsets = 24, 8
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
            self.image = getImage(spriteFolder, "rubber_1.png")
        elif self.trapState == OtherState.TRIGGERED:
            self.animateTrap()
        else:
            self.image = getImage(spriteFolder, "empty.png")
        self.checkPlayerCollision()
        self.rotateImage()
        if self.trapState == OtherState.OFF_SCREEN:
            self.image.set_colorkey(BLACK)
        else:
            self.image.set_colorkey(RED)

    # FLIP
    def checkPlayerCollision(self):
        if self.trapState != OtherState.TRIGGERED:
            for player in playerGroup:
                if self.collisionRect.colliderect(player.collisionRect):
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
        if self.getTrapAnimationStep() == 2:
            self.image = getImage(spriteFolder, "rubber_2.png")
        elif self.getTrapAnimationStep() == 3:
            self.image = getImage(spriteFolder, "rubber_3.png")
        elif self.getTrapAnimationStep() == 4:
            self.image = getImage(spriteFolder, "rubber_4.png")
        else:
            self.image = getImage(spriteFolder, "rubber_1.png")
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
            return 2
        elif self.frameCount % 33 // 3 in (1, 3, 7):
            return 3
        elif self.frameCount % 33 // 3 == 2:
            return 4
        else:
            return 1


class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(itemGroup)
        self.image = getImage(spriteFolder, "empty.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coordinates = (0, 0)
        self.itemState = OtherState.OFF_SCREEN
        self.frameCount = 0

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y

    def update(self):
        if self.itemState == OtherState.REVEALED:
            # self.image = getImage(spriteFolder, "rubber_1.png")
            pass
        else:
            self.image = getImage(spriteFolder, "empty.png")
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
    def __init__(self, passingDirection=Directions.RIGHT):
        super().__init__(itemGroup)
        self.image = getImage(spriteFolder, "points_100.png")
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
            self.image = getImage(spriteFolder, "empty.png")


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
