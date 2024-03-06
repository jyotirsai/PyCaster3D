import pygame as pg

_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if mini_map[i][j] == 1:
                    self.world_map[(j,i)] = mini_map[i][j]

    def draw(self):
        arr = []
        for row,col in self.world_map:
            arr.append(pg.draw.rect(self.game.screen, 'darkgray', (row*100, col*100, 100, 100), 2))
        return arr