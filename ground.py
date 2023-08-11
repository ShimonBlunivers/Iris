
import pygame


class Path(pygame.sprite.Sprite):

    def __init__(self, world, position, size = [100, 100], color = [255, 192 ,203], visible = True):
        self.world = world
        super().__init__(self.world.path_group)

        self.ID = "Path"

        self.color = color
        self.visible = visible

        self.original_position = position
        self.position = self.original_position

        self.size = size

        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def update(self):

        position = [self.position[0] + self.world.position[0], self.position[1] + self.world.position[1]]
        size = [self.size[0] * self.world.zoom, self.size[1] * self.world.zoom]

        self.rect.topleft = position
        self.rect.size = size

        if self.visible:
            self.draw()

    def draw(self):
        pygame.draw.rect(self.world.screen, self.color, self.rect)

    def is_touching(self, rect):
        return self.rect.colliderect(rect)