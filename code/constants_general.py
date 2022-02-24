from enum import Enum


# Game status constants
class Game_status(Enum):
    PLAYABLE_SCREEN = 0
    FINAL_SCREEN = 1
    GAME_OVER = 2


# Main Screen
MENU_SCREEN_SIZE = [480, 630]
MENU_SIZE = [300, 400]

# Game
SPEED_INCREMENT = 1.02

# Player
PLAYER_LASER_CD = 800

# Aliens
ALIEN_LASER_CD = 100
ALIEN_NUMBER_COLUMNS = 8
ALIEN_NUMBER_ROWS = 6
MIN_LASER_CD = 40
MAX_LASER_CD = 80

# Mothership
MOTHERSHIP_MIN_CD = 500
MOTHERSHIP_MAX_CD = 2000

# Lives
NUM_LIVES = 3


