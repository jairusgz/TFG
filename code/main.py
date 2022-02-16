import pygame as pg
import sys
import pygame_menu
import pygame.sprite
from pygame_menu import Theme

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
        self.player_sprite = Player(PLAYER_START_POS, (PLAYER_WIDTH, PLAYER_HEIGTH))
        self.player = pg.sprite.GroupSingle(self.player_sprite)
        self.controller = Controller(self.player_sprite)

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

        # Sistema de vidas
        self.lives = NUM_LIVES
        self.lives_img = pygame.image.load('../Resources/player.png').convert_alpha()
        self.lives_img = pg.transform.scale(self.lives_img, LIVES_IMG_DIMENSIONS)
        self.lives_x_pos = LIVES_X_START

    def set_player(self, player, player_value):
        self.controller = Controller(self.player_sprite, player_value)

    def run(self):
        # self.speed_modifier += SPEED_INCREMENT

        self.collisions()
        self.show_lives()

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

    def show_lives(self):
        x = self.lives_x_pos
        for live in range(self.lives - 1):
            x -= (live * LIVES_IMG_DIMENSIONS[0] + LIVES_SPACE)
            screen.blit(self.lives_img, (x, LIVES_Y))

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
                self.shoot_timer = randint(MIN_LASER_CD, MAX_LASER_CD)
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

                # Colisiones con los aliens
                if pg.sprite.spritecollide(laser, self.aliens, dokill=True):
                    laser.kill()
                    self.speed_modifier = self.speed_modifier * SPEED_INCREMENT
                    print(self.speed_modifier)

                # Colisiones con la madre nodriza
                if pg.sprite.spritecollide(laser, self.mothership, dokill=True):
                    laser.kill()

                # TODO Colisiones con los obstaculos

        # Alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:

                # TODO Modificar la colision con el jugador cuando este implementado el sistema de vidas
                if pg.sprite.spritecollide(laser, self.player, dokill=False):
                    laser.kill()
                    self.lives -= 1

                # TODO Colision con los obstaculos

                # Colision entre laseres.
                # El laser del jugador siempre se borra, y el del alien puede borrarse o continuar
                if pg.sprite.spritecollide(laser, self.player.sprite.lasers, dokill=True):
                    if choice([True, False]):
                        laser.kill()

def run_game(surface, game):
    clock = pg.time.Clock()

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()

        surface.fill([30, 30, 30])
        game.run()
        pg.display.flip()
        clock.tick(60)

def run_menu(surface, game):
    font = pg.font.Font('../Resources/NES_Font.otf', 20)
    custom_theme = pygame_menu.themes.THEME_DARK.copy()
    custom_theme.title_font = font
    custom_theme.widget_font = font

    menu = pygame_menu.Menu(
        height=300,
        theme=custom_theme,
        title='Select Player',
        width=400
    )

    menu.add.selector('Player: ', [('Human', False), ('AI', True)], onchange=game.set_player)
    menu.add.button('Leaderboard')
    menu.add.button('Play', lambda: run_game(surface, game))
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Space Invaders')
    screen = pg.display.set_mode(SCREEN_RES, RESIZABLE)
    game = Game()

    run_menu(screen, game)
