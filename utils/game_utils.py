import os
import pygame


def load_pygame_image(file_name):
    return pygame.transform.scale2x(
        pygame.image.load(
            os.path.join("images", file_name)
        )
    )
