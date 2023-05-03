# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,225)
BROWN = (139,69,19)
orange = (255, 165, 0)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Simulation"
BGCOLOR = DARKGREY

TILESIZE = 8
GRIDWIDTH = int(WIDTH / TILESIZE)
GRIDHEIGHT = int(HEIGHT / TILESIZE)

#time 
DAY_LENGTH = 600  # Length of a day in seconds (10 minutes)
day_lenth_min = 2
DAY_LENGTH_SECONDS = day_lenth_min * 60


# 1day/number of mintues  = days/min
# 1hr=1/24day
#(1/24)/( day/min) = minutes * 60 seconds/minute = secounds rounded up
SIMULATION_HOUR =  (day_lenth_min/24) * (1/day_lenth_min) * 60

#animal max numbers
bear_max_h = 410
bear_matrat_e = 15 # * health in kilos

boar_max_h = 320
boar_matrat_e = 24 # the matrat or max in this case is used to determin metabloic rate in a day

rabbit_max_h = 3 #kilos
rabbit_matrat_e = 190 # 190 * health

alligator_max_h = 455
alligator_matrat_e = 20