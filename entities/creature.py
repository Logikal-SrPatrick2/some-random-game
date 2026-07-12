from __future__ import annotations
from entities.entity import Entity
from entities.raycast import RayCast

class Creature(Entity):
    def __init__(self, physics_component, animation_component, manager, tile_manager, health=100, attack_cooldown_ms = 0.0, dmg = 0.0):
        super().__init__(physics_component, animation_component, manager, tile_manager)
        self.max_health = health
        self.health = health
        self.attack_cooldown = attack_cooldown_ms / 1000.0
        self.dmg = dmg

        self.time_accumulator = self.attack_cooldown

        self.on_successful_attack_callback = None
        self.on_activated_attack_callback = None

    def damageCreature(self, dmg):
        self.health -= dmg

    def healCreature(self, heal):
        self.health += heal

    def tick(self, dt):
        super().tick(dt)

        if self.health <= 0:
            self.on_death()

        if self.time_accumulator < self.attack_cooldown:
            self.time_accumulator += dt

    def attack(self, creature: Creature) -> bool:
        if self.time_accumulator >= self.attack_cooldown:
            if self.on_activated_attack_callback:
                self.on_activated_attack_callback()

            if creature:
                if not RayCast.raycast_2d_solid_tile_detection(self.physics.position, creature.physics.position, self.tile_manager):
                    creature.damageCreature(self.dmg)
                    if self.on_successful_attack_callback:
                        self.on_successful_attack_callback()

            self.time_accumulator -= self.attack_cooldown
            
            return True
        
        return False
    
    def on_death(self):
        self.manager.remove_entity(self)