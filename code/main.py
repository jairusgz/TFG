import pygame as pg
import sys
import pygame_menu
import pygame.sprite
from pygame_menu import Theme
from pygame_menu.widgets import Selector
from time import sleep

from player import Player
from pygame.locals import *
from controller import *
from laser import Laser
from constants import *
from alien import Alien, Mothership
from random import choice, randint


class Game:
    def __init__(self, ai=False):

        # Status of the game
        self.level = 1
        self.game_status = Game_status.PLAYABLE_SCREEN
        self.speed_modifier = 1
        self.countdown_active = False

        # Player and controller
        self.player_sprite = Player(PLAYER_START_POS, (PLAYER_WIDTH, PLAYER_HEIGTH))
        self.player = pg.sprite.GroupSingle(self.player_sprite)
        self.controller = Controller(self.player_sprite, ai_player=ai)

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
        self.mothership_score = 70

        # Life system
        self.lives = NUM_LIVES
        self.lives_img = pygame.image.load('../Resources/player.png').convert_alpha()
        self.lives_img = pg.transform.scale(self.lives_img, LIVES_IMG_DIMENSIONS)
        self.lives_x_pos = LIVES_X_START

        # Score system
        self.score = 0

    def run(self):
        if self.game_status == Game_status.PLAYABLE_SCREEN:
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
            self.show_score()

        elif self.game_status == Game_status.FINAL_SCREEN:
            self.show_score()
            self.show_final_screen()

    def show_lives(self):
        x = self.lives_x_pos
        for live in range(self.lives - 1):
            x -= (live * LIVES_IMG_DIMENSIONS[0] + LIVES_SPACE)
            screen.blit(self.lives_img, (x, LIVES_Y))

    def show_score(self):
        score_surf = pg.font.Font('../Resources/NES_Font.otf', SCORE_FONT_SIZE).render('SCORE: ' + str(self.score),
                                                                                       False, 'white')
        score_rect = score_surf.get_rect(topleft=[0, 0])
        screen.blit(score_surf, score_rect)

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

                alien = Alien(ALIEN_IMAGE_SIZE, color, x_coord, y_coord, value)
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
                alien_collisions = pg.sprite.spritecollide(laser, self.aliens, dokill=True)
                if alien_collisions:
                    self.score += alien_collisions[0].alien_score()
                    laser.kill()
                    self.speed_modifier = self.speed_modifier * SPEED_INCREMENT

                # Colisiones con la madre nodriza
                if pg.sprite.spritecollide(laser, self.mothership, dokill=True):
                    laser.kill()
                    self.score += self.calculate_mothership_value()

                # TODO Colisiones con los obstaculos

        # Alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pg.sprite.spritecollide(laser, self.player, dokill=False):
                    laser.kill()
                    if self.lives > 1:
                        self.lives -= 1
                    else:
                        self.game_over()

                # TODO Colision con los obstaculos

                # Colision entre laseres.
                # El laser del jugador siempre se borra, y el del alien puede borrarse o continuar
                if pg.sprite.spritecollide(laser, self.player.sprite.lasers, dokill=True):
                    if choice([True, False]):
                        laser.kill()

    def calculate_mothership_value(self):
        '''
        The score of the mothership is controlled by the number of shots fired by the player before the mothership is shot.
        It reaches its max value (300) on the 23rd shot and every 15th shot, according to
        http://www.classicgaming.cc/classics/space-invaders/play-guide
        '''

        if self.player_sprite.get_laser_count() <= 23:
            return 70 + self.player_sprite.get_laser_count() * 10
        else:
            return 150 + ((self.player_sprite.get_laser_count() - 23) % 16) * 10

    def game_over(self):
        # TODO Comprobar la score y añadir a leaderboard si esta en el top
        self.game_status = Game_status.FINAL_SCREEN

    def show_final_screen(self):
        final_surf = pg.font.Font('../Resources/NES_Font.otf', GAME_OVER_FONT_SIZE).render('GAME OVER', False, 'red')
        final_rect = final_surf.get_rect(center=GAME_OVER_CENTER_POS)
        screen.blit(final_surf, final_rect)
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.game_status = Game_status.GAME_OVER


class Menu:

    def __init__(self, surface):
        self.surface = surface
        self.ia_player = False
        self.font = pg.font.Font('../Resources/NES_Font.otf', 20)
        self.custom_theme = pygame_menu.themes.THEME_DARK.copy()
        self.custom_theme.title_font = self.font
        self.custom_theme.widget_font = self.font
        self.menu = pygame_menu.Menu(
            height=300,
            theme=self.custom_theme,
            title='Select Player',
            width=400
        )

        self.menu.add.selector('Player: ', [('Human', False), ('AI', True)], onchange=self.change_player)
        self.menu.add.button('Leaderboard')
        self.menu.add.button('Play', lambda: run_game(surface, Game(self.ia_player)))
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def run(self):
        self.menu.mainloop(self.surface)

    def change_player(self, values, selected_value):
        self.ia_player = selected_value


def run_game(surface, game):
    clock = pg.time.Clock()

    while game.game_status != Game_status.GAME_OVER:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()

        surface.fill([30, 30, 30])
        game.run()
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pg.init()
    while True:
        pg.display.set_caption('Space Invaders')
        screen = pg.display.set_mode(SCREEN_RES, RESIZABLE)
        menu = Menu(screen)

        menu.run()
