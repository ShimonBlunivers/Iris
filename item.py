import pygame
from label import Label

class Item:
    def __init__(self, world, name, path, stack = 64):
        self.world = world
        self.name = name
        self.image = pygame.image.load(f"files/items/{path}")

        self.world.item_list.append(self)

        self.stack = stack


class ItemDrop(pygame.sprite.Sprite):
    def __init__(self, world, item, position, size = 60):
        self.world = world
        self.item = item
        self.ID = self.item.name
        super().__init__([self.world.itemdrop_group, self.world.camera_group])

        self.image = self.item.image

        self.position = position
        self.starting_position = position.copy()
        self.offset = 0
        self.swing_strenght = 20
        self.going_up = True
        self.swing_speed = 1
        self.size = size

        self.pick_size_multiplier = 3

        self.image = pygame.transform.scale(self.image, [self.size, self.size])

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position[0] + self.world.position[0], self.position[1] + self.world.position[1]]

        self.picking_up_rect = self.rect.copy()
        self.picking_up_rect.width = self.rect.width * self.pick_size_multiplier
        self.picking_up_rect.height = self.rect.height * self.pick_size_multiplier

        self.picking_up = False

        self.picking_up_block = False

        self.block_timer = 0

        self.label = Label(self.world, self.item.name, self.position, [self.size, self.size])
        self.label.position = self.position

    def update(self):
        
        if self.picking_up_block:
            self.picking_up = False
        
        if self.picking_up_block:
            self.update_block()

        self.rect.topleft = [self.position[0] + self.world.position[0], self.position[1] + self.world.position[1] + self.offset]
        self.swing()
        self.detect_player()

    def swing(self):
        if self.going_up:
            if self.offset < self.swing_strenght:
                self.offset += self.swing_speed
            else:
                self.going_up = False
        else:
            if self.offset > -self.swing_strenght:
                self.offset -= self.swing_speed
            else:
                self.going_up = True

    def detect_player(self):

        self.picking_up_rect.center = [self.rect.center[0] - self.offset, self.rect.center[1] - self.offset]
        if not self.world.player.inventory_full and not self.picking_up_block:

            if not self.picking_up and self.picking_up_rect.colliderect(self.world.player.rect):
                self.picking_up = True

            if self.picking_up:
                self.position[0] += (self.world.player.position[0] - self.position[0]) / 4
                self.position[1] += (self.world.player.position[1] - self.position[1]) / 4

            if abs(self.world.player.position[0] - self.position[0]) < 20 and abs(self.world.player.position[1] - self.position[1]) < 20:
                self.world.player.pick_item(self, 1)
            
    def block_picking_up(self, time = 2.5):
        self.block_timer = time 
        self.time_when_blocked = self.world.now
        self.picking_up_block = True
    
    def update_block(self):
        if self.world.now - self.time_when_blocked >= self.block_timer:
            self.picking_up_block = False