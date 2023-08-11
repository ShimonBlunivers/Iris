import pygame, math

from animation import Animation
from label import Label

global karambit_image

karambit_image = pygame.image.load("files/kejn/karambit.png")
karambit_image = pygame.transform.scale(karambit_image, [50, 50])
karambit_image = pygame.transform.rotate(karambit_image, 90)

class Kejn(pygame.sprite.Sprite):

    def __init__(self, world, position):
        self.world = world

        super().__init__([self.world.trol_group, self.world.camera_group])

        self.walk_speed = 3
        
        self.attacking = False

        self.scale = 2.5

        self.size = [98, 115]

        self.size = [int(self.size[0] * self.scale), int(self.size[1] * self.scale)]

        self.image = pygame.image.load("files/kejn/kejn.png")
        self.image = pygame.transform.scale(self.image, self.size)

        # self.animations = []

        # self.standing_animation = Animation(self.world, self, [4, .5], ["trol/standing/1", "trol/standing/2"])

        # attacking_files = []

        # for i in range(5):
        #     attacking_files.append("trol/attacking/"+str(i+1))

        # self.attacking_animation = Animation(self.world, self, 0.2, attacking_files, repeat_times = 0)

        self.direction = [0, 0]

        self.spawn(position)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

        self.karambits = []
        self.spawn_karambits()

        self.label = Label(self.world, "Ahoj mrtki\nja jsem kejn a smrdim", self.rect.topleft, self.size)
        



    def spawn(self, position):
        self.original_position = position
        self.position = self.original_position

    def update(self):

        position = [self.position[0] + self.world.position[0], self.position[1] + self.world.position[1]]
        size = [self.size[0] * self.world.zoom, self.size[1] * self.world.zoom]

        self.rect.topleft = position
        self.rect.size = size

        for karambit in self.karambits:
            karambit.angle += 8

    def attack(self):
        self.attacking = True

    def spawn_karambits(self):

        center = [self.rect.center[0] - 100, self.rect.center[1]]
        amount = 40
        radius = 240

        step = 360 / amount

        for i in range(amount):



            self.karambits.append(Karambit(self.world, center, step * i, radius))

class Karambit:

    def __init__(self, world, position, angle, radius):

        self.world = world
        self.world.particles.append(self)

        self.center = [position[0], position[1]]
        self.position = [0, 0]
        self.angle = angle
        self.position[0] = self.center[0] + math.sin(math.radians(angle)) * radius
        self.position[1] = self.center[1] + math.cos(math.radians(angle)) * radius
        self.position = position
        self.radius = radius
        self.original_image = karambit_image

        self.image = self.original_image.copy()

    def update(self):
        self.position[0] = self.center[0] + math.sin(math.radians(self.angle))* self.radius
        self.position[1] = self.center[1] + math.cos(math.radians(self.angle))* self.radius
        position = [self.position[0] + self.world.position[0], self.position[1] + self.world.position[1]]
        self.image = pygame.transform.rotate(self.original_image.copy(), self.angle)

        

        self.world.screen.blit(self.image, position)