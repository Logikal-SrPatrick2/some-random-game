DEFAULT_CELL_SIZE = 128


class SpatialGrid:

    def __init__(self, cell_size: float = DEFAULT_CELL_SIZE):
        self.cell_size = cell_size
        self.cells = {} 

    def clear(self):
        self.cells.clear()

    def _cell_range(self, x: float, y: float, width: float, height: float):
        left = x - (width / 2.0)
        right = x + (width / 2.0)
        top = y - (height / 2.0)
        bottom = y + (height / 2.0)

        min_cx = int(left // self.cell_size)
        max_cx = int(right // self.cell_size)
        min_cy = int(top // self.cell_size)
        max_cy = int(bottom // self.cell_size)
        return min_cx, max_cx, min_cy, max_cy

    def insert(self, entity):
        phys = entity.physics
        max_w, max_h = phys.get_hitbox_bounds()
        
        min_cx, max_cx, min_cy, max_cy = self._cell_range(
            phys.position.x, phys.position.y, max_w, max_h
        )

        for cx in range(min_cx, max_cx + 1):
            for cy in range(min_cy, max_cy + 1):
                self.cells.setdefault((cx, cy), []).append(entity)

    def get_nearby_entities(self, entity):
        phys = entity.physics
        max_w, max_h = phys.get_hitbox_bounds()
        
        return self.get_nearby_at(
            phys.position.x, phys.position.y, max_w, max_h, exclude=entity
        )
    
    def get_nearby_at(self, x: float, y: float, width: float, height: float, exclude=None):
        min_cx, max_cx, min_cy, max_cy = self._cell_range(x, y, width, height)

        seen_ids = set()
        result = []

        for cx in range(min_cx - 1, max_cx + 2):
            for cy in range(min_cy - 1, max_cy + 2):
                bucket = self.cells.get((cx, cy))
                if not bucket:
                    continue
                for ent in bucket:
                    if ent is exclude:
                        continue
                    if id(ent) in seen_ids:
                        continue
                    seen_ids.add(id(ent))
                    result.append(ent)

        return result