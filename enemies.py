from sprite_object import *

class Enemies(AnimatedSprite):
    def __init__(self, game, path='resources/enemies/caco_demon/0.png', pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk = self.get_images(self.path + '/walk')

        self.attack_dist = 1.0
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 1
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.frame_counter = 0
        self.death_animated = False
    
    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
    
    def animate_death(self):
        if not self.alive:
            if self.animation_trigger and self.frame_counter < len(self.death_images)-1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1
    
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False
    
    def check_hit_in_enemy(self):
        if self.game.player.shot:
            if WIDTH//2 - self.sprite_half_width < self.screen_x < WIDTH//2 + self.sprite_half_width:
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()
    
    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.dead.append(self)

            if self.game.dead:
                self.game.enemies.append(Enemies(self.game))
    
    def run_logic(self):
        if self.alive:
            self.check_hit_in_enemy()
            self.animate_pain()
            self.movement()
            if self.pain:
                self.animate_pain()
            elif self.dist < self.attack_dist:
                self.animate(self.attack_images)
                self.game.player.get_damage(self.attack_damage)
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()
        
    def is_wall_position(self, x, y):
        return (x,y) in self.game.map.walls

    def check_wall_collision(self, dx, dy):
        if not self.is_wall_position(int(self.x+dx*self.size), int(self.y)):
            self.x += dx
        if not self.is_wall_position(int(self.x), int(self.y+dy*self.size)):
            self.y += dy
    
    def movement(self):
        next_pos = self.game.pathfinder.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        if next_pos not in self.game.enemy_pos:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle)*self.speed
            dy = math.sin(angle)*self.speed
            self.check_wall_collision(dx, dy)
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
