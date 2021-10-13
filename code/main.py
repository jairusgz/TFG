import pygame
import sys
from player import Player

class Game:
    def __init__(self):
        player_sprite = Player((100, 100))
        self.player = pygame.sprite.GroupSingle(player_sprite)

    def run(self):
        self.player.draw(screen)


if __name__ == '__main__':
    pygame.init()
    SCREEN_WIDTH = 160
    SCREEN_HEIGTH = 210
    SCREEN_RES = [SCREEN_WIDTH, SCREEN_HEIGTH]

    screen = pygame.display.set_mode(SCREEN_RES)
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill([30, 30, 30])
        game.run()
        pygame.display.flip()
        clock.tick(60)


