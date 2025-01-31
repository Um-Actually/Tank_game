import pygame
import math
class Hrac2():
    def __init__(self, x, y, sirka, vyska, speed):
        self.speed = speed
        self.rect = pygame.Rect(x, y, sirka, vyska) 
        self.image = pygame.Surface((sirka, vyska))
        self.image.fill((255, 0, 0))  
        self.velka_y = 0  
        self.na_zemi = False 

    def pohni_se(self, klavesa, maska):
      #pohyb hrac
        if klavesa[pygame.K_UP] and self.na_zemi:  
            self.velka_y = -20 
        if klavesa[pygame.K_DOWN]:
            self.rect.y += self.speed

        if klavesa[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if klavesa[pygame.K_RIGHT]:
            self.rect.x += self.speed


        self.velka_y += 1 
        self.rect.y += self.velka_y  
   
        self.na_zemi = False
       
        if maska.overlap(pygame.mask.from_surface(self.image), (self.rect.x, self.rect.y + self.rect.height)):
            self.na_zemi = True
            self.rect.y = (self.rect.y // 50) * 50  
            self.velka_y = 0 

       
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
