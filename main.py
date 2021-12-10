import pygame as pg
import sys
from player import Player
from pygame.locals import *
from controller import *
from laser import Laser
from constants import *

class Game:
    def __init__(self):
        player_sprite = Player(PLAYER_START_POS, (PLAYER_WIDTH, PLAYER_HEIGTH))
        self.player = pg.sprite.GroupSingle(player_sprite)
        self.controller = controller = Controller(player_sprite)

    def run(self):
        self.player.sprite.lasers.draw(screen)
        self.controller.get_input()
        self.player.draw(screen)
        self.player.update()


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


