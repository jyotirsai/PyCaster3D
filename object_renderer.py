import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', (WIDTH,HEIGHT))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', (WIDTH,HEIGHT))
    
    def draw(self):
        self.render_game_objects()
    
    def player_damage(self):
        self.screen.blit(self.blood_screen, (0,0))
    
    def game_over(self):
        self.screen.blit(self.game_over_image, (0,0))
    
    def render_game_objects(self):
        for depth, image, pos in sorted(self.game.raycasting.objects_to_render, reverse=True):
            self.screen.blit(image, pos)
    
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/wall.png')
        }