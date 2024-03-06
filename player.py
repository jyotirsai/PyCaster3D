from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.speed = PLAYER_SPEED
        self.angle_speed = PLAYER_ANGLE_SPEED
    
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        distance = self.speed*self.game.delta_time
        keys = pg.key.get_pressed()
        dx,dy = 0, 0
        if keys[pg.K_w]:
            dx += distance*cos_a
            dy += distance*sin_a
        if keys[pg.K_s]:
            dx -= distance*cos_a
            dy -= distance*sin_a
        if keys[pg.K_a]:
            dx += distance*sin_a
            dy -= distance*cos_a
        if keys[pg.K_d]:
            dx -= distance*sin_a
            dy += distance*cos_a
        
        self.check_wall_collision(dx, dy)
        
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_rel_x = mouse_x - self.game.screen.get_width() // 2
        pg.mouse.set_pos(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2) 
        self.angle += mouse_rel_x * self.game.delta_time * self.angle_speed 

    def is_wall_position(self, x, y):
        return (x,y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.is_wall_position(int(self.x+dx), int(self.y)):
            self.x += dx
        if self.is_wall_position(int(self.x), int(self.y+dy)):
            self.y += dy

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x*100, self.y*100),
                     (self.x*100 + WIDTH * math.cos(self.angle), self.y*100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()
    
    def pos(self):
        return self.x, self.y

    def map_pos(self):
        return int(self.x), int(self.y)
    
