from game.gameplay.level import BonusLevel
from game.sprites.black_hole import BlackHoleSprite
from game.sprites.gold import GoldSprite
from game.sprites.item import initializeLevelItems
from game.sprites.player import PlayerSprite
from game.sprites.trap import RubberTrapSprite
import game.tools.constants as c


def setLevelSprites(level):
    """Prepare the sprites for the level. Remove all leftover sprites from the previous level and set the
    coordinates of the item sprites, gold sprites, rubber trap sprites, and black hole sprites for the level
    being played.

    Args:
        level: A Level object representing the current level being played.
    """
    for group in c.oneLevelOnlyGroups:
        group.empty()

    level.initialize()
    initializeLevelItems(level)
    goldList = []
    rubberList = []
    for (x, y) in level.goldTilesVertical:
        goldList.append(GoldSprite())
        goldList[-1].setCoordinates(-25 + 48 * x, 49 + 48 * y)
    for (x, y) in level.goldTilesHorizontal:
        goldList.append(GoldSprite())
        goldList[-1].isHorizontal = True
        goldList[-1].setCoordinates(-1 + 48 * x, 25 + 48 * y)
    for (x, y) in level.rubberTilesVertical:
        rubberList.append(RubberTrapSprite())
        rubberList[-1].setCoordinates(-36 + 48 * x, 36 + 48 * y)
    for (x, y) in level.rubberTilesHorizontal:
        rubberList.append(RubberTrapSprite())
        rubberList[-1].isHorizontal = True
        rubberList[-1].setCoordinates(-14 + 48 * x, 14 + 48 * y)
    for (x, y) in level.activeRubberTraps:
        rubberList.append(RubberTrapSprite())
        rubberList[-1].isHorizontal = True
        rubberList[-1].trapState = c.OtherStates.REVEALED
        rubberList[-1].setCoordinates(-14 + 48 * x, 14 + 48 * y)
        rubberList[-1].update()
    BlackHoleSprite.reset()
    c.blackHoleGroup.add(BlackHoleSprite() for _ in range(len(level.blackHolePositions)))
    for (x, y), hole in zip(level.blackHolePositions, c.blackHoleGroup):
        hole.initialize(-1 + 48 * x, 49 + 48 * y)


def setLevelTime(level, levelCount):
    """Get and return the time the players have to complete the current level, determined by levelCount.

    The time they are given depends on whether the level is a bonus level and how many levels have been played
    this game.
    The first 21 levels follow a particular pattern for how much time is given. Since the boardOneLevel instance
    is never replayed, all following levels follow a 20-step pattern for how much time is given.

    Args:
        level: A Level object representing the current level being played.
        levelCount: An integer storing the current number of levels played this game.

    Returns:
        timeCount: An integer representing how much time the players are initially given to complete the level.
    """
    if isinstance(level, BonusLevel):
        timeCount = 300
    elif levelCount in range(5, 11) or (levelCount > 21 and levelCount % 20 in range(6, 11)):
        timeCount = 700
    elif levelCount in range(11, 16) or (levelCount > 21 and levelCount % 20 in range(11, 18)):
        timeCount = 600
    elif levelCount in range(16, 21) or (levelCount > 21 and (levelCount % 20 > 16 or levelCount % 20 == 0)):
        timeCount = 500
    else:
        timeCount = 800
    return timeCount


def setLevelConstants(levelCount):
    """Set the movement and rotation speed values for the players, depending on levelCount. Set levelCount for
    the GoldSprite class.

    The speed values depend on how many levels have been played this game.
    The first 21 levels follow a particular speed value pattern. Since the boardOneLevel instance is never
    replayed, all following levels follow a 20-step pattern for how much time is given.
    While rotation speed follows an inconsistent pattern, movement speed follows a simple pattern: It starts at a
    slow speed, increases on level 2, then increases more every 3 levels played.
    At level 21 and every 20 levels thereafter, it resets to its initial value and repeats the pattern.

    At levels above 21, gold sprites behave slightly differently.

    Args:
        levelCount: An integer storing the current number of levels played this game.
    """
    if levelCount == 1 or (levelCount > 21 and (levelCount - 2) % 20 == 0):
        PlayerSprite.rotationSpeed = 4.24
    elif levelCount in range(2, 5) or (levelCount > 21 and (levelCount - 2) % 20 in range(1, 4)):
        PlayerSprite.rotationSpeed = 5.63
    elif levelCount in range(5, 14) or (levelCount > 21 and (levelCount - 2) % 20 in range(4, 13)):
        PlayerSprite.rotationSpeed = 7.06
    else:
        PlayerSprite.rotationSpeed = 8.47

    speedValues = [2.12, 3.15, 3.62, 3.85, 4.12, 4.33, 4.62, 4.89]
    if levelCount == 1:
        movementIndex = 0
    elif levelCount < 22:
        movementIndex = (levelCount + 1) // 3
    elif (levelCount - 21) % 20 == 0:
        # This line is included because otherwise, if levelCount is 41, 61, 81..., the below formula would set
        # movementIndex to 0 instead of 7, as is desired.

        movementIndex = 7
    else:
        movementIndex = ((levelCount - 21) % 20 + 1) // 3
    PlayerSprite.movementSpeed = speedValues[movementIndex]
    GoldSprite.levelCount = levelCount
