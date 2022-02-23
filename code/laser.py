import pygame as pg


class Laser(pg.sprite.Sprite):
    def __init__(self, pos, speed, ai=False):

        global ct
        if ai:
            import constants_ai as ct
        else:
            import constants_player as ct

        super().__init__()
        self.image = pg.Surface([ct.LASER_WIDTH, ct.LASER_HEIGHT])
        self.image.fill('White')
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= -20 * ct.REESCALADO or self.rect.y >= ct.SCREEN_HEIGTH + 20 * ct.REESCALADO:
            self.kill()
