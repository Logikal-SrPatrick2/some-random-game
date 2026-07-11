from utils.vector2f import Vector2f

class TransitionFrames:
    
    @staticmethod
    def linear(start: Vector2f, end: Vector2f, frames: int) -> list[Vector2f]:
        if frames < 2:
            raise ValueError("Transitions require at least 2 frames (start and end).")
        
        result = []
        for i in range(frames):
            t = i / (frames - 1)
            # start + (end - start) * t
            result.append(start + (end - start) * t)
        return result

    @staticmethod
    def ease_in(start: Vector2f, end: Vector2f, frames: int) -> list[Vector2f]:
        if frames < 2:
            raise ValueError("Transitions require at least 2 frames.")
        
        result = []
        for i in range(frames):
            t = i / (frames - 1)
            t_eased = t * t  # f(t) = t^2
            result.append(start + (end - start) * t_eased)
        return result

    @staticmethod
    def ease_out(start: Vector2f, end: Vector2f, frames: int) -> list[Vector2f]:
        if frames < 2:
            raise ValueError("Transitions require at least 2 frames.")
        
        result = []
        for i in range(frames):
            t = i / (frames - 1)
            t_eased = t * (2.0 - t)  # f(t) = t * (2 - t)
            result.append(start + (end - start) * t_eased)
        return result

    @staticmethod
    def ease_in_out(start: Vector2f, end: Vector2f, frames: int) -> list[Vector2f]:
        if frames < 2:
            raise ValueError("Transitions require at least 2 frames.")
        
        result = []
        for i in range(frames):
            t = i / (frames - 1)
            t_eased = t * t * (3.0 - 2.0 * t)  
            result.append(start + (end - start) * t_eased)
        return result

    @staticmethod
    def expo(start: Vector2f, end: Vector2f, frames: int) -> list[Vector2f]:
        if frames < 2:
            raise ValueError("Transitions require at least 2 frames.")
        
        result = []
        for i in range(frames):
            t = i / (frames - 1)
            t_eased = 0.0 if t == 0 else (2.0 ** (10.0 * (t - 1.0)))
            result.append(start + (end - start) * t_eased)
            
        result[-1] = end
        return result