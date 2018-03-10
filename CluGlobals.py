import pygame
import os
import sys


gameFolder = os.path.dirname(__file__)
spriteFolder = os.path.join(gameFolder, "Sprites")
spriteSheetFolder = os.path.join(gameFolder, "SpriteSheets")
backgroundFolder = os.path.join(gameFolder, "Backgrounds")
titleFolder = os.path.join(gameFolder, "Titles")
musicFolder = os.path.join(gameFolder, "Music")

_imageLibrary = {}
_soundLibrary = {}


def getImage(folder, imageFile):
    global _imageLibrary
    image = _imageLibrary.get(imageFile)
    if image is None:
        fullPath = os.path.join(folder, imageFile)
        try:
            image = pygame.image.load(fullPath).convert()
            _imageLibrary[imageFile] = image
        except pygame.error:
            print("ERROR: Cannot find image '{}'".format(imageFile))
            pygame.quit()
            sys.exit()
    return image


def playSound(soundFile):
    global _soundLibrary
    sound = _soundLibrary.get(soundFile)
    if sound is None:
        fullPath = os.path.join(musicFolder, soundFile)
        try:
            sound = pygame.mixer.Sound(fullPath)
            _soundLibrary[soundFile] = sound
        except pygame.error:
            print("ERROR: Cannot find sound '{}'".format(soundFile))
            pygame.quit()
            sys.exit()
        # if soundFile == "push_or_shoot_enemy.wav":
        #     sound.set_volume(0.5)
    sound.play()
