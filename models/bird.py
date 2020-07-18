import pygame

from utils.game_utils import load_pygame_image


class Bird(object):
    BIRD_IMGS = [load_pygame_image(f"bird{indx}.png") for indx in range(1, 4)]
    ROT_VEL = 20
    MAX_ROTATION = 25
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = self.y
        self.tick_count = 0
        self.tilt = 0
        self.vel = 0
        self.img = self.BIRD_IMGS[0]
        self.img_count = 0

    def jump(self):
        self.vel = - 10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # For downward acceleration
        disp = self.tick_count * self.vel + 1.5 * self.tick_count ** 2
        if disp >= 16:  # Terminal Velocity
            disp = 16

        if disp < 0:
            disp -= 2

        self.y += disp
        if disp < 0 or self.y < self.height + 50:  # Tilt Up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:                                      # Tilt Down
            if self.tilt >= -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.BIRD_IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.BIRD_IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.BIRD_IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.BIRD_IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.BIRD_IMGS[0]
            self.img_count = 0

        # When nose diving, Birds image should remain constant
        if self.tilt <= - 80:
            self.img = self.BIRD_IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Tilt the bird
        self.blit_rotate_center(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    @staticmethod
    def blit_rotate_center(win, img, coords, tilt):
        rotated_image = pygame.transform.rotate(img, tilt)
        new_rect = rotated_image.get_rect(
            center=img.get_rect(topleft=coords).center
        )
        win.blit(rotated_image, new_rect.topleft)
