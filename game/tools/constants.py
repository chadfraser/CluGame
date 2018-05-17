from enum import Enum
import os
import pygame as pg


# # # FILE PATHS # # #

# GAME_FOLDER calls os.path.dirname twice to get the parent directory (As the resources folder is stored in the parent
# directory of constants.py).
GAME_FOLDER = os.path.dirname(os.path.dirname(__file__))
RESOURCE_FOLDER = os.path.join(GAME_FOLDER, "resources")
SPRITE_SHEET_FOLDER = os.path.join(RESOURCE_FOLDER, "sprite_sheets")
BACKGROUND_FOLDER = os.path.join(RESOURCE_FOLDER, "backgrounds")
MUSIC_FOLDER = os.path.join(RESOURCE_FOLDER, "music")

# # # MUSIC FILES # # #

TITLE_MUSIC = os.path.join(MUSIC_FOLDER, "music_title.mp3")
DEMO_MUSIC = os.path.join(MUSIC_FOLDER, "music_demo.mp3")
LEVEL_START_MUSIC = os.path.join(MUSIC_FOLDER, "music_level_start.mp3")
LEVEL_MUSIC = os.path.join(MUSIC_FOLDER, "music_level.mp3")
LOW_TIME_MUSIC = os.path.join(MUSIC_FOLDER, "music_low_time.mp3")
LEVEL_END_MUSIC = os.path.join(MUSIC_FOLDER, "music_level_end.mp3")
BONUS_LEVEL_MUSIC = os.path.join(MUSIC_FOLDER, "music_bonus.mp3")
GAME_OVER_MUSIC = os.path.join(MUSIC_FOLDER, "music_game_over.mp3")


# # # COLORS # # #

# Used as general background or font colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)

# Used as level background colors
DARK_RED = (168, 0, 16)
DARK_GREEN = (0, 80, 0)
DARK_BLUE = (36, 24, 140)
PURPLE = (68, 0, 156)
DARK_ORANGE = (124, 8, 0)

# Used as player-specific font colors
RED = (255, 0, 0)  # Red is also used as the color key for trap and display sprite sheets
HOT_PINK = (255, 0, 95)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  # Blue and yellow are also used for the UrchinSprite class
YELLOW = (255, 200, 15)

# Used as special menu font colors
ORANGE = (250, 150, 55)
PINK = (250, 115, 180)
CYAN = (60, 180, 250)


# # # PYGAME CONSTANTS # # #

pg.mixer.pre_init(frequency=44100, buffer=512)
pg.init()
pg.font.init()

CLOCK = pg.time.Clock()
FPS = 60


# # # FONT AND TEXT # # #

FONT_FILE = os.path.join(RESOURCE_FOLDER, "Nintendo NES.ttf")
FONT = pg.font.Font(FONT_FILE, 16)
DEMO_FONT = pg.font.Font(FONT_FILE, 48)
CAPTION = "Clu Clu Land Special"


# # # DISPLAY CONSTANTS # # #

SCREEN_SIZE = (512, 448)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption(CAPTION)


class PlayerStates(Enum):
    """Possible states for the player sprites."""
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
    LEVEL_END = "level end"
    DEAD = "dead"


class ArmStates(Enum):
    """Possible states for the players' arm sprites."""
    EXTENDED = "extended"
    SWINGING = "swinging"
    OFF_SCREEN = "off screen"


class EnemyStates(Enum):
    """Possible states for the enemy sprites."""
    MOVING = "moving"
    BALL = "ball"
    SMALL_BALL = "small ball"
    WAITING = "waiting"
    EXPLODING = "exploding"
    OFF_SCREEN = "off screen"


class TextStates(Enum):
    """Possible states for the game over text sprites."""
    NOT_REVEALED = "not revealed"
    ONSCREEN = "onscreen"
    OFF_SCREEN = "off-screen"


class OtherStates(Enum):
    """Possible states for other miscellaneous sprites."""
    REVEALED = "revealed"
    UPSIDE_DOWN = "upside down"
    FLIPPING_UP = "flipping up"
    FLIPPING_DOWN = "flipping down"
    DELAYED_UP = "delayed up"
    DELAYED_DOWN = "delayed down"
    OFF_SCREEN = "off screen"
    COLLECTED = "collected"
    TRIGGERED = "triggered"
    DEAD = "dead"


class Directions(Enum):
    """Possible directions objects can be facing or moving.
    Includes the four cardinal directions, as well as clockwise and counter-clockwise.
    """
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    CLOCKWISE = "clockwise"
    COUNTER = "counter-clockwise"


# The directionsDict associates each string representation of the four cardinal directions with the corresponding
# Directions Enum, to assign the Enum value to a variable when passed the string.
# The directionList is ordered such that 90 * [index] is the number of degrees an image facing right would have to
# rotate to face that direction.

directionsDict = {"up": Directions.UP, "down": Directions.DOWN, "left": Directions.LEFT, "right": Directions.RIGHT}
directionList = [Directions.RIGHT, Directions.UP, Directions.LEFT, Directions.DOWN]

demoGroup = pg.sprite.Group()

displayGroup = pg.sprite.Group()
itemGroup = pg.sprite.Group()
blackHoleGroup = pg.sprite.Group()
enemyGroup = pg.sprite.Group()
goldGroup = pg.sprite.Group()
rubberGroup = pg.sprite.Group()
armGroup = pg.sprite.Group()
playerGroup = pg.sprite.Group()
attackGroup = pg.sprite.Group()
textGroup = pg.sprite.Group()


# oneLevelOnlyGroups includes all groups that should be deleted at the start of each level
# demoGroup is excluded from allGroups because we are not concerned with updating it during normal gameplay, as it only
# updates during the demo.

oneLevelOnlyGroups = (displayGroup, blackHoleGroup, enemyGroup, goldGroup, rubberGroup, attackGroup, textGroup)
allGroups = (displayGroup, itemGroup, blackHoleGroup, enemyGroup, goldGroup, rubberGroup, armGroup, playerGroup,
             attackGroup, textGroup)
