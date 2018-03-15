import pygame as pg

from game.gameplay.state import checkQuitGame
import game.tools.constants as c
from game.tools.controls import controlsDicts


def displayChangeControlMenu(titleImageOne, titleImageTwo, subtitleImage, numberOfPlayers):
    """Display the menu to change each selected players' controls.

    Args:
        titleImageOne: The leftmost TitleImage sprite.
        titleImageTwo: The rightmost TitleImage sprite.
        subtitleImage: The TitleBoxSprite to be drawn on the screen.
        numberOfPlayers: An integer showing how many players' controls will be changed.
    """
    for sprite in [titleImageOne, titleImageTwo, subtitleImage]:
        sprite.setTitleImage()
    frameCount = controlChangeIndex = 0
    currentPlayerIndex = 1
    # If only one player is changing their controls, the text reads "SELECT X BUTTON".
    # Otherwise, it reads "P_ X BUTTON".
    # Therefore, we change the base coordinates of the text if there are more than one players to ensure that the text
    # remains centered.

    if numberOfPlayers == 1:
        textCoordinates = (90, 345)
    else:
        textCoordinates = (122, 345)

    while True:
        # This loop continues until all available players have chosen their controls.

        checkQuitGame()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                controlChangeIndex = changeControlInput(controlChangeIndex, event, currentPlayerIndex, numberOfPlayers)
                frameCount = 0
        if controlChangeIndex == 6:
            # There are only six items in each sub-dictionary of the controlsDicts.
            # Therefore, if we reach index 6 of our controlsList (A default "none" value), we loop back to index 0 and
            # set the controls for the next player.

            if currentPlayerIndex == numberOfPlayers:
                return
            else:
                currentPlayerIndex += 1
                controlChangeIndex = 0

        controlsList = ["shoot", "pause", "up", "down", "left", "right", "none"]
        controlToChange = controlsList[controlChangeIndex]
        c.SCREEN.fill(c.BLACK)
        subtitleText = c.FONT.render("SECRETS OF OLD CLU CLU LAND", False, c.WHITE)
        c.SCREEN.blit(subtitleText, (42, 275))
        for sprite in [titleImageOne, titleImageTwo, subtitleImage]:
            c.SCREEN.blit(sprite.image, sprite.coordinates)

        # We change the location where we will draw the text whenever the number of letters in the control we will set
        # changes. This ensures that the text is always centered on the screen.

        if controlChangeIndex == 2:
            textCoordinates = setTextCoordinates(23, numberOfPlayers)
        elif controlChangeIndex == 3:
            textCoordinates = setTextCoordinates(5, numberOfPlayers)
        elif controlChangeIndex == 5:
            textCoordinates = setTextCoordinates(0, numberOfPlayers)
        if numberOfPlayers == 1:
            controlInputText = c.FONT.render("SELECT '{}' BUTTON".format(controlToChange.upper()), False, c.WHITE)
        else:
            controlInputText = c.FONT.render("P{} '{}' BUTTON".format(currentPlayerIndex, controlToChange.upper()),
                                             False, c.WHITE)
        # The text onscreen flashes every 30 frames.

        if frameCount % 60 < 30:
            c.SCREEN.blit(controlInputText, textCoordinates)
        pg.display.update()
        frameCount += 1
        c.CLOCK.tick(c.FPS)


def changeControlInput(controlChangeIndex, event, currentPlayerIndex, numberOfPlayers):
    """Change the key used to control a specific action from a specific player, as determined by the arguments.

    Args:
        controlChangeIndex: An integer representing which control we are currently changing.
        event: A key object that was pressed by the user.
        currentPlayerIndex: An integer representing which player's controls we are currently changing.
        numberOfPlayers: An integer showing how many players' controls will be changed.
            This is passed as an argument so that we do not overwrite any controls for players who do not wish to
            change their controls.
    Returns:
        controlChangeIndex: An integer representing which control we are next changing.
    """
    controlsList = ["shoot", "pause", "up", "down", "left", "right", "none"]
    # currentIndex is just one lower than currentPlayerIndex. This is used for the sake of consistency and simplicity
    # in assigning values to specific indexes of the controlsDicts.

    currentIndex = currentPlayerIndex - 1
    if controlChangeIndex == 0 and currentIndex == 0:
        for listIndex, controls in enumerate(controlsDicts):
            # Once the first player inputs his first control, every other player's controls are set to blank.
            # This is done as we have later code that ensures that no single key can control two actions between any
            # players. By removing every player's controls preemptively, we can prevent this from triggering if, for
            # example, player one wants to input a key that player two uses by default.
            # If fewer than four players are inputting their controls, this stops setting controls to blank once it has
            # done so for each acting player. This ensures that, should the user later choose to start a 4-player game,
            # player 4 still has controls set.

            if numberOfPlayers <= listIndex:
                break
            controlsDicts[listIndex] = controlsDicts[currentIndex].fromkeys(controlsDicts[currentIndex], "None")
    if not any(event.key in controlValue.values() for controlValue in controlsDicts):
        if controlChangeIndex == 6:
            if currentIndex + 1 == numberOfPlayers:
                # Ideally, this conditional will never evaluate to True, since the displayChangeControlMenu function
                # will return before these criteria are True.
                # It is only included as a safeguard against crashing if somehow the user does manage to reach this
                # function at this point.

                pg.mixer.music.stop()
                pg.time.delay(500)
        else:
            controlsDicts[currentIndex][controlsList[controlChangeIndex]] = event.key
            controlChangeIndex += 1
    return controlChangeIndex


def chooseNumberOfPlayers(titleImageOne, titleImageTwo, subtitleImage, textToDisplay):
    """Choose how many players will be controlled in whichever function is called next.

    This is used to either choose how many players will play the game, or to choose how many players will change
    their controls.

    Args:
        titleImageOne: The leftmost TitleImage sprite.
        titleImageTwo: The rightmost TitleImage sprite.
        subtitleImage: The TitleBoxSprite to be drawn on the screen.
        textToDisplay: A string of text that should be displayed on the screen.
            It should either be "GAME" or "CONTROLS"
    """
    for sprite in [subtitleImage, titleImageOne, titleImageTwo]:
        sprite.setTitleImage()
    subtitleText = c.FONT.render("SECRETS OF OLD CLU CLU LAND", False, c.WHITE)
    playerNumbersText = [c.FONT.render("1 PLAYER", False, c.CYAN),
                         c.FONT.render("2 PLAYER", False, c.CYAN),
                         c.FONT.render("3 PLAYER", False, c.CYAN),
                         c.FONT.render("4 PLAYER", False, c.CYAN)]
    playerTextCoordinates = [(60, 310), (320, 310), (60, 370), (320, 370)]
    optionText = c.FONT.render(textToDisplay, False, c.CYAN)
    cursorText = c.FONT.render(">", False, c.ORANGE)
    cursorLocation = (40, 310)
    # Since the word "GAME" has fewer characters than the word "CONTROLS", the text's coordinates are all adjusted 30
    # pixels to the right if "GAME" is the text to be displayed, to ensure it remains centered.

    optionTextCoordinates = [(60, 330), (320, 330), (60, 390), (320, 390)]
    if textToDisplay == "GAME":
        optionTextCoordinates = [(90, 330), (350, 330), (90, 390), (350, 390)]

    while True:
        checkQuitGame()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == controlsDicts[0]["pause"] or event.key == pg.K_RETURN:
                    coordinatesIndex = [(), (40, 310), (300, 310), (40, 370), (300, 370)]
                    return coordinatesIndex.index(cursorLocation)
                elif event.key == controlsDicts[0]["left"] or event.key == controlsDicts[0]["right"]:
                    if cursorLocation[0] == 40:
                        cursorLocation = (300, cursorLocation[1])
                    else:
                        cursorLocation = (40, cursorLocation[1])
                elif event.key == controlsDicts[0]["up"] or event.key == controlsDicts[0]["down"]:
                    if cursorLocation[1] == 310:
                        cursorLocation = (cursorLocation[0], 370)
                    else:
                        cursorLocation = (cursorLocation[0], 310)
        c.SCREEN.fill(c.BLACK)
        c.SCREEN.blit(subtitleText, (42, 275))
        for sprite in [titleImageOne, titleImageTwo, subtitleImage]:
            c.SCREEN.blit(sprite.image, sprite.coordinates)
        for text, coords in zip(playerNumbersText, playerTextCoordinates):
            c.SCREEN.blit(text, coords)
        for coords in optionTextCoordinates:
            c.SCREEN.blit(optionText, coords)
        c.SCREEN.blit(cursorText, cursorLocation)
        pg.display.update()
        c.CLOCK.tick(c.FPS)


def setTextCoordinates(value, numberOfPlayers):
    """Change the horizontal location of where text should appear on the screen.

    Args:
        value: An integer amount of pixels that the text should be shifted to the right.
        numberOfPlayers: An integer showing how many players' controls will be changed.
            If only one player is changing their controls, the text reads "SELECT X BUTTON".
            Otherwise, it reads "P_ X BUTTON".
            Therefore, we accept this argument to ensure that the text remains centered.
    Returns:
        textCoordinates: A tuple location to blit the text on the screen.
    """
    if numberOfPlayers == 1:
        textCoordinates = (90 + value, 345)
    else:
        textCoordinates = (122 + value, 345)
    return textCoordinates
