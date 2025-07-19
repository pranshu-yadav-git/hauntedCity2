from ursina import *

class Ghost(Entity):
    def __init__(self, player, **kwargs):
        super().__init__()
        self.model = 'sphere'
        self.color = color.red
        self.collider = 'box'
        self.scale = 1
        self.player = player

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.look_at(self.player)
        self.position += self.forward * time.dt * 2
        self.position += (self.player.position - self.position).normalized() * time.dt

        if distance(self.position, self.player.position) < 1.5:
            self.player.take_damage(10)

        if not self.player or not self.player.alive:
            return  # Don't update if player doesn't exist or is dead
        if not self.player or not hasattr(self.player, 'world_position'):
            return  # Skip this frame, player is gone

        try:
            self.look_at(self.player)
        except Exception:
            return  # player is likely destroyed        
