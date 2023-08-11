import pygame

from animation import Animation


class Trol(pygame.sprite.Sprite):

    def __init__(self, world, position):
        self.world = world

        super().__init__([self.world.entity_group, self.world.camera_group])

        self.walk_speed = 3

        self.ID = "Trol"
        
        self.attacking = False

        self.scale = 6

        self.size = [25, 50]

        self.size = [int(self.size[0] * self.scale), int(self.size[1] * self.scale)]

        self.animations = []

        self.idle_animation = Animation(self.world, self, [4, .5], ["trol/idle/0", "trol/idle/1"])

        attacking_files = []

        for i in range(5):
            attacking_files.append("trol/attack/"+str(i))

        self.attacking_animation = Animation(self.world, self, 0.2, attacking_files, repeat_times = 0)

        self.direction = [0, 0]

        self.spawn(position)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def spawn(self, position):
        self.original_position = position
        self.position = self.original_position

    def update(self):

        if self.direction[0] == 0:
            self.idle_animation.animate()

        if self.attacking:
            self.attacking_animation.animate()
            if self.attacking_animation.finished:
                self.attacking = False
        
        position = [self.position[0] + self.world.position[0], self.position[1] + self.world.position[1]]
        size = [self.size[0] * self.world.zoom, self.size[1] * self.world.zoom]

        self.rect.topleft = position
        self.rect.size = size

    def attack(self):
        self.attacking = True
        self.attacking_animation.reset_cycles()