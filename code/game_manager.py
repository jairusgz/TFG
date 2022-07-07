import pygame.sprite

from obstacle import Block
from controller import *
from laser import Laser
from game_parameters import *
from alien import *
from random import choice, randint
from leaderboard_manager import *
import time


class GameManager:
    _instance = None

    # Assures that there is only one instance of the class
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):

        # Status of the game
        self._ai_player = False
        self._pixel_array = None
        self._player_name = 'Unnamed'
        self._level = None
        self._game_status = Game_status.UNINITIALIZED
        self._speed_modifier = None
        self._high_scores = None

        # Player and controller
        self._player_sprite = None
        self._player = None
        self._controller = None

        # Aliens
        self._aliens = pg.sprite.Group()
        self._alien_lasers = pygame.sprite.Group()
        self._alien_direction = None
        self._shoot_count = None
        self._shoot_timer = None

        # Mothership
        self._mothership = pygame.sprite.GroupSingle()
        self._mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)
        self._mothership_count = 0
        self._mothership_score = 70

        # Obstacles
        self._blocks = pg.sprite.Group()

        # Life system
        self._lives = None

        # Score system
        self._score = 0
        self._clipped_reward = 0

        # Audio
        self._music = pg.mixer.Sound('../Resources/space_invaders_theme.wav')
        self._music.set_volume(1)

        self._shoot_sound = pg.mixer.Sound('../Resources/shoot.wav')
        self._shoot_sound.set_volume(0.1)

        self._explosion_sound = pg.mixer.Sound('../Resources/explosion.wav')
        self._explosion_sound.set_volume(0.1)

        self._alien_hit_sound = pg.mixer.Sound('../Resources/invaderkilled.wav')
        self._alien_hit_sound.set_volume(0.1)

        self._mothership_sound = pg.mixer.Sound('../Resources/ufo_lowpitch.wav')
        self._mothership_sound.set_volume(0.1)

        self._game_over_sound = pg.mixer.Sound('../Resources/game_over.wav')
        self._game_over_sound.set_volume(0.8)

    def setup(self, ai_player, player_name='AI', controller=None):

        self._ai_player = ai_player
        if ai_player:
            self._player_name = 'AI'
            if controller:
                self._controller = controller
                self._controller.set_new_episode(self._score)
            elif TRAINING_MODE:
                self._controller = Controller_AI_trainer()
            else:
                self._controller = Controller_AI()

        else:
            self._player_name = player_name.upper()
            self._controller = Controller_Human()

        self._level = 1
        self._speed_modifier = 1
        self._player_sprite = Player(PLAYER_START_POS, PLAYER_DIMENSIONS, PLAYER_SPEED, LASER_SPEED,
                                     LASER_DIMENSIONS, SCREEN_RES)
        self._player = pg.sprite.GroupSingle(self._player_sprite)

        self._controller.set_player(self._player_sprite)

        self.__alien_setup(ALIEN_NUMBER_ROWS, ALIEN_NUMBER_COLUMNS, ALIEN_START_POS, ALIEN_X_SPACING,
                           ALIEN_Y_SPACING)

        self._alien_direction = ALIEN_X_SPEED
        self._shoot_count = 0
        self._shoot_timer = randint(MIN_LASER_CD, MAX_LASER_CD)

        # Mothership
        self._mothership = pygame.sprite.GroupSingle()
        self._mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)
        self._mothership_count = 0
        self._mothership_score = 70

        # Obstacles
        self.__obstacle_setup()

        # Life system
        self._lives = NUM_LIVES

        # Score system
        self._game_status = Game_status.PLAYABLE_SCREEN

        # Score system
        self._score = 0
        self._clipped_reward = 0

        # Audio
        if not TRAINING_MODE:
            self._music.play(-1)

    def read_high_scores(self):
        return LeaderboardManager.read_high_scores()

    def __next_level(self):
        # Advance to next level and adjust speed modifier
        self._level += 1
        self._speed_modifier = 1 + self._level / 10

        # Reset the aliens and the mothership timer and value
        self.__alien_setup(ALIEN_NUMBER_ROWS, ALIEN_NUMBER_COLUMNS, ALIEN_START_POS, ALIEN_X_SPACING,
                           ALIEN_Y_SPACING)
        self.__obstacle_setup()
        self._mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)
        self._mothership_count = 0
        self._mothership_score = 70
        self._alien_direction = ALIEN_X_SPEED * self._speed_modifier
        self._shoot_count = 0

    def run(self, surface):
        if self._game_status == Game_status.PLAYABLE_SCREEN:
            self._controller.action()
            self.__check_collisions()

            self._player.update()
            self._aliens.update(self._alien_direction)
            self.__alien_border_constraint()
            self.__alien_shoot()

            self.__mothership_spawn()
            self._mothership.update()

            self._alien_lasers.update()
            self._clipped_reward -= 0.001
            if self._ai_player:
                self._controller.stack_frame(pg.surfarray.array3d(surface), self._clipped_reward)
                if self._game_status == Game_status.GAME_OVER:
                    self.__final_screen()

    def __create_obstacle(self, x_start, y_start):
        for row_idx, row in enumerate(OBSTACLE_SHAPE):
            for col_idx, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_idx * BLOCK_SIZE
                    y = y_start + row_idx * BLOCK_SIZE
                    block = Block(BLOCK_SIZE, BLOCK_COLOR, x, y)
                    self._blocks.add(block)

    def __obstacle_setup(self):
        self._blocks.empty()
        x_start = OBSTACLE_X_START
        for i in range(NUM_OBSTACLES):
            self.__create_obstacle(x_start, OBSTACLE_Y_START)
            x_start += OBSTACLE_LENGTH + OBSTACLE_SPACE

    def __alien_setup(self, rows, columns, start_pos, x_spacing, y_spacing):
        self._aliens.empty()
        x_coord, y_coord = start_pos
        for r in range(rows):
            for c in range(columns):

                if r < 1:
                    alien = Alien_yellow(ALIEN_IMAGE_SIZE, (x_coord, y_coord))
                elif r < 3:
                    alien = Alien_green(ALIEN_IMAGE_SIZE, (x_coord, y_coord))
                else:
                    alien = Alien_red(ALIEN_IMAGE_SIZE, (x_coord, y_coord))

                self._aliens.add(alien)
                x_coord += x_spacing
            y_coord += y_spacing
            x_coord = start_pos[0]

    def __alien_border_constraint(self):
        aliens = self._aliens.sprites()
        for alien in aliens:
            if alien.rect.right >= SCREEN_WIDTH:
                self._alien_direction = - ALIEN_X_SPEED * self._speed_modifier
                self.__alien_hit_border(ALIEN_Y_SPEED)
            elif alien.rect.left <= 0:
                self._alien_direction = ALIEN_X_SPEED * self._speed_modifier
                self.__alien_hit_border(ALIEN_Y_SPEED)

    def __alien_hit_border(self, y_distance):
        if self._aliens:
            for alien in self._aliens.sprites():
                alien.rect.y += y_distance

    def __alien_shoot(self):
        if self._aliens.sprites():
            if self._shoot_count == self._shoot_timer:
                alien = choice(self._aliens.sprites())
                laser = Laser(alien.rect.center, LASER_SPEED, LASER_DIMENSIONS, SCREEN_HEIGHT)
                self._alien_lasers.add(laser)
                self._shoot_timer = randint(MIN_LASER_CD, MAX_LASER_CD)
                self._shoot_count = 0
                if not TRAINING_MODE:
                    self._shoot_sound.play()

            else:
                self._shoot_count += 1

    def __mothership_spawn(self):
        if self._aliens.sprites():

            if self._mothership_count == self._mothership_cd:
                self._mothership.add(
                    Mothership(MOTHERSHIP_Y, MOTHERSHIP_IMAGE_SIZE, choice(['right', 'left']),
                               MOTHERSHIP_SPEED, SCREEN_RES))
                self._mothership_count = 0
                self._mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)
                if not TRAINING_MODE:
                    self._mothership_sound.play()
            else:
                self._mothership_count += 1

    def __check_collisions(self):

        # Player lasers
        if self._player.sprite.lasers:
            for laser in self._player.sprite.lasers:

                # Collision with aliens
                alien_collisions = pg.sprite.spritecollide(laser, self._aliens, dokill=False)
                if alien_collisions:
                    self._score += alien_collisions[0].value
                    alien_collisions[0].kill()
                    laser.kill()
                    self._speed_modifier *= SPEED_INCREMENT
                    self._clipped_reward += alien_collisions[0].value / 100
                    if self._alien_direction < 0:
                        self._alien_direction = - ALIEN_X_SPEED * self._speed_modifier
                    else:
                        self._alien_direction = ALIEN_X_SPEED * self._speed_modifier

                    if not TRAINING_MODE:
                        self._alien_hit_sound.play()

                    # Advance to next level if all the aliens are killed
                    if not self._aliens:
                        self.__next_level()

                # Collision with Mothership
                if pg.sprite.spritecollide(laser, self._mothership, dokill=True):
                    laser.kill()
                    self._score += self.__calculate_mothership_value()
                    self._clipped_reward += 1

                    if not TRAINING_MODE:
                        self._explosion_sound.play()

                # Collision with Obstacles
                if pg.sprite.spritecollide(laser, self._blocks, dokill=True):
                    laser.kill()

        # Alien lasers
        if self._alien_lasers:
            for laser in self._alien_lasers:

                # Collision with player
                if pg.sprite.spritecollide(laser, self._player, dokill=False):
                    laser.kill()

                    if not TRAINING_MODE:
                        self._explosion_sound.play()

                    if self._lives > 1:
                        self._lives -= 1
                        self._clipped_reward -= 0.3
                    else:
                        if not TRAINING_MODE:
                            self._music.stop()
                            self._game_over_sound.play()
                        self.__final_screen()

                # Collision with obstacles
                if pg.sprite.spritecollide(laser, self._blocks, dokill=True):
                    laser.kill()

                '''
                Collision between lasers:
                The laser shot from the player always gets destroyed when hit by another laser, but the laser 
                from the alien may survive the collision, as said in 
                https://www.classicgaming.cc/classics/space-invaders/play-guide
                '''
                if pg.sprite.spritecollide(laser, self._player.sprite.lasers, dokill=True):
                    if choice([True, False]):
                        laser.kill()

        if self._aliens:
            for alien in self._aliens:

                # Collision with bottom of the screen
                if alien.rect.bottom >= ALIEN_MAX_Y:
                    if TRAINING_MODE:
                        self._game_status = Game_status.GAME_OVER
                    else:
                        self._music.stop()
                        self._game_over_sound.play()
                        self._game_status = Game_status.FINAL_SCREEN

                # Collision with obstacles
                pg.sprite.spritecollide(alien, self._blocks, dokill=True)


    def __calculate_mothership_value(self):
        """
        The score of the mothership is controlled by the number of shots fired by the player before the mothership is
        destroyed. It reaches its max value (300) on the 23rd shot and every 15th shot, according to
        https://www.classicgaming.cc/classics/space-invaders/play-guide
        """

        if self._player_sprite.laser_count <= 23:
            return 70 + self._player_sprite.laser_count * 10
        else:
            return 150 + ((self._player_sprite.laser_count - 23) % 16) * 10

    def __final_screen(self):
        if TRAINING_MODE:
            self.setup(ai_player=True, controller=self._controller)
        else:
            self.__write_high_scores()
            self._game_status = Game_status.FINAL_SCREEN

    def __write_high_scores(self):
        LeaderboardManager.write_high_scores(self._player_name, self._score)

    @property
    def game_status(self):
        return self._game_status

    @property
    def lives(self):
        return self._lives

    @property
    def score(self):
        return self._score

    @property
    def aliens(self):
        return self._aliens

    @property
    def player(self):
        return self._player

    @property
    def mothership(self):
        return self._mothership

    @property
    def alien_lasers(self):
        return self._alien_lasers

    @property
    def obstacles(self):
        return self._blocks

    def set_game_over(self):
        self._game_status = Game_status.GAME_OVER
