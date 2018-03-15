import pygame
import random

from game.tools.asset_cache import getImage
import game.tools.constants as c


class Level:
    """Create a new level object.

    This class should not be called directly. Only call its subclasses.

    Attributes:
        rubberTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal rubber
            traps.
        rubberTilesVertical: A list of tuples indicating which columns and rows to place vertical rubber traps.
        goldTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal gold sprites.
        goldTilesVertical: A list of tuples indicating which columns and rows to place vertical gold sprites.
    """

    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        """Init Level using the lists of tuples rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal,
        and goldTilesVertical.

        Instance variables:
            image: A None type object. Subclasses replace this with a Surface object of the image to be drawn for
                the current level.
            standardImage: A None type object. Subclasses replace this with a Surface object of the image to be
                seen in standard play of the current level.
            lightImage: A None type object. Subclasses replace this with a Surface object of a lighter variant of
                the image to be seen in standard play of the current level.
                Designed to be used when an ItemClock object is active, or to give the illusion of the level
                flashing.
            backgroundColor: A tuple indicating the color of the level's background.
            activeRubberTraps: An empty list. Subclasses replace this with a list of tuples indicating which
                columns and rows have horizontal rubber traps that begin the game in an active state.
            playerStartPositions: A list of four tuples indicating which columns and rows each player starts on.
            blackHolePositions: An empty list. Subclasses replace this with a list of tuples indicating which
                columns and start with a black hole sprite.
            itemTiles: An empty list. Subclasses replace this with a list of tuples indicating which columns and
                rows can have items spawned on them.
            levelBorderRects: An empty list. Subclasses replace this with a list of rect objects that form the
                boundaries of the level.
            isFlashing: A boolean indicating if the level should be in a flashing animation, switching between
                its standardImage and lightImage.
            frameCount: An integer that increases whenever the flashBoard method is called.
        """
        self.image = self.standardImage = self.lightImage = None
        self.backgroundColor = c.BLACK
        self.rubberTilesHorizontal = rubberTilesHorizontal
        self.rubberTilesVertical = rubberTilesVertical
        self.goldTilesHorizontal = goldTilesHorizontal
        self.goldTilesVertical = goldTilesVertical
        self.activeRubberTraps = []
        self.playerStartPosition = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.blackHolePositions = []
        self.itemTiles = []
        self.levelBorderRects = []
        self.isFlashing = False
        self.frameCount = 0

    def initialize(self):
        """Set the relevant variables of the level to its initial values."""
        self.isFlashing = False
        self.image = self.standardImage
        self.frameCount = 0

    def flashBoard(self):
        """Switch the level's image between standardImage and flashingImage every 6 frames."""
        if self.isFlashing:
            self.frameCount += 1
            if self.frameCount % 12 < 6:
                self.image = self.standardImage
            else:
                self.image = self.lightImage


class BoardOneLevel(Level):
    """Create a new object of the first variant of levels.

    Attributes:
        rubberTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal rubber
            traps.
        rubberTilesVertical: A list of tuples indicating which columns and rows to place vertical rubber traps.
        goldTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal gold sprites.
        goldTilesVertical: A list of tuples indicating which columns and rows to place vertical gold sprites.
    """

    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        """Init BoardOneLevel using the lists of tuples rubberTilesHorizontal, rubberTilesVertical,
        goldTilesHorizontal, and goldTilesVertical.

        Instance variables:
            standardImage: The image to be drawn for the level during standard gameplay.
            lightImage: A lighter variant of standardImage, designed to be used when an ItemClock object is
                active, or to give the illusion of the level flashing.
            image: The current image to be drawn for the level.
                Defaults to the standardImage.
            backgroundColor: A tuple indicating the color of the level's background.
            playerStartPositions: A list of four tuples indicating which columns and rows each player starts on.
            blackHolePositions: A list of four tuples indicating which columns and rows each black hole sprite
                starts on.
            itemTiles: A list of tuples indicating which columns and rows can have items spawned on them.
                This should include every tile that a player can reach, except those tiles that the players start
                on.
            levelBorderRects: A list of rect objects that form the boundaries of the level.
        """
        super().__init__(rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical)
        self.standardImage = getImage(c.BACKGROUND_FOLDER, "background_1A.png")
        self.lightImage = getImage(c.BACKGROUND_FOLDER, "background_1B.png")
        self.image = self.standardImage
        self.backgroundColor = c.DARK_RED
        self.playerStartPosition = [(1, 1), (9, 1), (2, 7), (8, 7)]
        self.blackHolePositions = [(5, 4)]
        self.itemTiles = [(x, y) for x in range(1, 10) for y in range(0, 8) if (x, y) not in self.playerStartPosition
                          and (x, y) not in self.blackHolePositions and (x, y) not in [(1, 0), (9, 0), (1, 7),
                                                                                       (9, 7)]]
        self.levelBorderRects = [pygame.Rect(0, 0, 80, 84), pygame.Rect(0, 0, 512, 36), pygame.Rect(0, 0, 39, 448),
                                 pygame.Rect(432, 0, 80, 84), pygame.Rect(477, 0, 39, 448),
                                 pygame.Rect(0, 380, 80, 84), pygame.Rect(432, 380, 80, 84),
                                 pygame.Rect(0, 426, 512, 36)]


class BoardTwoLevel(Level):
    """Create a new object of the second variant of levels.

    Attributes:
        rubberTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal rubber
            traps.
        rubberTilesVertical: A list of tuples indicating which columns and rows to place vertical rubber traps.
        goldTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal gold sprites.
        goldTilesVertical: A list of tuples indicating which columns and rows to place vertical gold sprites.
    """

    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        """Init BoardTwoLevel using the lists of tuples rubberTilesHorizontal, rubberTilesVertical,
        goldTilesHorizontal, and goldTilesVertical.

        Instance variables:
            standardImage: The image to be drawn for the level during standard gameplay.
            lightImage: A lighter variant of standardImage, designed to be used when an ItemClock object is
                active, or to give the illusion of the level flashing.
            image: The current image to be drawn for the level.
                Defaults to the standardImage.
            backgroundColor: A tuple indicating the color of the level's background.
            playerStartPositions: A list of four tuples indicating which columns and rows each player starts on.
            blackHolePositions: A list of four tuples indicating which columns and rows each black hole sprite
                starts on.
            itemTiles: A list of tuples indicating which columns and rows can have items spawned on them.
                This should include every tile that a player can reach, except those tiles that the players start
                on.
            levelBorderRects: A list of rect objects that form the boundaries of the level.
        """
        super().__init__(rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical)
        self.standardImage = getImage(c.BACKGROUND_FOLDER, "background_2A.png")
        self.lightImage = getImage(c.BACKGROUND_FOLDER, "background_2B.png")
        self.image = self.standardImage
        self.backgroundColor = c.DARK_GREEN
        self.playerStartPosition = [(4, 0), (6, 0), (1, 5), (9, 5)]
        self.blackHolePositions = [(2, 6), (8, 6)]
        self.itemTiles = [(x, y) for x in range(1, 10) for y in range(0, 8) if (x, y) not in self.playerStartPosition
                          and (x, y) not in self.blackHolePositions and (x, y) not in [(1, 0), (9, 0), (1, 7),
                                                                                       (9, 7)]]
        self.levelBorderRects = [pygame.Rect(0, 0, 80, 84), pygame.Rect(0, 0, 512, 36), pygame.Rect(0, 0, 39, 448),
                                 pygame.Rect(432, 0, 80, 84), pygame.Rect(477, 0, 39, 448),
                                 pygame.Rect(0, 380, 80, 84), pygame.Rect(432, 380, 80, 84),
                                 pygame.Rect(0, 426, 512, 36)]


class BoardThreeLevel(Level):
    """Create a new object of the third variant of levels.

    Attributes:
        rubberTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal rubber
            traps.
        rubberTilesVertical: A list of tuples indicating which columns and rows to place vertical rubber traps.
        goldTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal gold sprites.
        goldTilesVertical: A list of tuples indicating which columns and rows to place vertical gold sprites.
    """

    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        """Init BoardThreeLevel using the lists of tuples rubberTilesHorizontal, rubberTilesVertical,
        goldTilesHorizontal, and goldTilesVertical.

        Instance variables:
            standardImage: The image to be drawn for the level during standard gameplay.
            lightImage: A lighter variant of standardImage, designed to be used when an ItemClock object is
                active, or to give the illusion of the level flashing.
            image: The current image to be drawn for the level.
                Defaults to the standardImage.
            backgroundColor: A tuple indicating the color of the level's background.
            playerStartPositions: A list of four tuples indicating which columns and rows each player starts on.
            blackHolePositions: A list of four tuples indicating which columns and rows each black hole sprite
                starts on.
            itemTiles: A list of tuples indicating which columns and rows can have items spawned on them.
                This should include every tile that a player can reach, except those tiles that the players start
                on.
            levelBorderRects: A list of rect objects that form the boundaries of the level.
        """
        super().__init__(rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical)
        self.standardImage = getImage(c.BACKGROUND_FOLDER, "background_3A.png")
        self.lightImage = getImage(c.BACKGROUND_FOLDER, "background_3B.png")
        self.image = self.standardImage
        self.backgroundColor = c.DARK_BLUE
        self.playerStartPosition = [(4, 1), (4, 6), (1, 3), (9, 3)]
        self.blackHolePositions = [(4, 4), (6, 4)]
        self.itemTiles = [(x, y) for x in range(1, 10) for y in range(0, 8) if (x, y) not in self.playerStartPosition
                          and (x, y) not in self.blackHolePositions and (x, y) not in [(4, 0), (5, 0), (6, 0),
                                                                                       (4, 7), (5, 7), (6, 7)]]
        self.levelBorderRects = [pygame.Rect(0, 0, 512, 36), pygame.Rect(0, 0, 39, 448), pygame.Rect(477, 0, 39, 448),
                                 pygame.Rect(0, 426, 512, 36), pygame.Rect(190, 0, 134, 84),
                                 pygame.Rect(190, 380, 134, 84)]


class BoardFourLevel(Level):
    """Create a new object of the fourth variant of levels.

    Attributes:
        rubberTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal rubber
            traps.
        rubberTilesVertical: A list of tuples indicating which columns and rows to place vertical rubber traps.
        goldTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal gold sprites.
        goldTilesVertical: A list of tuples indicating which columns and rows to place vertical gold sprites.
    """

    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        """Init BoardFourLevel using the lists of tuples rubberTilesHorizontal, rubberTilesVertical,
        goldTilesHorizontal, and goldTilesVertical.

        Instance variables:
            standardImage: The image to be drawn for the level during standard gameplay.
            lightImage: A lighter variant of standardImage, designed to be used when an ItemClock object is
                active, or to give the illusion of the level flashing.
            image: The current image to be drawn for the level.
                Defaults to the standardImage.
            backgroundColor: A tuple indicating the color of the level's background.
            playerStartPositions: A list of four tuples indicating which columns and rows each player starts on.
            blackHolePositions: A list of four tuples indicating which columns and rows each black hole sprite
                starts on.
            itemTiles: A list of tuples indicating which columns and rows can have items spawned on them.
                This should include every tile that a player can reach, except those tiles that the players start
                on.
            levelBorderRects: A list of rect objects that form the boundaries of the level.
        """
        super().__init__(rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical)
        self.standardImage = getImage(c.BACKGROUND_FOLDER, "background_4A.png")
        self.lightImage = getImage(c.BACKGROUND_FOLDER, "background_4B.png")
        self.image = self.standardImage
        self.backgroundColor = c.PURPLE
        self.playerStartPosition = [(4, 0), (6, 0), (1, 7), (9, 7)]
        self.blackHolePositions = [(2, 2), (8, 2), (4, 6), (6, 6)]
        self.itemTiles = [(x, y) for x in range(0, 11) for y in range(0, 8) if (x, y) not in self.playerStartPosition
                          and (x, y) not in self.blackHolePositions and (x, y) not in [(5, 0), (0, 1), (5, 1), (10, 1),
                                                                                       (0, 2), (10, 2), (0, 3),
                                                                                       (10, 3), (0, 4), (10, 4),
                                                                                       (0, 5), (10, 5), (0, 6), (5, 6),
                                                                                       (10, 6), (5, 7)]]
        self.levelBorderRects = [pygame.Rect(0, 0, 512, 36), pygame.Rect(238, 0, 36, 132),
                                 pygame.Rect(238, 346, 36, 132), pygame.Rect(0, 426, 512, 36),
                                 pygame.Rect(0, 92, 38, 280), pygame.Rect(476, 92, 38, 280)]


class BoardFiveLevel(Level):
    """Create a new object of the fifth variant of levels.

    Attributes:
        rubberTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal rubber
            traps.
        rubberTilesVertical: A list of tuples indicating which columns and rows to place vertical rubber traps.
        goldTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal gold sprites.
        goldTilesVertical: A list of tuples indicating which columns and rows to place vertical gold sprites.
    """

    def __init__(self, rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical):
        """Init BoardFiveLevel using the lists of tuples rubberTilesHorizontal, rubberTilesVertical,
        goldTilesHorizontal, and goldTilesVertical.

        Instance variables:
            standardImage: The image to be drawn for the level during standard gameplay.
            lightImage: A lighter variant of standardImage, designed to be used when an ItemClock object is
                active, or to give the illusion of the level flashing.
            image: The current image to be drawn for the level.
                Defaults to the standardImage.
            backgroundColor: A tuple indicating the color of the level's background.
            activeRubberTraps: A list of tuples indicating which columns and rows have horizontal rubber traps
                which begin the game in an active state.
            playerStartPositions: A list of four tuples indicating which columns and rows each player starts on.
            blackHolePositions: A list of four tuples indicating which columns and rows each black hole sprite
                starts on.
            itemTiles: A list of tuples indicating which columns and rows can have items spawned on them.
                This should include every tile that a player can reach, except those tiles that the players start
                on.
            levelBorderRects: A list of rect objects that form the boundaries of the level.
        """
        super().__init__(rubberTilesHorizontal, rubberTilesVertical, goldTilesHorizontal, goldTilesVertical)
        self.standardImage = getImage(c.BACKGROUND_FOLDER, "background_5A.png")
        self.lightImage = getImage(c.BACKGROUND_FOLDER, "background_5B.png")
        self.image = self.standardImage
        self.backgroundColor = c.DARK_ORANGE
        self.activeRubberTraps = [(1, 4), (9, 4)]
        self.playerStartPosition = [(1, 0), (9, 0), (3, 7), (5, 7)]
        self.blackHolePositions = [(2, 4), (4, 4), (6, 4), (8, 4)]
        self.itemTiles = [(x, y) for x in range(0, 11) for y in range(0, 8) if (x, y) not in self.playerStartPosition
                          and (x, y) not in self.blackHolePositions and (x, y) not in [(0, 0), (5, 0), (10, 0),
                                                                                       (0, 7), (5, 7), (10, 7)]]
        self.levelBorderRects = [pygame.Rect(0, 0, 512, 36), pygame.Rect(238, 0, 40, 84), pygame.Rect(0, 426, 512, 36),
                                 pygame.Rect(238, 380, 40, 84), pygame.Rect(0, 0, 36, 84), pygame.Rect(478, 0, 36, 84),
                                 pygame.Rect(0, 380, 36, 84), pygame.Rect(478, 380, 36, 84)]


class BonusLevel(Level):
    """Create a new object of the sixth, bonus variant of levels.

    Note that since the bonus level style is unique, the arguments that are usually passed to the other level
    variants are instead created as constant instance variables in the bonus level __init__ method.
    """

    def __init__(self):
        """Init BonusLevel.

        Instance variables:
            goldTilesHorizontal: A list of tuples indicating which columns and rows to place horizontal gold
                sprites.
            goldTilesVertical: A list of tuples indicating which columns and rows to place vertical gold sprites.
            standardImage: The image to be drawn for the level during standard gameplay.
            lightImage: A lighter variant of standardImage, designed to be used when an ItemClock object is
                active, or to give the illusion of the level flashing.
            image: The current image to be drawn for the level.
                Defaults to the standardImage.
            backgroundColor: A tuple indicating the color of the level's background.
            playerStartPositions: A list of four tuples indicating which columns and rows each player starts on.
            levelBorderRects: A list of rect objects that form the boundaries of the level.
        """
        goldTilesHorizontal = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (2, 2), (3, 2), (4, 2), (5, 2),
                               (6, 2), (7, 2), (8, 2), (2, 3), (8, 3), (2, 4), (8, 4), (2, 5), (8, 5), (2, 6), (3, 6),
                               (4, 6), (5, 6), (6, 6), (7, 6), (8, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                               (8, 7)]
        goldTilesVertical = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (2, 2), (3, 2), (8, 2),
                             (9, 2), (2, 3), (3, 3), (8, 3), (9, 3), (2, 4), (3, 4), (8, 4), (9, 4), (2, 5), (3, 5),
                             (8, 5), (9, 5), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6)]
        super().__init__([], [], goldTilesHorizontal, goldTilesVertical)
        self.standardImage = getImage(c.BACKGROUND_FOLDER, "background_6A.png")
        self.lightImage = getImage(c.BACKGROUND_FOLDER, "background_6B.png")
        self.image = self.standardImage
        self.backgroundColor = c.DARK_RED
        self.playerStartPosition = [(5, 1), (7, 1), (4, 6), (8, 6)]
        self.levelBorderRects = [pygame.Rect(0, 0, 512, 36), pygame.Rect(188, 186, 136, 94),
                                 pygame.Rect(0, 426, 512, 36), pygame.Rect(0, 0, 39, 448),
                                 pygame.Rect(477, 0, 39, 448)]


# Create an instance of each of the 41 different level patterns. This ensures that there is exactly one copy of each
# level pattern at all times, with the proper gold tiles and rubber trap tiles.

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
# boardOneLevels = [HEART, HOUSE, FACE, HUMAN]

SAMPLE = BoardOneLevel([], [], [(3, 1)], [(3, 1)])

boardOneLevels = [SAMPLE]
boardTwoLevels = [CLOWN, SPADE, MOUSE, EAGLE]
boardThreeLevels = [SUBMARINE, GLASSES, KOALA, BUTTERFLY]
boardFourLevels = [HOLE, KEY, RIBBON, LETTER_H]
boardFiveLevels = [SPIDER, LETTER_X, BOX, DIAMOND]

allBoardsPastOneList = [boardTwoLevels, boardThreeLevels, boardFourLevels, boardFiveLevels]


def getLevelOrder():
    """Get a random order of the 21 levels to be played, including one of the boardOneLevels, one of the bonus
    levels, and four of each other variant of levels.

    Note that though the order of when each specific level instance is played is randomized, the order will
    always follow the following pattern, repeated endlessly:
        boardOneLevel, boardTwoLevel, boardThreeLevel, boardFourLevel, boardFiveLevel, BonusLevel
                       boardTwoLevel, boardThreeLevel, boardFourLevel, boardFiveLevel, BonusLevel
                       boardTwoLevel, boardThreeLevel, boardFourLevel, boardFiveLevel, BonusLevel
                       boardTwoLevel, boardThreeLevel, boardFourLevel, boardFiveLevel, BonusLevel

    Returns:
        A list of Level objects in the order to be played.
    """
    random.shuffle(boardOneLevels)
    newLevelOrder = [boardOneLevels[0]]
    for boardList in allBoardsPastOneList:
        random.shuffle(boardList)
    for num in range(4):
        for boardList in allBoardsPastOneList:
            newLevelOrder.append(boardList[num])
        newLevelOrder.append(BONUS_LEVEL)
    return newLevelOrder
