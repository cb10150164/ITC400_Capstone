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
DAY_LENGTH_SECONDS = 5 * 60

#animal max numbers
bear_max_h = 900
bear_max_e = 15 # * health in kilos

boar_max_h = 700
boar_max_e = 24 # the matrat or max in this case is used to determin metabloic rate in a day

rabbit_max_h = 6
rabbit_matrat_e = 190 # 190 * health

alli_max_h = 1000
alli_matrat_e = 20