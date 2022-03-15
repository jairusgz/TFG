import pygame as pg
import pygame as pg
from pygame_menu import Theme
from pygame_menu.widgets import Selector
import pygame_menu

from game import Game
from constants_general import *

ct = None


class GameScreen:
    def __init__(self):
        font = pg.font.Font('../Resources/NES_Font.otf', 20)
        custom_theme = pygame_menu.themes.THEME_DARK.copy()
        custom_theme.title_font = font
        custom_theme.widget_font = font

        self._surface = pg.display.set_mode(MENU_SCREEN_SIZE)
        self._game_manager = Game()

        self._player_name = 'Unnamed'
        self._surface = pg.display.set_mode(MENU_SCREEN_SIZE)
        self._ai_player = False
        self._menu = pygame_menu.Menu(
            width=MENU_SIZE[0],
            height=MENU_SIZE[1],
            theme=custom_theme,
            title='Select Player'
        )

        self._menu.add.text_input('Name: ', onreturn=self.__change_name, default='Unnamed')
        self._menu.add.selector('Player: ', [('Human', False), ('AI', True)], onchange=self.__change_player)
        self._menu.add.button('Leaderboard')
        self._menu.add.button('Play', lambda: self.__run_game())
        self._menu.add.button('Quit', pygame_menu.events.EXIT)

    def run_menu(self):
        self._menu.mainloop(self._surface)

    def __change_player(self, values, selected_value):
        self._ai_player = selected_value

    def __change_name(self, name):
        self._player_name = name

    def __run_game(self):
        self._game_manager.setup(self._ai_player, self._player_name)
        clock = pg.time.Clock()

        while self._game_manager.get_game_status != Game_status.GAME_OVER:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    exit()

            self._surface.fill([30, 30, 30])
            # self._surface.fill([87, 72, 0], rect=(ct.PLANET_X, ct.PLANET_Y, ct.PLANET_WIDTH, ct.PLANET_HEIGHT))
            self._game_manager.run()
            pg.display.flip()
            clock.tick(60)

        pg.display.set_mode(MENU_SCREEN_SIZE)

    def show_score(self):
        score_surf = pg.font.Font('../Resources/NES_Font.otf', ct.SCORE_FONT_SIZE).render('SCORE: ' + str(self._score),
                                                                                          False, 'white')
        score_rect = score_surf.get_rect(topleft=[0, 0])
        self._surface.blit(score_surf, score_rect)


if __name__ == '__main__':
    pg.init()
    while True:
        pg.display.set_caption('Space Invaders')
        gui = GameScreen()
        gui.run_menu()
