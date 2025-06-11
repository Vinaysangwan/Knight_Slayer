import pygame

BASE_SPRITE_PATH = "assets/sprites/"


def load_image(path: str) -> pygame.image:
    img = pygame.image.load(BASE_SPRITE_PATH + path).convert_alpha()
    return img


def load_surface_frame(path, frame: list, size: list) -> pygame.Surface:
    img = pygame.Surface((size[0], size[1])).convert_alpha()
    img.blit(load_image(path), (0, 0), (frame[0] * size[0], frame[1] * size[1], size[0], size[1]))
    img.set_colorkey((0, 0, 0))
    return img


def load_surfaces(path: str, frame_pos: list, count: list, size=[16, 16]):
    sprites_list = []
    for i in range(count[0]):
        for j in range(count[1]):
            sprites_list.append(load_surface_frame(path, frame=(frame_pos[0] + i, frame_pos[1] + j), size=size))

    return sprites_list


class Animation:
    def __init__(self, sprites: list, duration: int, loop=True):
        self.sprites = sprites
        self.duration = duration
        self.loop = loop

        self.frame_dur = 0
        self.done = False

    def get_Animation(self):
        return self

    def get_Anim_Image(self):
        return self.sprites[int(self.frame_dur // self.duration)]

    def update(self):
        if self.loop:
            self.frame_dur = (self.frame_dur + 1) % (self.duration * len(self.sprites))
        else:
            self.frame_dur = min(self.frame_dur + 1, self.duration * len(self.sprites) - 1)
            if self.frame_dur >= self.duration * len(self.sprites):
                self.done = True
