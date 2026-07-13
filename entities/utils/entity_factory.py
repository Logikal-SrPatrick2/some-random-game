from entities.creatures.player import Player
from entities.creatures.roaming_alien import RoamingAlien
from entities.utils.entity_manager import EntityManager

def entity_factory(entity_type: str, attributes: dict, manager: EntityManager, tile_manager):
    x = float(attributes.get("x", 0.0))
    y = float(attributes.get("y", 0.0))
    width = int(attributes.get("width", 128))
    height = int(attributes.get("height", 128))

    if entity_type == "Player":
        player = Player(manager, tile_manager, x, y, width, height)
        manager.add_entity(player)
        return player
        
    elif entity_type == "RoamingAlien":
        alien = RoamingAlien(manager, tile_manager, x, y, width, height)
        manager.add_entity(alien)
        return alien

    print(f"Warning: Entity type '{entity_type}' is not registered in the factory pipeline.")
    return None