import math

class Vector2f:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other: 'Vector2f') -> 'Vector2f':
        return Vector2f(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2f') -> 'Vector2f':
        return Vector2f(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2f':
        return Vector2f(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> 'Vector2f':
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> 'Vector2f':
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide a vector by zero.")
        return Vector2f(self.x / scalar, self.y / scalar)

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def length_squared(self) -> float:
        return self.x ** 2 + self.y ** 2

    def normalize(self) -> 'Vector2f':
        mag = self.length()
        if mag == 0:
            return Vector2f(0.0, 0.0)
        return self / mag

    @classmethod
    def zero(cls) -> 'Vector2f':
        return cls(0.0, 0.0)

    @classmethod
    def distance(cls, vec1: 'Vector2f', vec2: 'Vector2f') -> float:
        return (vec2 - vec1).length()
    
    @property
    def is_zero(self) -> bool:
        return math.isclose(self.x, 0.0, abs_tol=1e-9) and math.isclose(self.y, 0.0, abs_tol=1e-9)

    def __repr__(self) -> str:
        return f"Vector2f({self.x:.2f}, {self.y:.2f})"