import pygame as pg
import math
from settings import *

class Rendering:
    def __init__(self, game):
        self.game = game
    
    def raycasting(self):
        ray_angle = self.game.player.angle - FOV/2 + 0.0001
        player_x, player_y = self.game.player.pos()
        map_x, map_y = self.game.player.map_pos()
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

            depth_hori = (y_hori - player_y) / sin_a
            x_hori = player_x + depth_hori * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for _ in range(MAX_DEPTH):
                if (int(x_hori), int(y_hori)) in self.game.map.walls:
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

            depth_vert = (x_vert - player_x) / cos_a
            y_vert = player_y+depth_vert*sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for _ in range(MAX_DEPTH):
                if (int(x_vert), int(y_vert)) in self.game.map.walls:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            depth = min(depth_vert, depth_hori)
            projected_height = CAMERA_PLANE_DIST / (depth + 0.000001)

            pg.draw.rect(self.game.screen, 'white', (ray*SCALE, HEIGHT/2 - projected_height//2, SCALE, projected_height))


    def update(self):
        self.raycasting()