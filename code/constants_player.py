# Constantes Generales
REESCALADO = 3

# Constantes de Pantalla
SCREEN_WIDTH = 160 * REESCALADO
SCREEN_HEIGTH = 210 * REESCALADO
SCREEN_RES = [SCREEN_WIDTH, SCREEN_HEIGTH]
SCORE_FONT_SIZE = 10 * REESCALADO
GAME_OVER_FONT_SIZE = 15 * REESCALADO
GAME_OVER_CENTER_POS = [SCREEN_WIDTH / 2, SCREEN_HEIGTH / 2]
FINAL_SCORE_CENTER_POS = [SCREEN_WIDTH / 2, SCREEN_HEIGTH / 2 + 20 * REESCALADO]
RETURN_FONT_SIZE = GAME_OVER_FONT_SIZE // 2
RETURN_CENTER_POS = [FINAL_SCORE_CENTER_POS[0], FINAL_SCORE_CENTER_POS[1] + GAME_OVER_FONT_SIZE]

# Constantes del Jugador
PLAYER_SPEED = 6
PLAYER_START_POS = [SCREEN_WIDTH / 2, SCREEN_HEIGTH - 6]
PLAYER_DIMENSIONS = [45, 24]

# Constantes de los Aliens
ALIEN_IMAGE_SIZE = [10 * REESCALADO, 8 * REESCALADO]

ALIEN_START_POS = [20 * REESCALADO, 30 * REESCALADO]
ALIEN_X_SPACING = 5 * REESCALADO + ALIEN_IMAGE_SIZE[0]
ALIEN_Y_SPACING = 5 * REESCALADO + ALIEN_IMAGE_SIZE[1]
ALIEN_X_SPEED = 0.3 * REESCALADO
ALIEN_Y_SPEED = 1 * REESCALADO


# Constantes de la nave nodriza
MOTHERSHIP_SPEED = 0.8 * REESCALADO
MOTHERSHIP_IMAGE_SIZE = [15 * REESCALADO, 10 * REESCALADO]
MOTHERSHIP_Y = ALIEN_START_POS[1] - ALIEN_Y_SPACING

# Constantes del Laser
LASER_WIDTH = 1 * REESCALADO
LASER_HEIGHT = 6 * REESCALADO
LASER_SPEED = 3 * REESCALADO

# Constantes de puntuacion y vidas
LIVES_X_START = SCREEN_WIDTH - (15 * REESCALADO)
LIVES_Y = 5 * REESCALADO
LIVES_SPACE = 3 * REESCALADO
LIVES_IMG_DIMENSIONS = PLAYER_DIMENSIONS
