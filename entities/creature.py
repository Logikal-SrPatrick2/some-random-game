from entities.entity import Entity

class Creature(Entity):
    def __init__(self, physics_component, animation_component, manager, tile_manager, health=100):
        super().__init__(physics_component, animation_component, manager, tile_manager)
        self.health = health

    def damageCreature(self, dmg):
        self.health -= dmg

    def healCreature(self, heal):
        self.health += heal