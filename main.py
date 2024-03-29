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
        self.previous_day = 0
        self.current_day = 1
        pg.display.set_caption(f"{TITLE} - Day {self.current_day}")
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.background_sprites = pg.sprite.Group()
        self.rabbit_sprite = pg.sprite.Group()
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.day_elapsed_time = 0
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
        self.bear_sprite = pg.sprite.Group()
        self.boar_sprite = pg.sprite.Group()
        self.alligator_sprite = pg.sprite.Group()

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                    self.player_sprite.add(self.player)

        self.active_grass_tiles = []
        self.consumed_grass_tiles = []  
        for row in range(GRIDWIDTH):
            for col in range(GRIDWIDTH):
                grass = Grass(self, col, row)
                self.active_grass_tiles.append(grass)
                self.grass_tiles.add(grass)

        self.rabbit = Rabbit(self, randint(0, GRIDWIDTH - 1), randint(0, GRIDHEIGHT - 1))
        self.bear = Bear(self, randint(0, GRIDWIDTH - 1), randint(0, GRIDHEIGHT - 1))
        self.boar = Boar(self, randint(0, GRIDWIDTH - 1), randint(0, GRIDHEIGHT - 1))
        self.alligator = Alligator(self, randint(0, GRIDWIDTH - 1), randint(0, GRIDHEIGHT - 1))
        self.rabbit_sprite.add(self.rabbit)
        self.bear_sprite.add(self.bear)
        self.boar_sprite.add(self.boar)
        self.alligator_sprite.add(self.alligator)
        self.all_sprites.add(self.rabbit)

        self.all_sprites.add(self.rabbit)
        self.all_sprites.add(self.bear)
        self.all_sprites.add(self.boar)
        self.all_sprites.add(self.alligator)


    def run(self):
        self.playing = True
        self.simulation_time = 0
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.day_elapsed_time += self.dt
            self.simulation_time += self.dt
            self.current_day = int(self.simulation_time // DAY_LENGTH_SECONDS) + 1
            self.rabbit.move_cooldown = 0

            if self.day_elapsed_time >= DAY_LENGTH_SECONDS:
                self.day_elapsed_time -= DAY_LENGTH_SECONDS
           
            
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

    def count_population(self):
        rabbit_count = 0
        alligator_count = 0
        bear_count = 0
        boar_count = 0
        for sprite in self.all_sprites:
            if isinstance(sprite, Rabbit):
                rabbit_count += 1
            if isinstance(sprite, Alligator):  # Capitalize the class name
                alligator_count += 1
            if isinstance(sprite, Bear):
                bear_count += 1
            if isinstance(sprite, Boar):
                boar_count += 1
        return rabbit_count, bear_count, boar_count, alligator_count

    
    

    def update(self):
        self.all_sprites.update()
        self.update_window_caption()
        self.previous_day = self.current_day
        self.grass_tiles.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.background_sprites.draw(self.screen)
        self.walls.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.rabbit_sprite.draw(self.screen)
        self.bear_sprite.draw(self.screen)
        self.boar_sprite.draw(self.screen)
        self.alligator_sprite.draw(self.screen)
        pg.display.flip()
    
    def update_window_caption(self):
        rabbit_count, bear_count, boar_count, alligator_count = self.count_population()
        if self.previous_day != self.current_day:
            pg.display.set_caption(f"{TITLE} - Day {self.current_day} - Rabbits: {rabbit_count} - Bears: {bear_count} - Boars: {boar_count} - Alligators: {alligator_count}")
            
            self.previous_day = self.current_day
        else:
            pg.display.set_caption(f"{TITLE} - Day {self.current_day} - Rabbits: {rabbit_count} - Bears: {bear_count} - Boars: {boar_count} - Alligators: {alligator_count}")

if __name__ == "__main__":
    g = Game()
    g.new()
    print("i am here")
    while True:
        g.run()


