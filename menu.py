import pygame as pg
import sys
from settings import *

class MenuButton(pg.sprite.Sprite):
    def __init__(self, text, position, font, callback=None):
        super().__init__()
        self.text = text
        self.position = position
        self.font = font
        self.callback = callback
        self.create_surface()

    def create_surface(self):
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.position)

    def handle_click(self):
        if self.callback:
            self.callback()

class Menu:
    def __init__(self, screen):
        self.text_color = (255, 255, 255)
        self.menu_background_color = (128, 128, 128)
        self.screen = screen
        self.font = pg.font.SysFont(FONT, 36)
        self.menu_running = True
        self.buttons = pg.sprite.Group()

    def add_button(self, text, position, callback=None):
        button = MenuButton(text, position, self.font, callback)
        self.buttons.add(button)

    def run(self):
        pg.display.set_caption("ZombieFPS")
        
        while self.menu_running:
            self.screen.fill(self.menu_background_color)
            self.draw_buttons()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit_game()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.check_button_click(event.pos)

            pg.display.update()

    def draw_buttons(self):
        self.buttons.draw(self.screen)

    def check_button_click(self, mouse_pos):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                button.handle_click()

    def quit_game(self):
        pg.quit()
        sys.exit()