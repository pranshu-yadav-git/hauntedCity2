from ursina import *
import random

class DemonSpawner:
    def __init__(self, target):
        self.enemies = []
        self.spawn_timer = 0
        self.target = target

    def spawn(self):
        demon = Entity(model='sphere', color=color.red, scale=1, position=(random.randint(-20,20),0.5,random.randint(-20,20)), collider='box')
        self.enemies.append(demon)

    def update(self):
        self.spawn_timer += time.dt
        if self.spawn_timer > 5:
            self.spawn()
            self.spawn_timer = 0

        for enemy in self.enemies:
            enemy.look_at(self.target)
            enemy.position += enemy.forward * time.dt * 1
            if enemy.intersects(self.target).hit:
                self.target.health -= 1
        if not self.target or not hasattr(self.target, 'world_position'):
            return  # skip update if player is destroyed

        for enemy in self.enemies:
            if enemy and enemy.enabled:
                enemy.look_at(self.target)
