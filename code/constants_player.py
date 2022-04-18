
# Constantes de Pantalla
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 630
SCREEN_RES = [SCREEN_WIDTH, SCREEN_HEIGHT]
SCORE_FONT_SIZE = 30
GAME_OVER_FONT_SIZE = 45
GAME_OVER_CENTER_POS = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
FINAL_SCORE_CENTER_POS = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60]
RETURN_FONT_SIZE = GAME_OVER_FONT_SIZE // 2
RETURN_CENTER_POS = [FINAL_SCORE_CENTER_POS[0], FINAL_SCORE_CENTER_POS[1] + GAME_OVER_FONT_SIZE]

#Planeta
PLANET_WIDTH = SCREEN_WIDTH
PLANET_HEIGHT = SCREEN_HEIGHT // 10
PLANET_X = 0
PLANET_Y = SCREEN_HEIGHT - PLANET_HEIGHT

# Constantes del Jugador
PLAYER_SPEED = 6
PLAYER_START_POS = [SCREEN_WIDTH / 2, SCREEN_HEIGHT - 3 - PLANET_HEIGHT]
PLAYER_DIMENSIONS = [45, 24]

# Constantes de los Aliens
ALIEN_IMAGE_SIZE = [30, 24]
ALIEN_START_POS = [60, 120]
ALIEN_X_SPACING = 15 + ALIEN_IMAGE_SIZE[0]
ALIEN_Y_SPACING = 9 + ALIEN_IMAGE_SIZE[1]
ALIEN_X_SPEED = 0.8
ALIEN_Y_SPEED = 2
ALIEN_MAX_Y = SCREEN_HEIGHT - SCREEN_HEIGHT // 25

# Constantes de la nave nodriza
MOTHERSHIP_SPEED = 2.4
MOTHERSHIP_IMAGE_SIZE = [45, 35]
MOTHERSHIP_Y = ALIEN_START_POS[1] - ALIEN_Y_SPACING

# Constantes del Laser
LASER_DIMENSIONS = [3, 18]
LASER_SPEED = 9

# Constantes de puntuacion y vidas
LIVES_X_START = SCREEN_WIDTH - 45
LIVES_Y = 15
LIVES_SPACE = 9
LIVES_IMG_DIMENSIONS = PLAYER_DIMENSIONS
