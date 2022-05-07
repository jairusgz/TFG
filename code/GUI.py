import pygame as pg
import pygame_menu
import os
from game_manager import GameManager
from game_parameters import *
from leaderboard_manager import LeaderboardManager


class GameScreen:
    def __init__(self):
        font = pg.font.Font('../Resources/NES_Font.otf', 20)
        custom_theme = pygame_menu.themes.THEME_DARK.copy()
        custom_theme.title_font = font
        custom_theme.widget_font = font

        # Surface and Game Manager
        self._surface = pg.display.set_mode(MENU_SCREEN_SIZE)
        self._leaderboard_manager = LeaderboardManager()
        self._game_manager = GameManager(self._leaderboard_manager)
        self._leaderboard_screen = False

        # Player image, displayed at the top right as the number of lives
        self._lives_img = pg.image.load('../Resources/player.png').convert_alpha()

        # Game parameters
        self._player_name = 'Unnamed'
        self._ai_player = False

        # Menu setup
        self._menu = pygame_menu.Menu(
            width=MENU_SIZE[0],
            height=MENU_SIZE[1],
            theme=custom_theme,
            title='Select Player'
        )

        # Add widgets and handlers to the menu
        self._menu.add.text_input('Name: ', onchange=self.__change_name, default='Unnamed')
        self._menu.add.selector('Player: ', [('Human', False), ('AI', True)], onchange=self.__change_player)
        self._menu.add.button('Leaderboard', lambda: self.__run_leaderboard())
        self._menu.add.button('Play', lambda: self.__run_game())
        self._menu.add.button('Quit', pygame_menu.events.EXIT)

    # Start the program by starting the mainloop from the menu
    def run(self):
        if TRAINING_MODE:
            self._ai_player = True
            self._player_name = 'AI'
            self.__run_game()
            os.environ['SDL_VIDEODRIVER'] = 'dummy'
        else:
            self._menu.mainloop(self._surface)

    # Change player type, called from the selector widget when the value is changed
    def __change_player(self, values, selected_value):
        self._ai_player = selected_value

    # Change player name, called from the text input of the menu
    def __change_name(self, name):
        self._player_name = name

    # Setup the game manager and import the constants for the player or the AI
    def __setup_game(self):

        self._game_manager.setup(self._ai_player, self._player_name)
        self._lives_img = pg.transform.scale(self._lives_img, LIVES_IMG_DIMENSIONS)

    # Show the score on the top-left corner of the screen
    def __show_score(self):
        score_surf = pg.font.Font('../Resources/NES_Font.otf', SCORE_FONT_SIZE).render(
                                  'SCORE: ' + str(self._game_manager.score), False, 'white')

        score_rect = score_surf.get_rect(topleft=[0, 0])
        self._surface.blit(score_surf, score_rect)

    # Show the lives on the top-right corner of the screen
    def __show_lives(self):
        x = LIVES_X_START
        for live in range(self._game_manager.lives - 1):
            x -= (live * LIVES_IMG_DIMENSIONS[0] + LIVES_SPACE)
            self._surface.blit(self._lives_img, (x, LIVES_Y))

    # Draw all the objects of the game
    def __draw_sprites(self):
        self._game_manager.aliens.draw(self._surface)
        self._game_manager.alien_lasers.draw(self._surface)
        self._game_manager.mothership.draw(self._surface)
        self._game_manager.player.sprite.lasers.draw(self._surface)
        self._game_manager.player.draw(self._surface)

    # Show the final screen and wait for the user to press ESC to return to the menu
    def __show_final_screen(self):
        final_surf = pg.font.Font('../Resources/NES_Font.otf', GAME_OVER_FONT_SIZE).render('GAME OVER', False, 'red')
        final_rect = final_surf.get_rect(center=GAME_OVER_CENTER_POS)
        self._surface.blit(final_surf, final_rect)

        final_surf = pg.font.Font('../Resources/NES_Font.otf', RETURN_FONT_SIZE).render('Press Esc to return', False,
                                                                                           'white')
        final_rect = final_surf.get_rect(center=RETURN_CENTER_POS)
        self._surface.blit(final_surf, final_rect)

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self._game_manager.set_game_over()

    def __show_leaderboard(self):
        leaderboard_title_surf = pg.font.Font('../Resources/NES_Font.otf', LEADERBOARD_TITLE_FONT_SIZE).render\
                                             ('Leaderboard', False, 'white')
        leaderboard_title_rect = leaderboard_title_surf.get_rect(center=LEADERBOARD_TITLE_CENTER_POS)
        self._surface.blit(leaderboard_title_surf, leaderboard_title_rect)

        leaderboard_data = self._leaderboard_manager.read_high_scores()
        center_pos = LEADERBOARD_CENTER_POS[0], LEADERBOARD_CENTER_POS[1] - 40

        for i, d in enumerate(leaderboard_data.iterrows()):
            data = f'{d[1][0]} {d[1][1]}'
            surface = pg.font.Font('../Resources/NES_Font.otf', LEADERBOARD_FONT_SIZE).render(data, False, 'white')
            rect = surface.get_rect(center=center_pos)
            center_pos = center_pos[0], center_pos[1] + 40

            self._surface.blit(surface, rect)

        keys = pg.key.get_pressed()
        print(keys[pg.K_ESCAPE])
        if keys[pg.K_ESCAPE]:
            self._leaderboard_screen = False

    def __run_leaderboard(self):
        clock = pg.time.Clock()
        self._leaderboard_screen = True
        while self._leaderboard_screen:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    exit()

            self._surface.fill([30, 30, 30])
            self.__show_leaderboard()
            pg.display.flip()
            clock.tick(FPS)

        pg.display.set_mode(MENU_SCREEN_SIZE)


    # Setup a new game and start it
    def __run_game(self):
        """
        Main loop of the program. It setups a new game and start it until the status changes to GAME_OVER
        Each iteration of the loop, it calls the run function of the game manager that updates the sprites and handles
        collisions, timers, lasers... and then print the updated sprites on the screen.

        If the game status changes to FINAL_SCREEN, it calls the method show_final_screen that shows the final screen
        and waits for the player to press ESC to return to the menu.
        """
        self.__setup_game()
        clock = pg.time.Clock()
        while self._game_manager.game_status != Game_status.GAME_OVER:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    exit()

            self._surface.fill([30, 30, 30])
            if self._game_manager.game_status == Game_status.FINAL_SCREEN:
                self.__show_final_screen()
            else:
                self._surface.fill([87, 72, 0], rect=(PLANET_X, PLANET_Y, PLANET_WIDTH, PLANET_HEIGHT))
                self._game_manager.run(self._surface)
                self.__draw_sprites()
                self.__show_lives()
            self.__show_score()
            pg.display.flip()
            clock.tick(FPS)

        pg.display.set_mode(MENU_SCREEN_SIZE)


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Space Invaders')
    gui = GameScreen()
    gui.run()
