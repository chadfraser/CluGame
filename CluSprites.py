import pygame
import os
import random
from enum import Enum


"""Spinning, collision with walls, collision with other player, uncovering gold, collision with enemies,
spawning enemies, uncovering rubber, collision with rubber, level complete, spawning items, random level order"""


SCREEN_SIZE = (512, 448)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

BLACK = (0, 0, 0)
# P1_COLOR = (216, 40, 0)
# P2_COLOR = (0, 168, 0)
# P1_FLASH_COLOR = (252, 116, 96)
# P2_FLASH_COLOR = (76, 220, 72)
gameFolder = os.path.dirname(__file__)
spriteFolder = os.path.join(gameFolder, "Sprites")
backgroundFolder = os.path.join(gameFolder, "Backgrounds")
titleFolder = os.path.join(gameFolder, "Titles")

_imageLibrary = {}


def getImage(folder, imagePath):
    global _imageLibrary
    image = _imageLibrary.get(imagePath)
    if image is None:
        fullPath = os.path.join(folder, imagePath)
        image = pygame.image.load(fullPath).convert()
        _imageLibrary[imagePath] = image
    return image


listOfTitleSprites = ["title_01.png", "title_02.png", "title_03.png", "title_04.png", "title_05.png", "title_06.png",
                      "title_07.png", "title_08.png", "title_09.png", "title_10.png", "title_11.png", "title_12.png",
                      "title_13.png"]
listOfBlackHoleSprites = ["hole_1.png", "hole_2.png", "hole_3.png", "hole_4.png"]


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
    FALLING = "falling"
    EXPLODING = "exploding"
    OFF_SCREEN = "off screen"
    DEAD = "dead"


class EnemyState(Enum):
    MOVING = "moving"
    BALL = "ball"
    SMALL_BALL = "small ball"
    STUNNED = "stunned"
    STUNNED_BALL = "stunned ball"
    STUNNED_SMALL_BALL = "stunned small ball"
    EXPLODING = "exploding"
    OFF_SCREEN = "off screen"
    DEAD = "dead"


class Directions(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


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
    def __init__(self, playerNumber=1):
        super().__init__()
        self.playerNumber = playerNumber
        self.lives = 5
        self.image = getImage(spriteFolder, "p1_ball_1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.baseCoordinates = (0, 0)
        self.coordinates = (0, 0)
        self.playerState = PlayerStates.OFF_SCREEN
        self.facingDirection = Directions.RIGHT
        self.frameCount = 0
        self.directionList = [Directions.RIGHT, Directions.UP, Directions.LEFT, Directions.DOWN]

    def rotateImage(self):
        if self.facingDirection in self.directionList:
            rotationDegrees = 90 * self.directionList.index(self.facingDirection)
            self.image = pygame.transform.rotate(self.image, rotationDegrees)

    def setCoordinates(self, x, y):
        self.coordinates = x, y

    def putSpriteInBall(self):
        self.facingDirection = Directions.RIGHT
        self.playerState = PlayerStates.BALL
        if self.playerNumber == 1:
            self.image = getImage(spriteFolder, "p1_ball_1.png")
        else:
            self.image = getImage(spriteFolder, "p2_ball_1.png")
        self.lives = max(0, self.lives - 1)
        self.frameCount = 0
        self.image.set_colorkey(BLACK)

    def update(self):
        self.frameCount += 1
        self.fallIntoBlackHole()
        self.animateDeath()

        if self.playerState == PlayerStates.BALL:
            if self.frameCount % 16 < 9:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_ball_2.png")
                else:
                    self.image = getImage(spriteFolder, "p2_ball_2.png")
            else:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_ball_1.png")
                elif self.playerNumber == 2:
                    self.image = getImage(spriteFolder, "p2_ball_1.png")
            if self.frameCount % 16 == 0:
                self.frameCount = 0
        elif self.playerState == PlayerStates.MOVING:
            self.moveSprite()
            if self.frameCount % 8 < 5:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_move_2.png")
                else:
                    self.image = getImage(spriteFolder, "p2_move_2.png")
            else:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_move_1.png")
                else:
                    self.image = getImage(spriteFolder, "p2_move_1.png")
            if self.frameCount % 8 == 0:
                self.frameCount = 0
        elif self.playerState == PlayerStates.FALLING:
            if self.frameCount % 32 < 9:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_fall_2.png")
                else:
                    self.image = getImage(spriteFolder, "p2_fall_2.png")
            elif self.frameCount % 32 < 17:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_fall_3.png")
                else:
                    self.image = getImage(spriteFolder, "p2_fall_3.png")
            elif self.frameCount % 32 < 25:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_fall_4.png")
                else:
                    self.image = getImage(spriteFolder, "p2_fall_4.png")
            elif self.frameCount % 32 == 0:
                self.playerState = PlayerStates.OFF_SCREEN
                self.image = getImage(spriteFolder, "empty.png")
                self.frameCount = 0
        elif self.playerState == PlayerStates.EXPLODING:
            if self.frameCount % 32 < 9:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_death_2.png")
                else:
                    self.image = getImage(spriteFolder, "p2_death_2.png")
            elif self.frameCount % 32 < 17:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_death_3.png")
                else:
                    self.image = getImage(spriteFolder, "p2_death_3.png")
            elif self.frameCount % 32 < 25:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_death_4.png")
                else:
                    self.image = getImage(spriteFolder, "p2_death_4.png")
            if self.frameCount % 32 == 0:
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
        self.rotateImage()
        self.image.set_colorkey(BLACK)

    def startMoving(self, direction):
        if self.playerState == PlayerStates.BALL:
            self.image = getImage(spriteFolder, "p1_move_1.png")
            if direction == "up":
                self.facingDirection = Directions.UP
            elif direction == "down":
                self.facingDirection = Directions.DOWN
            elif direction == "left":
                self.facingDirection = Directions.LEFT
            else:
                self.facingDirection = Directions.RIGHT
            self.playerState = PlayerStates.MOVING
            self.frameCount = 0
            self.image.set_colorkey(BLACK)
            self.rotateImage()

    def moveSprite(self):
        if self.facingDirection == Directions.UP:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - 1)
        elif self.facingDirection == Directions.DOWN:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + 1)
        elif self.facingDirection == Directions.LEFT:
            self.setCoordinates(self.coordinates[0] - 1, self.coordinates[1])
        elif self.facingDirection == Directions.RIGHT:
            self.setCoordinates(self.coordinates[0] + 1, self.coordinates[1])

    def fallIntoBlackHole(self, blackHoles=None):
        if blackHoles is None:
            blackHoles = []
        for hole in blackHoles:
            if pygame.sprite.collide_rect(self, hole):
                self.frameCount = 0
                self.facingDirection = Directions.RIGHT
                self.playerState = PlayerStates.FALLING
                self.image = getImage(spriteFolder, "p1_fall_1.png")

    def animateDeath(self, enemies=None):
        if enemies is None:
            enemies = []
        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                self.frameCount = 0
                self.facingDirection = Directions.RIGHT
                self.playerState = PlayerStates.EXPLODING
                self.image = getImage(spriteFolder, "p1_death_1.png")


class SonicWaveSprite(pygame.sprite.Sprite):
    def __init__(self, direction, firingPlayerNumber=1):
        super().__init__()
        self.image = getImage(spriteFolder, "wave_1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coordinates = (0, 0)
        self.direction = direction
        self.firingPlayerNumber = firingPlayerNumber
        self.frameCount = 0
        self.directionList = [Directions.RIGHT, Directions.UP, Directions.LEFT, Directions.DOWN]

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

    def rotateImage(self):
        if self.direction in self.directionList:
            rotationDegrees = 90 * self.directionList.index(self.direction)
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

        if self.frameCount % 2 == 1:
            self.image = getImage(spriteFolder, "wave_1.png")
        else:
            self.image = getImage(spriteFolder, "wave_2.png")
        self.rotateImage()
        self.image.set_colorkey(BLACK)


class BlackHoleSprite(pygame.sprite.Sprite):
    blackHoleAnimations = getImagesFromList(spriteFolder, listOfBlackHoleSprites)

    def __init__(self):
        super().__init__()
        self.image = getImage(spriteFolder, "hole_1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.animationCount = 0
        self.frameCount = 0

    def update(self):
        self.frameCount += 1
        if self.frameCount % 6 == 0:
            self.animationCount += 1
            if self.animationCount < len(self.blackHoleAnimations):
                self.image = self.blackHoleAnimations[self.animationCount]
            else:
                self.animationCount = 0
                self.frameCount = 0
                self.image = self.blackHoleAnimations[0]


class UrchinSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = getImage(spriteFolder, "urchin_ball_2.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coordinates = (0, 0)
        self.enemyState = EnemyState.SMALL_BALL
        self.facingDirection = Directions.RIGHT
        self.animationCount = 0
        self.frameCount = 0
        self.directionList = [Directions.RIGHT, Directions.UP, Directions.LEFT, Directions.DOWN]

    def setCoordinates(self, x, y):
        self.coordinates = x, y

    def rotateImage(self):
        if self.facingDirection in self.directionList:
            rotationDegrees = 90 * self.directionList.index(self.facingDirection)
            self.image = pygame.transform.rotate(self.image, rotationDegrees)

    def update(self):
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
                    self.setRandomDirection()
                    self.frameCount = 0
                    self.animationCount = 0
        elif self.enemyState == PlayerStates.BALL:
            if self.frameCount % 3 == 0:
                self.image = getImage(spriteFolder, "urchin_ball_2.png")
                self.enemyState = EnemyState.SMALL_BALL
                self.frameCount = 0
        elif self.enemyState == EnemyState.MOVING:
            pass
        elif self.enemyState == EnemyState.STUNNED:
            pass
        elif self.enemyState == EnemyState.STUNNED_SMALL_BALL:
            pass
        elif self.enemyState == EnemyState.STUNNED_BALL:
            pass
        elif self.enemyState == EnemyState.EXPLODING:
            if self.frameCount % 15 < 6:
                self.image = getImage(spriteFolder, "urchin_explosion_2.png")
            elif self.frameCount % 15 < 11:
                self.image = getImage(spriteFolder, "urchin_explosion_3.png")
            if self.frameCount % 15 == 0:
                self.enemyState = EnemyState.OFF_SCREEN
                self.image = getImage(spriteFolder, "points_500.png")
                self.frameCount = 0
        elif self.enemyState == EnemyState.OFF_SCREEN:
            if self.frameCount % 32 == 0:
                self.enemyState = EnemyState.DEAD
                self.image = getImage(spriteFolder, "empty.png")
        self.rotateImage()
        self.image.set_colorkey(BLACK)

    def setRandomDirection(self):
        self.facingDirection = random.choice(Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT)


class GameOverTextSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = getImage(spriteFolder, "game_over_text.png")
        self.image.set_colorkey(BLACK)
        self.coordinates = (20, 478)

    def update(self):
        if self.coordinates[1] > 38:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 4)
