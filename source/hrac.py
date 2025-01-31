import pygame

class Hrac():
    def __init__(self, x, y, sirka, vyska, speed):
        self.speed = speed
        self.rect = pygame.Rect(x, y, sirka, vyska) 
        self.image = pygame.Surface((sirka, vyska))
        self.image.fill((0, 255, 0))
        
        self.velka_y = 0  
        self.na_zemi = False 

    def pohni_se(self, klavesa, maska):
        # Pohyb hráče
        if klavesa[pygame.K_w] and self.na_zemi: 
            self.velka_y = -20  

        if klavesa[pygame.K_s]:
            self.rect.y += self.speed

        if klavesa[pygame.K_a]:
            self.rect.x -= self.speed
        if klavesa[pygame.K_d]:
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

    def vykresli_se(self, screen):
        screen.blit(self.image, self.rect) 
