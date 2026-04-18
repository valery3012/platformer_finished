import pygame

class Rock:

    def __init__(self, x, y, size, image):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = image

    def draw(self, screen, scroll_x):
        screen.blit(self.image, (self.rect.x - scroll_x, self.rect.y))