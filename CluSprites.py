import pygame
import os
import random
from enum import Enum
from CluLevels import BonusLevel


"""Spinning: Animating
             Movement
             Moving over black hole
             Sound effect
   Enemies: Pushing
            Pushing sound effect
   Gold: 
         Level complete
         Barrier to enemies     DONE?
         Sound effect           DONE?
   Rubber: Uncovering           DONE?
           Bouncing             DONE?
           Animating            DONE?
           Barrier to enemies   DONE?
   Gameplay: Random item locations
             Random level order
             Spawning items
             Level complete (Tally points, animate, sound effects, bonus)
             Game over screen
   Bonus level differences"""

"""Fix issue with spinning urchins in WAITING phase"""
"""Fix pushing urchin sound effect"""
"""Fix window icon"""

"""apple banana  cherry  melon   pineapple
bag      clock   flag
p1end1   p1end2  p1turn1 p1turn2
p2end1   p2end2  p2turn1 p2turn2
pts800   pts1500
count_points    earn_bonus  grab_post_move_end"""

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
listOfGoldAnimationSprites = ["gold_flash.png", "gold_flip_1.png", "gold_flip_2.png", "gold_flip_3.png",
                              "gold_flip_4.png", "gold_flip_5.png", "gold_flip_6.png", "gold_flip_7.png",
                              "gold_flip_8.png",]
listOfBonusGoldAnimationSprites = ["gold_blue_flash.png", "gold_blue_flip_1.png", "gold_blue_flip_2.png",
                                   "gold_blue_flip_3.png", "gold_blue_flip_4.png", "gold_blue_flip_5.png",
                                   "gold_blue_flip_6.png", "gold_blue_flip_7.png", "gold_blue_flip_8.png"]

player1SpriteDict = {"ball 1": getImage(spriteFolder, "p1_ball_1.png"),
                     "ball 2": getImage(spriteFolder,"p1_ball_2.png"),
                     "arm 1": getImage(spriteFolder, "p1_arm_extend.png"),
                     "arm 2": getImage(spriteFolder, "p1_arm_rotate.png"),
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
                     "squish vertical 3": getImage(spriteFolder, "p1_squish_6.png")}
player2SpriteDict = {"ball 1": getImage(spriteFolder, "p2_ball_1.png"),
                     "ball 2": getImage(spriteFolder,"p2_ball_2.png"),
                     "arm 1": getImage(spriteFolder, "p2_arm_extend.png"),
                     "arm 2": getImage(spriteFolder, "p2_arm_rotate.png"),
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
                     "squish vertical 3": getImage(spriteFolder, "p2_squish_6.png")}


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
allGroups = (itemGroup, blackHoleGroup, enemyGroup, goldGroup, armGroup, playerGroup, rubberGroup, attackGroup)


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
        self.bouncingOffPlayer = False
        self.frameCount = 0

    def flipImage(self):
        if self.facingDirection == Directions.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.facingDirection == Directions.UP:
            self.image = pygame.transform.flip(self.image, False, True)

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
        self.image.set_colorkey(BLACK)

    def update(self):
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

        if self.bouncingOffPlayer:
            otherPlayers = [player for player in playerGroup if (player != self and
                            player.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING,
                                                   PlayerStates.HITTING_PLAYER_MOVING,
                                                   PlayerStates.HITTING_PLAYER_SWINGING])]
            if not any(player.collisionRect.colliderect(self.collisionRect) for player in otherPlayers):
                self.bouncingOffPlayer = False
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
            self.flipImage()
            self.image.set_colorkey(BLACK)

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
        for gold in goldGroup:
            if gold.collisionRect.collidepoint(self.rect.center) and gold.goldState in\
                    [OtherState.OFF_SCREEN, OtherState.REVEALED, OtherState.UPSIDE_DOWN]:
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
        self.flipImage()
        self.image.set_colorkey(BLACK)

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
        print(self.coordinates)
        self.moveAnimation()
        if self.frameCount < 11:
            storedPlayerSpeed = PlayerSprite.movementSpeed
            # PlayerSprite.movementSpeed = 1
            self.moveSprite()
            PlayerSprite.movementSpeed = storedPlayerSpeed

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
                    self.image.set_colorkey(BLACK)

    def checkEnemyCollision(self):
        if self.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING]:
            if any(enemy.rect.colliderect(self.collisionRect) and enemy.enemyState == EnemyState.MOVING
                   for enemy in enemyGroup):
                playSound("death.wav")
                self.frameCount = 0
                self.facingDirection = Directions.RIGHT
                self.playerState = PlayerStates.EXPLODING
                self.image = self.playerSpriteAnimations["death 1"]
                self.image.set_colorkey(BLACK)
            else:
                pushedEnemies = [enemy for enemy in enemyGroup if enemy.rect.colliderect(self.collisionRect) and
                                 enemy.enemyState in [EnemyState.STUNNED, EnemyState.STUNNED_SMALL_BALL,
                                                      EnemyState.STUNNED_BALL]]
                for enemy in pushedEnemies:
                    enemy.push(self)

    def checkOtherPlayerCollision(self):
        if self.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING]:
            otherPlayers = [player for player in playerGroup if (player != self and
                            player.playerState in [PlayerStates.MOVING, PlayerStates.SWINGING,
                                                   PlayerStates.HITTING_PLAYER_MOVING,
                                                   PlayerStates.HITTING_PLAYER_SWINGING])]
            if any(player.collisionRect.colliderect(self.collisionRect) for player in otherPlayers):
                collidingPlayer = pygame.sprite.spritecollide(self, playerGroup, False)[0]
                playSound("bounce_rubber_or_player.wav")
                self.frameCount = 0
                if not self.bouncingOffPlayer:
                    self.changeDirection()
                    self.bouncingOffPlayer = True
                if self.playerState == PlayerStates.MOVING:
                    self.playerState = PlayerStates.HITTING_PLAYER_MOVING
                else:
                    self.playerState = PlayerStates.HITTING_PLAYER_SWINGING
                if self.isFacingHorizontally():
                    self.image = self.playerSpriteAnimations["flash 1"]
                else:
                    self.image = self.playerSpriteAnimations["flash vertical 1"]
                if collidingPlayer.playerState not in [PlayerStates.HITTING_PLAYER_MOVING,
                                                       PlayerStates.HITTING_PLAYER_SWINGING]:
                    collidingPlayer.checkOtherPlayerCollision()
                self.flipImage()
                self.image.set_colorkey(BLACK)


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
                self.coordinates = (self.playerBody.rect.left + horizontalOffset, self.playerBody.rect.top - 13)
            elif self.extendedDirection == Directions.DOWN:
                self.coordinates = (self.playerBody.rect.left + horizontalOffset, self.playerBody.rect.bottom - 3)
            elif self.extendedDirection == Directions.LEFT:
                self.coordinates = (self.playerBody.rect.left - 14, self.playerBody.rect.top + verticalOffset)
            else:
                self.coordinates = (self.playerBody.rect.right - 4, self.playerBody.rect.top + verticalOffset)
        self.rect.topleft = self.coordinates
        if self.extendedDirection == Directions.UP:
            self.collisionRect = pygame.rect.Rect((x + 2, y), (12, 12))
        elif self.extendedDirection == Directions.DOWN:
            self.collisionRect = pygame.rect.Rect((x + 2, y + 4), (12, 12))
        elif self.extendedDirection == Directions.LEFT:
            self.collisionRect = pygame.rect.Rect((x, y + 2), (12, 12))
        else:
            self.collisionRect = pygame.rect.Rect((x + 4, y + 2), (12, 12))

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
            if self.playerNumber == 1:
                self.image = getImage(spriteFolder, "p1_arm_extend.png")
            else:
                self.image = getImage(spriteFolder, "p2_arm_extend.png")
        if self.armState == ArmStates.SWINGING:
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
        if self.extendedDirection == Directions.UP:
            grabCoordinates = (self.coordinates[0], self.coordinates[1] + 6)
        elif self.extendedDirection == Directions.DOWN:
            grabCoordinates = (self.coordinates[0], self.coordinates[1] + 10)
        elif self.extendedDirection == Directions.LEFT:
            grabCoordinates = (self.coordinates[0] - 2, self.coordinates[1] + 7)
        else:
            grabCoordinates = (self.coordinates[0] + 2, self.coordinates[1] + 7)
        if not any(self.rect.colliderect(levelRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects):
            if grabCoordinates[0] % 48 == 32 and grabCoordinates[1] % 48 == 42 and 70 < grabCoordinates[0] < 400 and \
                     20 < grabCoordinates[1] < 500:
                self.armState = ArmStates.SWINGING
                self.frameCount = 7
                self.playerBody.playerState = PlayerStates.SWINGING
                self.playerBody.frameCount = 7
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
        if self.frameCount % 22 < 12:
            if self.playerNumber == 1:
                self.image = getImage(spriteFolder, "p1_arm_extend.png")
            else:
                self.image = getImage(spriteFolder, "p2_arm_extend.png")
        else:
            if self.playerNumber == 1:
                self.image = getImage(spriteFolder, "p1_arm_rotate.png")
            else:
                self.image = getImage(spriteFolder, "p2_arm_rotate.png")
        if self.frameCount % 11 == 0:
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
            self.rotateImage()
            self.image.set_colorkey(BLACK)


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
                and BlackHoleSprite.blackHoleToSpawn == self:   # Change to 2 after testing
            newUrchin = UrchinSprite()
            newUrchin.setCoordinates(self.coordinates[0], self.coordinates[1])
            newUrchin.setRandomDirection()
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
    def __init__(self):
        super().__init__(enemyGroup)
        self.image = getImage(spriteFolder, "urchin_ball_2.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coordinates = (0, 0)
        self.enemyState = EnemyState.SMALL_BALL
        self.facingDirection = Directions.RIGHT
        self.bouncingOffUrchin = False
        self.animationCount = 0
        self.frameCount = 0

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
                if randomValue < 1:  # Change to 1 after testing
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

    def moveSprite(self, moveVal=1):
        if self.enemyState == EnemyState.WAITING:
            pass
        else:
            if self.facingDirection == Directions.UP:
                if self.frameCount % 18 == 0:
                    self.setRandomDirection()
                elif self.frameCount % 73 == 0 or any(self.rect.colliderect(levelRect)
                                                      for levelRect in PlayerSprite.currentLevel.levelBorderRects) \
                        or any(self.rect.colliderect(gold) for gold in goldGroup if
                               gold.goldState != OtherState.OFF_SCREEN ) \
                        or any(self.rect.colliderect(rubberTrap) for rubberTrap in rubberGroup
                               if rubberTrap.trapState != OtherState.OFF_SCREEN):
                    self.enemyState = EnemyState.MOVING
                self.setCoordinates(self.coordinates[0], self.coordinates[1] - moveVal)
            elif self.facingDirection == Directions.DOWN:
                self.setCoordinates(self.coordinates[0], self.coordinates[1] + moveVal)
            elif self.facingDirection == Directions.LEFT:
                self.setCoordinates(self.coordinates[0] - moveVal, self.coordinates[1])
            elif self.facingDirection == Directions.RIGHT:
                self.setCoordinates(self.coordinates[0] + moveVal, self.coordinates[1])
            if self.enemyState not in [EnemyState.STUNNED, EnemyState.STUNNED_BALL, EnemyState.STUNNED_SMALL_BALL]:
                if any(self.rect.colliderect(levelRect) for levelRect in PlayerSprite.currentLevel.levelBorderRects) \
                        or any(self.rect.colliderect(gold) for gold in goldGroup if
                               gold.goldState != OtherState.OFF_SCREEN ) \
                        or any(self.rect.colliderect(rubberTrap) for rubberTrap in rubberGroup
                               if rubberTrap.trapState != OtherState.OFF_SCREEN):
                    self.changeDirection()
        if self.bouncingOffUrchin:
            otherUrchins = [enemy for enemy in enemyGroup if (enemy != self and
                            enemy.enemyState not in [EnemyState.OFF_SCREEN, EnemyState.DEAD])]
            if not any(self.rect.colliderect(enemy) for enemy in otherUrchins):
                self.bouncingOffUrchin = False

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
                self.flipImage()
                self.image.set_colorkey(BLACK)

    def checkOtherUrchinCollision(self):
        if self.enemyState == EnemyState.MOVING:
            otherUrchins = [enemy for enemy in enemyGroup if (enemy != self and
                            enemy.enemyState not in [EnemyState.OFF_SCREEN, EnemyState.DEAD])]
            if any(self.rect.colliderect(enemy) for enemy in otherUrchins):
                self.frameCount = 0
                if not self.bouncingOffUrchin:
                    self.changeDirection()
                    self.bouncingOffUrchin = True
                self.moveSprite()
                self.flipImage()
                self.image.set_colorkey(BLACK)

    def push(self, pushingPlayer):
        self.animationCount = 0
        # if not pygame.mixer.Channel(1).get_busy():
        #     pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(musicFolder, "push_enemy.wav")))
        if self.frameCount % 2 == 0:
            playSound("push_enemy.wav")
        if self.isFacingHorizontally() == pushingPlayer.isFacingHorizontally():
            self.facingDirection = pushingPlayer.facingDirection
        self.moveSprite(2)
        if any(levelRect.colliderect(self.rect) for levelRect in PlayerSprite.currentLevel.levelBorderRects):
            self.enemyState = EnemyState.EXPLODING
            self.image = getImage(spriteFolder, "urchin_explosion_2.png")
            self.frameCount = 0
            self.flipImage()
            self.image.set_colorkey(BLACK)

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
            self.collisionRect = pygame.rect.Rect((x + 9, y + 1), (16, 32))
        else:
            self.collisionRect = pygame.rect.Rect((x + 1, y + 9), (32, 16))

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
        else:
            self.image = getImage(spriteFolder, "empty.png")
        if self.frameCount % 48 == 0:
            self.frameCount = 0
        self.rotateImage()
        self.image.set_colorkey(BLACK)

    def startFlipAnimation(self):
        self.frameCount = 0
        playSound("pass_over_gold.wav")
        if self.goldState in [OtherState.UPSIDE_DOWN, OtherState.OFF_SCREEN] and GoldSprite.levelCount > 22 and\
                not isinstance(PlayerSprite.currentLevel, BonusLevel):
            self.goldState = OtherState.FLIPPING_DOWN
        else:
            if self.alreadyRevealed:
                self.frameCount = 12
            self.goldState = OtherState.FLIPPING_UP

        """32187654 Going up        56781234 Going down     123456781234 New down       765432187654 New up
           32187654 Going left        56781234 Going right     123456781234 New down       765432187654 New left"""

    def flipUp(self):
        if self.frameCount % 3 == 0:
            if self.passingDirection in [Directions.UP, Directions.LEFT]:
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


class RubberTrap(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(rubberGroup)
        self.image = getImage(spriteFolder, "empty.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coordinates = (0, 0)
        self.trapState = OtherState.OFF_SCREEN
        self.collidingPlayer = None
        self.isHorizontal = False
        self.flipTrigger = False
        self.frameCount = 0

    def setCoordinates(self, x, y):
        self.coordinates = x, y
        self.rect.topleft = x, y

    def rotateImage(self):
        if self.isHorizontal:
            self.image = pygame.transform.rotate(self.image, 90)

    def flipImage(self):
        if self.isHorizontal:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
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
        self.image.set_colorkey(BLACK)

    def checkPlayerCollision(self):
        if any(self.rect.collidepoint(player.rect.center) for player in playerGroup) and \
                        self.trapState != OtherState.TRIGGERED:
            if self.trapState == OtherState.OFF_SCREEN:
                playSound("bounce_rubber_or_player.wav")
            else:
                playSound("bounce_wall.wav")
            self.collidingPlayer = pygame.sprite.spritecollide(self, playerGroup, False)[0]
            self.trapState = OtherState.TRIGGERED
            if self.collidingPlayer.facingDirection == Directions.RIGHT or \
                    self.collidingPlayer.facingDirection == Directions.UP:
                self.flipTrigger = True
            else:
                self.flipTrigger = False

    def animateTrap(self):
        self.frameCount += 1
        if self.frameCount % 36 in (1, 2, 3, 13, 14, 15, 19, 20, 21, 27, 28, 29, 33, 34, 35):
            self.image = getImage(spriteFolder, "rubber_2.png")
        elif self.frameCount % 36 in (4, 5, 6, 10, 11, 12, 22, 23, 24, 25, 26):
            self.image = getImage(spriteFolder, "rubber_3.png")
        elif self.frameCount % 36 in (7, 8, 9):
            self.image = getImage(spriteFolder, "rubber_4.png")
        else:
            self.image = getImage(spriteFolder, "rubber_1.png")
        if self.flipTrigger:
            self.flipImage()
        if 18 < self.frameCount < 30:
            self.flipImage()
        if self.frameCount == 9:
            self.collidingPlayer.hitWall()
        if self.frameCount % 36 == 0:
            self.trapState = OtherState.REVEALED


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
    def __init__(self):
        super().__init__()
        self.image = getImage(spriteFolder, "game_over_text.png")
        self.image.set_colorkey(BLACK)
        self.coordinates = (20, 478)

    def update(self):
        if self.coordinates[1] > 38:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 4)
