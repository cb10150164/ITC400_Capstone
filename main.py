import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from random import randint

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.grass_tiles = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.rabbit_sprite = pg.sprite.Group()  # Create the rabbit sprite group

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                    self.player_sprite.add(self.player)

        self.active_grass_tiles = []
        self.consumed_grass_tiles = []  # Add this line back
        for row in range(GRIDWIDTH):
            for col in range(GRIDWIDTH):
                grass = Grass(self, col, row)
                self.active_grass_tiles.append(grass)
                self.grass_tiles.add(grass)

        self.rabbit = Rabbit(self, randint(0, GRIDWIDTH - 1), randint(0, GRIDHEIGHT - 1))
        self.rabbit_sprite.add(self.rabbit)  # Add the rabbit to the rabbit sprite group


    def run(self):
        self.playing = True
        self.simulation_time = 0
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.simulation_time += self.dt
            #self.rabbit.consume_grass(self.active_grass_tiles, self.simulation_time)
            
            for grass in self.consumed_grass_tiles:
                if self.simulation_time - grass.consumption_time >= grass.regrowth_time:
                    self.active_grass_tiles.append(grass)
                    self.consumed_grass_tiles.remove(grass)

            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:  
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)


    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.grass_tiles.draw(self.screen)
        self.walls.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.rabbit_sprite.draw(self.screen)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()
    g.new()
    while True:
        g.run()
