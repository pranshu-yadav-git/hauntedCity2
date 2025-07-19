from ursina import *

class CityManager:
    def __init__(self, hud, player=None):
        self.index = 0
        self.hud = hud
        self.player = player

    def set_player(self, player):
        self.player = player

    def improve(self):
        self.index += 5

    def update(self):
        if self.player:
            self.hud.update(self.player.health, self.index)
