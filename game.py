import pygame as pg
import sys
from settings import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.game_state = "main_menu"
        self.main_menu()
    
    def initGame(self):
        pass
    
    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
    
    def draw(self):
        self.screen.fill('black')
        
    def key_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            if self.game_state == "main_menu":
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pg.mouse.get_pos() 
                        # Check only if Exit button is in clicked region 
                        if WIDTH // 2 - 50 < x < WIDTH // 2 + 50 and HEIGHT // 2 + 90 < y < HEIGHT // 2 + 130:
                            pg.quit()
                            sys.exit()
            
    def run(self):
        while True:
            self.key_events()
            self.update()
            self.draw()
    
    def main_menu(self):
        if self.game_state == "main_menu":
            self.font = pg.font.SysFont(FONT, 30)
            self.buttons = {
                "Start Game": (WIDTH//2, HEIGHT//2),
                "Settings": (WIDTH//2, HEIGHT//2 + 50),
                "Exit": (WIDTH // 2, HEIGHT // 2 + 100),
            }
            pg.display.set_caption("ZombieFPS Menu")
            text_color = (255, 255, 255)

            while True:
                self.screen.fill((128, 128, 128))
                textobj = self.font.render('Main Menu', True, text_color)
                textrect = textobj.get_rect(center=(WIDTH//2,HEIGHT//4))
                self.screen.blit(textobj, textrect)
                
                for text, (x, y) in self.buttons.items():
                    textobj = self.font.render(text, True, text_color)
                    textrect = textobj.get_rect(center=(x,y))
                    self.screen.blit(textobj, textrect)
            
                pg.display.update()
                self.key_events()

if __name__ == "__main__":
    game = Game()
    #menu.run()
