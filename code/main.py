import pygame as pg
import sys
from player import Player
from pygame.locals import *
from controller import *

class Game:
    def __init__(self):
        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGTH - 2), SCREEN_WIDTH, (15, 12))
        self.player = pg.sprite.GroupSingle(player_sprite)
        self.controller = controller = Controller(player_sprite)

    def run(self):
        self.controller.get_input()
        self.player.draw(screen)


if __name__ == '__main__':
    pg.init()

    SCREEN_WIDTH = 160
    SCREEN_HEIGTH = 210
    SCREEN_RES = [SCREEN_WIDTH, SCREEN_HEIGTH]

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


