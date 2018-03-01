import pygame
import os
import random

SCREEN_SIZE = (512, 448)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

BLACK = (0, 0, 0)
gameFolder = os.path.dirname(__file__)
backgroundFolder = os.path.join(gameFolder, "Backgrounds")

_imageLibrary = {}


def getImage(imagePath):
    global _imageLibrary
    image = _imageLibrary.get(imagePath)
    if image is None:
        fullPath = os.path.join(backgroundFolder, imagePath)
        try:
            image = pygame.image.load(fullPath).convert()
            _imageLibrary[imagePath] = image
        except pygame.error:
            print("ERROR: Cannot find image '{}'".format(imagePath))
            pygame.quit()
            sys.exit()
    return image


class Level:
    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        self.image = None
        self.standardImage = None
        self.lightImage = None
        self.itemTiles = []  # 9 wide, 7 high
        self.rubberTilesHorizontal = rubberTilesHorizontal
        self.rubberTilesVertical = rubberTilesVertical
        self.goldTilesHorizontal = goldTilesHorizontal
        self.goldTilesVertical = goldTilesVertical
        self.activeRubberTraps = []
        self.goldCount = 0
        self.playerStartPosition = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.blackHolePositions = []
        self.levelBorderRects = []
        self.isFlashing = False
        self.frameCount = 0
        # 50x50 tiles

    def initialize(self):
        self.goldCount = len(self.goldTilesVertical) + len(self.goldTilesHorizontal)
        self.isFlashing = False
        self.image = self.standardImage

    def flashBoard(self):
        if self.isFlashing:
            self.frameCount += 1
            if self.frameCount % 12 < 7:
                self.image = self.standardImage
            else:
                self.image = self.lightImage
            if self.frameCount == 12:
                self.frameCount = 0


class BoardOneLevel(Level):
    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        super().__init__(rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical)
        self.image = getImage("background_1A.png")
        self.image.set_colorkey(BLACK)
        self.standardImage = getImage("background_1A.png")
        self.lightImage = getImage("background_1B.png")
        self.playerStartPosition = [(2, 1), (10, 1), (3, 7), (9, 7)]
        self.blackHolePositions = [(5, 4)]
        self.levelBorderRects = [pygame.Rect(0, 0, 80, 84), pygame.Rect(0, 0, 512, 36), pygame.Rect(0, 0, 39, 448),
                                 pygame.Rect(432, 0, 80, 84), pygame.Rect(477, 0, 39, 448),
                                 pygame.Rect(0, 380, 80, 84), pygame.Rect(432, 380, 80, 84),
                                 pygame.Rect(0, 426, 512, 36)]


class BoardTwoLevel(Level):
    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        super().__init__(rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical)
        self.image = getImage("background_2A.png")
        self.image.set_colorkey(BLACK)
        self.standardImage = getImage("background_2A.png")
        self.lightImage = getImage("background_2B.png")
        self.playerStartPosition = [(5, 0), (7, 0), (2, 5), (10, 5)]
        self.blackHolePositions = [(2, 6), (8, 6)]
        self.levelBorderRects = [pygame.Rect(0, 0, 80, 84), pygame.Rect(0, 0, 512, 36), pygame.Rect(0, 0, 39, 448),
                                 pygame.Rect(432, 0, 80, 84), pygame.Rect(477, 0, 39, 448),
                                 pygame.Rect(0, 380, 80, 84), pygame.Rect(432, 380, 80, 84),
                                 pygame.Rect(0, 426, 512, 36)]


class BoardThreeLevel(Level):
    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        super().__init__(rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical)
        self.image = getImage("background_3A.png")
        self.image.set_colorkey(BLACK)
        self.standardImage = getImage("background_3A.png")
        self.lightImage = getImage("background_3B.png")
        self.playerStartPosition = [(6, 1), (6, 6), (2, 3), (10, 3)]
        self.blackHolePositions = [(4, 4), (6, 4)]
        self.levelBorderRects = [pygame.Rect(0, 0, 512, 36), pygame.Rect(0, 0, 39, 448), pygame.Rect(477, 0, 39, 448),
                                 pygame.Rect(0, 426, 512, 36), pygame.Rect(190, 0, 134, 84),
                                 pygame.Rect(190, 380, 134, 84)]


class BoardFourLevel(Level):
    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        super().__init__(rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical)
        self.image = getImage("background_4A.png")
        self.image.set_colorkey(BLACK)
        self.standardImage = getImage("background_4A.png")
        self.lightImage = getImage("background_4B.png")
        self.playerStartPosition = [(5, 0), (7, 0), (2, 7), (10, 7)]
        self.blackHolePositions = [(2, 2), (8, 2), (4, 6), (6, 6)]
        self.levelBorderRects = [pygame.Rect(0, 0, 512, 36), pygame.Rect(238, 0, 36, 132),
                                 pygame.Rect(238, 346, 36, 132), pygame.Rect(0, 426, 512, 36),
                                 pygame.Rect(0, 92, 38, 280), pygame.Rect(476, 92, 38, 280)]


class BoardFiveLevel(Level):
    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        super().__init__(rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical)
        self.image = getImage("background_5A.png")
        self.image.set_colorkey(BLACK)
        self.standardImage = getImage("background_5A.png")
        self.lightImage = getImage("background_5B.png")
        self.playerStartPosition = [(2, 0), (10, 0), (4, 7), (6, 7)]
        self.blackHolePositions = [(2, 4), (4, 4), (6, 4), (8, 4)]
        self.activeRubberTraps = [(1, 4), (9, 4)]
        self.levelBorderRects = [pygame.Rect(0, 0, 512, 36), pygame.Rect(238, 0, 40, 84), pygame.Rect(0, 426, 512, 36),
                                 pygame.Rect(238, 380, 40, 84), pygame.Rect(0, 0, 36, 84), pygame.Rect(478, 0, 36, 84),
                                 pygame.Rect(0, 380, 36, 84), pygame.Rect(478, 380, 36, 84)]


class BonusLevel(Level):
    def __init__(self):
        goldTilesHorizontal = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (2, 2), (3, 2), (4, 2), (5, 2),
                               (6, 2), (7, 2), (8, 2), (2, 3), (8, 3), (2, 4), (8, 4), (2, 5), (8, 5), (2, 6), (3, 6),
                               (4, 6), (5, 6), (6, 6), (7, 6), (8, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                               (8, 7)]
        goldTilesVertical = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (2, 2), (3, 2), (8, 2),
                             (9, 2), (2, 3), (3, 3), (8, 3), (9, 3), (2, 4), (3, 4), (8, 4), (9, 4), (2, 5), (3, 5),
                             (8, 5), (9, 5), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6)]
        super().__init__([], [], goldTilesHorizontal, goldTilesVertical)
        self.image = getImage("background_6A.png")
        self.image.set_colorkey(BLACK)
        self.standardImage = getImage("background_6A.png")
        self.lightImage = getImage("background_6B.png")
        self.playerStartPosition = [(5, 1), (7, 1), (4, 6), (8, 6)]
        # self.playerStartPosition = [(2, 4), (9, 4)]
        self.levelBorderRects = [pygame.Rect(0, 0, 512, 36), pygame.Rect(188, 186, 136, 94),
                                 pygame.Rect(0, 426, 512, 36), pygame.Rect(0, 0, 39, 448),
                                 pygame.Rect(477, 0, 39, 448)]


HEART = BoardOneLevel([], [(4, 3), (7, 3)],
                      [(3, 1), (4, 1), (6, 1), (7, 1), (2, 2), (5, 2), (8, 2), (2, 4), (8, 4), (3, 5), (7, 5), (4, 6),
                       (6, 6), (5, 7)],
                      [(3, 1), (5, 1), (6, 1), (8, 1), (2, 2), (9, 2), (2, 3), (9, 3), (3, 4), (8, 4), (4, 5), (7, 5),
                       (5, 6), (6, 6)])
HOUSE = BoardOneLevel([], [(4, 5), (7, 5)],
                      [(4, 1), (5, 1), (6, 1), (3, 2), (7, 2), (2, 3), (8, 3), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
                       (7, 4), (8, 4), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)],
                      [(4, 1), (7, 1), (3, 2), (8, 2), (2, 3), (9, 3), (3, 4), (8, 4), (3, 5), (8, 5), (3, 6), (8, 6)])
FACE = BoardOneLevel([(2, 4), (8, 4)], [],
                     [(4, 1), (6, 1), (4, 3), (6, 3), (2, 5), (8, 5), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
                      (8, 6), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)],
                     [(4, 1), (5, 1), (6, 1), (7, 1), (4, 2), (5, 2), (6, 2), (7, 2), (2, 5), (3, 5), (8, 5), (9, 5),
                      (3, 6), (8, 6)])
HUMAN = BoardOneLevel([(5, 3)], [],
                      [(5, 1), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (2, 3), (3, 3), (7, 3), (8, 3), (2, 4), (8, 4),
                       (5, 6), (4, 7), (6, 7)],
                      [(5, 1), (6, 1), (3, 2), (8, 2), (2, 3), (3, 3), (4, 3), (7, 3), (8, 3), (9, 3), (4, 4), (7, 4),
                       (4, 5), (7, 5), (4, 6), (5, 6), (6, 6), (7, 6)])
BUBBLES = BoardOneLevel([], [],
                        [],
                        [])
KE = BoardOneLevel([], [],
                   [],
                   [])
TELEVISION = BoardOneLevel([], [],
                           [],
                           [])
KOOPA = BoardOneLevel([], [],
                      [],
                      [])
CLOWN = BoardTwoLevel([(5, 2)], [(4, 6), (7, 6)],
                      [(3, 2), (7, 2), (2, 3), (4, 3), (6, 3), (8, 3), (2, 4), (4, 4), (6, 4), (8, 4), (3, 5), (5, 5),
                       (7, 5), (5, 7)],
                      [(3, 2), (4, 2), (7, 2), (8, 2), (2, 3), (5, 3), (6, 3), (9, 3), (3, 4), (4, 4), (7, 4), (8, 4),
                       (5, 5), (6, 5), (5, 6), (6, 6)])
SPADE = BoardTwoLevel([(5, 3)], [],
                      [(5, 1), (4, 2), (6, 2), (3, 3), (7, 3), (5, 4), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (4, 6),
                       (6, 6), (4, 7), (5, 7), (6, 7)],
                      [(5, 1), (6, 1), (4, 2), (7, 2), (3, 3), (8, 3), (3, 4), (5, 4), (6, 4), (8, 4), (5, 5), (6, 5),
                       (4, 6), (7, 6)])
MOUSE = BoardTwoLevel([], [(5, 3), (6, 3)],
                      [(3, 1), (7, 1), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (3, 3), (7, 3), (3, 5), (5, 5), (7, 5),
                       (4, 6), (5, 6), (6, 6), (5, 7)],
                      [(3, 1), (4, 1), (7, 1), (8, 1), (4, 2), (7, 2), (3, 3), (8, 3), (3, 4), (8, 4), (4, 5), (5, 5),
                       (6, 5), (7, 5), (5, 6), (6, 6)])
EAGLE = BoardTwoLevel([(4, 4), (6, 4)], [],
                      [(5, 1), (6, 1), (6, 2), (2, 3), (3, 3), (4, 3), (6, 3), (7, 3), (8, 3), (2, 4), (8, 4), (3, 5),
                       (4, 5), (6, 5), (7, 5), (4, 6), (5, 6), (6, 6), (4, 7), (6, 7)],
                      [(5, 1), (7, 1), (5, 2), (6, 2), (2, 3), (9, 3), (3, 4), (8, 4), (5, 5), (6, 5), (4, 6), (5, 6),
                       (6, 6), (7, 6)])
RAIN = BoardTwoLevel([], [],
                     [],
                     [])
CAR = BoardTwoLevel([], [],
                    [],
                    [])
MUSHROOM = BoardTwoLevel([], [],
                         [],
                         [])
SKULL = BoardTwoLevel([], [],
                      [],
                      [])
SUBMARINE = BoardThreeLevel([], [(3, 1), (8, 1)],
                            [(4, 3), (5, 3), (8, 3), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (7, 5),
                             (8, 5), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (8, 6)],
                            [(5, 2), (4, 3), (6, 3), (8, 3), (9, 3), (2, 4), (8, 4), (2, 5), (7, 5), (8, 5), (9, 5)])
GLASSES = BoardThreeLevel([(3, 2), (7, 2)], [],
                          [(3, 3), (4, 3), (6, 3), (7, 3), (2, 4), (5, 4), (8, 4), (3, 6), (4, 6), (6, 6), (7, 6)],
                          [(2, 1), (9, 1), (2, 2), (9, 2), (2, 3), (3, 3), (5, 3), (6, 3), (8, 3), (9, 3), (3, 4),
                           (5, 4), (6, 4), (8, 4), (3, 5), (5, 5), (6, 5), (8, 5)])
KOALA = BoardThreeLevel([(4, 3), (6, 3), (2, 6), (8, 6)], [],
                        [(2, 1), (8, 1), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (2, 3), (8, 3), (3, 5), (5, 5),
                         (7, 5), (4, 6), (5, 6), (6, 6)],
                        [(2, 1), (3, 1), (8, 1), (9, 1), (2, 2), (9, 2), (3, 3), (8, 3), (3, 4), (8, 4), (4, 5),
                         (5, 5), (6, 5), (7, 5)])
BUTTERFLY = BoardThreeLevel([], [(5, 2), (6, 2)],
                            [(2, 2), (8, 2), (3, 3), (7, 3), (4, 4), (5, 4), (6, 4), (4, 5), (6, 5), (2, 6), (3, 6),
                             (5, 6), (7, 6), (8, 6)],
                            [(2, 2), (3, 2), (8, 2), (9, 2), (2, 3), (4, 3), (7, 3), (9, 3), (2, 4), (5, 4), (6, 4),
                             (9, 4), (2, 5), (4, 5), (5, 5), (6, 5), (7, 5), (9, 5)])
FISH = BoardThreeLevel([], [],
                       [],
                       [])
CLU_CLU = BoardThreeLevel([], [],
                          [],
                          [])
CROWN = BoardThreeLevel([], [],
                        [],
                        [])
SWORD_SHIELD = BoardThreeLevel([], [],
                               [],
                               [])
HOLE = BoardFourLevel([(3, 3), (7, 3)], [(4, 4), (7, 4)],
                      [(3, 1), (7, 1), (3, 2), (7, 2), (5, 3), (2, 4), (5, 4), (8, 4), (2, 5), (5, 5), (8, 5), (3, 6),
                       (7, 6), (3, 7), (7, 7)],
                      [(3, 1), (4, 1), (7, 1), (8, 1), (5, 3), (6, 3), (2, 4), (3, 4), (5, 4), (6, 4), (8, 4), (9, 4),
                       (3, 6), (4, 6), (7, 6), (8, 6)])
KEY = BoardFourLevel([(2, 4), (4, 4), (6, 4), (8, 4)], [],
                     [(2, 1), (8, 1), (3, 2), (7, 2), (2, 3), (3, 3), (7, 3), (8, 3), (2, 5), (3, 5), (7, 5), (8, 5),
                      (2, 6), (8, 6), (3, 7), (7, 7)],
                     [(2, 1), (3, 1), (8, 1), (9, 1), (2, 2), (4, 2), (7, 2), (9, 2), (2, 5), (4, 5), (7, 5), (9, 5),
                      (3, 6), (4, 6), (7, 6), (8, 6)])
RIBBON = BoardFourLevel([(2, 4), (5, 4), (8, 4)], [],
                        [(2, 2), (3, 2), (7, 2), (8, 2), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
                         (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (2, 6), (3, 6), (7, 6), (8, 6)],
                        [(2, 2), (4, 2), (7, 2), (9, 2), (4, 3), (7, 3), (4, 4), (7, 4), (2, 5), (4, 5), (7, 5),
                         (9, 5)])
LETTER_H = BoardFourLevel([(4, 4), (6, 4)], [(3, 3), (8, 3), (3, 5), (8, 5)],
                          [(2, 1), (3, 1), (7, 1), (8, 1), (4, 3), (5, 3), (6, 3), (4, 5), (5, 5), (6, 5), (2, 7),
                           (3, 7), (7, 7), (8, 7)],
                          [(2, 1), (4, 1), (7, 1), (9, 1), (2, 2), (4, 2), (7, 2), (9, 2), (2, 3), (9, 3), (2, 4),
                           (9, 4), (2, 5), (4, 5), (7, 5), (9, 5), (2, 6), (4, 6), (7, 6), (9, 6)])
PUNCTUATION = BoardFourLevel([], [],
                             [],
                             [])
FROWN = BoardFourLevel([], [],
                       [],
                       [])
PYTHON = BoardFourLevel([], [],
                        [],
                        [])
FLIP = BoardFourLevel([], [],
                      [],
                      [])
SPIDER = BoardFiveLevel([(3, 4), (7, 4)], [(1, 2), (4, 2), (7, 2), (4, 5), (7, 5), (10, 5)],
                        [(2, 1), (8, 1), (5, 2), (2, 3), (8, 3), (2, 5), (8, 5), (5, 6), (2, 7), (8, 7)],
                        [(3, 1), (8, 1), (2, 2), (9, 2), (5, 3), (6, 3), (5, 4), (6, 4), (2, 5), (9, 5), (3, 6),
                         (8, 6)])
LETTER_X = BoardFiveLevel([(5, 3), (5, 5)], [(3, 1), (8, 1), (10, 2), (1, 5), (3, 6), (8, 6)],
                          [(4, 2), (5, 2), (6, 2), (2, 3), (8, 3), (5, 4), (2, 5), (8, 5), (4, 6), (5, 6), (6, 6)],
                          [(4, 1), (7, 1), (2, 2), (9, 2), (3, 3), (8, 3), (3, 4), (8, 4), (2, 5), (9, 5), (4, 6),
                           (7, 6)])
BOX = BoardFiveLevel([(5, 3), (3, 4), (7, 4), (5, 5)], [(3, 2), (8, 2), (3, 5), (8, 5)],
                     [(2, 1), (3, 1), (7, 1), (8, 1), (4, 2), (6, 2), (4, 6), (6, 6), (2, 7), (3, 7), (7, 7), (8, 7)],
                     [(1, 2), (2, 2), (4, 2), (7, 2), (9, 2), (10, 2), (1, 5), (2, 5), (4, 5), (7, 5), (9, 5),
                      (10, 5)])
DIAMOND = BoardFiveLevel([(3, 4), (5, 4), (7, 4)], [(4, 1), (7, 1), (4, 6), (7, 6)],
                         [(2, 2), (5, 2), (8, 2), (1, 3), (3, 3), (5, 3), (7, 3), (9, 3), (1, 5), (3, 5), (5, 5),
                          (7, 5), (9, 5), (2, 6), (5, 6), (8, 6)],
                         [(3, 1), (8, 1), (2, 2), (9, 2), (2, 5), (9, 5), (3, 6), (8, 6)])
INVERTED_DIAMOND = BoardFiveLevel([(3, 6), (7, 6)], [(3, 2), (8, 2)],
                                  [(2, 1), (8, 1), (1, 2), (9, 2), (5, 3), (3, 5), (5, 5), (7, 5), (1, 6), (9, 6),
                                   (2, 7), (8, 7)],
                                  [(2, 1), (9, 1), (1, 2), (10, 2), (3, 4), (8, 4), (1, 5), (10, 5), (2, 6), (9, 6)])
BOX_PLUS = BoardFiveLevel([], [(2, 2), (9, 2), (4, 5), (7, 5)],
                          [(2, 1), (8, 1), (5, 2), (5, 3), (5, 5), (5, 6), (3, 7), (7, 7)],
                          [(1, 2), (3, 2), (5, 2), (6, 2), (8, 2), (10, 2), (5, 3), (6, 3), (5, 4), (6, 4), (1, 5),
                           (2, 5), (3, 5), (5, 5), (6, 5), (8, 5), (9, 5), (10, 5)])
CRUSHER = BoardFiveLevel([(4, 2), (6, 6)], [(6, 3), (5, 4)],
                         [(2, 1), (8, 1), (6, 2), (1, 3), (9, 3), (1, 5), (9, 5), (4, 6), (2, 7), (8, 7)],
                         [(2, 1), (3, 1), (8, 1), (9, 1), (1, 2), (2, 2), (3, 2), (8, 2), (9, 2), (10, 2), (3, 3),
                          (8, 3), (3, 4), (8, 4), (1, 5), (2, 5), (3, 5), (8, 5), (9, 5), (10, 5), (2, 6), (3, 6),
                          (8, 6), (9, 6)])
KEY_PLUS = BoardFiveLevel([(3, 4), (5, 4), (7, 4)], [],
                          [(2, 1), (8, 1), (1, 2), (5, 2), (9, 2), (1, 3), (2, 3), (4, 3), (6, 3), (8, 3), (9, 3),
                           (1, 5), (2, 5), (4, 5), (6, 5), (8, 5), (9, 5), (1, 6), (5, 6), (9, 6), (2, 7), (8, 7)],
                          [(2, 1), (3, 1), (8, 1), (9, 1), (1, 2), (3, 2), (5, 2), (6, 2), (8, 2), (10, 2), (1, 5),
                           (3, 5), (5, 5), (6, 5), (8, 5), (10, 5), (2, 6), (3, 6), (8, 6), (9, 6)])
BONUS_LEVEL = BonusLevel()

# boardOneLevels = [HEART, HOUSE, FACE, HUMAN, BUBBLES, KE, TELEVISION, KOOPA]
# boardTwoLevels = [CLOWN, SPADE, MOUSE, EAGLE, RAIN, CAR, MUSHROOM, SKULL]
# boardThreeLevels = [SUBMARINE, GLASSES, KOALA, BUTTERFLY, FISH, CLU_CLU, CROWN, SWORD_SHIELD]
# boardFourLevels = [HOLE, KEY, RIBBON, LETTER_H, PUNCTUATION, FROWN, PYTHON, FLIP]
# boardFiveLevels = [SPIDER, LETTER_X, BOX, DIAMOND, INVERTED_DIAMOND, BOX_PLUS, CRUSHER, KEY_PLUS]
boardOneLevels = [HEART, HOUSE, FACE, HUMAN]
boardTwoLevels = [CLOWN, SPADE, MOUSE, EAGLE]
boardThreeLevels = [SUBMARINE, GLASSES, KOALA, BUTTERFLY]
boardFourLevels = [HOLE, KEY, RIBBON, LETTER_H]
boardFiveLevels = [SPIDER, LETTER_X, BOX, DIAMOND]

allBoardsList = [boardOneLevels, boardTwoLevels, boardThreeLevels, boardFourLevels, boardFiveLevels]


def getLevelOrder():
    random.shuffle(boardOneLevels)
    newLevelOrder = [boardOneLevels[0]]
    for boardList in allBoardsList[1:]:
        random.shuffle(boardList)
    for num in range(4):
        for boardList in allBoardsList[1:]:
            newLevelOrder.extend(boardList[num])
    return newLevelOrder
