import json
import os
from tiles.tile_manager import TILE_FACTORY, Floor
from tiles.base_tile import DEFAULT_TILE_SIZE
from entities.entity_factory import entity_factory
from utils.conversion_to_exe import resource_path

class LevelIO:
    @staticmethod
    def save_level(filename: str, tile_manager, entity_manager) -> bool:
        directory = "levels"
            
        path = os.path.join(directory, filename)

        path = resource_path(str(path))

        
        
        tile_matrix = []
        for y in range(tile_manager.rows):
            row = []
            for x in range(tile_manager.cols):
                row.append(tile_manager.tilemap[y][x].id)
            tile_matrix.append(row)
            
    
        entity_list = []
        for entity in entity_manager.entities:
    
            ent_name = getattr(entity, "name", type(entity).__name__)
                
            ent_data = {
                "type": ent_name, 
                "attributes": {
                    "x": entity.physics.position.x,
                    "y": entity.physics.position.y,
                    "width": entity.physics.width,
                    "height": entity.physics.height
                }
            }
           
            if hasattr(entity, "get_custom_attributes"):
                ent_data["attributes"].update(entity.get_custom_attributes())
                
            entity_list.append(ent_data)

        payload = {
            "metadata": {
                "rows": tile_manager.rows,
                "cols": tile_manager.cols
            },
            "tilemap": tile_matrix,
            "entities": entity_list
        }

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4)
            return True
        except Exception as e:
            print(f"Failed to save level config: {e}")
            return False

    @staticmethod
    def load_level(filename: str, tile_manager, entity_manager, entity_factory_cb = entity_factory) -> bool:
  
        path = os.path.join("levels", filename)
        path = resource_path(str(path))
        if not os.path.exists(path):
            return False
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)
                
            #  Map Tiles
            tile_manager.load_map(payload["tilemap"])
            
            entity_manager.entities.clear()
            for ent_data in payload.get("entities", []):
                print(f"Loading entity loop count: {len(payload.get('entities', []))}")
                entity_factory_cb(ent_data["type"], ent_data["attributes"], entity_manager, tile_manager)
            return True
        except Exception as e:
            print(f"Error parsing level script file: {e}")
            return False