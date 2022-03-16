import pygame.sprite

from controller import *
from laser import Laser
from constants_general import *
from alien import Alien, Mothership
from random import choice, randint


class Game:
    def __init__(self):

        # Status of the game
        self._player_name = 'Unnamed'
        self._level = 1
        self._game_status = Game_status.UNINITIALIZED
        self._speed_modifier = 1

        # Player and controller
        self._player_sprite = None
        self._player = None
        self._controller = None

        # Aliens
        self._aliens = None
        self._alien_lasers = None
        self._alien_direction = None
        self._shoot_count = None
        self._shoot_timer = None

        # Mothership
        self._mothership = pygame.sprite.GroupSingle()
        self._mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)
        self._mothership_count = None
        self._mothership_score = None

        # Life system
        self._lives = None

        self._lives_x_pos = None

        # Score system
        self._score = 0

    def setup(self, ai_player, player_name):
        global ct
        if ai_player:
            import constants_ai as ct
            self._player_name = 'AI'
        else:
            import constants_player as ct
            self._player_name = player_name

        self._player_sprite = Player(ct.PLAYER_START_POS, ct.PLAYER_DIMENSIONS, ct.PLAYER_SPEED, ct.LASER_SPEED,
                                     ct.LASER_DIMENSIONS, ct.SCREEN_RES)
        self._player = pg.sprite.GroupSingle(self._player_sprite)
        self._controller = Controller(self._player_sprite, ai_player)
        self._aliens = pg.sprite.Group()
        self._alien_lasers = pygame.sprite.Group()
        self.alien_setup(ALIEN_NUMBER_ROWS, ALIEN_NUMBER_COLUMNS, ct.ALIEN_START_POS, ct.ALIEN_X_SPACING,
                         ct.ALIEN_Y_SPACING)

        self._alien_direction = ct.ALIEN_X_SPEED
        self._shoot_count = 0
        self._shoot_timer = randint(MIN_LASER_CD, MAX_LASER_CD)

        # Mothership
        self._mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)
        self._mothership_count = 0
        self._mothership_score = 70

        # Life system
        self._lives = NUM_LIVES

        # Score system
        self._score = 0

        self._game_status = Game_status.PLAYABLE_SCREEN

    def run(self):
        if self._game_status == Game_status.PLAYABLE_SCREEN:
            self.collisions()

            self._player.update()
            self._aliens.update(self._alien_direction)
            self.alien_border_constraint()
            self.alien_shoot()

            self.mothership_spawn()
            self._mothership.update()

            self._alien_lasers.update()
            self._controller.get_input()

    def alien_setup(self, rows, columns, start_pos, x_spacing, y_spacing):
        x_coord, y_coord = start_pos
        for r in range(rows):
            for c in range(columns):

                if r < 1:
                    color = 'yellow'
                    value = 30
                elif r < 3:
                    color = 'green'
                    value = 20
                else:
                    color = 'red'
                    value = 10

                alien = Alien(ct.ALIEN_IMAGE_SIZE, color, [x_coord, y_coord], value)
                self._aliens.add(alien)
                x_coord += x_spacing
            y_coord += y_spacing
            x_coord = start_pos[0]

    def alien_border_constraint(self):
        aliens = self._aliens.sprites()
        for alien in aliens:
            if alien.rect.right >= ct.SCREEN_WIDTH:
                self._alien_direction = - ct.ALIEN_X_SPEED * self._speed_modifier
                self.alien_hit_border(ct.ALIEN_Y_SPEED)
            elif alien.rect.left <= 0:
                self._alien_direction = ct.ALIEN_X_SPEED * self._speed_modifier
                self.alien_hit_border(ct.ALIEN_Y_SPEED)

    def alien_hit_border(self, y_distance):
        if self._aliens:
            for alien in self._aliens.sprites():
                alien.rect.y += y_distance

    def alien_shoot(self):
        if self._aliens.sprites():
            if self._shoot_count == self._shoot_timer:
                alien = choice(self._aliens.sprites())
                laser = Laser(alien.rect.center, ct.LASER_SPEED, ct.LASER_DIMENSIONS, ct.SCREEN_HEIGHT)
                self._alien_lasers.add(laser)
                self._shoot_timer = randint(MIN_LASER_CD, MAX_LASER_CD)
                self._shoot_count = 0

            else:
                self._shoot_count += 1

    def mothership_spawn(self):
        if self._aliens.sprites():
            if self._mothership_count == self._mothership_cd:
                self._mothership.add(
                    Mothership(ct.MOTHERSHIP_Y, ct.MOTHERSHIP_IMAGE_SIZE, choice(['right', 'left']),
                               ct.MOTHERSHIP_SPEED, ct.SCREEN_RES))
                self._mothership_count = 0
                self._mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)
            else:
                self._mothership_count += 1

    def collisions(self):

        # Player lasers
        if self._player.sprite.lasers:
            for laser in self._player.sprite.lasers:

                # Collision with aliens
                alien_collisions = pg.sprite.spritecollide(laser, self._aliens, dokill=True)
                if alien_collisions:
                    self._score += alien_collisions[0].get_value()
                    laser.kill()
                    self._speed_modifier = self._speed_modifier * SPEED_INCREMENT

                # Collision with Mothership
                if pg.sprite.spritecollide(laser, self._mothership, dokill=True):
                    laser.kill()
                    self._score += self.calculate_mothership_value()

                # TODO Colisiones con los obstaculos

        # Alien lasers
        if self._alien_lasers:
            for laser in self._alien_lasers:
                if pg.sprite.spritecollide(laser, self._player, dokill=False):
                    laser.kill()
                    if self._lives > 1:
                        self._lives -= 1
                    else:
                        self.game_over()

                # TODO Colision con los obstaculos

                # Collision between lasers.
                '''
                The laser shoot from the player always gets destroyed when hit by another laser, but the laser 
                from the alien may shurvive the collision, as said in 
                https://www.classicgaming.cc/classics/space-invaders/play-guide
                '''
                if pg.sprite.spritecollide(laser, self._player.sprite.lasers, dokill=True):
                    if choice([True, False]):
                        laser.kill()

        if self._aliens:
            for alien in self._aliens:
                if alien.rect.bottom >= ct.ALIEN_MAX_Y:
                    self._game_status = Game_status.FINAL_SCREEN

    def calculate_mothership_value(self):
        '''
        The score of the mothership is controlled by the number of shots fired by the player before the mothership is shot.
        It reaches its max value (300) on the 23rd shot and every 15th shot, according to
        http://www.classicgaming.cc/classics/space-invaders/play-guide
        '''

        if self._player_sprite.get_laser_count() <= 23:
            return 70 + self._player_sprite.get_laser_count() * 10
        else:
            return 150 + ((self._player_sprite.get_laser_count() - 23) % 16) * 10

    def game_over(self):
        # TODO Comprobar la score y añadir a leaderboard si esta en el top
        self._game_status = Game_status.FINAL_SCREEN

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
