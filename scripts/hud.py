from ursina import *

class HUD:
    def __init__(self):
        self.health_bar = Entity(parent=camera.ui, model='quad', color=color.red, scale=(0.4, 0.03), position=(-0.5, 0.45))
        self.city_index = Text(text='City Index: 0', position=(-0.5, 0.4), origin=(0, 0), scale=1.5, background=True)

    def update(self, health, index):
        self.health_bar.scale_x = 0.4 * (health / 100)
        self.city_index.text = f"City Index: {index}"
