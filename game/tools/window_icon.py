import pygame as pg
import os

from game.sprites.sprite_sheet import SpriteSheet
import game.tools.constants as c


ICON_SHEET = SpriteSheet("display.png")
ICON = pg.image.load(os.path.join(c.RESOURCE_FOLDER, "game_display_icon.png")).convert()
ICON.set_colorkey(c.GREEN)
pg.display.set_icon(ICON)
