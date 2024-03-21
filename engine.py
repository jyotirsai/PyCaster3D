import pygame as pg
import math
from settings import *

class Engine:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.raycasting_results = []
        self.objects_to_render = []
    
    def update_sprites(self):
        for sprite in self.game.sprite_list:
            sprite.update()
        
    def update_enemies(self):
        self.game.enemy_pos = {enemy.map_pos for enemy in self.game.enemies if enemy.alive}
        for enemy in self.game.enemies:
            enemy.update()
    
    def render_objects(self):
        self.objects_to_render = []
        for cur_ray,values in enumerate(self.raycasting_results):
            depth, projected_height, texture, offset = values
            if projected_height < HEIGHT:
                wall_column = self.wall_textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, projected_height))
                wall_pos = (cur_ray * SCALE, HEIGHT//2 - projected_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / projected_height
                wall_column = self.wall_textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), TEXTURE_SIZE//2 - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (cur_ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))
    
    def raycast(self):
        self.raycasting_results = []
        ray_angle = self.game.player.angle - FOV/2 + 0.0001
        player_x, player_y = self.game.player.pos()
        map_x, map_y = self.game.player.map_pos

        texture_vert, texture_hori = 1, 1
        for ray in range(NUM_RAYS):
            cur_ray = ray_angle+ray*DELTA_ANGLE
            sin_a = math.sin(cur_ray)
            cos_a = math.cos(cur_ray)

            # horizontal intersections
            if sin_a > 0:
                # ray is looking down
                y_hori, dy = (map_y+1, 1)
            else:
                # ray is looking up
                y_hori, dy = (map_y - 0.000001, -1)

            depth_hori = (y_hori - player_y) / (sin_a-0.0001)
            x_hori = player_x + depth_hori * cos_a

            delta_depth = dy / (sin_a+0.0001)
            dx = delta_depth * cos_a
            
            for _ in range(MAX_DEPTH):
                tile_hori = int(x_hori), int(y_hori)
                if tile_hori in self.game.map.walls:
                    texture_hori = self.game.map.walls[tile_hori]
                    break
                x_hori += dx
                y_hori += dy
                depth_hori += delta_depth
            
            # vertical intersections
            if cos_a > 0:
                # ray moving right
                x_vert, dx = (map_x+1, 1)
            else:
                # ray moving left
                x_vert, dx = (map_x - 0.000001, -1)

            depth_vert = (x_vert - player_x) / (cos_a-0.0001)
            y_vert = player_y+depth_vert*sin_a

            delta_depth = dx / (cos_a+0.0001)
            dy = delta_depth * sin_a
            
            for _ in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.walls:
                    texture_vert = self.game.map.walls[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            
            if depth_vert < depth_hori:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hori, texture_hori
                x_hori %= 1
                offset = (1-x_hori) if sin_a > 0 else x_hori

            depth *= math.cos(self.game.player.angle - cur_ray)
            projected_height = CAMERA_PLANE_DIST / (depth + 0.000001)
            self.raycasting_results.append((depth, projected_height, texture, offset))
    
    def update(self):
        self.raycast()
        self.render_objects()
        self.update_sprites()
        self.update_enemies()
    
    def load_wall_textures(self):
        return {
            1: self.game.get_texture('resources/textures/wall.png')
        }
    
    def draw(self):
        for _, image, pos in sorted(self.objects_to_render, key=lambda t: t[0], reverse=True):
            self.screen.blit(image, pos)