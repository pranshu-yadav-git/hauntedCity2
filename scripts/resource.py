from ursina import *
import random

class ResourceSpawner:
    def __init__(self, city_manager):
        self.resources = []
        self.spawn_timer = 0
        self.city_manager = city_manager

    def spawn(self):
        item = Entity(model='cube', color=color.green, scale=0.5, position=(random.randint(-15,15),0.5,random.randint(-15,15)), collider='box')
        self.resources.append(item)

    def update(self):
        self.spawn_timer += time.dt
        if self.spawn_timer > 3:
            self.spawn()
            self.spawn_timer = 0

        valid_resources = []

        for item in self.resources:
            try:
                # This will throw an exception if the entity has been destroyed
                _ = item.position
            except Exception:
                continue  # Skip destroyed items

            if self.city_manager.player and distance(item.position, self.city_manager.player.position) < 1:
                destroy(item)
                self.city_manager.improve()
            else:
                valid_resources.append(item)

        self.resources = valid_resources

