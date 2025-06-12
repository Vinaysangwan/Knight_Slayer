import pygame
import sys

import pygame.display

from scripts.utils import load_surfaces
from scripts.tilemap import Tilemap

RENDER_SCALE: int = 2


class Game:
    def __init__(self):
        pygame.init()

        # Game Screen
        self.screen_size = [640, 480]
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Level Editor")
        self.display_size = [320, 240]
        self.display = pygame.surface.Surface(self.display_size)

        # Game Clock
        self.game_clock = pygame.time.Clock()

        # Camera Scroll
        self.scroll = [0, 0]

        # Game Assets
        self.assets = {
            "grass": load_surfaces("world_tileset.png", frame_pos=(0, 0), count=(2, 2)),
            "desert": load_surfaces("world_tileset.png", frame_pos=(2, 0), count=(2, 2)),
            "farming": load_surfaces("world_tileset.png", frame_pos=(4, 0), count=(2, 2)),
            "snow": load_surfaces("world_tileset.png", frame_pos=(6, 0), count=(2, 2)),
            "ice": load_surfaces("world_tileset.png", frame_pos=(8, 0), count=(2, 2)),
            "green_tree": load_surfaces("world_tileset.png", frame_pos=(0, 3), count=(1, 3)),
            "yellow_tree": load_surfaces("world_tileset.png", frame_pos=(1, 3), count=(1, 3)),
            "light_green_tree": load_surfaces("world_tileset.png", frame_pos=(2, 3), count=(1, 3)),
        }
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        # Tilemap
        self.tilemap = Tilemap(self)

        try:
            self.tilemap.load("map.json")
        except FileNotFoundError:
            pass

        self.movement = [False, False, False, False]

        # Mouse
        self.mouse_pos = pygame.mouse.get_pos()
        self.clicked = False
        self.right_clicked = False
        self.shift = False

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            self.poll_Event()
            self.update()
            self.render()

            self.screen.blit(pygame.transform.scale(self.display, (self.screen_size[0], self.screen_size[1])))

            pygame.display.update()
            self.game_clock.tick(60)

    def update(self):
        self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
        self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
        self.render_scroll = [int(self.scroll[0]), int(self.scroll[1])]

        self.current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
        self.current_tile_img.set_alpha(100)

        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = (self.mouse_pos[0] / RENDER_SCALE, self.mouse_pos[1] / RENDER_SCALE)

        self.tile_pos = (
            int((self.mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size),
            int((self.mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size),
        )

        if self.clicked:
            self.tilemap.tilemap[str(self.tile_pos[0]) + ";" + str(self.tile_pos[1])] = {
                "type": self.tile_list[self.tile_group],
                "variant": self.tile_variant,
                "pos": self.tile_pos,
            }

        if self.right_clicked:
            loc = str(self.tile_pos[0]) + ";" + str(self.tile_pos[1])
            if loc in self.tilemap.tilemap:
                del self.tilemap.tilemap[loc]

    def render(self):
        self.display.blit(self.current_tile_img, (5, 5))
        self.tilemap.render(self.display, self.render_scroll)
        self.display.blit(
            self.current_tile_img,
            (
                self.tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                self.tile_pos[1] * self.tilemap.tile_size - self.scroll[1],
            ),
        )

    def poll_Event(self):
        for event in pygame.event.get():

            # Close Event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Key Down Event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_d:
                    self.movement[1] = True
                if event.key == pygame.K_w:
                    self.movement[2] = True
                if event.key == pygame.K_s:
                    self.movement[3] = True
                if event.key == pygame.K_LSHIFT:
                    self.shift = True
                if event.key == pygame.K_o:
                    self.tilemap.save("map.json")
                if event.key == pygame.K_t:
                    self.tilemap.auto_Tile()

            # Key Up Event
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False
                if event.key == pygame.K_w:
                    self.movement[2] = False
                if event.key == pygame.K_s:
                    self.movement[3] = False
                if event.key == pygame.K_LSHIFT:
                    self.shift = False

            # Mouse Button Down Event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
                if event.button == 3:
                    self.right_clicked = True
                if event.button == 5:
                    if self.shift:
                        self.tile_group = (self.tile_group + 1) % (len(self.tile_list))
                        self.tile_variant = 0
                    else:
                        self.tile_variant = (self.tile_variant + 1) % (
                            len(self.assets[self.tile_list[self.tile_group]])
                        )

            # Mouse Button Up Event
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicked = False
                if event.button == 3:
                    self.right_clicked = False
                if event.button == 4:
                    if self.shift:
                        self.tile_group = (self.tile_group - 1) % (len(self.tile_list))
                        self.tile_variant = 0
                    else:
                        self.tile_variant = (self.tile_variant - 1) % (
                            len(self.assets[self.tile_list[self.tile_group]])
                        )


Game().run()
