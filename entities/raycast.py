from utils.vector2f import Vector2f
from tiles.tile_manager import TileManager
from tiles.base_tile import DEFAULT_TILE_SIZE

class RayCast:
    
    @staticmethod
    def raycast_2d_solid_tile_detection(start: Vector2f, end: Vector2f, tile_manager: TileManager) -> bool:
        if (end - start).is_zero:
            start_grid_x = int(start.x // DEFAULT_TILE_SIZE)
            start_grid_y = int(start.y // DEFAULT_TILE_SIZE)
            if 0 <= start_grid_x < tile_manager.cols and 0 <= start_grid_y < tile_manager.rows:
                return tile_manager.tilemap[start_grid_y][start_grid_x].is_solid
            return False

        start_grid_x = int(start.x // DEFAULT_TILE_SIZE)
        start_grid_y = int(start.y // DEFAULT_TILE_SIZE)
        end_grid_x = int(end.x // DEFAULT_TILE_SIZE)
        end_grid_y = int(end.y // DEFAULT_TILE_SIZE)

        ray_dir = (end - start).normalize()

        dx = abs(DEFAULT_TILE_SIZE / ray_dir.x) if ray_dir.x != 0 else 1e30
        dy = abs(DEFAULT_TILE_SIZE / ray_dir.y) if ray_dir.y != 0 else 1e30

        if ray_dir.x > 0:
            step_x = 1
            side_dist_x = ((start_grid_x + 1) * DEFAULT_TILE_SIZE - start.x) * (dx / DEFAULT_TILE_SIZE)
        elif ray_dir.x < 0:
            step_x = -1
            side_dist_x = (start.x - (start_grid_x * DEFAULT_TILE_SIZE)) * (dx / DEFAULT_TILE_SIZE)
        else:
            step_x = 0
            side_dist_x = 1e30

        if ray_dir.y > 0:
            step_y = 1
            side_dist_y = ((start_grid_y + 1) * DEFAULT_TILE_SIZE - start.y) * (dy / DEFAULT_TILE_SIZE)
        elif ray_dir.y < 0:
            step_y = -1
            side_dist_y = (start.y - (start_grid_y * DEFAULT_TILE_SIZE)) * (dy / DEFAULT_TILE_SIZE)
        else:
            step_y = 0
            side_dist_y = 1e30

        curr_x = start_grid_x
        curr_y = start_grid_y

        while True:
            if 0 <= curr_x < tile_manager.cols and 0 <= curr_y < tile_manager.rows:
                if tile_manager.tilemap[curr_y][curr_x].is_solid:
                    return True
            else:
                return False

            if curr_x == end_grid_x and curr_y == end_grid_y:
                return False

            if side_dist_x < side_dist_y:
                side_dist_x += dx
                curr_x += step_x
            else:
                side_dist_y += dy
                curr_y += step_y