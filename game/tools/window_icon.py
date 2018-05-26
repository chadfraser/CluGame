import pygame as pg
import os

import game.tools.constants as c


ICON = pg.image.load(os.path.join(c.RESOURCE_FOLDER, "game_display_icon.png")).convert()
ICON.set_colorkey(c.GREEN)
pg.display.set_icon(ICON)
