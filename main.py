import pygame
import sys

from scripts.utils import load_image, load_rect_image
from scripts.entities import PhysicalEntity
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Knight Slayer")

        self.game_clock = pygame.time.Clock()

        # Assets
        self.assets = {
            "grass": load_rect_image("world_tileset.png", top_left_pos=[0, 0], size=[64, 64]),
            "desert": load_rect_image("world_tileset.png", top_left_pos=[64, 0], size=[64, 64]),
            "field": load_rect_image("world_tileset.png", top_left_pos=[128, 0], size=[64, 64]),
            "snow": load_rect_image("world_tileset.png", top_left_pos=[192, 0], size=[64, 64]),
            "ice": load_rect_image("world_tileset.png", top_left_pos=[256, 0], size=[64, 64]),
            "player": load_image("knight.png"),
        }

        # Tilemap
        self.tilemap = Tilemap(self)

        # Player
        self.player = PhysicalEntity(self, "player", (50, 50), (32, 32))
        self.movement = [False, False]

    def run(self):
        while True:
            self.screen.fill((0, 20, 100))

            self.poll_Event()
            self.update()
            self.render()

            pygame.display.update()
            self.game_clock.tick(60)

    def update(self):
        self.player.update(movement=(self.movement[1] - self.movement[0], 0) * 5)

    def render(self):
        self.tilemap.render(self.screen)
        self.player.render(self.screen)

    def poll_Event(self):
        for event in pygame.event.get():

            # Quit Event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Key Down Event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_LEFT:
                    self.movement[0] = True
                elif event.key == pygame.K_RIGHT:
                    self.movement[1] = True

            # Key Up Event
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                elif event.key == pygame.K_RIGHT:
                    self.movement[1] = False


# Calling the Run Function of the Game Class
Game().run()
