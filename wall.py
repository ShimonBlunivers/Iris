import pygame

from label import Label


class Wall(pygame.sprite.Sprite):

    def __init__(self, world, position, size = [100, 100]):
        self.world = world
        super().__init__([self.world.wall_group, self.world.camera_group])
        self.position = position
        self.size = size

        self.ID = "Wall"

        self.image = pygame.image.load("files/wall/0.png")
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()

        self.label = Label(self.world, "Wall", self.position, self.size)

    def update(self):
        self.rect.x = self.position[0] + self.world.position[0]
        self.rect.y = self.position[1] + self.world.position[1]