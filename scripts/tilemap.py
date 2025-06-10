import pygame


class Tilemap:
    def __init__(self, game, img_size=64, tile_size=32):
        self.game = game
        self.img_size = img_size
        self.tile_size = tile_size

        self.tilemap = {}

        for i in range(10):
            self.tilemap[str(3 + i) + ";10"] = {"type": "grass", "variant_pos": [0, 0], "pos": [3 + i, 10]}

    def render(self, surf):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(
                self.game.assets[tile["type"]],
                (tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size),
                (tile["variant_pos"][0], tile["variant_pos"][1], self.tile_size, self.tile_size),
            )
