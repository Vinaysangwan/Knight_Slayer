import pygame

PHYSICAL_TILES = {"grass", "desert", "farming", "snow", "ice"}


class Tilemap:
    def __init__(self, game, tile_size=32):
        self.game = game
        self.tile_size = tile_size

        self.tilemap = {}

        for i in range(10):
            self.tilemap[str(i + 3) + ";10"] = {"type": "grass", "variant": 0, "pos": [i + 3, 10]}
            self.tilemap["10;" + str(i + 5)] = {"type": "desert", "variant": 0, "pos": [10, i + 5]}

    def get_Neighbor_tiles(self, pos: list):
        neighbor_tiles = []

        current_cell = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

        for i in range(-1, 2):
            for j in range(-1, 2):
                loc = str(current_cell[0] + i) + ";" + str(current_cell[1] + j)
                if loc in self.tilemap:
                    neighbor_tiles.append(self.tilemap[loc])

        return neighbor_tiles

    def get_Neighbor_tiles_Rects(self, pos: list):
        rects = []

        for tile in self.get_Neighbor_tiles(pos):
            if tile["type"] in PHYSICAL_TILES:
                rects.append(
                    pygame.Rect(
                        tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size, self.tile_size, self.tile_size
                    )
                )

        return rects

    def render(self, surf, offset=[0, 0]):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] * self.tile_size - offset[0], tile["pos"][1] * self.tile_size - offset[1]),
            )
