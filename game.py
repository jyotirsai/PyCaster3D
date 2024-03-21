import pygame as pg
import sys
from settings import *
from menu import *
from map import *
from player import *
from engine import *
from object_handler import *
from weapon import *
from pathfinder import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.game_state = "main_menu"
        self.create_menu()

    def create_menu(self):
        self.menu = Menu(self.screen)

        self.menu.add_button("Start Game", (WIDTH // 2, HEIGHT // 2), callback=self.start_game)
        self.menu.add_button("Settings", (WIDTH // 2, HEIGHT // 2 + 50), callback=self.show_settings)
        self.menu.add_button("Exit", (WIDTH // 2, HEIGHT // 2 + 100), callback=self.quit_game)

    def start_game(self):
        print("Start Game")
        pg.mouse.set_visible(False)
        self.menu.menu_running = False
        self.game_state = "in_game"
        self.init_game()

    def show_settings(self):
        print("Show Settings")

    def quit_game(self):
        pg.quit()
        sys.exit()
    
    def get_texture(self, path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def init_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.engine = Engine(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.pathfinder = PathFinder(self)

    def update(self):
        self.player.update()
        self.engine.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')
    
    def game_over(self):
        game_over_image = self.get_texture('resources/textures/game_over.png', (WIDTH,HEIGHT))
        self.screen.blit(game_over_image, (0,0))

    def draw(self):
        self.screen.fill('black')
        self.engine.draw()
        self.weapon.draw()
        #self.map.draw()
        #self.player.draw()

    def key_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            if self.game_state == "main_menu":
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pg.mouse.get_pos()
                    self.menu.check_button_click((x, y))
            
            if self.game_state == "in_game":
                self.player.single_fire_event(event)

    def run(self):
        while True:
            if self.game_state == "main_menu":
                self.menu_running = True
                self.menu.run()
            elif self.game_state == "in_game":
                self.update()
                self.draw()
            self.key_events()

