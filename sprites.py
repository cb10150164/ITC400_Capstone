import pygame as pg
import random
from settings import *
from random import choice

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x = (self.x + dx) % GRIDWIDTH
            self.y = (self.y + dy) % GRIDHEIGHT

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Tile:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

class Grass(Tile, pg.sprite.Sprite):
    def __init__(self, game, x, y):
        Tile.__init__(self, game, x, y)
        self.groups = game.background_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.consumed = False
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.regrowth_time = 2 * DAY_LENGTH_SECONDS

    def consumed(self, current_time):
        self.consumption_time = current_time
    def update(self):
        if self.consumed and self.game.simulation_time - self.consumption_time >= self.regrowth_time:
            self.consumed = False
            self.image.fill(GREEN)


class Animal(pg.sprite.Sprite):
    def __init__(self, game, x, y, health, strength, speed, energy, aggression, herding, territorial):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.health = health
        self.strength = strength
        self.speed = speed
        self.energy = energy
        self.aggression = aggression
        self.herding = herding
        self.territorial = territorial
        self.last_energy_loss_time = 0

    def reduce_health(self):
        self.health -= 1
        if self.health <= 0:
            self.die()

    def die(self):
        self.kill()

    def move(self, dx=0, dy=0):
        new_x = (self.x + self.velocity.x) % GRIDWIDTH
        new_y = (self.y + self.velocity.y) % GRIDHEIGHT

        if 0 <= new_x < GRIDWIDTH and 0 <= new_y < GRIDHEIGHT:
            self.x = new_x
            self.y = new_y
            self.rect.x = self.x * TILESIZE
            self.rect.y = self.y * TILESIZE

    def update(self):
        if random.random() < self.speed:
            self.move()
            if hasattr(self, 'consume'):
                if self.energy <= self.max_energy / 2:
                    self.consume(self.game, self.game.simulation_time)

        if self.game.simulation_time - self.last_energy_loss_time >= SIMULATION_HOUR:
            energy_loss = self.energy_loss_per_hour()
            self.decrease_energy(energy_loss)
            self.last_energy_loss_time = self.game.simulation_time

class Alligator(Animal):
    def __init__(self, game, x, y, health=None, energy=None):
        super().__init__(game, x, y, health=170, strength=20, speed=.4, energy=100, aggression=50, herding=True, territorial=True)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKGREY)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.max_energy = self.health * alligator_matrat_e

    def energy_loss_per_hour(self):
        return SIMULATION_HOUR * self.health

    def decrease_energy(self, energy_loss):
        self.energy -= energy_loss
        if self.energy <= 0:
            self.reduce_health()
            self.energy = self.health * alligator_matrat_e

    def consume(self, game, simulation_time):
        prey_to_consume = pg.sprite.spritecollide(self, game.rabbit_sprite, False)
        if prey_to_consume:
            prey = prey_to_consume[0]
            prey.die()
            self.energy += 80

    def update(self):
        if self.game.simulation_time - self.last_energy_loss_time >= SIMULATION_HOUR:
            energy_loss = self.energy_loss_per_hour()
            self.decrease_energy(energy_loss)
            self.last_energy_loss_time = self.game.simulation_time

        if random.random() < self.speed:
            self.move()
            if self.energy <= self.max_energy / 2:
                self.consume(self.game, self.game.simulation_time)


class Boar(Animal):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, health=170, strength=20, speed=.4, energy=100, aggression=50, herding=True, territorial=True)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.max_energy = self.health * boar_matrat_e

    def energy_loss_per_hour(self):
        return SIMULATION_HOUR * self.health

    def decrease_energy(self, energy_loss):
        self.energy -= energy_loss
        if self.energy <= 0:
            self.reduce_health()
            self.energy = self.health * boar_matrat_e

    def consume(self, game, simulation_time):
        grass_to_consume = pg.sprite.spritecollide(self, game.grass_tiles, False)
        if grass_to_consume:
            grass = grass_to_consume[0]
            if not grass.consumed:
                grass.consumed = True
                grass.consumption_time = simulation_time
                grass.image.fill(YELLOW)  # Change the color to yellow
                self.energy += 25  # Adjust the energy gain as needed

            if self.energy > self.max_energy:
                self.health += 1
                self.energy = self.health * boar_matrat_e

    def update(self):
        if self.game.simulation_time - self.last_energy_loss_time >= SIMULATION_HOUR:
            energy_loss = self.energy_loss_per_hour()
            self.decrease_energy(energy_loss)
            self.last_energy_loss_time = self.game.simulation_time

        if random.random() < self.speed:
            self.move()
            if self.energy <= self.max_energy / 2:
                self.consume(self.game, self.game.simulation_time)

class Bear(Animal):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, health=300, strength=20, speed=.5, energy=100, aggression=50, herding=False, territorial=True)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.last_energy_loss_time = 0
        
    def move(self, dx=0, dy=0):
        new_x = (self.x + self.velocity.x) % GRIDWIDTH
        new_y = (self.y + self.velocity.y) % GRIDHEIGHT

        if 0 <= new_x < GRIDWIDTH and 0 <= new_y < GRIDHEIGHT:
            self.x = new_x
            self.y = new_y
            self.rect.x = self.x * TILESIZE
            self.rect.y = self.y * TILESIZE   
            
    def update(self):
        if random.random() < self.speed:
            self.move()
            
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Rabbit(Animal):
    def __init__(self, game, x, y):
        health = random.uniform(1, rabbit_max_h)
        # Calculate initial energy based on health and matrat
        energy = health * rabbit_matrat_e
        super().__init__(game, x, y, health=health, strength=20, speed=.3, energy=energy, aggression=50, herding=False, territorial=False)
        self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.max_energy = self.health * rabbit_matrat_e
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (TILESIZE // 2, TILESIZE // 2)) # Scale the image
        self.rect.x = x * TILESIZE + TILESIZE // 4 # Center the sprite within the tile horizontally
        self.rect.y = y * TILESIZE + TILESIZE // 4
        self.last_energy_loss_time = 0
       
    def energy_loss_per_hour(self):
        return SIMULATION_HOUR * self.health
           
    def decrease_energy(self, energy_loss):
        self.energy -= energy_loss
        if self.energy <= 0:
            self.reduce_health()
            self.energy = rabbit_matrat_e * self.health


    def consume_grass(self, game, simulation_time):
        grass_to_consume = pg.sprite.spritecollide(self, game.grass_tiles, False)
        if grass_to_consume:
            grass = grass_to_consume[0]
            if not grass.consumed:
                grass.consumed = True
                grass.consumption_time = simulation_time
                grass.image.fill(YELLOW)  # Change the color to yellow
                self.energy += 33
           
            if self.energy > self.max_energy:
                self.health += 1
                self.energy = self.health * rabbit_matrat_e

    
    def update(self):
        #print("Rabbit update method called")
        if random.random() < self.speed:
            self.move()
            if self.energy <= self.max_energy / 2:
                self.consume_grass(self.game, self.game.simulation_time)

            #self.move(dx, dy)
            #self.consume_grass(self.game, self.game.simulation_time)
            # Set the move_cooldown to the current simulation_time plus the desired cooldown time in seconds
            
        if self.game.simulation_time - self.last_energy_loss_time >= SIMULATION_HOUR:
            energy_loss = self.energy_loss_per_hour()
            self.decrease_energy(energy_loss)
            self.last_energy_loss_time = self.game.simulation_time

        
    def move(self, dx=0, dy=0):
        new_x = (self.x + self.velocity.x) % GRIDWIDTH
        new_y = (self.y + self.velocity.y) % GRIDHEIGHT

        if 0 <= new_x < GRIDWIDTH and 0 <= new_y < GRIDHEIGHT:
            self.x = new_x
            self.y = new_y
            self.rect.x = self.x * TILESIZE + TILESIZE // 4
            self.rect.y = self.y * TILESIZE + TILESIZE // 4

    def die(self):
        self.kill()