import pygame, time

class Animation:

    def __init__(self, world, parent, frequency, files, start_frame = 0, repeat_times = None):
        self.world = world
        self.parent = parent
        self.start_time = time.time()
        self.repeat_times = repeat_times

        if type(frequency) != list:
            self.frequency = []
            for i in range(len(files)):
                self.frequency.append(frequency)
        else:
            self.frequency = frequency

        self.parent.animations.append(self)

        self.finished = False
        self.frames = []
        
        for file in files:

            image = pygame.image.load("files/"+file+".png")
            image = pygame.transform.scale(image, parent.size)
            self.frames.append(image)
        
        self.frame = start_frame % len(self.frames)

        self.original_frequency = self.frequency

        self.cycle = 0
        
        self.parent.image = self.frames[self.frame]
    def animate(self):

        if self.repeat_times == None or self.cycle <= self.repeat_times:
            duration = time.time() - self.start_time
            if duration >= self.frequency[self.frame]:
                
                self.start_time = time.time()
                self.frame = (self.frame + 1) % len(self.frames)

                if self.frame == 0:

                    self.cycle += 1
        else:
            self.finished = True

        self.parent.image = self.frames[self.frame]
        
    def reset_cycles(self):
        self.cycle = 0
        self.finished = False

    def change_frequency(self, frequency):
        if type(frequency) != list:
            self.frequency = []
            for i in range(len(self.frames)):
                self.frequency.append(frequency)
        else:
            self.frequency = frequency