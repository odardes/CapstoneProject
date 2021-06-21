from pathlib import Path

# Establish window resolution (x, y)
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 500
RESOLUTION = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
ROWS = 10
CAR_WIDTH = 200
CAR_HEIGHT = 100

# Establish FPS (frames-per-second) and time delta
FPS = 30
time_delta = 1/FPS

# Establish colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (192, 192, 192)

# Font sizes and type
default_font_size = 15

# Car path
image_player_car = str(Path("Images/gray_car.png"))
