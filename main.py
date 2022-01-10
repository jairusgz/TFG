import pygame as pg
import sys

import pygame.sprite

from player import Player
from pygame.locals import *
from controller import *
from laser import Laser
from constants import *
from alien import Alien, Mothership
from random import choice, randint


class Game:
    def __init__(self):
        # Jugador y controlador para el juador y la IA
        player_sprite = Player(PLAYER_START_POS, (PLAYER_WIDTH, PLAYER_HEIGTH))
        self.player = pg.sprite.GroupSingle(player_sprite)
        self.controller = controller = Controller(player_sprite)


        self.speed_modifier = 1

        # Aliens
        self.aliens = pg.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(ALIEN_NUMBER_ROWS, ALIEN_NUMBER_COLUMNS, ALIEN_START_POS, ALIEN_X_SPACING, ALIEN_Y_SPACING)
        self.alien_direction = ALIEN_X_SPEED
        self.shoot_count = 0
        self.shoot_timer = randint(MIN_LASER_CD, MAX_LASER_CD)

        # Mothership
        self.mothership = pygame.sprite.GroupSingle()
        self.mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)
        self.mothership_count = 0

    def run(self):
        self.speed_modifier += SPEED_INCREMENT

        self.collisions()

        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_border_constraint()
        self.alien_shoot()

        self.mothership_spawn()
        self.mothership.update()

        self.player.sprite.lasers.draw(screen)
        self.alien_lasers.update()
        self.controller.get_input()

        self.player.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.mothership.draw(screen)


    def alien_setup(self, rows, columns, start_pos, x_spacing, y_spacing):
        x_coord, y_coord = start_pos
        for r in range(rows):
            for c in range(columns):

                if r < 1:
                    color = 'yellow'
                elif r < 3:
                    color = 'green'
                else:
                    color = 'red'

                alien = Alien(ALIEN_IMAGE_SIZE, color, x_coord, y_coord)
                self.aliens.add(alien)
                x_coord += x_spacing
            y_coord += y_spacing
            x_coord = start_pos[0]

    def alien_border_constraint(self):
        aliens = self.aliens.sprites()
        for alien in aliens:
            if alien.rect.right >= SCREEN_WIDTH:
                self.alien_direction = - ALIEN_X_SPEED * self.speed_modifier
                self.alien_hit_border(ALIEN_Y_SPEED)
            elif alien.rect.left <= 0:
                self.alien_direction = ALIEN_X_SPEED * self.speed_modifier
                self.alien_hit_border(ALIEN_Y_SPEED)

    def alien_hit_border(self, y_distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += y_distance

    def alien_shoot(self):
        if self.aliens.sprites():
            if self.shoot_count == self.shoot_timer:
                alien = choice(self.aliens.sprites())
                laser = Laser(alien.rect.center, LASER_SPEED)
                self.alien_lasers.add(laser)
                self.shoot_timer = randint(round(MIN_LASER_CD / self.speed_modifier),
                                           round(MAX_LASER_CD / self.speed_modifier))
                self.shoot_count = 0

            else:
                self.shoot_count += 1

    def mothership_spawn(self):
        if self.aliens.sprites():
            if self.mothership_count == self.mothership_cd:
                self.mothership.add(Mothership(MOTHERSHIP_IMAGE_SIZE, choice(['right', 'left']), MOTHERSHIP_SPEED))
                self.mothership_count = 0
                self.mothership_cd = randint(MOTHERSHIP_MIN_CD, MOTHERSHIP_MAX_CD)
            else:
                self.mothership_count += 1

    def collisions(self):

        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pg.sprite.spritecollide(laser, self.aliens, dokill=True):
                    laser.kill()

                if pg.sprite.spritecollide(laser, self.mothership, dokill=True):
                    laser.kill()

        # Alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pg.sprite.spritecollide(laser, self.player, dokill=False):
                    laser.kill()
                    print('Player hit')


if __name__ == '__main__':
    pg.init()

    screen = pg.display.set_mode(SCREEN_RES, RESIZABLE)
    clock = pg.time.Clock()
    game = Game()

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()

        screen.fill([30, 30, 30])
        game.run()
        pg.display.flip()
        clock.tick(60)
