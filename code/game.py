import pygame as pg
import sys

import pygame.sprite
from time import sleep
from player import Player
from pygame.locals import *
from controller import *
from laser import Laser
from constants_general import *
from alien import Alien, Mothership
from random import choice, randint

ct = None


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
        self._controller = Controller()

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
        self._lives_img = pygame.image.load('../Resources/player.png').convert_alpha()
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
        self._controller.set_player(self._player)
        self._controller.set_ai_player(ai_player)
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
        self._lives_img = pg.transform.scale(self._lives_img, ct.LIVES_IMG_DIMENSIONS)
        self._lives_x_pos = ct.LIVES_X_START

        # Score system
        self._score = 0

        self._game_status = Game_status.INITIALIZED

    def run(self):
        if self._game_status == Game_status.PLAYABLE_SCREEN:
            self.collisions()
            self.show_lives()

            self._player.update()
            self._aliens.update(self._alien_direction)
            self.alien_border_constraint()
            self.alien_shoot()

            self.mothership_spawn()
            self._mothership.update()

            self._player.sprite.lasers.draw(self.surface)
            self._alien_lasers.update()
            self._controller.get_input()

            self._player.draw(self.surface)
            self._aliens.draw(self.surface)
            self._alien_lasers.draw(self.surface)
            self._mothership.draw(self.surface)
            self.show_score()

        elif self._game_status == Game_status.FINAL_SCREEN:
            self.show_score()
            self.show_final_screen()

    def show_lives(self):
        x = self._lives_x_pos
        for live in range(self._lives - 1):
            x -= (live * ct.LIVES_IMG_DIMENSIONS[0] + ct.LIVES_SPACE)
            self.surface.blit(self._lives_img, (x, ct.LIVES_Y))

    def show_score(self):
        score_surf = pg.font.Font('../Resources/NES_Font.otf', ct.SCORE_FONT_SIZE).render('SCORE: ' + str(self._score),
                                                                                          False, 'white')
        score_rect = score_surf.get_rect(topleft=[0, 0])
        self.surface.blit(score_surf, score_rect)

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
                        # self.lives -= 1
                        print('Hit')
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

    def show_final_screen(self):
        final_surf = pg.font.Font('../Resources/NES_Font.otf', ct.GAME_OVER_FONT_SIZE).render('GAME OVER', False, 'red')
        final_rect = final_surf.get_rect(center=ct.GAME_OVER_CENTER_POS)
        self.surface.blit(final_surf, final_rect)

        final_surf = pg.font.Font('../Resources/NES_Font.otf', ct.RETURN_FONT_SIZE).render('Press Esc to return', False,
                                                                                           'white')
        final_rect = final_surf.get_rect(center=ct.RETURN_CENTER_POS)
        self.surface.blit(final_surf, final_rect)

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self._game_status = Game_status.GAME_OVER

    @property
    def get_game_status(self):
        return self._game_status
