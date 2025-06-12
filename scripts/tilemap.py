import pygame
import json

PHYSICAL_TILES = {"grass", "desert", "farming", "snow", "ice"}
AUTOTILE_TILES = {"grass", "desert", "farming", "snow", "ice"}
AUTOTILE_TREES = {"green_tree", "yellow_tree", "light_green_tree"}

rules_autotile_tiles = {
    tuple(sorted([(0, 1)])): 0,
    tuple(sorted([(0, -1)])): 1,
    tuple(sorted([(0, -1), (0, 1)])): 1,
    tuple(sorted([])): 0,
}

rules_autotile_trees = {
    tuple(sorted([(0, 1)])): 0,
    tuple(sorted([(0, 1), (0, -1)])): 1,
    tuple(sorted([(0, -1)])): 2,
}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size

        self.tilemap = {}

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

    def auto_Tile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]

            neighbor_tiles = set()
            neighbor_trees = set()
            for shift in [(0, -1), (0, 1)]:
                check_loc = str(tile["pos"][0] + shift[0]) + ";" + str(tile["pos"][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]["type"] in AUTOTILE_TILES:
                        neighbor_tiles.add(shift)
                    elif self.tilemap[check_loc]["type"] in AUTOTILE_TREES:
                        neighbor_trees.add(shift)

            neighbor_tiles = tuple(sorted(neighbor_tiles))
            neighbor_trees = tuple(sorted(neighbor_trees))

            if neighbor_tiles in rules_autotile_tiles:
                tile["variant"] = rules_autotile_tiles[neighbor_tiles]

            if neighbor_trees in rules_autotile_trees:
                tile["variant"] = rules_autotile_trees[neighbor_trees]

    def render(self, surf, offset=[0, 0]):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] * self.tile_size - offset[0], tile["pos"][1] * self.tile_size - offset[1]),
            )

    def save(self, path: str):
        f = open(path, "w")
        json.dump({"Tile Size": self.tile_size, "Tilemap": self.tilemap}, f)
        f.close()

    def load(self, path: str):
        f = open(path, "r")
        map_data = json.load(f)
        f.close()

        self.tile_size = map_data["Tile Size"]
        self.tilemap = map_data["Tilemap"]
