import pygame

BASE_SPRITES_PATH = "assets/sprites/"


def load_image(path):
    img = pygame.image.load(BASE_SPRITES_PATH + path).convert_alpha()
    return img


def load_rect_image(path, top_left_pos=[0, 0], size=[32, 32]):
    img = pygame.image.load(BASE_SPRITES_PATH + path).convert_alpha()
    rect = pygame.Rect(*top_left_pos, *size)
    img.subsurface(rect)
    return img
