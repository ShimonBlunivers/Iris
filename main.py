import pygame, json, time


from pygame import mixer

from light import Light
from text import Text
from player import Player
from item import Item
from hud import HUD

from objects import objects

pygame.init()
mixer.init()


class World:

    FONT = pygame.font.Font("files/text/fonts/november.regular.ttf", 32)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED =  (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self):
        self.world = self

        self.resolution = (1920, 1080) 
        self.screen = pygame.display.set_mode([self.resolution[0], self.resolution[1]])

        self.transparent_layer = pygame.surface.Surface([self.resolution[0], self.resolution[1]])

        self.icon = pygame.image.load("files/icon.png")

        pygame.display.set_caption('Iris')
        pygame.display.set_icon(self.icon)


        self.original_darkness = 95     # %

        self.original_brightness = 10     # %

        self.darkness = self.original_darkness
        self.brightness = self.original_brightness

        self.shadow_layer = pygame.surface.Surface([self.resolution[0], self.resolution[1]])

        self.shadow_layer.fill([0, 0, 0])
        self.shadow_layer.set_colorkey([255, 255, 255])
        self.shadow_layer.set_alpha(int(255*self.darkness/100)%256)

        self.light_layer = pygame.surface.Surface([self.resolution[0], self.resolution[1]])

        self.light_layer.fill([0, 0, 0])
        self.light_layer.set_colorkey([0, 0, 0])
        self.light_layer.set_alpha(int(255*self.brightness/100)%256)

        self.text_layer = pygame.surface.Surface([self.resolution[0], self.resolution[1]])
        self.text_layer.fill([69, 69, 69])
        self.text_layer.set_colorkey([69, 69, 69])

        self.talk_layer = pygame.surface.Surface([self.resolution[0], self.resolution[1]])
        self.talk_layer.fill([69, 69, 69])
        self.talk_layer.set_colorkey([69, 69, 69])

        self.item_hover_layer = pygame.surface.Surface([self.resolution[0], self.resolution[1]])
        self.item_hover_layer.fill([69, 69, 69])
        self.item_hover_layer.set_colorkey([69, 69, 69])
        self.item_hover_layer.set_alpha(155)

        self.background_color = [17, 51, 0]

        self.position = [0, 0]
        self.zoom = 1
        self.scroll = [0, 0]

        self.running = True

        self.day = True

        #   SYSTEM INIT

        cursor = pygame.image.load("files/cursor/0.png")
        self.cursor = pygame.cursors.Cursor((0, 0), cursor)
        pygame.mouse.set_cursor(self.cursor)

        self.mouse_rect = pygame.rect.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)

        self.transparent_layer_opacity = 122
        self.transparent_layer.set_alpha(self.transparent_layer_opacity)
        self.transparent_layer.set_colorkey([69, 69, 69])

        #   SPRITE GROUPS

        self.label_list = []
        self.particles = []

        self.camera_group = CameraGroup(self)

        self.itemdrop_group = pygame.sprite.Group() 
        self.HUD_group = pygame.sprite.Group()
        self.light_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.entity_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.path_group = pygame.sprite.Group()
        self.torch_group = pygame.sprite.Group()

        #   TIME SETUP

        self.day_duration = 10

        self.fps_clock = pygame.time.Clock()
        self.start_time = time.time()

        self.FPS = 60

        self.prev_time = time.time()

        #   ITEM INITIALIZATION

        self.item_list = []

        self.shovel_item = Item(self, "Shovel", "shovel/0.png")
        self.key_item = Item(self.world, "Key", "key/0.png")

        #   OBJECT INITIALIZATION

        self.objects = objects

        #   WORLD CREATION

        self.player = Player(self)
        self.player_vision = Light(self, self.player.sight, [self.player.rect.center[0], self.player.rect.center[1]], 60, self.player)
        self.HUD = HUD(self, self.player)

        with open('files/world.txt') as world_file:
            data = json.load(world_file)
            for key in data:
                args = []
                for obj in data[key]:
                    for arg in obj:
                        args.append(arg)
                    self.objects[key](self, *args)
                    args = []


    def update(self):

        #   MOUSE

        self.mouse_rect.topleft = pygame.mouse.get_pos()

        #   TEXT CLEAR

        self.text_layer.fill([69, 69, 69])

        #   TIME   

        self.game_clock = round(time.time() - self.start_time, 2)
        self.fps_clock.tick(self.FPS)
        self.now = time.time()
        self.delta_time = (self.now - self.prev_time) * 100
        self.prev_time = self.now

        #   SPRITE UPDATE
        
        self.update_light()
        
        label_counter = {}
        offset = 0
        for i in range(len(self.label_list)):
            self.label_list[i].update()
            if self.label_list[i].active and self.label_list[i].text != "":
                if not self.label_list[i].text in label_counter.keys(): 
                    label_counter[self.label_list[i].text] = 1
                else:
                    label_counter[self.label_list[i].text] += 1
        for key in label_counter:

            if label_counter[key] == 1: 
                txt = Text(world, [self.mouse_rect.left, self.mouse_rect.top + offset], key)
            else:
                txt = Text(world, [self.mouse_rect.left, self.mouse_rect.top + offset], key + " " + str(label_counter[key]) + "x")
            offset -= txt.border.get_rect().height

        self.path_group.update()
        self.wall_group.update()
        self.torch_group.update()
        self.itemdrop_group.update()
        self.player_group.update()

        for sprite in self.entity_group.sprites():
            try:
                sprite.group.update()
            except:
                sprite.update()

        #   DEBUG

        #   CAMERA UPDATE

        self.camera_group.update()
        self.screen.blit(self.transparent_layer, [0, 0])

        #   DISPLAY UPDATE

        for particle in self.particles:
            particle.update()

        self.screen.blit(self.shadow_layer, [0, 0])
        self.screen.blit(self.light_layer, [0, 0])
        
        #   HUD UPDATE

        self.HUD_group.update()

        self.screen.blit(self.item_hover_layer, [0, 0])

        self.screen.blit(self.text_layer, [0, 0])
        self.screen.blit(self.talk_layer, [0, 0])

        pygame.display.flip()
        self.transparent_layer.fill([69, 69, 69])
        self.item_hover_layer.fill([69, 69, 69])
        self.talk_layer.fill([69, 69, 69])
        self.screen.fill(self.background_color)

    def update_light(self):
        self.change_light_alpha()
        self.change_shadow_alpha()
        self.shadow_layer.fill([0, 0, 0])
        self.light_layer.fill([0, 0, 0])
        self.light_group.update()
        
    def change_shadow_alpha(self):
        self.shadow_layer.set_alpha(int(255*self.darkness/100)%256)

    def change_light_alpha(self):
        self.light_layer.set_alpha(int(255*self.brightness/100)%256)


class CameraGroup(pygame.sprite.Group):
    def __init__(self, world):

        self.world = world

        super().__init__()

    def update(self):
        
        self.custom_draw(self.world.screen)
        self.move_camera(self.world.player)
        # self.apply_transparency_SFX()

    def custom_draw(self, screen):
        before_player = True
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.bottom):
            surface = screen

            if not before_player:
                if sprite.rect.colliderect(self.world.player.rect):
                    surface = self.world.transparent_layer

            try:
                list = sprite.group
                for s in list:
                    surface.blit(s.image, s.rect)
            except:
                surface.blit(sprite.image, sprite.rect)
            
            if type(sprite) == Player:
                before_player = False
            
    def move_camera(self, follow, smoothing = 20):
        followed_position = [follow.position[0] + follow.size[0]/2, follow.position[1] + follow.size[1]/2]
        camera_center = [self.world.resolution[0]/2, self.world.resolution[1]/2]

        self.world.position[0] -= int(((followed_position[0] + self.world.position[0]) - camera_center[0]) /smoothing)
        self.world.position[1] -= int(((followed_position[1] + self.world.position[1]) - camera_center[1]) /smoothing)

    def apply_transparency_SFX(self):
        step = 10
        line_width = 3
        for phase in range(int(self.world.resolution[0]/step)):
            x = phase * step + self.world.position[0] % step
            y = phase * step + self.world.position[1] % step
            pygame.draw.line(self.world.transparent_layer, [69, 69, 69], [x, 0], [0, y], line_width)
            pygame.draw.line(self.world.transparent_layer, [69, 69, 69], [x, self.world.resolution[1]], [0, self.world.resolution[1] - y], line_width)



world = World()

while world.running:

    world.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            world.running = False
            pygame.quit()
