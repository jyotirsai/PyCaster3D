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
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.health_recovery_delay = 500
        self.time_prev = pg.time.get_ticks()
    
    def health_recovery(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            
            if self.health < PLAYER_MAX_HEALTH:
                self.health += 1
    
    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()

        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            self.game.game_state = "menu"
    
    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.shot = True
                self.game.weapon.reloading = True
    
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
        return (x,y) in self.game.map.walls

    def check_wall_collision(self, dx, dy):
        player_scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if not self.is_wall_position(int(self.x+dx*player_scale), int(self.y)):
            self.x += dx
        if not self.is_wall_position(int(self.x), int(self.y+dy*player_scale)):
            self.y += dy

    def draw(self):
        #pg.draw.line(self.game.screen, 'yellow', (self.x*100, self.y*100),
        #             (self.x*100 + WIDTH * math.cos(self.angle), self.y*100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()
        self.health_recovery()
    
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
