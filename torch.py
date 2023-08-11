import pygame, random
from animation import Animation
from light import Light


class Torch(pygame.sprite.Sprite):

    def __init__(self, world, position):
        self.world = world
        super().__init__([self.world.torch_group, self.world.camera_group])
        self.position = position
        self.size = [60, 80]
        self.strength = 60

        self.ID = "Torch"

        starting_frame = random.randint(0, 2)

        self.light = Light(self.world, 220, [self.position[0] + self.size[0]/2, self.position[1] + 10], 50)

        self.animations = []

        self.animation = Animation(self.world, self, .7, ["torch/0", "torch/1", "torch/2",], start_frame = starting_frame)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])


    def update(self):
        self.animation.animate()
        self.rect.x = self.position[0] + self.world.position[0]
        self.rect.y = self.position[1] + self.world.position[1]