import pygame
import math

class Hrac():
    def __init__(self, x, y, sirka, vyska, speed):
        self.speed = speed
        self.rect = pygame.Rect(x, y, sirka, vyska)
        self.image = pygame.image.load("tank_A_textury/tank_A_les.png")  # Načítání textury hráče
        self.image = pygame.transform.scale(self.image, (sirka, vyska))  # Přizpůsobení velikosti obrázku
        
        self.velka_y = 0  # Vertikální rychlost (gravitace)
        self.na_zemi = False  
        
    def pohni_se(self, klavesa, maska):
        # Pohyb hráče
        if klavesa[pygame.K_s]:
            self.rect.y += self.speed  
        
        if klavesa[pygame.K_a]:
            self.rect.x -= self.speed  
        
        if klavesa[pygame.K_d]:
            self.rect.x += self.speed  

        # Simulace gravitace
        self.velka_y += 1
        self.rect.y += self.velka_y
        
        self.na_zemi = False

        # Test, zda hráč není ve vzduchu 
        if maska.overlap(pygame.mask.from_surface(self.image), (self.rect.x, self.rect.y + self.rect.height)):
            self.na_zemi = True
            self.rect.y = (self.rect.y // 5) *5 # Upravujeme pozici na zemi################
            self.velka_y = 0
        

        if self.na_zemi:
            self.pohyb_na_sikme_plosine(maska)
        
        # Omezení by hráč neprošel skrz zem
        if self.rect.top < 0:
            self.rect.top = 0
            self.na_zemi = True
        
        if self.rect.bottom > 720:
            self.rect.bottom = 720
            self.na_zemi = True
        
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.right > 1280:
            self.rect.right = 1280
    
    def pohyb_na_sikme_plosine(self, maska):
        # Získání pozice hráče
        x, y = self.rect.topleft

        if maska.overlap(pygame.mask.from_surface(self.image), (x, y)):
            sklon = 0.5  # Sklon šikmé plochy
            
            if sklon > 0:  
                self.rect.x += self.speed * math.cos(sklon)
                self.rect.y -= self.speed * math.sin(sklon)
            else:  
                self.rect.x += self.speed * math.cos(sklon)
                self.rect.y += self.speed * math.sin(sklon)

            self.rect.y = round(self.rect.y)

    def vykresli_se(self, screen):
        screen.blit(self.image, self.rect)
