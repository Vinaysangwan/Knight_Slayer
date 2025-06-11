import pygame


class PhysicalEntity:
    def __init__(self, game, e_type: str, pos: list, size=[16, 16], sprite_offset=[0, 0]):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.sprite_offset = sprite_offset
        self.size = [size[0], size[1]]

        self.velocity = [0, 0]
        self.collision = {"up": False, "down": False, "left": False, "right": False}

        self.frame = 0
        self.flip = False
        self.current_action = ""
        self.set_Action("Idle")
        self.animation

    def set_Action(self, action: str):
        if self.current_action != action:
            self.current_action = action
            self.animation = self.game.assets[self.type + "/" + self.current_action].get_Animation()

    def get_Entity_Rect(self):
        self.collision = {"up": False, "down": False, "left": False, "right": False}
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

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
                self.pos[0] = entity_rect.x

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
                self.pos[1] = entity_rect.y

        if frame_movement[0] < 0:
            self.flip = True
        elif frame_movement[0] > 0:
            self.flip = False

        # Gravity
        if self.collision["down"] or self.collision["up"]:
            self.velocity[1] = 0
        else:
            self.velocity[1] = min(self.velocity[1] + 0.1, 5)

        # Update Animation
        self.animation.update()

    def render(self, surf, offset=[0, 0]):
        surf.blit(
            pygame.transform.flip(self.animation.get_Anim_Image(), self.flip, False),
            (self.pos[0] - offset[0] - self.sprite_offset[0], self.pos[1] - offset[1] - self.sprite_offset[1]),
        )


class Player(PhysicalEntity):
    def __init__(self, game, pos):
        super().__init__(game, "player", pos, size=[14, 16], sprite_offset=[0, 3])

        self.air_time = 0

    def update(self, tilemap, movement=[0, 0]):
        super().update(tilemap, movement)

        if self.air_time > 4:
            self.set_Action("Jump")
        elif movement[0] != 0:
            self.set_Action("Run")
        else:
            self.set_Action("Idle")

        if self.collision["down"]:
            self.air_time = 0
        else:
            self.air_time += 1
