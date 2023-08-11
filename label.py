import pygame


class Label:

    def __init__(self, world, text, position, size, follow_camera = True, follow = None):
        self.world = world
        self.world.label_list.append(self)
        self.active = False
        self.position = position
        self.size = size
        self.follow_camera = follow_camera
        self.follow = follow

        self.rect = pygame.rect.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

        self.text = text

    def update(self):
        if self.follow != None:
            self.position = self.follow.position

        if self.world.mouse_rect.colliderect(self.rect):
            self.active = True
        else:
            self.active = False
        if self.follow_camera:
            self.rect.left = self.position[0] + self.world.position[0]
            self.rect.top = self.position[1] + self.world.position[1]
    
    def kill(self):
        self.active = False
        self.world.label_list.remove(self)