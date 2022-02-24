# Rescaling
REESCALADO = 1

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

# Constantes del Jugador
PLAYER_SPEED = 2
PLAYER_START_POS = [SCREEN_WIDTH / 2, SCREEN_HEIGHT - 2]
PLAYER_DIMENSIONS = [15, 8]

# Constantes de los Aliens
ALIEN_IMAGE_SIZE = [10, 8]

ALIEN_START_POS = [20, 30]
ALIEN_X_SPACING = 5 + ALIEN_IMAGE_SIZE[0]
ALIEN_Y_SPACING = 5 + ALIEN_IMAGE_SIZE[1]
ALIEN_X_SPEED = 0.3
ALIEN_Y_SPEED = 1


# Constantes de la nave nodriza
MOTHERSHIP_SPEED = 0.8
MOTHERSHIP_IMAGE_SIZE = [15, 10]
MOTHERSHIP_Y = ALIEN_START_POS[1] - ALIEN_Y_SPACING

# Constantes del Laser
LASER_DIMENSIONS = [1, 6]
LASER_SPEED = 3

# Constantes de puntuacion y vidas
LIVES_X_START = SCREEN_WIDTH - (15 * REESCALADO)
LIVES_Y = 5 * REESCALADO
LIVES_SPACE = 3 * REESCALADO
LIVES_IMG_DIMENSIONS = PLAYER_DIMENSIONS