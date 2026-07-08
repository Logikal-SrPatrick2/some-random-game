from states.manager import StateManager

class State:
    def __init__(self, manager: StateManager):
        self.manager = manager
        self.blocks_ticking = False
        self.blocks_rendering = False
        self.objects = []
        self.camera = None
    
    def player_input(self, inputs):
        for object in self.objects:
            object.player_input(inputs)

    def tick(self, dt):
        for object in self.objects:
            object.tick(dt)

    def render(self, graphics):
        if self.camera:
            for object in self.objects:
                object.render(graphics, self.camera)
        else:
            for object in self.objects:
                object.render(graphics)