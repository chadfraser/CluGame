import pygame as pg

import game.demo.demo_sprites as d_sprite
from game.gameplay.state import checkQuitGame
from game.tools.asset_cache import playSound
import game.tools.constants as c
from game.tools.controls import controlsDicts


def animateDemo():
    """Play the demo animation until the user presses return to cancel it."""
    pg.mixer.music.load(c.DEMO_MUSIC)
    pg.mixer.music.play()
    playerNames = [c.DEMO_FONT.render("BUBBLES", False, c.RED), c.DEMO_FONT.render("GLOOPY", False, c.GREEN),
                   c.DEMO_FONT.render("NEMO", False, c.BLUE), c.DEMO_FONT.render("DIZZY", False, c.YELLOW)]
    playerNameCoordinates = [(103, 61), (127, 61), (145, 337), (122, 337)]

    coverRect = pg.Rect(20, -260, 380, 260)
    displayRects = [pg.Rect(20, -260, 380, 260), pg.Rect(480, 180, 380, 260), pg.Rect(120, 444, 380, 260),
                    pg.Rect(-380, 20, 380, 260)]
    nameRects = [pg.Rect(86, 47, 540, 100), pg.Rect(86, 46, 540, 100), pg.Rect(57, 324, 540, 100),
                 pg.Rect(57, 324, 540, 100)]
    spriteCoords = [(0, 4), (-4, 0), (0, -4), (4, 0)]

    for demoNum in range(4):
        # Initialize each scene of the demo by setting frameCount to 0, removing all sprites from demoGroup, and
        # resetting the base class variables of the PlayerDemoSprite class.

        frameCount = 0
        c.demoGroup.empty()
        d_sprite.initialize()
        c.SCREEN.fill(c.GREY)
        pg.display.update()

        createDemoSprites(demoNum, displayRects)

        alphaKey = 255
        # Each scene of the demo animation is 600 frames long.

        while frameCount < 600:
            checkQuitGame()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == controlsDicts[0]["pause"] or event.key == pg.K_RETURN:
                        pg.mixer.music.stop()
                        c.SCREEN.fill(c.BLACK)
                        return
            frameCount += 1
            # Only the sprites inside of the display rect are visible.
            # The display rect moves from off of one edge of the screen towards the either side for 104 frames.
            # Every sprite moves this amount in addition to their regular movement, to create the illusion of them
            # moving with the display.
            # A grey rect stays against one side of the display rect to cover up every sprite that moves past the edge
            # of the display rect.

            if frameCount < 105:
                displayRects[demoNum].topleft = [displayRects[demoNum].topleft[0] + spriteCoords[demoNum][0],
                                                 displayRects[demoNum].topleft[1] + spriteCoords[demoNum][1]]
                if demoNum == 0:
                    coverRect.bottomleft = displayRects[demoNum].topleft
                elif demoNum == 1:
                    coverRect.topleft = displayRects[demoNum].topright
                elif demoNum == 2:
                    coverRect.topleft = displayRects[demoNum].bottomleft
                else:
                    coverRect.topright = displayRects[demoNum].topleft
                for sprite in c.demoGroup:
                    sprite.coordinates = (sprite.coordinates[0] + spriteCoords[demoNum][0],
                                          sprite.coordinates[1] + spriteCoords[demoNum][1])

            if frameCount < 328:
                # For the first 328 frames, the sprites are all animated and move as desired, with the player sprite
                # constantly staying in the middle of the display rect.

                pg.draw.rect(c.SCREEN, c.BLACK, displayRects[demoNum])
                for sprite in c.demoGroup:
                    sprite.setCoordinates()
                    sprite.update()
                    c.SCREEN.blit(sprite.image, sprite.coordinates)
                pg.draw.rect(c.SCREEN, c.GREY, coverRect)
                pg.display.update(coverRect)
                pg.display.update(displayRects[demoNum])

            elif frameCount == 328:
                # On the 328th frame, all sprites stop moving. Any sprite that has a monochrome image variant switches
                # to that image.
                # The name display and player character's name appears as well, but they are hidden by the screen
                # being covered by a white rect in the following conditional statement.

                playSound("item_appears_or_collected.wav")
                demoNameBlock = d_sprite.DemoNameDisplay(demoNum, (nameRects[demoNum].left, nameRects[demoNum].top))
                for sprite in c.demoGroup:
                    sprite.setMonochromeImage()

            else:
                # Grey rects are drawn on all four sides of the display rect to ensure that all demo sprites outside of
                # the display rect are covered up.
                # The flashScreen function is called every frame, gradually decreasing the visibility of the white rect
                # covering the screen.

                c.SCREEN.fill(c.GREY)
                pg.draw.rect(c.SCREEN, c.BLACK, displayRects[demoNum])
                for sprite in c.demoGroup:
                    c.SCREEN.blit(sprite.image, sprite.coordinates)
                pg.draw.rect(c.SCREEN, c.GREY, (displayRects[demoNum].right, 0,
                                                c.SCREEN_SIZE[0] - displayRects[demoNum].right, c.SCREEN_SIZE[1]))
                pg.draw.rect(c.SCREEN, c.GREY, (0, 0, displayRects[demoNum].left, c.SCREEN_SIZE[1]))
                pg.draw.rect(c.SCREEN, c.GREY, (0, 0, c.SCREEN_SIZE[0], displayRects[demoNum].top))
                pg.draw.rect(c.SCREEN, c.BLACK, (nameRects[demoNum].left, nameRects[demoNum].top, 365, 65))
                c.SCREEN.blit(demoNameBlock.image, demoNameBlock.coordinates)
                c.SCREEN.blit(playerNames[demoNum], playerNameCoordinates[demoNum])
                alphaKey = flashScreen(frameCount, alphaKey)
                pg.display.update()
            c.CLOCK.tick(c.FPS)


def createDemoSprites(demoNum, displayRects):
    """Create the sprites required for the current scene of the demo animation.

    Since each tile of the demo board is 96 x 96 pixels, many of these sprites are designed to be offset from the
    previous by 96 pixels in one or both directions.

    Arguments:
        demoNum: An integer showing which scene of the demo animation we wish to create sprites for.
        displayRects: A list of rect objects. One rect is to be drawn for each scene of the demo animation, and
            only sprites within the drawn rect will be visible.
    """
    if demoNum == 0:
        for num in range(4):
            d_sprite.DemoGoldSprite((458 + 96 * (num + num // 2), -164))
        for num in range(14):
            for postNum in range(2):
                d_sprite.PostSprite((-196 + 96 * num, -194 + 96 * postNum))
        d_sprite.DemoWallSprite(0, (668 + 96 * 3, -294))
        d_sprite.DemoPlayerSprite(0, (180, -182))

    elif demoNum == 1:
        for num in range(10):
            for postNum in range(6):
                d_sprite.PostSprite((1474 - 96 * num, 246 + 96 * postNum))
        d_sprite.DemoArmSprite(1, (1430 - 96 * 8, 242 + 96 * 1))
        d_sprite.DemoPlayerSprite(1, (638, 274))

    elif demoNum == 2:
        for num in range(12):
            for postNum in range(2):
                d_sprite.PostSprite((734 - 96 * num, 510 + 96 * postNum))
        d_sprite.DemoWallSprite(2, (-452, 222))
        d_sprite.DemoHoleSprite((474, 540))
        d_sprite.DemoUrchinSprite((474 - 96 * 5, 540))
        d_sprite.DemoWaveSprite((174, 540))
        d_sprite.DemoPlayerSprite(2, (290, 522))
        d_sprite.DemoPlayerSprite.facingDirection = c.Directions.LEFT

    else:
        for num in range(2):
            for postNum in range(2):
                d_sprite.PostSprite((-448 + 384 * num, 86 + 96 * postNum))
                d_sprite.PostSprite((-352 + 384 * num, 86 + 96 * postNum))
        for num in range(2):
            d_sprite.DemoRubberTrapSprite(num, (-276 + 96 * num, 86))
        d_sprite.DemoArmSprite(3, (-200, 90), True)
        d_sprite.DemoPlayerSprite(3, (-224, 112))

    d_sprite.DemoDisplay(demoNum, displayRects[demoNum].topleft)


def flashScreen(frameCount, alphaKey):
    """Cover the screen with a fully white rect. After 34 frames, this white rect grows less visible every
    frame.

    Returns:
        alphaKey: An integer storing how visible the white rect should be.
    """
    screenCovering = pg.Surface(c.SCREEN_SIZE)
    screenCovering.fill(c.WHITE)
    screenCovering.set_alpha(alphaKey)
    if frameCount > 364:
        alphaKey = max(0, alphaKey - 3)
    c.SCREEN.blit(screenCovering, (0, 0))
    pg.display.update()
    return alphaKey
