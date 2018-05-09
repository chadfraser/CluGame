import os
import pygame
import sys

import game.tools.constants as c


_imageLibrary = {}
_soundLibrary = {}


def getImage(folder, imageFile):
    """Get an image from the passed folder and file location.

    If the image has not already been loaded, it loads the image as a pygame image object.
    If the image has already been loaded before, it simply returns the image.
    This increases speed, as it prevents images from needlessly loading multiple times.

    Args:
        folder: The string path that the image can be found in.
        imageFile: The string of the file for the image, not including the file path.
    
    Returns:
        image: A pygame image object made with the passed image file.
    """
    global _imageLibrary
    image = _imageLibrary.get(imageFile)
    if image is None:
        fullPath = os.path.join(folder, imageFile)
        try:
            image = pygame.image.load(fullPath).convert()
            _imageLibrary[imageFile] = image
        except pygame.error:
            print("ERROR: Cannot find image '{}' in folder '{}'".format(imageFile, folder))
            pygame.quit()
            sys.exit()
    return image


def playSound(soundFile):
    """Play a sound from the passed file location, in the music folder path.

    If the sound has not already been loaded, it loads the sound as a pygame mixer sound object.
    If the sound has already been loaded before, it simply returns the sound.
    This increases speed, as it prevents sounds from needlessly loading multiple times.

    Args:
        soundFile: The string of the file for the sound, not including the file path.
    """
    global _soundLibrary
    sound = _soundLibrary.get(soundFile)
    if sound is None:
        fullPath = os.path.join(c.MUSIC_FOLDER, soundFile)
        try:
            sound = pygame.mixer.Sound(fullPath)
            _soundLibrary[soundFile] = sound
        except pygame.error:
            print("ERROR: Cannot find sound '{}'".format(soundFile))
            pygame.quit()
            sys.exit()
    sound.play()
