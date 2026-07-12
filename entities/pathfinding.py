import heapq
from utils.vector2f import Vector2f
from tiles.base_tile import DEFAULT_TILE_SIZE
from tiles.tile_manager import TileManager
from entities.entity_physics import EntityPhysics
from entities.hitbox import HitboxType

class PathFinding:
    def __init__(self, tile_manager: TileManager):
        self.tile_manager = tile_manager

    def find_path(self, start_pos: Vector2f, end_pos: Vector2f, entity_physics: EntityPhysics) -> list[Vector2f]:
        if not entity_physics.main_hitbox:
            return []

        hitbox = entity_physics.main_hitbox
        if hitbox.type == HitboxType.RECTANGLE:
            tiles_w = max(1, int(hitbox.w_or_r // DEFAULT_TILE_SIZE))
            tiles_h = max(1, int(hitbox.height // DEFAULT_TILE_SIZE))
        else:
            tiles_w = max(1, int((hitbox.w_or_r * 2.0) // DEFAULT_TILE_SIZE))
            tiles_h = tiles_w

        start_x = int(start_pos.x // DEFAULT_TILE_SIZE)
        start_y = int(start_pos.y // DEFAULT_TILE_SIZE)
        end_x = int(end_pos.x // DEFAULT_TILE_SIZE)
        end_y = int(end_pos.y // DEFAULT_TILE_SIZE)

        if not self._is_footprint_walkable(start_x, start_y, tiles_w, tiles_h):
            return []
        if not self._is_footprint_walkable(end_x, end_y, tiles_w, tiles_h):
            return []

        open_set = []
        heapq.heappush(open_set, (0, start_x, start_y))
        
        came_from = {}
        g_score = {(start_x, start_y): 0.0}
        
        while open_set:
            _, cx, cy = heapq.heappop(open_set)

            if cx == end_x and cy == end_y:
                path = []
                curr = (end_x, end_y)
                while curr in came_from:
                    gx, gy = curr
                    wx = (gx * DEFAULT_TILE_SIZE) + (DEFAULT_TILE_SIZE / 2.0)
                    wy = (gy * DEFAULT_TILE_SIZE) + (DEFAULT_TILE_SIZE / 2.0)
                    path.append(Vector2f(wx, wy))
                    curr = came_from[curr]
                path.reverse()
                return path

            for nx, ny in self._get_valid_neighbors(cx, cy, tiles_w, tiles_h):
                tentative_g = g_score[(cx, cy)] + 1.0
                
                if tentative_g < g_score.get((nx, ny), float('inf')):
                    came_from[(nx, ny)] = (cx, cy)
                    g_score[(nx, ny)] = tentative_g
                    h = abs(nx - end_x) + abs(ny - end_y)
                    heapq.heappush(open_set, (tentative_g + h, nx, ny))

        return []

    def _is_footprint_walkable(self, origin_x: int, origin_y: int, tiles_w: int, tiles_h: int) -> bool:
        if origin_x < 0 or origin_y < 0 or origin_x + tiles_w > self.tile_manager.cols or origin_y + tiles_h > self.tile_manager.rows:
            return False
            
        for ty in range(origin_y, origin_y + tiles_h):
            for tx in range(origin_x, origin_x + tiles_w):
                if self.tile_manager.tilemap[ty][tx].is_solid:
                    return False
        return True

    def _get_valid_neighbors(self, cx: int, cy: int, tiles_w: int, tiles_h: int) -> list[tuple[int, int]]:
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if self._is_footprint_walkable(nx, ny, tiles_w, tiles_h):
                neighbors.append((nx, ny))
        return neighbors