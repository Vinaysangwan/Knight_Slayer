import pygame

BASE_SPRITES_PATH = "assets/sprites/"


def load_image(path):
    img = pygame.image.load(BASE_SPRITES_PATH + path).convert_alpha()
    return img
