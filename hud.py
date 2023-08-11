import pygame

from label import Label

class HUD(pygame.sprite.Sprite):
    
    def __init__(self, world, player):
        self.world = world
        self.player = player
        super().__init__(self.world.HUD_group)

        self.surface = pygame.surface.Surface([self.world.resolution[0], self.world.resolution[1]])
        self.surface.fill([69, 69, 69])

        self.surface.set_colorkey([69, 69, 69])

        self.clean_surface = self.surface.copy()

        self.opacity = 100

        self.surface.set_alpha(int(255*self.opacity/100)%256)

        self.inventory_slots = InventorySlots(self.world, self)

        self.healthbar = HealthBar(self.world, self)
        self.staminabar = StaminaBar(self.world, self)

    def update(self):
        self.surface = self.clean_surface
        self.healthbar.update()
        self.staminabar.update()
        self.inventory_slots.update()
        self.world.screen.blit(self.surface, [0, 0])


class InventorySlots:
    def __init__(self, world, hud):
        self.world = world
        self.hud = hud
        self.slots = []
        number_of_slots = 9
        self.bar_color = [100, 100, 100]
        self.background = [50, 50, 50]

        self.highlighted_slot = None

        self.highlighted_color = [250, 255, 135]

        self.bar_size = self.world.resolution[0] / (number_of_slots+4)

        self.border = 6

        for i in range(number_of_slots):
            newSlot = Slot(self.world, self, i)
            self.slots.append(newSlot)

    def set_highlighted(self, index):
        if not self.slots[index].highlight_locked:
            self.highlighted_slot = None
            if self.slots[index].highlighted:
                self.slots[index].highlighted = False
                self.slots[index].highlight_locked = True
            else:
                for slot in self.slots:
                    slot.highlighted = False
                    slot.highlight_locked = False

                self.highlighted_slot = self.slots[index]
                self.slots[index].highlighted = True
                self.slots[index].highlight_locked = True


    def update(self):
        for slot in self.slots:
            slot.update()


    def find_item(self, item):
        for slot in self.slots:
            if slot.item == item:
                if slot.full == False:
                    return slot

        return None

class Slot:

    def __init__(self, world, inventory_slots, index):
        self.world = world
        self.inventory_slots = inventory_slots
        self.index = index
        self.background = self.inventory_slots.background
        self.bar_color = self.inventory_slots.bar_color

        self.size = self.inventory_slots.bar_size

        self.rect = pygame.Rect(0, 0, self.inventory_slots.bar_size, self.inventory_slots.bar_size)
        self.rect.left = self.inventory_slots.bar_size * 2 + self.inventory_slots.bar_size * self.index
        self.rect.bottom = self.world.resolution[1]
        self.position = [self.rect.left, self.rect.top]

        self.highlighted = False
        self.highlight_locked = False

        self.item = None

        self.amount = 0

        self.amount_label = ""

        self.label = Label(self.world, "", self.position, [self.size, self.size], False)

        self.max_amount = 0

        self.full = False

        self.item_image_size = self.rect.width - self.inventory_slots.border*2 - 10
        self.item_image_rect = self.rect.copy()
        self.item_image_rect.width = self.item_image_size
        self.item_image_rect.height = self.item_image_size
        self.item_image_rect.center = self.rect.center

    def update(self):
    
        if self.amount < self.max_amount:
            self.full = False

        if self.amount == 0:
            self.item = None

        pygame.draw.rect(self.inventory_slots.hud.surface, self.background, self.rect)

        if self.item != None:
            self.max_amount = self.item.stack
            self.amount_label = str(self.amount)
            text = self.world.FONT.render(self.amount_label, True, self.world.WHITE)
            
            self.inventory_slots.hud.surface.blit(pygame.transform.scale(self.item.image.copy(), [self.item_image_size, self.item_image_size]), self.item_image_rect)
            self.inventory_slots.hud.surface.blit(text, [self.rect.x + 10, self.rect.y + 14])

        if self.highlighted:
            pygame.draw.rect(self.inventory_slots.hud.surface, self.inventory_slots.highlighted_color, self.rect, width=self.inventory_slots.border)
        else:
            pygame.draw.rect(self.inventory_slots.hud.surface, self.bar_color, self.rect, width=self.inventory_slots.border)

        if self.item != None:
            self.label.text = self.item.name
        else:
            self.label.text = ""

    def assign_item(self, item):
        amount = 1
        if self.item != item:
            self.item = item

        if self.amount + amount <= item.stack:
            self.amount += amount

        else:
            if self.amount == self.max_amount:
                self.full = True


class HealthBar:

    def __init__(self, world, hud):
        self.world = world
        self.hud = hud
        self.player = self.hud.player

        self.size = [100, 600]

        self.outline = [50, 50, 50]

        self.health_color = [136, 8, 8]
        self.background = [100, 100, 100]

        self.padding = [10, self.world.resolution[1]/2 - (self.size[1]/2)]

        self.rect = pygame.Rect(self.padding[0], self.padding[1], self.size[0], self.size[1])
        self.health_rect = pygame.Rect(self.padding[0], self.padding[1], self.size[0], self.size[1])

        self.health_percent = self.player.max_health / self.player.health

        self.label = Label(self.world, "Health", self.rect.topleft, self.size, False)

    def update(self):
        text = self.world.FONT.render(str(int(self.health_percent * 100)) + "%", True, self.world.WHITE)

        pygame.draw.rect(self.hud.surface, self.background, self.rect)
        pygame.draw.rect(self.hud.surface, self.health_color, self.health_rect)
        pygame.draw.rect(self.hud.surface, self.outline, self.rect, width = 5)

        self.health_percent = self.player.health / self.player.max_health

        self.health_rect.height = self.rect.height * self.health_percent

        self.health_rect.bottom = self.rect.bottom

        text_rect = text.get_rect()

        self.hud.surface.blit(text, [self.rect.center[0] - text_rect.width/2, self.rect.center[1] - text_rect.height/2])

class StaminaBar:

    def __init__(self, world, hud):
        self.world = world
        self.hud = hud
        self.player = self.hud.player

        self.size = [100, 600]

        self.outline = [50, 50, 50]

        self.stamina_color = [136, 133, 8]
        self.background = [100, 100, 100]

        self.padding = [self.hud.healthbar.size[0] + self.hud.healthbar.padding[0] + 10, self.world.resolution[1]/2 - (self.size[1]/2)]

        self.rect = pygame.Rect(self.padding[0], self.padding[1], self.size[0], self.size[1])
        self.stamina_rect = pygame.Rect(self.padding[0], self.padding[1], self.size[0], self.size[1])

        self.stamina_percent = self.player.max_stamina / self.player.stamina

        self.label = Label(self.world, "Stamina", self.rect.topleft, self.size, False)

    def update(self):
        text = self.world.FONT.render(str(int(self.stamina_percent * 100)) + "%", True, self.world.WHITE)

        pygame.draw.rect(self.hud.surface, self.background, self.rect)
        pygame.draw.rect(self.hud.surface, self.stamina_color, self.stamina_rect)
        pygame.draw.rect(self.hud.surface, self.outline, self.rect, width = 5)

        self.stamina_percent = self.player.stamina / self.player.max_stamina

        self.stamina_rect.height = self.rect.height * self.stamina_percent

        self.stamina_rect.bottom = self.rect.bottom

        text_rect = text.get_rect()

        self.hud.surface.blit(text, [self.rect.center[0] - text_rect.width/2, self.rect.center[1] - text_rect.height/2])

class ItemHover:

    def __init__(self, world, slot):
        self.world = world
        self.slot = slot

        self.rect = self.slot.item_image_rect.copy()

        self.rect.width = self.rect.width /1.2
        self.rect.height = self.rect.height /1.2

        self.image = pygame.transform.scale(self.slot.item.image, [self.rect.width, self.rect.height])
    
    def update(self):

        self.rect.center = pygame.mouse.get_pos()
        self.world.item_hover_layer.blit(self.image, self.rect)