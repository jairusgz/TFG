import pygame.sprite
import pandas as pd
from player import Player
from controller import *
from laser import Laser
from game_parameters import *
from alien import *
from random import choice, randint


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

        # Life system
        self._lives = None

        # Score system
        self._score = 0

    def setup(self, ai_player, player_name, controller=None):

        self._ai_player = ai_player
        if ai_player:
            self._player_name = 'AI'
            if controller:
                self._controller = controller
                self._controller.set_new_episode()
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

        self._high_scores = pd.read_csv('../Data/high_scores.csv')

        self._alien_direction = ALIEN_X_SPEED
        self._shoot_count = 0
        self._shoot_timer = randint(MIN_LASER_CD, MAX_LASER_CD)

        # Mothership
        self._mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)

        # Life system
        self._lives = NUM_LIVES

        # Score system
        self._game_status = Game_status.PLAYABLE_SCREEN

        # Score system
        self._score = 0

    def __next_level(self):
        # Advance to next level and adjust speed modifier
        self._level += 1
        self._speed_modifier = 1 + self._level / 10

        # Reset the aliens and the mothership timer and value
        self.__alien_setup(ALIEN_NUMBER_ROWS, ALIEN_NUMBER_COLUMNS, ALIEN_START_POS, ALIEN_X_SPACING,
                           ALIEN_Y_SPACING)
        self._mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)
        self._mothership_count = 0
        self._mothership_score = 70
        self._alien_direction = ALIEN_X_SPEED * self._speed_modifier
        self._shoot_count = 0

    def run(self, surface):
        if self._game_status == Game_status.PLAYABLE_SCREEN:
            if self._ai_player and TRAINING_MODE:
                self._controller.stack_frame(pg.surfarray.array3d(surface), self._score)
            self.__check_collisions()

            self._player.update()
            self._aliens.update(self._alien_direction)
            self.__alien_border_constraint()
            self.__alien_shoot()

            self.__mothership_spawn()
            self._mothership.update()

            self._alien_lasers.update()

            self._controller.action()

    def __alien_setup(self, rows, columns, start_pos, x_spacing, y_spacing):
        self._aliens.empty()
        x_coord, y_coord = start_pos
        for r in range(rows):
            for c in range(columns):

                if r < 1:
                    alien = Alien_red(ALIEN_IMAGE_SIZE, (x_coord, y_coord))
                elif r < 3:
                    alien = Alien_green(ALIEN_IMAGE_SIZE, (x_coord, y_coord))
                else:
                    alien = Alien_yellow(ALIEN_IMAGE_SIZE, (x_coord, y_coord))

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
            else:
                self._mothership_count += 1

    def __check_collisions(self):

        # Player lasers
        if self._player.sprite.lasers:
            for laser in self._player.sprite.lasers:

                # Collision with aliens
                alien_collisions = pg.sprite.spritecollide(laser, self._aliens, dokill=True)
                if alien_collisions:
                    self._score += alien_collisions[0].value
                    laser.kill()
                    self._speed_modifier *= SPEED_INCREMENT
                    if self._alien_direction < 0:
                        self._alien_direction = - ALIEN_X_SPEED * self._speed_modifier
                    else:
                        self._alien_direction = ALIEN_X_SPEED * self._speed_modifier

                    # Advance to next level if all the aliens are killed
                    if not self._aliens:
                        self.__next_level()

                # Collision with Mothership
                if pg.sprite.spritecollide(laser, self._mothership, dokill=True):
                    laser.kill()
                    self._score += self.__calculate_mothership_value()

                # TODO Colisiones con los obstaculos

        # Alien lasers
        if self._alien_lasers:
            for laser in self._alien_lasers:
                if pg.sprite.spritecollide(laser, self._player, dokill=False):
                    laser.kill()
                    if self._lives > 1:
                        self._lives -= 1
                    else:
                        self.__final_screen()

                # TODO Colision con los obstaculos

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
                if alien.rect.bottom >= ALIEN_MAX_Y:
                    if self._ai_player and TRAINING_MODE:
                        self.__final_screen()
                    else:
                        self._game_status = Game_status.FINAL_SCREEN

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
        if self._ai_player and TRAINING_MODE:
            self.setup(ai_player=True, controller=self._controller)
        else:
            self.__write_high_scores()
            self._game_status = Game_status.FINAL_SCREEN

    def __write_high_scores(self):
        self._high_scores = self._high_scores.append({'Player_name': self._player_name, 'Score': self._score},
                                                     ignore_index=True)
        top_10 = self._high_scores.sort_values(by=['Score'], ascending=False)[:3]
        top_10.to_csv('../Data/high_scores.csv', index=False)

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

    def set_game_over(self):
        self._game_status = Game_status.GAME_OVER
