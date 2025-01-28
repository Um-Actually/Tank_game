import pygame

class Hrac():
    def __init__(self, x, y, sirka, vyska, speed):
        self.speed = speed
        self.rect = pygame.Rect(x, y, sirka, vyska)  # Používáme pygame.Rect pro určení pozice a velikosti
        self.image = pygame.Surface((sirka, vyska))
        self.image.fill((255, 0, 0))  # Červená barva

    def pohni_se(self, klavesa):
        if klavesa[pygame.K_w]:
            self.rect.y -= self.speed
        if klavesa[pygame.K_s]:
            self.rect.y += self.speed

        # Kontrola hranic pro vertikální pohyb
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

        if klavesa[pygame.K_a]:
            self.rect.x -= self.speed
        if klavesa[pygame.K_d]:
            self.rect.x += self.speed

        # Kontrola hranic pro horizontální pohyb
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

    def vykresli_se(self, screen):
        screen.blit(self.image, self.rect)  # Vykreslíme hráče na obrazovku
