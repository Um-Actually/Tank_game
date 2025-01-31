import pygame
import math

class Hrac():
    def __init__(self, x, y, sirka, vyska, speed):
        self.speed = speed
        self.rect = pygame.Rect(x, y, sirka, vyska)
        self.image = pygame.Surface((sirka, vyska))
        self.image.fill((0, 255, 0))
        
        self.velka_y = 0  # Vertikální rychlost (gravitace)
        self.na_zemi = False  # Je hráč na zemi nebo ve vzduchu?
        
    def pohni_se(self, klavesa, maska):
        # Pohyb hráče
        if klavesa[pygame.K_w] and self.na_zemi:
            self.velka_y = -20  # Skok nahoru
        
        if klavesa[pygame.K_s]:
            self.rect.y += self.speed  # Pohyb dolů
        
        if klavesa[pygame.K_a]:
            self.rect.x -= self.speed  # Pohyb vlevo
        
        if klavesa[pygame.K_d]:
            self.rect.x += self.speed  # Pohyb vpravo

        # Simulace gravitace
        self.velka_y += 1
        self.rect.y += self.velka_y
        
        # Kontrola, jestli je hráč na zemi
        self.na_zemi = False

        # Test, zda hráč není ve vzduchu a je na nějaké platformě (maska)
        if maska.overlap(pygame.mask.from_surface(self.image), (self.rect.x, self.rect.y + self.rect.height)):
            self.na_zemi = True
            self.rect.y = (self.rect.y // 50) * 50  # Upravujeme pozici na zemi
            self.velka_y = 0
        
        # Pokud je hráč na šikmé ploše
        if self.na_zemi:
            self.pohyb_na_sikme_plosine(maska)
        
        # Omezení pohybu ve vertikálním směru (aby hráč neprošel skrz zem)
        if self.rect.top < 0:
            self.rect.top = 0
            self.na_zemi = True
        
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.na_zemi = True
        
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.right > 800:
            self.rect.right = 800
    
    def pohyb_na_sikme_plosine(self, maska):

        # Získání pozice hráče
        x, y = self.rect.topleft
        

        if maska.overlap(pygame.mask.from_surface(self.image), (x, y)):
            sklon = 0.5 
            
           
            if sklon > 0:  
              
                self.rect.x += self.speed * math.cos(sklon)
                self.rect.y -= self.speed * math.sin(sklon)
            else:  
                
                self.rect.x += self.speed * math.cos(sklon)
                self.rect.y += self.speed * math.sin(sklon)

            self.rect.y = round(self.rect.y)

    def vykresli_se(self, screen):
        screen.blit(self.image, self.rect)
        
    def vykresli_se(self, screen):
        screen.blit(self.image, self.rect)
