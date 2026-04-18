import pygame

class Window:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Platformer")

    def fill(self):
        self.screen.fill((100, 200, 255))  # небо

    def update(self):
        pygame.display.update()
