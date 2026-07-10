class StateManager:
    def __init__(self):
        self.stack = []
    
    def change_state(self, new_state):
        self.stack.clear()
        self.stack.append(new_state)

    def push(self, new_state):
        self.stack.append(new_state)

    def pop(self):
        if len(self.stack) > 1:
            self.stack.pop()

    def player_input(self, inputs):
        if self.stack:
            self.stack[-1].player_input(inputs)

    def tick(self, dt):
        if not self.stack:
            return

        states_to_tick = []
        for state in reversed(self.stack):
            states_to_tick.append(state)
            if state.blocks_ticking:
                break 

        for state in reversed(states_to_tick):
            state.tick(dt)

    def audio(self, mixer):
        if self.stack:
            self.stack[-1].audio(mixer)

    def render(self, graphics):
        if not self.stack:
            return

        first_visible_index = 0
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].blocks_rendering:
                first_visible_index = i
                break

        for i in range(first_visible_index, len(self.stack)):
            self.stack[i].render(graphics)