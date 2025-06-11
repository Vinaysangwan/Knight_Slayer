import pygame
import sys

import pygame.display

from scripts.utils import load_surfaces, Animation
from scripts.entities import Player
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()

        # Game Screen
        self.screen_size = [640, 480]
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Knight Slayer")
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
            "player": load_surfaces("small-knight.png", frame_pos=(0, 0), count=(4, 1), size=(14, 19)),
            "player/Idle": Animation(
                load_surfaces("small-knight.png", frame_pos=(0, 0), count=(4, 1), size=(14, 19)), duration=6
            ),
            "player/Run": Animation(
                load_surfaces("small-knight.png", frame_pos=(0, 2), count=(8, 2), size=(14, 19)), duration=3
            ),
            "player/Jump": Animation(
                load_surfaces("small-knight.png", frame_pos=(0, 5), count=(1, 1), size=(14, 19)), duration=2
            ),
        }

        # Tilemap
        self.tilemap = Tilemap(self)

        # Player
        self.player = Player(self, [100, 100])
        self.movement = [False, False]

    def run(self):
        while True:
            self.display.fill((20, 152, 220))

            self.poll_Event()
            self.update()
            self.render()

            self.screen.blit(pygame.transform.scale(self.display, (self.screen_size[0], self.screen_size[1])))

            pygame.display.update()
            self.game_clock.tick(60)

    def update(self):
        self.scroll[0] += (self.player.pos[0] - self.display_size[0] / 2 - self.scroll[0]) / 30
        self.scroll[1] += (self.player.pos[1] - self.display_size[1] / 2 - self.scroll[1]) / 30
        self.render_scroll = [int(self.scroll[0]), int(self.scroll[1])]

        self.player.update(self.tilemap, [self.movement[1] - self.movement[0], 0])

    def render(self):
        self.tilemap.render(self.display, self.render_scroll)
        self.player.render(self.display, self.render_scroll)

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
                if event.key == pygame.K_LEFT:
                    self.movement[0] = True
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = True
                if event.key == pygame.K_UP:
                    self.player.velocity[1] = -3

            # Key Up Event
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False


Game().run()
