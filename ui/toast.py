from systems.input_handler import InputHandler
from auditory.mixer import Mixer
from graphics.renderer import Renderer
from utils.transition_frames import TransitionFrames
from utils.vector2f import Vector2f
from collections import deque

class Toast:
    def __init__(self):
        self._queue = deque()
        self.target_pos = Vector2f(20, 250)

        self.current_toast_tuple = None
        self.transition = True
        self.trans_frame_index = 0
        self.current_x = 0
        self.current_y = 0
        self.time_accumulator = 0.0

    def execute_toast(self, content: str, transition_no_of_frames: int, persistence_ms: int):
        if persistence_ms <= 0 or transition_no_of_frames <= 0:
            raise ValueError("[TOAST] MUST BE POSITIVE")
        
        x = Renderer.orbitron.size(content)[0] * -1
        y = 250 # sige na nga eto default

        trans_frames = TransitionFrames.ease_out(Vector2f(x,y), self.target_pos, transition_no_of_frames)

        persistence = persistence_ms / 1000.0
        
        self._queue.append((content, trans_frames, persistence))

    def player_input(self, inputs: InputHandler):
        pass

    def tick(self, dt: float):
        if self._queue and not self.current_toast_tuple:
            self.current_toast_tuple = self._queue.popleft()
            self.transition = True
            self.trans_frame_index = 0
            self.time_accumulator = 0.0

        if self.current_toast_tuple:
            if self.transition:
                current_frame = self.current_toast_tuple[1][self.trans_frame_index]

                self.current_x = current_frame.x
                self.current_y = current_frame.y

                self.trans_frame_index += 1
                if self.trans_frame_index == len(self.current_toast_tuple[1]):
                    self.transition = False
            else:
                # persistence
                self.time_accumulator += dt
                if self.time_accumulator >= self.current_toast_tuple[2]:
                    print("TOAST DONE!")
                    self.current_toast_tuple = None

    def audio(self, mixer: Mixer):
        pass

    def render(self, graphics: Renderer):
        if self.current_toast_tuple:
            graphics.draw_text(self.current_toast_tuple[0], (255, 255, 255), x=int(self.current_x), y=int(self.current_y),
                                customFont=graphics.orbitron, debug=False)