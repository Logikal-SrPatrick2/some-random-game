from graphics.render_mode import RenderMode
from graphics.renderer import Renderer
from graphics.image_asset import ImageAsset

class Animation:
    def __init__(self, frame_assets, frame_duration_ms=100, loops=True):
        self.frames: list[ImageAsset] = frame_assets
        self.frame_duration = frame_duration_ms / 1000.0
        self.loops = loops
        self.done = False
        
        self.current_frame_index = 0
        self.time_accumulator = 0.0

    def resize(self, width: float, height: float):
        for frame in self.frames:
            frame.resize(width, height)

    def tick(self, dt):
        self.time_accumulator += dt
        while self.time_accumulator >= self.frame_duration:
            self.time_accumulator -= self.frame_duration
            self.current_frame_index += 1
            
            if self.current_frame_index >= len(self.frames):
                if self.loops:
                    self.current_frame_index = 0
                else:
                    self.current_frame_index = len(self.frames) - 1 
                    self.done = True

    def render(self, graphics, x, y, mode: RenderMode = RenderMode.TOP_LEFT):
        active_frame = self.frames[self.current_frame_index]
        active_frame.render(graphics, x, y, mode)

    def reset(self):
        self.current_frame_index = 0

    @property
    def calculate_auto_pivot(self) -> int:
        """
        note: ung maximum kukunin
        """

        max_offset = 0
        for frame in self.frames:
            offset = frame.calculate_auto_pivot
            if offset > max_offset:
                max_offset = offset

        return max_offset