from utils.game_utils import load_pygame_image


class Ground(object):
    BASE_IMAGE = load_pygame_image("base.png")
    VEL = 5
    WIDTH = BASE_IMAGE.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.BASE_IMAGE, (self.x1, self.y))
        win.blit(self.BASE_IMAGE, (self.x2, self.y))
