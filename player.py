import pygame
from random import *
from animation import Animation
from pygame import mixer
from hud import ItemHover
from item import ItemDrop

mixer.init()

mixer.set_num_channels(3)

slide_channel = mixer.Channel(0)

slide = mixer.Sound("files/player/walk/slide.wav")

walk_channel = mixer.Channel(1)

walk = mixer.Sound("files/player/walk/walk.mp3")

heartbeat_channel = mixer.Channel(2)

heartbeat = mixer.Sound("files/player/run/heartbeat.wav")


class Player(pygame.sprite.Sprite):

    def __init__(self, world):
        self.world = world
        super().__init__([self.world.player_group, self.world.camera_group])

        self.max_health = 100
        self.max_stamina = 100

        self.ID = "Player"

        self.running_price = .6
        self.stamina_regen = .2

        self.max_sight = 300
        self.sight = self.max_sight

        self.health = self.max_health
        self.stamina = self.max_stamina

        self.original_walk_speed = 4
        self.walk_speed = self.original_walk_speed

        self.run_speed = 6

        self.scale = 4

        self.size = [17, 35]

        self.size = [int(self.size[0] * self.scale), int(self.size[1] * self.scale)]

        self.animations = []

        self.dead = False

        self.inventory_full = False

        #   CONTROL VARIABLES

        self.show_inventory = False

        self.q_lock = False

        self.tab_lock = False

        self.mouse_click_available = True

        self.picked_slot = None

        self.hover_item = None

        self.running = False

        #   LOADING IMAGES

        walk_text = []

        for i in range(16):
            walk_text.append(f"player/walk/{i}")

        self.walk_animation = Animation(self.world, self, .05, walk_text)
        self.idle_animation = Animation(self.world, self, [5, .3], ["player/idle/0", "player/idle/1"])

        self.spawn([400, 300])

        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

        self.leg_rec = pygame.Rect(self.position[0], self.position[1] + self.size[1] - 20, self.size[0], 20)

    def spawn(self, position):
        self.original_position = position
        self.position = self.original_position

    def control(self):

        keys = pygame.key.get_pressed()

        speed = self.walk_speed

        velocity = pygame.Vector2([0, 0])

        direction = [0, 0] # X, Y      1 = dolů, doprava       -1 = nahoru, doleva

        #   DEBUG
   
        if keys[pygame.K_c]:
            k = randint(0, len(self.world.item_list) - 1)
            ItemDrop(self.world, self.world.item_list[k], [400, 200])

        #   CONTROLS

        if self.hover_item != None:
            self.hover_item.update()

        if self.mouse_click_available and pygame.mouse.get_pressed()[0]:
            for slot in self.world.HUD.inventory_slots.slots:
                if self.world.mouse_rect.colliderect(slot.rect):
                    if slot.item != None:
                        self.picked_slot = slot
                        self.hover_item = ItemHover(self.world, self.picked_slot)

        if self.picked_slot != None and pygame.mouse.get_pressed()[2]:
            self.picked_slot = None
            self.hover_item = None

        if self.picked_slot != None and not pygame.mouse.get_pressed()[0]:
            hit_anything = False
            for slot in self.world.HUD.inventory_slots.slots:
                if self.world.mouse_rect.colliderect(slot.rect):
                    hit_anything = True
                    item1 = self.picked_slot.item
                    amount1 = self.picked_slot.amount
                    item2 = slot.item
                    amount2 = slot.amount

                    self.picked_slot.item = item2
                    self.picked_slot.amount = amount2
                    slot.item = item1
                    slot.amount = amount1
            if not hit_anything:
                self.drop_item(self.picked_slot, self.picked_slot.amount)

        if keys[pygame.K_TAB] and not self.tab_lock:
            self.show_inventory = not self.show_inventory
            self.tab_lock = True
        elif not keys[pygame.K_TAB]:
            self.tab_lock = False

        if keys[pygame.K_q] and not self.q_lock:

            self.drop_item(self.world.HUD.inventory_slots.highlighted_slot)
            self.q_lock = True
        elif not keys[pygame.K_q]:
            self.q_lock = False

        if keys[pygame.K_LSHIFT]:
            self.running = True
        else:
            self.running = False

        if keys[pygame.K_1]:
            self.world.HUD.inventory_slots.set_highlighted(0)
        else:
            self.world.HUD.inventory_slots.slots[0].highlight_locked = False
        if keys[pygame.K_2]:
            self.world.HUD.inventory_slots.set_highlighted(1)
        else:
            self.world.HUD.inventory_slots.slots[1].highlight_locked = False
        if keys[pygame.K_3]:
            self.world.HUD.inventory_slots.set_highlighted(2)
        else:
            self.world.HUD.inventory_slots.slots[2].highlight_locked = False
        if keys[pygame.K_4]:
            self.world.HUD.inventory_slots.set_highlighted(3)
        else:
            self.world.HUD.inventory_slots.slots[3].highlight_locked = False
        if keys[pygame.K_5]:
            self.world.HUD.inventory_slots.set_highlighted(4)
        else:
            self.world.HUD.inventory_slots.slots[4].highlight_locked = False
        if keys[pygame.K_6]:
            self.world.HUD.inventory_slots.set_highlighted(5)
        else:
            self.world.HUD.inventory_slots.slots[5].highlight_locked = False
        if keys[pygame.K_7]:
            self.world.HUD.inventory_slots.set_highlighted(6)
        else:
            self.world.HUD.inventory_slots.slots[6].highlight_locked = False
        if keys[pygame.K_8]:
            self.world.HUD.inventory_slots.set_highlighted(7)
        else:
            self.world.HUD.inventory_slots.slots[7].highlight_locked = False
        if keys[pygame.K_9]:
            self.world.HUD.inventory_slots.set_highlighted(8)
        else:
            self.world.HUD.inventory_slots.slots[8].highlight_locked = False

        if pygame.mouse.get_pressed()[0]:
            self.mouse_click_available = False
        else:
            self.mouse_click_available = True
            self.picked_slot = None
            self.hover_item = None

        if keys[pygame.K_a]:
            direction[0] -= 1

        if keys[pygame.K_d]:
            direction[0] += 1

        if keys[pygame.K_w]:
            direction[1] -= 1

        if keys[pygame.K_s]:
            direction[1] += 1

        stamina_regen = self.stamina_regen
        
        if self.running:
            
            if self.stamina > 0 and (direction[0] != 0 or direction[1] != 0):
                if self.stamina > 2:
                    speed = self.run_speed
                    self.walk_animation.change_frequency(.032)
                else:
                    self.walk_animation.change_frequency(self.walk_animation.original_frequency)
                if self.stamina - self.running_price < 0:
                    self.stamina = 0
                else:
                    self.stamina = self.stamina - self.running_price

        else:
            if direction[0] != 0 or direction[1] != 0:
                stamina_regen = stamina_regen/2
            if self.stamina < self.max_stamina:
                if self.stamina + stamina_regen > self.max_stamina:
                    self.stamina = self.max_stamina
                else:
                    self.stamina = self.stamina + stamina_regen      
        
        velocity.x += speed * direction[0]
        velocity.y += speed * direction[1]

        self.direction = direction
        self.update_position(velocity)

    def check_collision(self, velocity):
        velocity = [velocity[0] * self.world.delta_time *1.2, velocity[1] * self.world.delta_time *1.2]
        collision = [False, False]

        rectX = pygame.Rect(self.leg_rec.x + velocity[0], self.leg_rec.y, self.leg_rec.width, self.leg_rec.height)
        rectY = pygame.Rect(self.leg_rec.x, self.leg_rec.y + velocity[1], self.leg_rec.width, self.leg_rec.height)
        for wall in self.world.wall_group:
            if rectX.colliderect(wall.rect):
                collision[0] = True
            if rectY.colliderect(wall.rect):
                collision[1] = True

        return collision

    def update_position(self, velocity):

        if not self.check_collision(velocity)[0]:
            self.position[0] += velocity[0] * self.world.delta_time

            if velocity[1] != 0 and velocity[0] == 0:

                if not slide_channel.get_busy():
                    slide_channel.play(slide)
            else:
                slide_channel.stop()

        if not self.check_collision(velocity)[1]:
            self.position[1] += velocity[1] * self.world.delta_time

        if velocity[0] != 0:
            if not walk_channel.get_busy():
                walk_channel.play(walk)
        else:
            walk_channel.stop()

    def update(self):
        self.world.player_vision.radius = self.sight

        self.inventory_full = self.check_inventory()

        if self.stamina < 20:
            if not heartbeat_channel.get_busy():
                heartbeat_channel.play(heartbeat)
            self.world.darkness = 100

            if self.stamina < 7:
                self.walk_speed = self.original_walk_speed / 2
                self.sight = self.max_sight * 1/3
                self.world.brightness = 5

                self.walk_animation.change_frequency(.1)
            else:
                self.sight = self.max_sight * self.stamina/20
                
        else:
            self.walk_speed = self.original_walk_speed
            self.sight = self.max_sight
            self.world.darkness = self.world.original_darkness
            self.world.brightness = self.world.original_brightness
            heartbeat_channel.stop()
            self.walk_animation.change_frequency(self.walk_animation.original_frequency)
        if self.health <= 0:
            self.dead = True

        if not self.dead:
            self.control()

        if self.direction[0] == 0:
            self.idle_animation.animate()
        else:
            self.walk_animation.animate()

        position = [self.position[0] + self.world.position[0], self.position[1] + self.world.position[1]]
        size = [self.size[0] * self.world.zoom, self.size[1] * self.world.zoom]

        self.rect.topleft = position
        self.rect.size = size

        self.leg_rec.x = self.rect.x
        self.leg_rec.bottomleft = self.rect.bottomleft

        if self.direction[0] == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def pick_item(self, itemdrop, amount = 1):
        slot = self.find_available_slot(itemdrop)
        for i in range(amount):
            if slot != None:
                if not slot.full:
                    slot.assign_item(itemdrop.item)
                else:
                    slot = self.find_available_slot(itemdrop)

    def find_available_slot(self, itemdrop):
        item = itemdrop.item
        slot = self.world.HUD.inventory_slots.find_item(item)
        if slot == None:
            for s in self.world.HUD.inventory_slots.slots:
                if s.item == None:
                    slot = s
                    break
        if slot != None:
            itemdrop.label.kill()
            itemdrop.kill()
        else:
            itemdrop.picking_up = False
            itemdrop.position = itemdrop.starting_position.copy()
        return slot

    def check_inventory(self):
        inventory_full = True
        for slot in self.world.HUD.inventory_slots.slots:
            if not slot.full:
                inventory_full = False

        return inventory_full

    def drop_item(self, slot, amount = 1):
        if slot != None and slot.item != None:
            for i in range(amount):
                drop = ItemDrop(self.world, slot.item, self.position.copy())
                drop.block_picking_up()
            slot.amount -= amount