import pygame, math

from animation import Animation
from label import Label

class King(pygame.sprite.Sprite):

    def __init__(self, world, position):
        self.world = world

        super().__init__([self.world.entity_group, self.world.camera_group])

        self.walk_speed = 3

        self.ID = "King"
        
        self.attacking = False

        self.scale = 2.5

        self.size = [80, 110]

        self.size = [int(self.size[0] * self.scale), int(self.size[1] * self.scale)]

        self.animations = []

        self.idle_animation = Animation(self.world, self, [5, .5], ["king/idle/0", "king/idle/1"])
        
        self.wave_animation = Animation(self.world, self, [4, .4], ["king/wave/0", "king/wave/1"])

        self.direction = [0, 0]

        self.spawn(position)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

        self.label = Label(self.world, "The King", self.rect.topleft, self.size, follow=self)


        self.throne_background = Throne(self, 0)
        self.throne_frontground = Throne(self, 1)

        self.group = pygame.sprite.Group([self.throne_background, self, self.throne_frontground])

        self.waving = False


    def spawn(self, position):
        self.original_position = list(position)
        self.position = self.original_position

    def update(self):
        if self.waving:
            self.wave_animation.animate()
        else:
            self.idle_animation.animate()

        position = [self.position[0] + self.world.position[0], self.position[1] + self.world.position[1]]
        size = [self.size[0] * self.world.zoom, self.size[1] * self.world.zoom]

        self.rect.topleft = position
        self.rect.size = size


    def attack(self):
        self.attacking = True


class Throne(pygame.sprite.Sprite):

    def __init__(self, king, index):
        self.king = king
        self.world = self.king.world
        self.index = index
        self.position = king.position.copy()

        super().__init__()

        if self.index == 0:
            self.image = pygame.transform.scale(pygame.image.load("files/king/throne/0.png"), king.size)
        elif self.index == 1:
            self.image = pygame.transform.scale(pygame.image.load("files/king/throne/1.png"), king.size)

        self.rect = self.image.get_rect()


    def update(self):
        self.position = self.king.position
        position = [self.position[0] + self.world.position[0], self.position[1] + self.world.position[1]]
        self.rect.topleft = position