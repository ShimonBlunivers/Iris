import pygame, random


class Light(pygame.sprite.Sprite):

    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]

    def __init__(self, world, radius, position = [0, 0], intensity = 80, follow = None, offset = [0, 0]):
        self.world = world
        super().__init__(self.world.light_group)

        self.position = position

        self.radius = radius

        self.percent_intensity = intensity
        self.intensity = (self.percent_intensity/100)*self.radius

        self.follow = follow

        self.offset = offset

        self.surface = pygame.surface.Surface([radius*2, radius*2])
        self.surface.fill(self.BLACK)
        self.surface.set_colorkey(self.BLACK)
        pygame.draw.circle(self.surface, self.WHITE, [radius, radius], self.intensity)

        self.r = 0

        self.light_surface = self.surface.copy()
        pygame.draw.circle(self.light_surface, self.WHITE, [radius, radius], radius)

        self.changed = False


    def update(self):
        
        self.intensity = (self.percent_intensity/100)*self.radius
        if self.follow != None:
            self.move(self.follow)

        timer = .7

        if round(round(self.world.game_clock, 1) % timer, 1) == 0 and not self.changed:

            self.changed = True

            self.r = random.randint(0, 3)
        
        elif not round(round(self.world.game_clock, 1) % timer, 1) == 0:
            self.changed = False

        self.surface.fill(self.BLACK)
        self.light_surface.fill(self.BLACK)
        pygame.draw.circle(self.surface, self.WHITE, [self.radius, self.radius], self.radius - self.r)
        pygame.draw.circle(self.light_surface, self.WHITE, [self.radius + (self.r-(self.r/2)), self.radius + (self.r-(self.r/2))], self.intensity - self.r)

        self.world.shadow_layer.blit(self.surface, [self.position[0] + self.world.position[0] - self.radius, self.position[1] + self.world.position[1] - self.radius])
        self.world.light_layer.blit(self.light_surface, [self.position[0] + self.world.position[0] - self.radius, self.position[1] + self.world.position[1] - self.radius])

    def move(self, follow):
        followed_position = [follow.position[0] + follow.size[0]/2 + self.offset[0], follow.position[1] + follow.size[1]/2 + self.offset[1]]


        self.position[0] = followed_position[0]
        self.position[1] = followed_position[1]