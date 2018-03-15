import pygame as pg

from game.sprites.sprite_sheet import SpriteSheet
from game.sprites.urchin import UrchinSprite
import game.tools.constants as c


class BlackHoleSprite(pg.sprite.Sprite):
    """Create a sprite of the black hole obstacle.

    Class variables:
        maxEnemies: An integer showing the maximum number of enemies than can be onscreen at a time.
            Stored in the BlackHoleSprite class, as this class uses it to determine whether or not it can spawn
            another enemy.
        blackHolesList: A list of all of the black hole sprites in the level. Used to set an order for the hole
            that will spawn the next enemy.
        blackHoleToSpawn: A BlackHoleSprite object, showing which is the next black hole object that will spawn
            an enemy.
        preparingEnemySpawn: A boolean indicating if a black hole sprite is in the process of spawning an enemy.
        enemySpawnCountdown: An integer counting down with each frame as long as preparingEnemySpawn is True.
            Once it reaches 0, a new enemy is spawned. It resets to baseSpawnCountdown if preparingEnemySpawn is
            False.
            It is initially set to 35, so the first enemy spawns quickly.
        baseSpawnCountdown: An integer representing the number of frames enemySpawnCountdown resets to when
            preparingEnemySpawn is False.
    """

    maxEnemies = 2
    blackHolesList = []
    blackHoleToSpawn = None
    preparingEnemySpawn = True
    enemySpawnCountdown = 35
    baseSpawnCountdown = 509

    def __init__(self):
        """Init BlackHoleSprite.

        Instance variables:
            spriteSheet: The SpriteSheet object for the hole sprite sheet image.
            animationFrames: A list of 4 Surface objects from the SpriteSheet object.
            coordinates: A tuple location to blit the sprite on the screen.
            frameCount: An integer that increases whenever the update method is called.
            animationCount: An integer tracking from where in animationFrame the sprite should take its next
                image.
            image: The current image to be drawn for the sprite.
                Defaults to the first Surface object in animationFrames.
            rect: A rect object for the sprite.
        """
        super().__init__(c.blackHoleGroup)
        spriteSheet = SpriteSheet("hole.png")
        self.animationFrames = []
        self.coordinates = (0, 0)
        self.frameCount = self.animationCount = 0

        self.animationFrames.extend(spriteSheet.getStripImages(0, 0, 34, 34))
        self.image = self.animationFrames[0]
        self.image.set_colorkey(c.BLACK)
        self.rect = self.image.get_rect()

    def initialize(self, x, y):
        """Reset some of the class' attributes to its proper initial values.

        This should be called whenever the player begins a new level, and at no other point.
        This adds this sprite instance to the blackHolesList class variable, and if the blackHoleToSpawn class
        variable is empty (i.e., this is the only item in blackHolesList so far), it sets blackHoleToSpawn to
        this sprite instance.
        """
        self.setCoordinates(x, y)
        BlackHoleSprite.blackHolesList.append(self)
        BlackHoleSprite.preparingEnemySpawn = True
        BlackHoleSprite.enemySpawnCountdown = 35
        if BlackHoleSprite.blackHoleToSpawn is None:
            BlackHoleSprite.blackHoleToSpawn = self

    def setCoordinates(self, x, y):
        """Set the sprite's coordinates to the passed arguments.

        This also adjusts the location of rect.

        Args:
            x: An integer x coordinate to draw the sprite.
            y: An integer y coordinate to draw the sprite.
        """
        self.coordinates = x, y
        self.rect.topleft = x, y

    def update(self):
        """Increase frameCount. Depending on frameCount, the length of the enemyGroup, and the class variables,
        determine which methods to call.

        The sprite's image changes every 6 frames, cycling through the animationFrames list.
        To keep frameCount from increasing without bounds, it resets to 0 every 6 frames.
        If there are fewer enemies alive than maxEnemies, preparingEnemySpawn is set to True and
        enemySpawnCountdown is set to baseSpawnCountdown.
        Once preparingEnemySpawn is True, enemySpawnCounter counts down every frame.
        Once enemySpawnCounter reaches 0, an enemy is spawned. If there are still fewer than maxEnemies alive,
        then enemySpawnCounter is set to 160 to spawn another enemy shortly.
        Otherwise, preparingEnemySpawn is set to False again until an enemy is killed.
        """
        self.frameCount += 1
        if self.frameCount % 6 == 0:
            self.animationCount += 1
            if self.animationCount >= len(self.animationFrames):
                self.animationCount = 0
            self.image = self.animationFrames[self.animationCount]
            self.frameCount = 0
        if len(c.enemyGroup) < BlackHoleSprite.maxEnemies and BlackHoleSprite.blackHoleToSpawn == self:
            if not BlackHoleSprite.preparingEnemySpawn:
                BlackHoleSprite.preparingEnemySpawn = True
                BlackHoleSprite.enemySpawnCountdown = BlackHoleSprite.baseSpawnCountdown
            elif BlackHoleSprite.enemySpawnCountdown > 0:
                BlackHoleSprite.enemySpawnCountdown -= 1
            else:
                self.spawnEnemy()
                if len(c.enemyGroup) < BlackHoleSprite.maxEnemies:
                    BlackHoleSprite.enemySpawnCountdown = 160
                else:
                    BlackHoleSprite.preparingEnemySpawn = False
        self.image.set_colorkey(c.BLACK)

    def spawnEnemy(self):
        """Create a new enemy sprite on the same coordinates as this sprite, then choose the next black hole
        sprite that will spawn an enemy.
        """
        newUrchin = UrchinSprite()
        newUrchin.setCoordinates(self.coordinates[0], self.coordinates[1])
        newUrchin.setRandomDirection()
        BlackHoleSprite.chooseNextBlackHoleToSpawn()

    @classmethod
    def chooseNextBlackHoleToSpawn(cls):
        """Choose the next black hole sprite that will spawn an enemy.

        If the current blackHoleToSpawn is the last item in blackHolesList, the next blackHoleToSpawn is set to
        the first item in blackHolesList (Note that this is the same object if blackHolesList only contains one
        object).
        Otherwise, the blackHoleToSpawn is set to the next item in blackHolesList.
        """
        if cls.blackHoleToSpawn == cls.blackHolesList[-1]:
            cls.blackHoleToSpawn = cls.blackHolesList[0]
        else:
            currentSpawnIndex = cls.blackHolesList.index(cls.blackHoleToSpawn)
            cls.blackHoleToSpawn = cls.blackHolesList[currentSpawnIndex + 1]
