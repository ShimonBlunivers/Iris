import pygame

global background_image, topleft, topright, bottomleft, bottomright

background_image = pygame.image.load("files/text/border/background.png")
topleft = pygame.transform.scale(pygame.image.load("files/text/border/topleft.png"), [15, 15])
topright = pygame.transform.scale(pygame.image.load("files/text/border/topright.png"), [15, 15])
bottomleft = pygame.transform.scale(pygame.image.load("files/text/border/bottomleft.png"), [15, 15])
bottomright = pygame.transform.scale(pygame.image.load("files/text/border/bottomright.png"), [15, 15])


class Text:

    def __init__(self, world, position, txt):
        if txt == "":
            return

        self.world = world
        self.position = position
        self.txt = txt.split("\n")
        self.surface = self.world.text_layer

        self.width = 0
        
        self.text = []
        for line in self.txt:
            text = self.world.FONT.render(line, True, self.world.WHITE)
            self.text.append(text)
            if text.get_rect().width > self.width:
                self.width = text.get_rect().width
        
        self.line_height = self.text[0].get_rect().height

        self.box = pygame.rect.Rect(self.position[0], self.position[1], self.width,  self.line_height* len(self.text))

        self.spacing = 20
        self.box.bottomleft = [self.position[0] + self.spacing, self.position[1] - self.spacing]

        if self.box.right + self.spacing >= self.world.resolution[0]:
            self.box.right = self.world.resolution[0] - self.spacing
        elif self.box.left - self.spacing <= 0:
            self.box.left = self.spacing

        if self.box.bottom + self.spacing >= self.world.resolution[1]:
            self.box.bottom = self.world.resolution[1] - self.spacing
        elif self.box.top - self.spacing <= 0:
            self.box.top = self.spacing

        self.box.left = self.box.left - self.spacing
        self.box.top = self.box.top - self.spacing

        self.box.width = self.box.width + self.spacing * 2
        self.box.height = self.box.height + self.spacing * 2

        self.border = pygame.transform.scale(background_image, [self.box.width, self.box.height])

        self.surface.blit(self.border, self.box.topleft)

        pygame.draw.rect(self.surface, [24, 20, 37], self.box, width = 7)
        
        self.surface.blit(topleft, self.box.topleft)
        self.surface.blit(topright, [self.box.topright[0] - 15, self.box.topright[1]])
        self.surface.blit(bottomleft, [self.box.bottomleft[0], self.box.bottomleft[1] - 15])
        self.surface.blit(bottomright, [self.box.bottomright[0] - 15, self.box.bottomright[1] - 15])

        for i in range(len(self.text)):
            self.surface.blit(self.text[i], [self.box.left + self.spacing, self.box.top + self.spacing + self.line_height * i])