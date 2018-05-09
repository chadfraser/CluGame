import pygame as pg
import random

from game.gameplay.level import BonusLevel
from game.sprites.player import PlayerSprite
from game.sprites.sprite_sheet import SpriteSheet
from game.sprites.urchin import UrchinSprite
import game.tools.constants as c
from game.tools.asset_cache import playSound


class Item(pg.sprite.Sprite):
    """Create a sprite of an item.

    This class should not be called directly. Only call its subclasses.
    """

    def __init__(self):
        """Init ItemSprite.

        Instance variables:
            spriteSheet: The SpriteSheet object for the item sprite sheet image.
            animationFrames: A list of 16 Surface objects from the SpriteSheet object
            coordinates: A tuple location to blit the sprite on the screen.
            itemState: An OtherStatess Enum instance of the current state of the sprite.
                Used to determine which methods get called and when.
            collectingPlayer: An instance of the PlayerSprite class that collects this item.
                Is a None type variable until the item is collected.
            frameCount: An integer that increases whenever the collectItem method is called.
            imageDict: A dict associating keys with Surface objects from the SpriteSheet object.
            image: The current image to be drawn for the sprite.
                Defaults to the emptyImage.
            baseImage: The image that the sprite will change to once it's been revealed.
                What image that is depends on the specific subclass.
            rect: A rect object for the sprite.
            collisionRect: A smaller rect object used for checking collision between this sprite and others.
                This creates a better visual for collision than using the main rect object.
            triggerRect: A smaller rect object at different coordinates than the collisionRect.
        """
        super().__init__(c.itemGroup)
        spriteSheet = SpriteSheet("item.png")
        self.animationFrames = []
        self.coordinates = (0, 0)
        self.itemState = c.OtherStates.OFF_SCREEN
        self.collectingPlayer = None
        self.frameCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 34, 34))
        self.animationFrames.extend(spriteSheet.getStripImages(0, 34, 34, 34))
        self.imageDictKeys = ["apple", "banana", "cherry", "eggplant", "melon", "pineapple", "strawberry", "800",
                              "bag", "clock", "flag", "glasses", "explosion 1", "explosion 2", "empty", "1500"]
        self.imageDict = dict(zip(self.imageDictKeys, self.animationFrames))

        self.image = self.baseImage = self.imageDict["empty"]
        self.rect = self.image.get_rect()
        self.collisionRect = pg.rect.Rect((0, 0), (18, 28))
        self.triggerRect = pg.rect.Rect((0, 0), (18, 28))

    def setCoordinates(self, x, y):
        """Set the sprite's coordinates to the passed arguments.

        This also adjusts the location of rect and collisionRect.

        Args:
            x: An integer x coordinate to draw the sprite.
            y: An integer y coordinate to draw the sprite.
        """
        self.coordinates = x, y
        self.rect.topleft = x, y
        self.collisionRect.topleft = x + 8, y + 4

    def reset(self):
        self.setCoordinates(0, 0)
        self.triggerRect.topleft = (0, 0)
        self.itemState = c.OtherStates.DEAD

    def initialize(self, x, y, triggerX, triggerY):
        """Set the sprite's coordinates and triggerRect's coordinates using the passed arguments.

        Args:
            x: An integer indicating the column the sprite will be placed on.
            y: An integer indicating the row the sprite will be placed on.
            triggerX: An integer indicating the column the sprite's triggerRect will be placed on.
            triggerY: An integer indicating the row the sprite's triggerRect will be placed on.
        """
        self.setCoordinates(-1 + 48 * x, 49 + 48 * y)
        self.triggerRect.topleft = (-1 + 48 * triggerX, 49 + 48 * triggerY)
        self.itemState = c.OtherStates.OFF_SCREEN

    def update(self):
        """Check if the item is colliding with any players. Depending on itemState, determine which method to
        call.
        """
        self.checkPlayerCollision()
        if self.itemState == c.OtherStates.COLLECTED:
            self.collectItem()
        elif self.itemState == c.OtherStates.REVEALED:
            self.image = self.baseImage
        else:
            self.image = self.imageDict["empty"]
        self.image.set_colorkey(c.BLACK)

    def checkPlayerCollision(self):
        """Check if the sprite's rects are colliding with any of the player sprites.

        If the item sprite is in the REVEALED state and collides with a player sprite, its state becomes the
        COLLECTED state.
        If the item sprite is in the OFF_SCREEN state and its triggerRect collides with a player sprite, its
        state becomes the REVEALED state.
        """
        for player in c.playerGroup:
            if self.rect.colliderect(player.collisionRect) and self.itemState == c.OtherStates.REVEALED:
                self.collectingPlayer = player
                self.itemState = c.OtherStates.COLLECTED
            elif self.triggerRect.colliderect(player.collisionRect) and self.itemState == c.OtherStates.OFF_SCREEN:
                playSound("item_appears_or_collected.wav")
                self.itemState = c.OtherStates.REVEALED

    def collectItem(self):
        """Not to be called directly, but inherited by subclasses."""
        pass


class MinorItem(Item):
    """Create a sprite of a minor item, that only gives the player 800 points.

    Attributes:
        imageKey: A string representation of which image the sprite should take.
            If imageKey is not in the Item class' imageDict, will raise a KeyError.
    """

    def __init__(self, imageKey):
        """Init MinorItemSprite.

        Instance variables:
            baseImage: The image that the sprite will change to once it's been revealed.
        """
        super().__init__()
        self.baseImage = self.imageDict[imageKey]

    def collectItem(self):
        """Increase frameCount. Depending on frameCount, collectItem has different effects.

        On the first frame, increase the collecting player's score by 800.
        The sprite then spends 12 frames with each of the explosion images.
        Its image then changes to an 800 for 32 frames, representing its value in points.
        After 56 frames total, the item's state changes to DEAD.
        """
        self.frameCount += 1
        if self.frameCount == 1:
            self.collectingPlayer.score += 800
        if self.frameCount % 56 < 12:
            self.image = self.imageDict["explosion 1"]
        elif self.frameCount % 56 < 24:
            self.image = self.imageDict["explosion 2"]
        else:
            self.image = self.imageDict["800"]
        if self.frameCount == 24:
            playSound("item_appears_or_collected.wav")
        if self.frameCount % 56 == 0:
            self.itemState = c.OtherStates.DEAD


class ItemBag(Item):
    """Create a sprite of a bag item."""

    def __init__(self):
        """Init ItemBagSprite.

        Instance variables:
            baseImage: The image that the sprite will change to once it's been revealed.
        """
        super().__init__()
        self.baseImage = self.imageDict["bag"]

    def collectItem(self):
        """Increase frameCount. Depending on frameCount, collectItem has different effects.

        On the first frame, increase the collecting player's score by 800.
        The sprite then spends 12 frames with each of the explosion images.
        Its image then changes to an 1500 for 32 frames, representing its value in points.
        After 56 frames total, the item's state changes to DEAD.
        """
        self.frameCount += 1
        if self.frameCount == 1:
            self.collectingPlayer.score += 1500
        if self.frameCount % 56 < 12:
            self.image = self.imageDict["explosion 1"]
        elif self.frameCount % 56 < 24:
            self.image = self.imageDict["explosion 2"]
        else:
            self.image = self.imageDict["1500"]
        if self.frameCount == 24:
            playSound("item_appears_or_collected.wav")
        if self.frameCount % 56 == 0:
            self.itemState = c.OtherStates.DEAD


class ItemClock(Item):
    """Create a sprite of a clock item."""

    def __init__(self):
        """Init ItemClockSprite.

        Instance variables:
            baseImage: The image that the sprite will change to once it's been revealed.
        """
        super().__init__()
        self.baseImage = self.imageDict["clock"]

    def collectItem(self):
        """Increase frameCount. Depending on frameCount, collectItem has different effects.

        On the first frame, it sets the UrchinSprite class variable isFrozen to True, sets the instance variable
        isFrozen for every other player sprite to True, and sets the level's image to its lighter variant.
        The sprite then spends 12 frames with each of the explosion images.
        After 24 frames total, the item's image changes to a fully transparent, blank image.
        After 513 frames total, the item undoes the aforementioned changes and its state changes to DEAD.
        """
        self.frameCount += 1
        if self.frameCount == 1:
            PlayerSprite.currentLevel.image = PlayerSprite.currentLevel.lightImage
            UrchinSprite.isFrozen = True
            for sprite in c.playerGroup:
                if sprite is not self.collectingPlayer:
                    sprite.isFrozen = True
        if self.frameCount < 12:
            self.image = self.imageDict["explosion 1"]
        elif 12 < self.frameCount < 24:
            self.image = self.imageDict["explosion 2"]
        if self.frameCount == 24:
            playSound("item_appears_or_collected.wav")
            self.image = self.imageDict["empty"]
        if self.frameCount == 513:
            PlayerSprite.currentLevel.image = PlayerSprite.currentLevel.standardImage
            UrchinSprite.isFrozen = False
            for sprite in c.playerGroup:
                if sprite is not self.collectingPlayer:
                    sprite.isFrozen = False
                    if sprite.playerState == c.PlayerStates.FINISHED_SWINGING:
                        sprite.frameCount = 0
            self.itemState = c.OtherStates.DEAD


class ItemFlag(Item):
    """Create a sprite of a flag item."""

    def __init__(self):
        """Init ItemFlagSprite.

        Instance variables:
            baseImage: The image that the sprite will change to once it's been revealed.
        """
        super().__init__()
        self.baseImage = self.imageDict["flag"]

    def collectItem(self):
        """Increase frameCount. Depending on frameCount, collectItem has different effects.

        On the first frame, increase the collecting player's lives by 1.
        The sprite then spends 12 frames with each of the explosion images.
        After 24 frames total, the item's state changes to DEAD.
        """
        self.frameCount += 1
        if self.frameCount == 1:
            self.collectingPlayer.lives += 1
        if self.frameCount % 24 < 12:
            self.image = self.imageDict["explosion 1"]
        else:
            self.image = self.imageDict["explosion 2"]
        if self.frameCount == 24:
            playSound("item_appears_or_collected.wav")
            self.image = self.imageDict["empty"]
            self.itemState = c.OtherStates.DEAD


class ItemGlasses(Item):
    """Create a sprite of a glasses item."""

    def __init__(self):
        """Init ItemGlassesSprite.

        Instance variables:
            baseImage: The image that the sprite will change to once it's been revealed.
        """
        super().__init__()
        self.baseImage = self.imageDict["glasses"]

    def collectItem(self):
        """Increase frameCount. Depending on frameCount, collectItem has different effects.

        On the first frame, changes the state of all OFF_SCREEN items and gold sprites to reveal them.
        The sprite then spends 12 frames with each of the explosion images.
        After 24 frames total, the item's state changes to DEAD.
        """
        self.frameCount += 1
        if self.frameCount == 1:
            for sprite in c.itemGroup:
                if sprite.itemState == c.OtherStates.OFF_SCREEN:
                    sprite.itemState = c.OtherStates.REVEALED

            for sprite in c.goldGroup:
                if sprite.goldState == c.OtherStates.OFF_SCREEN:
                    sprite.goldState = c.OtherStates.UPSIDE_DOWN
        if self.frameCount % 24 < 12:
            self.image = self.imageDict["explosion 1"]
        else:
            self.image = self.imageDict["explosion 2"]
        if self.frameCount == 24:
            playSound("item_appears_or_collected.wav")
            self.image = self.imageDict["empty"]
            self.itemState = c.OtherStates.DEAD


# Create an instance of each of the 11 different items. This ensures that there is exactly one copy of each item at all
# times, and that each minor item has the proper baseImage.

APPLE_ITEM = MinorItem("apple")
BANANA_ITEM = MinorItem("banana")
CHERRY_ITEM = MinorItem("cherry")
EGGPLANT_ITEM = MinorItem("eggplant")
MELON_ITEM = MinorItem("melon")
PINEAPPLE_ITEM = MinorItem("pineapple")
STRAWBERRY_ITEM = MinorItem("strawberry")
BAG_ITEM = ItemBag()
CLOCK_ITEM = ItemClock()
FLAG_ITEM = ItemFlag()
GLASSES_ITEM = ItemGlasses()
minorItems = [APPLE_ITEM, BANANA_ITEM, CHERRY_ITEM, EGGPLANT_ITEM, MELON_ITEM, PINEAPPLE_ITEM, STRAWBERRY_ITEM]
majorItems = [BAG_ITEM, CLOCK_ITEM, FLAG_ITEM, GLASSES_ITEM]


def initializeLevelItems(level):
    """Randomly decide which items to include in the level, where to place them, and where to place their
    triggerRects.

    To ensure that no items exist off-screen, or from the previous level, this function first sets all items'
    itemState to DEAD, and only then initializes the randomly sampled items.
    """
    for item in c.itemGroup:
        item.reset()
    if isinstance(level, BonusLevel):
        return
    numberOfMinorItems = random.randint(2, 4)
    numberOfMajorItems = random.randint(0, min(3, 5 - numberOfMinorItems))
    currentMinorItems = random.sample(minorItems, numberOfMinorItems)
    currentMajorItems = random.sample(majorItems, numberOfMajorItems)
    currentItems = currentMinorItems + currentMajorItems
    triggerLocations = random.choices(level.itemTiles, k=(numberOfMajorItems + numberOfMinorItems))
    itemLocations = random.sample(level.itemTiles, k=(numberOfMajorItems + numberOfMinorItems))
    for num, item in enumerate(currentItems):
        item.initialize(itemLocations[num][0], itemLocations[num][1],
                        triggerLocations[num][0], triggerLocations[num][1])
