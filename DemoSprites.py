import pygame
from CluSprites import SpriteSheet, Directions
from CluGlobals import playSound


BLACK = (0, 0, 0)
demoGroup = pygame.sprite.Group()


class DemoSprite(pygame.sprite.Sprite):
    def __init__(self, coordinates=(0, 0)):
        super().__init__(demoGroup)
        self.spriteSheet = SpriteSheet("demo.png")
        self.animationFrames = []
        self.coordinates = coordinates
        self.frameCount = 0
        self.emptyImage = self.spriteSheet.getSheetImage(546, 416, 32, 32)
        self.image = self.emptyImage
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def setCoordinates(self):
        if DemoPlayerSprite.swingValue != (0, 0):
            self.coordinates = (self.coordinates[0] + DemoPlayerSprite.swingValue[0],
                                self.coordinates[1] + DemoPlayerSprite.swingValue[1])
        elif not DemoPlayerSprite.paused:
            if DemoPlayerSprite.facingDirection == Directions.UP:
                offsets = (0, 4)
            elif DemoPlayerSprite.facingDirection == Directions.DOWN:
                offsets = (0, -4)
            elif DemoPlayerSprite.facingDirection == Directions.LEFT:
                offsets = (4, 0)
            else:
                offsets = (-4, 0)
            self.coordinates = (self.coordinates[0] + offsets[0], self.coordinates[1] + offsets[1])
        self.rect.topleft = self.coordinates

    def setMonochromeImage(self):
        pass


class PostSprite(DemoSprite):
    def __init__(self, coordinates=(0, 0)):
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(0, 0, 32, 32, 2)
        self.image = self.animationFrames[0]

    def setMonochromeImage(self):
        self.image = self.animationFrames[1]


class DemoPlayerSprite(DemoSprite):
    facingDirection = Directions.RIGHT
    swingValue = (0, 0)
    paused = False

    def __init__(self, demoNumber=0, coordinates=(0, 0)):
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
        self.frameCount += 1
        if self.facingDirection in [Directions.LEFT, Directions.RIGHT]:
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
        if DemoPlayerSprite.facingDirection == Directions.LEFT and 0 < self.frameCount:
            self.image = pygame.transform.flip(self.image, True, False)
        elif DemoPlayerSprite.facingDirection == Directions.UP and 0 < self.frameCount:
            self.image = pygame.transform.flip(self.image, False, True)

    def playerOneUpdate(self):
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
                DemoPlayerSprite.facingDirection = Directions.LEFT
                self.coordinates = (self.coordinates[0] - 16, self.coordinates[1])

    def playerTwoUpdate(self):
        if 106 < self.frameCount < 147 or 170 < self.frameCount < 211 or 232 < self.frameCount:
            self.swing()
            if 5 < self.swingFrameCount < 15 or 23 < self.swingFrameCount < 35 or 44 < self.swingFrameCount < 54 or\
                    62 < self.swingFrameCount < 73:
                if self.frameCount % 8 < 4:
                    self.image = self.animationFrames[2]
                else:
                    self.image = self.animationFrames[3]
                if 23 < self.swingFrameCount < 35 and not self.clockwise:
                    self.image = pygame.transform.flip(self.image, False, True)
            elif 14 < self.swingFrameCount < 24 or 53 < self.swingFrameCount < 63:
                if self.frameCount % 8 < 4:
                    self.image = self.animationFrames[4]
                else:
                    self.image = self.animationFrames[5]

        if self.swingFrameCount == 6:
            if self.clockwise:
                DemoPlayerSprite.facingDirection = Directions.DOWN
            else:
                DemoPlayerSprite.facingDirection = Directions.UP
        elif self.swingFrameCount == 24 or self.swingFrameCount == 45:
            DemoPlayerSprite.facingDirection = Directions.LEFT
        elif self.swingFrameCount == 63:
            DemoPlayerSprite.facingDirection = Directions.RIGHT

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
                DemoPlayerSprite.facingDirection = Directions.RIGHT
                self.coordinates = (self.coordinates[0] + 18, self.coordinates[1])

    def playerFourUpdate(self):
        if self.animated:
            if self.frameCount == 8:
                self.animated = False
                if DemoPlayerSprite.facingDirection == Directions.RIGHT:
                    DemoPlayerSprite.facingDirection = Directions.LEFT
                else:
                    DemoPlayerSprite.facingDirection = Directions.RIGHT
                self.frameCount = 0

                for sprite in demoGroup:
                    if isinstance(sprite, DemoArmSprite):
                        if DemoPlayerSprite.facingDirection == Directions.RIGHT:
                            sprite.coordinates = (sprite.coordinates[0] + 12, sprite.coordinates[1])
                        else:
                            sprite.coordinates = (sprite.coordinates[0] - 12, sprite.coordinates[1])

    def setCoordinates(self):
        self.rect.topleft = self.coordinates


class DemoArmSprite(DemoSprite):
    def __init__(self, demoNumber=1, coordinates=(0, 0), flipped=False):
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(64, 0, 32, 32, 4)
        self.demoNumber = demoNumber
        self.flipped = flipped
        self.extendedDirection = Directions.RIGHT

    def update(self):
        self.frameCount += 1
        self.image = self.emptyImage
        if self.demoNumber == 1:
            if 100 < self.frameCount < 147 or 164 < self.frameCount < 211 or 226 < self.frameCount:
                self.image = self.animationFrames[0]
                if 120 < self.frameCount < 130 or 183 < self.frameCount < 193 or 246 < self.frameCount < 256 or\
                        285 < self.frameCount < 296 or 324 < self.frameCount:
                    self.image = pygame.transform.rotate(self.image, 270)
                if 129 < self.frameCount < 141 or 192 < self.frameCount < 204 or 255 < self.frameCount < 267 or\
                        295 < self.frameCount < 306:
                    self.image = self.animationFrames[1]
                    self.image = pygame.transform.rotate(self.image, 90)
                elif 111 < self.frameCount < 121 or 174 < self.frameCount < 184 or 237 < self.frameCount < 247 or\
                        276 < self.frameCount < 286 or 315 < self.frameCount < 325:
                    self.image = self.animationFrames[2]
            else:
                self.image = self.emptyImage
            self.adjustPosition()
            if self.extendedDirection == Directions.LEFT:
                self.image = pygame.transform.flip(self.image, True, False)
            if self.frameCount in [107, 171, 233]:
                playSound("grab_post_move_end.wav")

        else:
            if 50 < self.frameCount < 150 or 180 < self.frameCount < 215 or 280 < self.frameCount:
                self.image = self.animationFrames[3]
            elif self.frameCount == 180:
                self.flipped = False
                self.coordinates = (self.coordinates[0], self.coordinates[1] + 88)
            elif self.frameCount == 215:
                self.flipped = True
                self.coordinates = (self.coordinates[0], self.coordinates[1] - 88)
            if DemoPlayerSprite.facingDirection == Directions.LEFT:
                self.image = pygame.transform.flip(self.image, True, False)
        if self.flipped:
            self.image = pygame.transform.flip(self.image, False, True)

    def setCoordinates(self):
        if DemoPlayerSprite.paused:
            self.coordinates = (self.coordinates[0] + DemoPlayerSprite.swingValue[0],
                                self.coordinates[1] + DemoPlayerSprite.swingValue[1])
        self.rect.topleft = self.coordinates

    def adjustPosition(self):
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
            self.extendedDirection = Directions.LEFT
        if self.frameCount == 193 or self.frameCount == 296:
            self.extendedDirection = Directions.RIGHT


class DemoGoldSprite(DemoSprite):
    def __init__(self, coordinates=(0, 0)):
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(0, 32, 68, 68, 10)
        self.animationPosition = 0
        self.timesFlipped = 0
        self.flipping = False
        self.rect = self.image.get_rect()

    def update(self):
        self.frameCount += 1
        if self.flipping and 9 < self.frameCount:
            self.flipUp()
        elif self.timesFlipped:
            if self.frameCount % 12 < 6:
                self.image = self.animationFrames[3]
            else:
                self.image = self.animationFrames[8]
        for sprite in demoGroup:
            if isinstance(sprite, DemoPlayerSprite) and self.rect.colliderect(sprite.rect) and\
                    0 < self.frameCount and not self.flipping:
                playSound("pass_over_gold.wav")
                self.flipping = True
                self.frameCount = 9 * self.timesFlipped

    def flipUp(self):
        if self.timesFlipped == 0:
            if self.frameCount % 3 == 0:
                if self.animationPosition == 7:
                    self.animationPosition = 0
                else:
                    self.animationPosition += 1
        else:
            if self.frameCount % 3 == 0:
                if self.animationPosition == 0:
                    self.animationPosition = 7
                else:
                    self.animationPosition -= 1
        self.image = self.animationFrames[self.animationPosition]
        if self.frameCount == 36:
            self.timesFlipped += 1
            self.frameCount = 0
            self.flipping = False

    def setMonochromeImage(self):
        self.image = self.animationFrames[9]


class DemoHoleSprite(DemoSprite):
    def __init__(self, coordinates=(0, 0)):
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(0, 100, 68, 68, 5)
        self.animationCount = 0
        self.image = self.animationFrames[0]
        self.rect = self.image.get_rect()

    def update(self):
        self.frameCount += 1
        if self.frameCount % 6 == 0:
            self.animationCount += 1
            if self.animationCount == 4:
                self.animationCount = 0
            self.image = self.animationFrames[self.animationCount]

        for sprite in demoGroup:
            if isinstance(sprite, DemoPlayerSprite) and self.rect.collidepoint(sprite.rect.center) and\
                            self.frameCount and not sprite.animated:
                sprite.animated = True
                sprite.frameCount = 0

    def setMonochromeImage(self):
        self.image = self.animationFrames[4]


class DemoUrchinSprite(DemoSprite):
    def __init__(self, coordinates=(0, 0)):
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(136, 168, 68, 68, 7)
        self.animationCount = 0
        self.image = self.animationFrames[0]
        self.rect = self.image.get_rect()

    def update(self):
        self.frameCount += 1
        if self.animationCount == 0:
            if self.frameCount % 8 < 5:
                self.image = self.animationFrames[0]
            else:
                self.image = self.animationFrames[1]
        elif self.animationCount == 1:
            if self.frameCount < 3:
                self.image = self.animationFrames[2]
            elif self.frameCount % 8 < 5:
                self.image = self.animationFrames[3]
            else:
                self.image = self.animationFrames[4]
        elif self.animationCount == 2:
            if self.frameCount > 3:
                self.coordinates = (self.coordinates[0] - 4, self.coordinates[1])
        else:
            if self.frameCount < 5:
                self.image = self.animationFrames[5]
            elif self.frameCount < 10:
                self.image = self.animationFrames[6]
            else:
                self.kill()
        for sprite in demoGroup:
            if isinstance(sprite, DemoWaveSprite) and self.rect.collidepoint(sprite.rect.center) and\
                    0 < self.frameCount:
                playSound("push_or_shoot_enemy.wav")
                self.animationCount = 1
                self.frameCount = 0
            elif isinstance(sprite, DemoPlayerSprite) and self.rect.colliderect(sprite.rect) and\
                    self.animationCount == 1:
                self.animationCount = 2
                self.frameCount = 0


class DemoWaveSprite(DemoSprite):
    def __init__(self, coordinates=(0, 0)):
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(0, 168, 68, 68, 2)
        self.rect = self.image.get_rect()

    def update(self):
        self.frameCount += 1
        if self.frameCount == 28:
            playSound("shoot_wave.wav")
        if 28 < self.frameCount:
            self.coordinates = (self.coordinates[0] - 8, self.coordinates[1])
            self.image = self.animationFrames[0]
            if self.frameCount % 2 == 0:
                self.image = self.animationFrames[1]


class DemoRubberTrapSprite(DemoSprite):
    def __init__(self, demoNumber=0, coordinates=(0, 0)):
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(0, 520, 96, 120, 6)
        self.demoNumber = demoNumber
        self.animated = False
        self.image = self.animationFrames[0]

    def update(self):
        self.frameCount += 1
        self.rect = pygame.Rect(self.coordinates[0] + 20, self.coordinates[1], 50, 120)
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
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.frameCount % 33 == 0:
                self.frameCount = 0
                self.animated = False
            if self.demoNumber == 0:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.animationFrames[0]

        for sprite in demoGroup:
            if isinstance(sprite, DemoPlayerSprite) and self.rect.collidepoint(sprite.rect.center) and\
                            not self.animated:
                playSound("bounce_rubber_or_player.wav")
                self.frameCount = sprite.frameCount = 0
                self.animated = True
                sprite.animated = True

    def setMonochromeImage(self):
        self.image = self.animationFrames[4]
        if self.demoNumber == 1:
            self.image = self.animationFrames[5]
            self.image = pygame.transform.flip(self.image, True, False)


class DemoWallSprite(DemoSprite):
    def __init__(self, demoNumber=0, coordinates=(0, 0)):
        super().__init__(coordinates)
        self.animationFrames = self.spriteSheet.getStripImages(680, 0, 255, 564)
        self.demoNumber = demoNumber
        self.image = self.animationFrames[0]
        if demoNumber == 2:
            self.image = self.animationFrames[1]
        self.rect = self.image.get_rect()

    def update(self):
        self.frameCount += 1
        if self.demoNumber == 2:
            self.image = self.animationFrames[1]
            self.image = pygame.transform.flip(self.image, True, False)

        for sprite in demoGroup:
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


class DemoDisplay(pygame.sprite.Sprite):
    def __init__(self, demoNumber=0, coordinates=(0, 0)):
        super().__init__(demoGroup)
        self.spriteSheet = SpriteSheet("demo_display.png")
        self.animationFrames = []
        self.coordinates = coordinates
        self.frameCount = 0
        self.demoNumber = demoNumber

        self.animationFrames.extend(self.spriteSheet.getStripImages(0, 0, 380, 260))
        self.animationFrames.extend(self.spriteSheet.getStripImages(0, 260, 380, 260))

        self.image = self.animationFrames[self.demoNumber]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def setCoordinates(self):
        self.rect.topleft = self.coordinates

    def setMonochromeImage(self):
        pass


class DemoNameDisplay(DemoDisplay):
    def __init__(self, demoNumber=0, coordinates=(0, 0)):
        super().__init__(demoNumber, coordinates)

        self.image = self.spriteSheet.getSheetImage(0, 520, 365, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()


def initialize():
    DemoPlayerSprite.facingDirection = Directions.RIGHT
    DemoPlayerSprite.paused = False
    DemoPlayerSprite.swingValue = (0, 0)
