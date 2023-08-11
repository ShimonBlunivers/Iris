import pygame, json

from objects import objects

pygame.init()

class Menu:

    def __init__(self, world):
        self.world = world
        self.size = [210, self.world.resolution[1] + 10]
        self.color = [245, 126, 7]
        self.border_color = [117, 60, 4]

        self.rect = pygame.Rect(-5, -5, self.size[0], self.size[1])

        self.slots = []

        for i in range(len(self.world.objects)):
            slot = Slot(self.world, [10 ,10 + 190 * i], [180, 180], list(self.world.objects.values())[i], list(self.world.objects)[i])
            self.slots.append(slot)

    def update(self):
        if self.world.show_inventory:
            pygame.draw.rect(self.world.screen, self.color, self.rect)
            pygame.draw.rect(self.world.screen, self.border_color, self.rect, width = 5)
            for slot in self.slots:
                slot.update()
class Slot:
    
    def __init__(self, world, position, size, obj, image_path):
        self.world = world
        self.original_position = position
        self.position = self.original_position
        self.size = size
        self.border_color = [138, 68, 0]
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.object = obj
        self.image = pygame.image.load(f"files/{image_path.lower()}/icon.png")
        self.image = pygame.transform.scale(self.image, [self.rect.width - 20, self.rect.height - 20])
         
    def update(self):
        self.rect.top = self.original_position[1] + self.world.mouse_scroll
        pygame.draw.rect(self.world.screen, self.border_color, self.rect, width = 4)
        self.world.screen.blit(self.image, [self.rect.left + 10, self.rect.top + 10])

class ObjectHover:

    def __init__(self, world, object):
        self.world = world
        self.object = object

        self.rect = self.object.rect.copy()

        self.rect.width = self.rect.width
        self.rect.height = self.rect.height
        self.sticking = False
        self.stick_to = None

        self.hitbox_rect = self.rect.copy()

        try:
            self.image = pygame.transform.scale(self.object.image, [self.rect.width, self.rect.height])
        except:
            self.image = pygame.surface.Surface([self.rect.width, self.rect.height])
            self.image.fill(self.object.color)

        self.offset = [
            pygame.mouse.get_pos()[0] - self.rect.left,
            pygame.mouse.get_pos()[1] - self.rect.top
            ]

    def update(self):
        self.hitbox_rect.topleft = [pygame.mouse.get_pos()[0] - self.offset[0], pygame.mouse.get_pos()[1] - self.offset[1]]

        if self.sticking:
            if pygame.mouse.get_pos()[0] > self.stick_to.rect.right and pygame.mouse.get_pos()[1] > self.stick_to.rect.top and pygame.mouse.get_pos()[1] < self.stick_to.rect.bottom:
                self.rect.left = self.stick_to.rect.right
                self.rect.bottom = self.stick_to.rect.bottom
            elif pygame.mouse.get_pos()[0] < self.stick_to.rect.left and pygame.mouse.get_pos()[1] > self.stick_to.rect.top and pygame.mouse.get_pos()[1] < self.stick_to.rect.bottom:
                self.rect.right = self.stick_to.rect.left
                self.rect.bottom = self.stick_to.rect.bottom
            elif pygame.mouse.get_pos()[1] > self.stick_to.rect.bottom and pygame.mouse.get_pos()[0] > self.stick_to.rect.left and pygame.mouse.get_pos()[0] < self.stick_to.rect.right:
                self.rect.top = self.stick_to.rect.bottom
                self.rect.left = self.stick_to.rect.left
            elif pygame.mouse.get_pos()[1] < self.stick_to.rect.top and pygame.mouse.get_pos()[0] > self.stick_to.rect.left and pygame.mouse.get_pos()[0] < self.stick_to.rect.right:
                self.rect.bottom = self.stick_to.rect.top
                self.rect.left = self.stick_to.rect.left

            else:
                self.sticking = False
                self.stick_to = None

        if not self.sticking:
            self.rect.topleft = [pygame.mouse.get_pos()[0] - self.offset[0], pygame.mouse.get_pos()[1] - self.offset[1]]
        self.world.object_move_layer.blit(self.image, self.rect)


class Editor:

    FONT = pygame.font.Font("files/text/fonts/november.regular.ttf", 32)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED =  (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


    def __init__(self):

        self.position = [0, 0]
        self.zoom = 1

        self.label_list = []
        self.particles = []

        self.mouse_scroll = 0

        self.camera_group = pygame.sprite.Group() 

        self.itemdrop_group = pygame.sprite.Group() 
        self.HUD_group = pygame.sprite.Group()
        self.light_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.entity_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.path_group = pygame.sprite.Group()
        self.torch_group = pygame.sprite.Group()

        self.resolution = (1280, 720)
        self.screen = pygame.display.set_mode([self.resolution[0], self.resolution[1]])

        self.object_move_layer = pygame.surface.Surface([self.resolution[0], self.resolution[1]])
        self.object_move_layer.fill([69, 69, 69])
        self.object_move_layer.set_colorkey([69, 69, 69])
        self.object_move_layer.set_alpha(155)

        self.icon = pygame.image.load("files/icon.png")

        pygame.display.set_caption('Iris - Editor')
        pygame.display.set_icon(self.icon)

        self.running = True

        self.background_color = [17, 51, 0]

        self.mouse_rect = pygame.rect.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)

        self.sprite_group = pygame.sprite.Group()

        self.objects = objects

        self.object_list = []

        self.load()

        self.show_inventory = True
        self.tab_lock = False
        self.mouse_click_available = True
        self.middle_click_available = True

        self.menu = Menu(self)

        self.picked_from_slot = False
        self.picked_slot = None

        self.copying = False

        self.picked_object = None
        self.hover_object = None
        self.highlight_color = [246, 252, 73]

        self.modes = ["move", "scale"]
        self.mode = self.modes[0]

        self.scaled_object = None

        self.mode_text = self.FONT.render(self.mode, True, [0, 0, 0])

        self.grab_position = [0, 0, 0, 0]

    def load(self):
        with open('files/world.txt') as world_file:
            data = json.load(world_file)
            for key in data:
                args = []
                for obj in data[key]:
                    for arg in obj:
                        args.append(arg)
                    self.object_list.append(self.objects[key](self, *args))
                    args = []


    def save(self):

        data = {}

        for obj in self.object_list:

            if obj.ID == "Trol":
                try:
                    data[obj.ID] = [*data[obj.ID], [obj.position]]
                except:
                    data[obj.ID] = [[obj.position]]
            elif obj.ID == "King":
                try:
                    data[obj.ID] = [*data[obj.ID], [obj.position]]
                except:
                    data[obj.ID] = [[obj.position]]
            elif obj.ID == "Path":
                try:
                    data[obj.ID] = [*data[obj.ID], [obj.position, obj.size, obj.color, obj.visible]]
                except:
                    data[obj.ID] = [[obj.position, obj.size, obj.color, obj.visible]]
            elif obj.ID == "Wall":
                try:
                    data[obj.ID] = [*data[obj.ID], [obj.position, obj.size]]
                except:
                    data[obj.ID] = [[obj.position, obj.size]]
            elif obj.ID == "Torch":
                try:                
                    data[obj.ID] = [*data[obj.ID], [obj.position]]
                except:
                    data[obj.ID] = [[obj.position]]

        with open("files/world.txt", "w") as world_file:
            json.dump(data, world_file)

    def update(self):
        self.control()


        self.mouse_rect.topleft = pygame.mouse.get_pos()

        for obj in self.object_list:
            obj.update()
            try:
                list = obj.group
                for s in list:
                    s.update()
                    self.screen.blit(s.image, s.rect)
            except:
                try:
                    self.screen.blit(obj.image, obj.rect)
                except:
                    pass

        if self.hover_object != None:
            self.hover_object.update()

        if self.picked_object != None:
            hit = False
            if self.hover_object.object.ID == "Wall":
                for object in self.object_list:
                    if self.hover_object.hitbox_rect.colliderect(object):
                        if (self.copying or object != self.hover_object.object) and object.ID == "Wall":
                            hit = True
                            self.hover_object.sticking = True
                            self.hover_object.stick_to = object
                    
            if not hit:
                self.hover_object.sticking = False
                self.hover_object.stick_to = None

            if self.picked_from_slot:
                pygame.draw.rect(self.screen, self.highlight_color, self.picked_slot.rect, width = 4)
            else:
                pygame.draw.rect(self.screen, self.highlight_color, self.picked_object.rect, width = 3)


        self.menu.update()
        
        self.screen.blit(self.object_move_layer, [0, 0])

#       TEXT RENDER

        self.mode_text = self.FONT.render(self.mode, True, [0, 0, 0])

        self.screen.blit(self.mode_text, [1180, 670])

        pygame.display.flip()
        self.object_move_layer.fill([69, 69, 69])
        self.screen.fill(self.background_color)

    def control(self):
        keys = pygame.key.get_pressed()
        speed = 2

        if keys[pygame.K_LSHIFT]:
            speed = 4

        if keys[pygame.K_LALT]:
            self.copying = True
        else:
            self.copying = False

        if keys[pygame.K_TAB] and not self.tab_lock:
            self.show_inventory = not self.show_inventory
            self.tab_lock = True
        elif not keys[pygame.K_TAB]:
            self.tab_lock = False

        if keys[pygame.K_1]:
            self.mode = self.modes[0]
        elif keys[pygame.K_2]:
            self.mode = self.modes[1]


        if not keys[pygame.K_LCTRL]:
            if keys[pygame.K_w]:
                self.position[1] += speed
            if keys[pygame.K_s]:
                self.position[1] -= speed
            if keys[pygame.K_a]:
                self.position[0] += speed
            if keys[pygame.K_d]:
                self.position[0] -= speed

        if keys[pygame.K_LCTRL] and keys[pygame.K_s]:
            self.save()
        
        if self.mode == self.modes[0]:
            if pygame.mouse.get_pressed()[0]:
                if self.mouse_click_available:
                    if self.show_inventory and self.mouse_rect.colliderect(self.menu.rect):
                        for slot in self.menu.slots:
                            if slot.rect.colliderect(self.mouse_rect):
                                self.picked_object = slot.object(self, slot.rect.topleft)
                                self.hover_object = ObjectHover(self, self.picked_object)
                                self.hover_object.offset = [self.hover_object.rect.width/2, self.hover_object.rect.height/2]
                                self.picked_from_slot = True
                                self.picked_slot = slot
                    else:
                        for object in self.object_list:
                            if object.rect.colliderect(self.mouse_rect):
                                self.picked_object = object
                                self.hover_object = ObjectHover(self, self.picked_object)
                            
                self.mouse_click_available = False
            else:
                if self.picked_object != None:
                    if self.picked_object not in self.object_list:
                        self.object_list.append(self.picked_object)
                    
                    if self.copying:
                        newObject = type(self.picked_object)(self, [self.hover_object.rect.topleft[0] - self.position[0], self.hover_object.rect.topleft[1] - self.position[1]])
                        self.object_list.append(newObject)
                    else:
                        self.picked_object.position = [self.hover_object.rect.topleft[0] - self.position[0], self.hover_object.rect.topleft[1] - self.position[1]]
                self.picked_object = None
                self.mouse_click_available = True

            if self.picked_object != None and keys[pygame.K_x]:
                if self.picked_object in self.object_list:
                    self.object_list.remove(self.picked_object)
                self.picked_object = None


            if pygame.mouse.get_pressed()[2]:
                self.picked_object = None

        if self.picked_object == None:
            self.hover_object = None
            self.picked_from_slot = False
            self.picked_slot = None

#              SCALING

        if self.mode == self.modes[1]:
            if pygame.mouse.get_pressed()[0]:
                if self.mouse_click_available:
                    self.mouse_click_available = False
                    for object in self.object_list:
                        if object.rect.colliderect(self.mouse_rect):
                            self.scaled_object = object
                            pygame.mouse.set_pos(object.rect.right, object.rect.bottom)
            
                if self.scaled_object != None:
                    try:
                        self.scaled_object.size[0] = self.mouse_rect.x - self.scaled_object.rect.x 
                        self.scaled_object.size[1] = self.mouse_rect.y - self.scaled_object.rect.y
                    except:
                        print("UNSCALABLE!")
            else:
                self.scaled_object = None
                self.mouse_click_available = True

#           CLICK AND DRAG

        if pygame.mouse.get_pressed()[1]:
            if self.middle_click_available:
                self.middle_click_available = False
                self.grab_position[0] = self.mouse_rect.centerx 
                self.grab_position[1] = self.mouse_rect.centery 
                self.grab_position[2] = self.position[0]
                self.grab_position[3] = self.position[1]
            
            self.position[0] = self.mouse_rect.x - self.grab_position[0] + self.grab_position[2]
            self.position[1] = self.mouse_rect.y - self.grab_position[1] + self.grab_position[3]


        else: self.middle_click_available = True


editor = Editor()


while editor.running:

    editor.update()

    for event in pygame.event.get():
        if editor.menu.rect.colliderect(editor.mouse_rect):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    editor.mouse_scroll += 10
                if event.button == 5:
                    editor.mouse_scroll -= 10

        if event.type == pygame.QUIT:
            editor.running = False
            pygame.quit()
        