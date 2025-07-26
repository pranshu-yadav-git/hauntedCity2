# tree.py
from ursina import *

class Tree(Entity):
    def __init__(self, position=(0, 0.1, 0), planted=False):
        super().__init__(
            model='assets/models/tree.glb',  # Replace with your model path
            position=position,
            rotation=(0, 0, 90),  # Lying down like a fallen sapling
            scale=0.1,
            collider='box'
        )
        self.is_tree = True
        self.is_planted = planted
        self.is_holdable = True
        self.is_thrown = False
        self.velocity = Vec3(0, 0, 0)
        self.angular_velocity = Vec3(0, 0, 0)