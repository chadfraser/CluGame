import pygame as pg

import game.tools.constants as c
from game.tools.asset_cache import getImage


class SpriteSheet:
    """Create a sprite sheet object using an image file in the sprite sheet folder.

    The sprite sheet object should be used to create a sprite sheet attribute for sprite classes.
    This class just stores the image file passed to it and provides methods for separating that file into smaller
    images.
    These separated images should be stored in a list or dict in each sprite class, so those images can be
    accessed as needed.

    Attributes:
        imageName: The string of the file for the sprite sheet image file, not including the file path.
    """

    def __init__(self, imageName):
        """Init SpriteSheet with the imageName string."""
        self.sheet = getImage(c.SPRITE_SHEET_FOLDER, imageName)

    def getSheetImage(self, x, y, width, height, key=c.BLACK):
        """Take a rectangular segment of self.sheet and return it as a Surface object.

        This should be used to get a single image from the sprite sheet. To get multiple images in a row, use
        getStripImage instead.

        Args:
            x: An integer x coordinate of the left edge of the desired segment.
            y: An integer y coordinate of the top edge of the desired segment.
            width: An integer width of the desired Surface object.
            height: An integer height of the desired Surface object.
            key: A tuple representing the color key used for transparency in the returned image.

        Returns:
            image: The desired segment as a Surface object with the above color key.
        """
        image = pg.Surface([width, height]).convert()
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(key)
        return image

    def getStripImages(self, x, y, width, height, numberOfImages=0, key=c.BLACK):
        """Take a rectangular segment of self.sheet and return it as a list of Surface objects.

        This method only returns a row of images from the sprite sheet. If you need multiple images in a column,
        you will have to call this method multiple times.
        This should be used to get multiple images from the sprite sheet at once. To get a single image, use
        getStripImage instead.

        Args:
            x: An integer x coordinate of the left edge of the desired segment.
            y: An integer y coordinate of the top edge of the desired segment.
            width: An integer width of the desired Surface object.
            height: An integer height of the desired Surface object.
            numberOfImages: An integer count of how many Surface objects from the row are desired.
                If numberOfImages is 0, this method returns a list of as many Surface objects as possible with
                the above arguments.
                If numberOfImages is positive, this method returns a list of that many Surface objects with the
                above arguments.
                If the width of self.image is less than (width * numberOfImages), this method returns a list of
                as many segments of the passed width as possible.
            key: A tuple representing the color key used for transparency in the returned image.

        Returns:
            imageList: A list of the desired segments as Surface objects with the above color key.
        """
        spriteSheetWidth = self.sheet.get_size()[0]
        if numberOfImages != 0:
            spriteSheetWidth = width * numberOfImages + x
        imageList = []
        while x + width <= spriteSheetWidth:
            image = self.getSheetImage(x, y, width, height, key)
            imageList.append(image)
            x += width
        return imageList
