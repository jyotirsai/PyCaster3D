from sprite_object import *
from enemies import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.enemies = []
        self.enemies_path = 'resources/enemies/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.animated_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_enemy = self.add_enemies
        self.enemy_pos = {}

        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))

        add_enemy(Enemies(game))
        add_enemy(Enemies(game, pos=(11.5, 4.5)))
    
    def update(self):
        self.enemy_pos = {enemy.map_pos for enemy in self.enemies if enemy.alive}
        [sprite.update() for sprite in self.sprite_list]
        [enemy.update() for enemy in self.enemies]
    
    def add_enemies(self, enemy):
        self.enemies.append(enemy)
    
    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)