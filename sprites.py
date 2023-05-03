import pygame as pg
import random
import math
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

        if not self.collide_with_walls(new_x - self.x, 0):  # Check for horizontal collisions
            self.x = new_x
            self.rect.x = self.x * TILESIZE

        if not self.collide_with_walls(0, new_y - self.y):  # Check for vertical collisions
            self.y = new_y
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

    def collide_with_walls(self, dx=0, dy=0):
        future_rect = pg.Rect(self.rect.x + dx * TILESIZE, self.rect.y + dy * TILESIZE, self.rect.width, self.rect.height)
        for wall in self.game.walls:
            if future_rect.colliderect(wall.rect):
                return True
        return False
    def get_distance_to(self, target):
        dx, dy = self.x - target.x, self.y - target.y
        return math.sqrt(dx ** 2 + dy ** 2)




    def make_decision(self):
        # Decision-making based on the animal's current state
        actions = {
            'drink': self.needs_drink(),
            'rest': self.needs_rest(),
            'eat': self.needs_eat(),
            'reproduce': self.needs_reproduce(),
        }

        # Sort actions based on priority
        sorted_actions = sorted(actions.items(), key=lambda x: x[1], reverse=True)

        # Execute the highest priority action
        action, priority = sorted_actions[0]

        if action == 'drink':
            if self.is_near_water():
                self.last_water_drinking_time = self.game.simulation_time
            else:
                self.move_towards_water()
        elif action == 'rest':
            self.rest()
        elif action == 'eat':
            self.find_food_and_eat()
        elif action == 'reproduce':
            self.find_mate()
    
    def needs_reproduce(self):
        time_since_last_reproduction = self.game.simulation_time - self.last_reproduction_time

    # Prioritize reproduction when the animal is ready to reproduce
        priority = max(0, (time_since_last_reproduction - self.reproduction_interval) / self.reproduction_interval)

        return priority
    def needs_eat(self):
        energy_fraction = self.energy / self.max_energy

        if energy_fraction > 0.5:  # More than half energy
            hunger_priority = 2 * (1 - energy_fraction)
        elif 0.33 <= energy_fraction <= 0.5:  # Between 1/3 and half energy
            hunger_priority = 3 * (1 - energy_fraction)
        else:  # Less than 1/3 energy
            hunger_priority = 4 * (1 - energy_fraction)

        return hunger_priority

    def needs_drink(self):
        time_since_last_drink = self.game.simulation_time - self.last_water_drinking_time

    # If the animal is getting close to its water-drinking interval,
    # the priority increases as the time gets closer to the interval.
        priority = max(0, (self.water_drinking_interval - time_since_last_drink) / self.water_drinking_interval)

        return priority

    def needs_rest(self):
        if self.resting:
            return 0  # If the bear is already resting, it doesn't need to rest again

        time_since_last_rest = self.game.simulation_time - self.last_rest_start_time
         # Prioritize resting when the bear has been active for a long time
        priority = max(0, (time_since_last_rest - self.rest_duration) / self.rest_duration)
        return priority

    def is_near_water(self):
        wall = pg.sprite.spritecollide(self, self.game.walls, False, pg.sprite.collide_rect_ratio(1.1))
        return bool(wall)

    def move_towards_water(self):
        closest_water = None
        closest_water_dist = None
        for water in self.game.water_tiles:
            dist = self.get_distance_to(water)
            if closest_water is None or dist < closest_water_dist:
                closest_water = water
                closest_water_dist = dist

        if closest_water is not None:
            self.move_towards(closest_water)
    
    def reproduce(self, partner):
        offspring_health = (self.health + partner.health) / 2 + random.uniform(-5, 5)
        offspring_strength = (self.strength + partner.strength) / 2 + random.uniform(-1, 1)
        offspring_speed = (self.speed + partner.speed) / 2 + random.uniform(-0.01, 0.01)
        offspring_aggression = (self.aggression + partner.aggression) / 2 + random.uniform(-5, 5)

        offspring = self.__class__(self.game, self.x, self.y, health=offspring_health, strength=offspring_strength, speed=offspring_speed, aggression=offspring_aggression)
        self.game.all_sprites.add(offspring)

        self.energy -= self.energy_loss_for_reproduction()
        partner.energy -= partner.energy_loss_for_reproduction()

    def find_mate(self):
        potential_mates = pg.sprite.spritecollide(self, self.game.all_sprites, False, collided=pg.sprite.collide_circle)
        potential_mates = [mate for mate in potential_mates if isinstance(mate, self.__class__) and mate != self]
        if potential_mates:
            mate = random.choice(potential_mates)
            self.reproduce(mate)


















class Alligator(Animal):
    def __init__(self, game, x, y, health=None, energy=None):
        health = random.uniform(70, alligator_max_h)
        # Calculate initial energy based on health and matrat
        energy = health * alligator_matrat_e
        super().__init__(game, x, y, health=health, strength=20, speed=.3, energy=energy, aggression=50, herding=False, territorial=False)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.last_energy_loss_time = 0
        self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.max_energy = self.health * alligator_matrat_e
        self.water_drinking_interval = DAY_LENGTH_SECONDS * 7
        self.last_water_drinking_time = 0

    def energy_loss_per_hour(self):
        return SIMULATION_HOUR * self.health

    def decrease_energy(self, energy_loss):
        self.energy -= energy_loss
        if self.energy <= 0:
            self.reduce_health()
            self.energy = self.health * alligator_matrat_e

    def hunt_rabbit(self):
        # Hunt for rabbit
        closest_rabbit = None
        closest_rabbit_dist = None
        for rabbit in self.game.rabbit_sprite:
            dist = self.get_distance_to(rabbit)
            if closest_rabbit is None or dist < closest_rabbit_dist:
                closest_rabbit = rabbit
                closest_rabbit_dist = dist
        
        if closest_rabbit is not None:
            if closest_rabbit_dist <= 1:  # Close enough to attack
                self.attack(closest_rabbit)
            else:
                self.move_towards(closest_rabbit)

    def update(self):
        self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.hunt_rabbit()
        if self.energy >= self.max_energy/2:
            self.move()

        if self.game.simulation_time - self.last_energy_loss_time >= SIMULATION_HOUR:
            energy_loss = self.energy_loss_per_hour()
            self.decrease_energy(energy_loss)
            self.last_energy_loss_time = self.game.simulation_time
        if self.game.simulation_time - self.last_water_drinking_time >= self.water_drinking_interval:
            self.drink_water()

        if self.game.simulation_time - self.last_water_drinking_time > self.water_drinking_interval:
            self.die()
            
    def attack(self, prey):
        prey.reduce_health()
        if isinstance(prey, Rabbit) and prey.health <= 0:
            prey.die()
            self.energy += 80

    def move_towards(self, target):
        dx, dy = target.x - self.x, target.y - self.y
        if dx > 0:
            self.velocity.x = self.speed
        elif dx < 0:
            self.velocity.x = -self.speed
        if dy > 0:
            self.velocity.y = self.speed
        elif dy < 0:
            self.velocity.y = -self.speed

        new_x = (self.x + self.velocity.x) % GRIDWIDTH
        new_y = (self.y + self.velocity.y) % GRIDHEIGHT

    def is_near_water(self):
        wall = pg.sprite.spritecollide(self, self.game.walls, False, pg.sprite.collide_rect_ratio(1.1))
        return bool(wall)

    def drink_water(self):
        if self.is_near_water():
            self.last_water_drinking_time = self.game.simulation_time






















class Boar(Animal):
    def __init__(self, game, x, y):
        health = random.uniform(100, boar_max_h)
        # Calculate initial energy based on health and matrat
        energy = health * boar_matrat_e
        super().__init__(game, x, y, health=health, strength=20, speed=.1, energy=energy, aggression=50, herding=False, territorial=False)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.last_energy_loss_time = 0
        self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.max_energy = self.health * boar_matrat_e
        self.water_drinking_interval = DAY_LENGTH_SECONDS * 3
        self.last_water_drinking_time = 0

    def energy_loss_per_hour(self):
        return SIMULATION_HOUR * self.health

    def decrease_energy(self, energy_loss):
        self.energy -= energy_loss
        if self.energy <= 0:
            self.reduce_health()
            self.energy = self.health * boar_matrat_e

    def consume(self, game, simulation_time):
        if self.energy >= self.max_energy:  # Stop consuming if the energy is at or above the maximum
            return

        grass_to_consume = pg.sprite.spritecollide(self, game.grass_tiles, False)
        if grass_to_consume:
            grass = grass_to_consume[0]
            if not grass.consumed:
                grass.consumed = True
                grass.consumption_time = simulation_time
                grass.image.fill(YELLOW)  # Change the color to yellow
                self.energy += 33  # Adjust the energy gain as needed

            if self.energy > self.max_energy:
                self.health += 1
                self.energy = self.health * boar_matrat_e
                self.max_energy = self.health * boar_matrat_e


    def update(self):
        if random.random() < 0.1:  # Adjust this value for more or less frequent direction changes
            self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.move()

        if self.energy <= self.max_energy / 2:
            self.consume(self.game, self.game.simulation_time)

        if self.game.simulation_time - self.last_energy_loss_time >= SIMULATION_HOUR:
            energy_loss = self.energy_loss_per_hour()
            self.decrease_energy(energy_loss)
            self.last_energy_loss_time = self.game.simulation_time
        if self.game.simulation_time - self.last_water_drinking_time >= self.water_drinking_interval:
            self.drink_water()

        if self.game.simulation_time - self.last_water_drinking_time > self.water_drinking_interval:
            self.die()

    def move(self):
        new_x = (self.x + self.velocity.x) % GRIDWIDTH
        new_y = (self.y + self.velocity.y) % GRIDHEIGHT

        if not self.collide_with_walls(new_x - self.x, new_y - self.y):
            if 0 <= new_x < GRIDWIDTH and 0 <= new_y < GRIDHEIGHT:
                self.x = new_x
                self.y = new_y
                self.rect.x = self.x * TILESIZE
                self.rect.y = self.y * TILESIZE
    def is_near_water(self):
        wall = pg.sprite.spritecollide(self, self.game.walls, False, pg.sprite.collide_rect_ratio(1.1))
        return bool(wall)

    def drink_water(self):
        if self.is_near_water():
            self.last_water_drinking_time = self.game.simulation_time

















class Bear(Animal):
    def __init__(self, game, x, y):
        health = random.uniform(45, bear_max_h)
        # Calculate initial energy based on health and matrat
        energy = health * bear_matrat_e
        super().__init__(game, x, y, health=health, strength=20, speed=.1, energy=energy, aggression=50, herding=False, territorial=False)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.last_energy_loss_time = 0
        self.water_drinking_interval = DAY_LENGTH_SECONDS * 7
        self.last_water_drinking_time = 0

    def move(self):
        new_x = (self.x + self.velocity.x) % GRIDWIDTH
        new_y = (self.y + self.velocity.y) % GRIDHEIGHT

        if not self.collide_with_walls(new_x - self.x, new_y - self.y):
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
        if self.game.simulation_time - self.last_water_drinking_time >= self.water_drinking_interval:
            self.drink_water()

        if self.game.simulation_time - self.last_water_drinking_time > self.water_drinking_interval:
            self.die()

    def is_near_water(self):
        wall = pg.sprite.spritecollide(self, self.game.walls, False, pg.sprite.collide_rect_ratio(1.1))
        return bool(wall)

    def drink_water(self):
        if self.is_near_water():
            self.last_water_drinking_time = self.game.simulation_time















class Rabbit(Animal):
    def __init__(self, game, x, y):
        health = random.uniform(1, rabbit_max_h)
        # Calculate initial energy based on health and matrat
        energy = health * rabbit_matrat_e
        super().__init__(game, x, y, health=health, strength=20, speed=.1, energy=energy, aggression=50, herding=False, territorial=False)
        self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.max_energy = self.health * rabbit_matrat_e
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.last_water_drinking_time = 0
        self.water_drinking_interval = DAY_LENGTH_SECONDS  # One day in simulation time
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

    def is_near_water(self):
        wall = pg.sprite.spritecollide(self, self.game.walls, False, pg.sprite.collide_rect_ratio(1.1))
        return bool(wall)

    def drink_water(self):
        if self.is_near_water():
            self.last_water_drinking_time = self.game.simulation_time

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
                self.energy = self.health * rabbit_matrat_e

    
    def update(self):
        if random.random() < 0.1:  # Adjust this value for more or less frequent direction changes
            self.velocity = pg.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1])) * self.speed
        self.move()

        if self.energy <= self.max_energy / 2:
            self.consume_grass(self.game, self.game.simulation_time)

        if self.game.simulation_time - self.last_energy_loss_time >= SIMULATION_HOUR:
            energy_loss = self.energy_loss_per_hour()
            self.decrease_energy(energy_loss)
            self.last_energy_loss_time = self.game.simulation_time
        if self.game.simulation_time - self.last_water_drinking_time >= self.water_drinking_interval:
            self.drink_water()

        if self.game.simulation_time - self.last_water_drinking_time > self.water_drinking_interval:
            self.die()

    def move(self, dx=0, dy=0):
        new_x = (self.x + self.velocity.x) % GRIDWIDTH
        new_y = (self.y + self.velocity.y) % GRIDHEIGHT

        if not self.collide_with_walls(new_x - self.x, new_y - self.y):
            if 0 <= new_x < GRIDWIDTH and 0 <= new_y < GRIDHEIGHT:
                self.x = new_x
                self.y = new_y
                self.rect.x = self.x * TILESIZE + TILESIZE // 4
                self.rect.y = self.y * TILESIZE + TILESIZE // 4

    def die(self):
        self.kill()