import pygame

class Coin:
    def __init__(self, x, y, image):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.image = pygame.transform.scale(image, (30, 30))
        self.collected = False

    def draw(self, screen, scroll_x):
        if not self.collected:
            screen.blit(self.image, (self.rect.x - scroll_x, self.rect.y))