import pygame
import os
import random
from enum import Enum


"""Spinning: Extended arm
             Animating
             Movement
             Colliding with enemy
             Moving over black hole
             Sound effect
   Enemies: Pushing
            Killing 
            Pushing/kiling/wave sound effect
   Gold: Uncovering
         Animating
         Level complete
         Barrier to enemies
         Sound effect 
   Rubber: Uncovering
           Bouncing
           Animating
           Barrier to enemies
           Sound effect
   Gameplay: Random item locations
             Random level order
             Spawning items
             Level complete (Tally points, animate, sound effects, bonus)
             Game over screen
   Bonus level differences"""

"""Fix issue with spinning urchins in WAITING phase"""

"""Collect clock: Change color of ..."""


SCREEN_SIZE = (512, 448)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

BLACK = (0, 0, 0)
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
    DEAD = "dead"


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


class Directions(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


playerGroup = pygame.sprite.Group()
attackGroup = pygame.sprite.Group()
blackHoleGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
itemGroup = pygame.sprite.Group()
goldGroup = pygame.sprite.Group()
allGroups = (itemGroup, blackHoleGroup, enemyGroup, goldGroup, playerGroup, attackGroup)


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
    currentLevel = None

    def __init__(self, playerNumber=1):
        super().__init__(playerGroup)
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

    def flipImage(self):
        if self.facingDirection == Directions.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.facingDirection == Directions.UP:
            self.image = pygame.transform.flip(self.image, False, True)

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y

    def isFacingHorizontally(self):
        return self.facingDirection in [Directions.RIGHT, Directions.LEFT]

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
        self.checkEnemyCollision()
        self.checkBlackHoleCollision()
        self.checkOtherPlayerCollision()
        self.frameCount += 1

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
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p1_move_2.png")
                    else:
                        self.image = getImage(spriteFolder, "p1_move_4.png")
                else:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p2_move_2.png")
                    else:
                        self.image = getImage(spriteFolder, "p2_move_4.png")
            else:
                if self.playerNumber == 1:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p1_move_1.png")
                    else:
                        self.image = getImage(spriteFolder, "p1_move_3.png")
                else:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p2_move_1.png")
                    else:
                        self.image = getImage(spriteFolder, "p2_move_3.png")
            if self.frameCount % 8 == 0:
                self.frameCount = 0
        elif self.playerState == PlayerStates.HITTING_WALL:
            if self.frameCount % 3 < 6 < 5:
                if self.playerNumber == 1:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p1_squish_2.png")
                    else:
                        self.image = getImage(spriteFolder, "p1_squish_5.png")
                else:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p2_squish_2.png")
                    else:
                        self.image = getImage(spriteFolder, "p2_squish_5.png")
            else:
                if self.playerNumber == 1:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p1_squish_3.png")
                    else:
                        self.image = getImage(spriteFolder, "p1_squish_6.png")
                else:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p2_squish_3.png")
                    else:
                        self.image = getImage(spriteFolder, "p2_squish_6.png")
            if self.frameCount % 8 == 0:
                self.frameCount = 0
                self.rebound()
        elif self.playerState == PlayerStates.FALLING:
            if 7 < self.frameCount % 40 < 17:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_fall_2.png")
                else:
                    self.image = getImage(spriteFolder, "p2_fall_2.png")
            elif 16 < self.frameCount % 40 < 25:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_fall_3.png")
                else:
                    self.image = getImage(spriteFolder, "p2_fall_3.png")
            elif 24 < self.frameCount % 40 < 33:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_fall_4.png")
                else:
                    self.image = getImage(spriteFolder, "p2_fall_4.png")
            if self.frameCount % 40 == 0:
                self.playerState = PlayerStates.OFF_SCREEN
                self.image = getImage(spriteFolder, "empty.png")
                self.frameCount = 0
        elif self.playerState == PlayerStates.EXPLODING:
            if 7 < self.frameCount % 40 < 17:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_death_2.png")
                else:
                    self.image = getImage(spriteFolder, "p2_death_2.png")
            elif 16 < self.frameCount % 40 < 25:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_death_3.png")
                else:
                    self.image = getImage(spriteFolder, "p2_death_3.png")
            elif 24 < self.frameCount % 40 < 33:
                if self.playerNumber == 1:
                    self.image = getImage(spriteFolder, "p1_death_4.png")
                else:
                    self.image = getImage(spriteFolder, "p2_death_4.png")
            if self.frameCount % 40 == 0:
                self.playerState = PlayerStates.OFF_SCREEN
                self.image = getImage(spriteFolder, "empty.png")
                self.frameCount = 0
                self.frameCount = 0
        elif self.playerState == PlayerStates.OFF_SCREEN:
            if self.lives > 0 and self.frameCount % 160 == 0:
                self.setCoordinates(self.baseCoordinates[0], self.baseCoordinates[1])
                self.putSpriteInBall()
                self.frameCount = 0
            elif self.lives == 0:
                self.playerState = PlayerStates.DEAD
        elif self.playerState == PlayerStates.HITTING_PLAYER_MOVING:
            if self.frameCount % 8 < 5:
                if self.playerNumber == 1:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p1_move_flash_2.png")
                    else:
                        self.image = getImage(spriteFolder, "p1_move_flash_4.png")
                else:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p2_move_flash_2.png")
                    else:
                        self.image = getImage(spriteFolder, "p2_move_flash_4.png")
            else:
                if self.playerNumber == 1:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p1_move_flash.png")
                    else:
                        self.image = getImage(spriteFolder, "p1_move_flash_3.png")
                else:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p2_move_flash.png")
                    else:
                        self.image = getImage(spriteFolder, "p2_move_flash_3.png")
            if self.frameCount % 8 == 0:
                self.moveSprite()
                self.frameCount = 0
                self.playerState = PlayerStates.MOVING
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
            if self.playerNumber == 1:
                if self.isFacingHorizontally():
                    self.image = getImage(spriteFolder, "p1_move_1.png")
                else:
                    self.image = getImage(spriteFolder, "p1_move_3.png")
            else:
                if self.isFacingHorizontally():
                    self.image = getImage(spriteFolder, "p2_move_1.png")
                else:
                    self.image = getImage(spriteFolder, "p2_move_3.png")
            self.playerState = PlayerStates.MOVING
            self.frameCount = 0
            self.flipImage()
            self.image.set_colorkey(BLACK)

    def moveSprite(self):
        if self.facingDirection == Directions.UP:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - 2)
        elif self.facingDirection == Directions.DOWN:
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + 2)
        elif self.facingDirection == Directions.LEFT:
            self.setCoordinates(self.coordinates[0] - 2, self.coordinates[1])
            if self.rect.right < 0:
                self.rect.left = 512
                self.setCoordinates(512, self.coordinates[1])
        elif self.facingDirection == Directions.RIGHT:
            self.setCoordinates(self.coordinates[0] + 2, self.coordinates[1])
            if self.rect.left > 512:
                self.rect.right = 0
                self.setCoordinates(-48, self.coordinates[1])
        if any(self.rect.colliderect(levelRect) for levelRect in self.currentLevel.levelBorderRects):
            self.hitWall()

    def hitWall(self):
        self.frameCount = 0
        playSound("bounce_wall.wav")
        self.playerState = PlayerStates.HITTING_WALL
        if self.playerNumber == 1:
            if self.isFacingHorizontally():
                self.image = getImage(spriteFolder, "p1_squish_1.png")
            else:
                self.image = getImage(spriteFolder, "p1_squish_4.png")
        else:
            if self.isFacingHorizontally():
                self.image = getImage(spriteFolder, "p2_squish_1.png")
            else:
                self.image = getImage(spriteFolder, "p2_squish_4.png")
        self.flipImage()
        self.image.set_colorkey(BLACK)

    def rebound(self):
        self.changeDirection(2)
        if self.playerNumber == 1:
            if self.isFacingHorizontally():
                self.image = getImage(spriteFolder, "p1_move_1.png")
            else:
                self.image = getImage(spriteFolder, "p1_move_3.png")
        else:
            if self.isFacingHorizontally():
                self.image = getImage(spriteFolder, "p2_move_1.png")
            else:
                self.image = getImage(spriteFolder, "p2_move_3.png")
        self.playerState = PlayerStates.MOVING
        self.flipImage()
        self.image.set_colorkey(BLACK)

    def changeDirection(self, moveVal):
        if self.facingDirection == Directions.UP:
            self.facingDirection = Directions.DOWN
            self.setCoordinates(self.coordinates[0], self.coordinates[1] + moveVal)
        elif self.facingDirection == Directions.DOWN:
            self.facingDirection = Directions.UP
            self.setCoordinates(self.coordinates[0], self.coordinates[1] - moveVal)
        elif self.facingDirection == Directions.LEFT:
            self.facingDirection = Directions.RIGHT
            self.setCoordinates(self.coordinates[0] + moveVal, self.coordinates[1])
        elif self.facingDirection == Directions.RIGHT:
            self.facingDirection = Directions.LEFT
            self.setCoordinates(self.coordinates[0] - moveVal, self.coordinates[1])

    def checkBlackHoleCollision(self):
        if self.playerState == PlayerStates.MOVING:
            if any(hole.rect.collidepoint(self.rect.center) for hole in blackHoleGroup):
                collidingHole = pygame.sprite.spritecollide(self, blackHoleGroup, False)[0]
                self.coordinates = collidingHole.coordinates
                self.rect.topleft = collidingHole.coordinates
                playSound("death.wav")
                self.frameCount = 0
                self.facingDirection = Directions.RIGHT
                self.playerState = PlayerStates.FALLING
                self.image = getImage(spriteFolder, "p1_fall_1.png")
                self.image.set_colorkey(BLACK)

    def checkEnemyCollision(self):
        if self.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING]:
            if any(enemy.rect.collidepoint(self.rect.center) and enemy.enemyState == EnemyState.MOVING
                   for enemy in enemyGroup):
                playSound("death.wav")
                self.frameCount = 0
                self.facingDirection = Directions.RIGHT
                self.playerState = PlayerStates.EXPLODING
                self.image = getImage(spriteFolder, "p1_death_1.png")
                self.image.set_colorkey(BLACK)

    def checkOtherPlayerCollision(self):
        if self.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING]:
            otherPlayers = [player for player in playerGroup if (player != self and
                            player.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING,
                                                   PlayerStates.HITTING_PLAYER_MOVING,
                                                   PlayerStates.HITTING_PLAYER_SWINGING])]
            if any(player.rect.collidepoint(self.rect.center) for player in otherPlayers):
                collidingPlayer = pygame.sprite.spritecollide(self, playerGroup, False)[0]
                playSound("bounce_player.wav")
                self.frameCount = 0
                self.changeDirection(0)
                if self.playerState == PlayerStates.MOVING:
                    self.playerState = PlayerStates.HITTING_PLAYER_MOVING
                else:
                    self.playerState = PlayerStates.HITTING_PLAYER_SWINGING
                if self.playerNumber == 1:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p1_move_flash.png")
                    else:
                        self.image = getImage(spriteFolder, "p1_move_flash_3.png")
                else:
                    if self.isFacingHorizontally():
                        self.image = getImage(spriteFolder, "p2_move_flash.png")
                    else:
                        self.image = getImage(spriteFolder, "p2_move_flash_3.png")
                if collidingPlayer.playerState not in [PlayerStates.HITTING_PLAYER_MOVING,
                                                       PlayerStates.HITTING_PLAYER_SWINGING]:
                    collidingPlayer.checkOtherPlayerCollision()
                self.flipImage()
                self.image.set_colorkey(BLACK)


class SonicWaveSprite(pygame.sprite.Sprite):
    def __init__(self, direction, firingPlayerNumber=1):
        super().__init__(attackGroup)
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
        self.rect.topleft = x, y

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

        if self.frameCount == 32:
            self.kill()
        self.rotateImage()
        self.image.set_colorkey(BLACK)


class BlackHoleSprite(pygame.sprite.Sprite):
    blackHoleAnimations = getImagesFromList(spriteFolder, listOfBlackHoleSprites)
    blackHoleToSpawn = None
    onCooldown = False

    def __init__(self):
        super().__init__(blackHoleGroup)
        self.image = getImage(spriteFolder, "hole_1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coordinates = (0, 0)
        self.animationCount = 0
        self.frameCount = 0

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y
        self.chooseNextBlackHoleToSpawn()

    def update(self):
        self.frameCount += 1
        if len(enemyGroup) < 4 and self.frameCount % 36 == 0 and not BlackHoleSprite.onCooldown \
                and BlackHoleSprite.blackHoleToSpawn == self:
            newUrchin = UrchinSprite()
            newUrchin.setCoordinates(self.coordinates[0], self.coordinates[1])
            enemyGroup.add(newUrchin)
            self.frameCount = 1
            BlackHoleSprite.onCooldown = True
        if self.frameCount % 216 == 0 and BlackHoleSprite.blackHoleToSpawn == self:
            BlackHoleSprite.onCooldown = False
            BlackHoleSprite.chooseNextBlackHoleToSpawn()
            self.frameCount = 0
        if self.frameCount % 6 == 0:
            self.animationCount += 1
            if self.animationCount < len(self.blackHoleAnimations):
                self.image = self.blackHoleAnimations[self.animationCount]
            else:
                self.animationCount = 0
                self.image = self.blackHoleAnimations[0]

    @classmethod
    def chooseNextBlackHoleToSpawn(cls):
        if len(blackHoleGroup) > 1:
            possibleBlackHoles = [item for item in blackHoleGroup if item != cls.blackHoleToSpawn]
        else:
            possibleBlackHoles = [item for item in blackHoleGroup]
        cls.blackHoleToSpawn = random.choice(possibleBlackHoles)


class UrchinSprite(pygame.sprite.Sprite):
    currentLevel = None

    def __init__(self):
        super().__init__(enemyGroup)
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
        self.rect.topleft = x, y

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
                    self.setRandomDirection()
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
                if randomValue < 21:  #
                    self.frameCount = 1
                    self.enemyState = EnemyState.WAITING
                elif randomValue < 6:
                    self.setRandomDirection()
            self.moveSprite()
            if self.frameCount % 8 < 5:
                if self.isFacingHorizontally():
                    self.image = getImage(spriteFolder, "urchin_2.png")
                else:
                    self.image = getImage(spriteFolder, "urchin_4.png")
            else:
                if self.isFacingHorizontally():
                    self.image = getImage(spriteFolder, "urchin_1.png")
                else:
                    self.image = getImage(spriteFolder, "urchin_3.png")
            if self.frameCount % 80 == 0:
                self.frameCount = 0
        elif self.enemyState == EnemyState.WAITING:
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
                self.frameCount = 0
        elif self.enemyState == EnemyState.OFF_SCREEN:
            if self.frameCount % 32 == 0:
                self.enemyState = EnemyState.DEAD
                self.image = getImage(spriteFolder, "empty.png")
        self.flipImage()
        self.image.set_colorkey(BLACK)

    def moveSprite(self):
        if self.enemyState == EnemyState.WAITING:
            if self.frameCount % 18 == 0:
                self.setRandomDirection()
            elif self.frameCount % 73 == 0 or any(self.rect.colliderect(levelRect)
                                                  for levelRect in self.currentLevel.levelBorderRects):
                self.enemyState = EnemyState.MOVING
        else:
            if self.facingDirection == Directions.UP:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - 1)
            elif self.facingDirection == Directions.DOWN:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + 1)
            elif self.facingDirection == Directions.LEFT:
                self.setCoordinates(self.coordinates[0] - 1, self.coordinates[1])
            elif self.facingDirection == Directions.RIGHT:
                self.setCoordinates(self.coordinates[0] + 1, self.coordinates[1])
            if any(self.rect.colliderect(levelRect) for levelRect in self.currentLevel.levelBorderRects):
                self.changeDirection()

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
                self.flipImage()
                self.image.set_colorkey(BLACK)

    def checkOtherUrchinCollision(self):
        if self.enemyState == EnemyState.MOVING:
            otherUrchins = [enemy for enemy in enemyGroup if (enemy != self and
                            enemy.enemyState not in [EnemyState.OFF_SCREEN, EnemyState.DEAD])]
            if any(enemy.rect.collidepoint(self.rect.center) for enemy in otherUrchins):
                self.frameCount = 0
                self.changeDirection()
                self.flipImage()
                self.image.set_colorkey(BLACK)

    def setRandomDirection(self):
        self.facingDirection = random.choice([Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT])


class GameOverTextSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = getImage(spriteFolder, "game_over_text.png")
        self.image.set_colorkey(BLACK)
        self.coordinates = (20, 478)

    def update(self):
        if self.coordinates[1] > 38:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 4)
