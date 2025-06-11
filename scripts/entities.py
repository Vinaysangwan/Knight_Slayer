import pygame


class PhysicalEntity:
    def __init__(self, game, e_type: str, pos: list, size=[32, 32], offset=[0, 0]):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.offset = offset

        self.frame = 0
        self.velocity = [0, 0]
        self.collision = {"up": False, "down": False, "left": False, "right": False}

    def get_Entity_Rect(self):
        self.collision = {"up": False, "down": False, "left": False, "right": False}
        return pygame.Rect(self.pos[0] + self.offset[0], self.pos[1] + self.offset[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=[0, 0]):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Collison in X-axis
        self.pos[0] += frame_movement[0]
        entity_rect = self.get_Entity_Rect()
        for rect in tilemap.get_Neighbor_tiles_Rects(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collision["left"] = True
                elif frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collision["right"] = True
                self.pos[0] = entity_rect.x - self.offset[0]

        # Collison in Y-axis
        self.pos[1] += frame_movement[1]
        entity_rect = self.get_Entity_Rect()
        for rect in tilemap.get_Neighbor_tiles_Rects(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collision["up"] = True
                elif frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collision["down"] = True
                self.pos[1] = entity_rect.y - self.offset[1]

        # Gravity
        if self.collision["down"] or self.collision["up"]:
            self.velocity[1] = 0
        else:
            self.velocity[1] = min(self.velocity[1] + 0.1, 5)

    def render(self, surf):
        surf.blit(self.game.assets[self.type][self.frame], self.pos)
