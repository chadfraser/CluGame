import pygame as pg

from game.sprites.sprite_sheet import SpriteSheet
import game.tools.constants as c


class TitleTextSprite(pg.sprite.Sprite):
    """Create a sprite of the text 'CLU' used in the title screen.

    Attributes:
        isLeft: A boolean indicating if this instance is the leftmost TitleTextSprite object.
    """

    def __init__(self, isLeft=True):
        """Init TitleTextSprite with the isLeft boolean.

        Instance variables:
            spriteSheet: The SpriteSheet object for the title sprite sheet image.
            animationFrames: A list of 13 Surface objects from the SpriteSheet object.
            coordinates: A tuple location to blit the sprite on the screen.
                If isLeft is True, then the coordinates are further to the left than if it is False.
            rotationCount: An integer tracking from where in animationFrame the sprite should take its next
                image.
            frameCount: An integer that increases whenever the update method is called.
                Used to control when other methods should be called.
            image: The current image to be drawn for the sprite.
                Defaults to the first image in animationFrames, the text 'CLU' facing backwards.
        """
        super().__init__()
        spriteSheet = SpriteSheet("title.png")
        self.animationFrames = []
        self.isLeft = isLeft
        if isLeft:
            self.coordinates = (98, 54)
        else:
            self.coordinates = (274, 54)
        self.rotationCount = self.frameCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 144, 82))
        self.animationFrames.extend(spriteSheet.getStripImages(0, 82, 144, 82))
        self.animationFrames.extend(spriteSheet.getStripImages(0, 164, 144, 82, 3))
        self.image = self.animationFrames[0]
        self.image.set_colorkey(c.BLACK)

    def update(self):
        """Increase frameCount. While frameCount is in a certain range, depending on if isLeft is true, calls the
        rotateAnimation method.
        """
        self.frameCount += 1
        if self.isLeft:
            if (20 < self.frameCount < 132 and self.frameCount % 2 == 1) or 289 < self.frameCount < 394:
                self.rotateAnimation()
        else:
            if (150 < self.frameCount < 272 and self.frameCount % 2 == 1) or 289 < self.frameCount < 394:
                self.rotateAnimation()
        self.image.set_colorkey(c.BLACK)

    def rotateAnimation(self):
        """Cycle through the animation frames of the Title Text Sprite object.
        If isLeft, this method cycles through the animation frames in the positive direction.
        Otherwise, this method cycles through the animation frames in the negative direction.
        This creates the illusion of the sprite image to be rotating left or right.
        """
        self.rotationCount += 1
        if self.isLeft:
            if self.rotationCount < len(self.animationFrames):
                self.image = self.animationFrames[self.rotationCount]
            else:
                self.rotationCount = 0
                self.image = self.animationFrames[0]
        else:
            if self.rotationCount < len(self.animationFrames):
                self.image = self.animationFrames[-self.rotationCount]
            else:
                self.rotationCount = 0
                self.image = self.animationFrames[-1]

    def setTitleImage(self):
        """Set the image of the sprite to its fifth animation frame, such that it appears facing forwards."""
        self.image = self.animationFrames[4]
        self.image.set_colorkey(c.BLACK)

    def setTitleImageBackwards(self):
        """Set the image of the sprite to its first animation frame, such that it appears facing backwards."""
        self.image = self.animationFrames[0]
        self.frameCount = self.rotationCount = 0
        self.image.set_colorkey(c.BLACK)


class TitleBoxSprite(pg.sprite.Sprite):
    """Create a sprite of the text 'LAND' and the title box surrounding it, used in the title screen."""

    def __init__(self):
        """Init TitleBoxSprite.

        Instance variables:
            spriteSheet: The SpriteSheet object for the title sprite sheet image.
            animationFrames: A list of 2 Surface objects from the SpriteSheet object.
            coordinates: A tuple location to blit the sprite on the screen.
            frameCount: An integer that increases whenever the update method is called.
                Used to control when other methods should be called.
            image: The current image to be drawn for the sprite.
                Defaults to the first image in animationFrames, the text 'CLU' facing backwards.
        """
        super().__init__()
        spriteSheet = SpriteSheet("display.png")
        self.animationFrames = []
        self.coordinates = (50, 22)
        self.frameCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 416, 242, key=c.RED))
        self.image = self.animationFrames[0]
        self.image.set_colorkey(c.RED)

    def update(self):
        """Increase frameCount. Sets the image of the sprite to be either of the Surface objects in
        animationFrames, depending on frameCount.
        """
        self.frameCount += 1
        if self.frameCount < 500 or self.frameCount % 10 > 4:
            self.image = self.animationFrames[0]
        else:
            self.image = self.animationFrames[1]
        self.image.set_colorkey(c.RED)

    def setTitleImage(self):
        """Set the image of the sprite to its first animation frame, such that it appears in color."""
        self.image = self.animationFrames[0]
        self.frameCount = 0
        self.image.set_colorkey(c.RED)
