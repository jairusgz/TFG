
# Constantes de Pantalla
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 210
SCREEN_RES = [SCREEN_WIDTH, SCREEN_HEIGHT]
SCORE_FONT_SIZE = 10
GAME_OVER_FONT_SIZE = 15
GAME_OVER_CENTER_POS = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
FINAL_SCORE_CENTER_POS = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20]
RETURN_FONT_SIZE = GAME_OVER_FONT_SIZE // 2
RETURN_CENTER_POS = [FINAL_SCORE_CENTER_POS[0], FINAL_SCORE_CENTER_POS[1] + GAME_OVER_FONT_SIZE]

# Planeta
PLANET_WIDTH = SCREEN_WIDTH
PLANET_HEIGHT = SCREEN_HEIGHT // 10
PLANET_X = 0
PLANET_Y = SCREEN_HEIGHT - PLANET_HEIGHT

# Constantes del Jugador
PLAYER_SPEED = 2
PLAYER_START_POS = [SCREEN_WIDTH / 2, SCREEN_HEIGHT - 2 - PLANET_HEIGHT]
PLAYER_DIMENSIONS = [15, 8]

# Constantes de los Aliens
ALIEN_IMAGE_SIZE = [10, 8]

ALIEN_START_POS = [20, 40]
ALIEN_X_SPACING = 5 + ALIEN_IMAGE_SIZE[0]
ALIEN_Y_SPACING = 3 + ALIEN_IMAGE_SIZE[1]
ALIEN_X_SPEED = 0.3
ALIEN_Y_SPEED = 1
ALIEN_MAX_Y = SCREEN_HEIGHT - SCREEN_HEIGHT // 25

# Constantes de la nave nodriza
MOTHERSHIP_SPEED = 0.8
MOTHERSHIP_IMAGE_SIZE = [15, 10]
MOTHERSHIP_Y = ALIEN_START_POS[1] - ALIEN_Y_SPACING

# Constantes del Laser
LASER_DIMENSIONS = [1, 6]
LASER_SPEED = 3

# Constantes de puntuacion y vidas
LIVES_X_START = SCREEN_WIDTH - 15
LIVES_Y = 5
LIVES_SPACE = 3
LIVES_IMG_DIMENSIONS = PLAYER_DIMENSIONS

