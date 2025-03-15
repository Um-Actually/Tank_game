import pygame
import math

class Projektil:
    def __init__(self, x, y, uhel, smer_vpravo, rychlost, typ="standardni"):
        self.x = x
        self.y = y
        self.uhel = uhel
        self.smer_vpravo = smer_vpravo
        self.rychlost = rychlost
        self.typ = typ
        self.aktivni = True
        self.gravitace = 0.5
        
        self.lifetime = None
        self.max_lifetime = None
        
        # Nastavení vlastností podle typu náboje
        if typ == "standardni":
            self.damage = 12
            self.radius = 5
            self.barva = (255, 0, 0)  
            self.pocet =5
        elif typ == "velky":
            self.damage = 25
            self.radius = 7
            self.barva = (255, 255, 0) 
            self.rychlost= rychlost*0.6
        elif typ == "rychly":
            self.damage = 7
            self.radius = 3
            self.rychlost = rychlost * 1.75
            self.barva = (0, 255, 255)  
        elif typ == "smoke":
            self.damage = 0
            self.radius = 200
            self.rychlost = rychlost * 0
            self.barva = (255, 255, 255)
            self.max_lifetime = 60 * 10  
            self.lifetime = 0
            self.gravitace = 0 

        if self.smer_vpravo:
            self.vx = math.cos(math.radians(uhel)) * self.rychlost
            self.vy = -math.sin(math.radians(uhel)) * self.rychlost
            self.x = x-25
        else:
            self.vx = -math.cos(math.radians(uhel)) * self.rychlost
            self.vy = -math.sin(math.radians(uhel)) * self.rychlost
            self.x = x+25
        
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
    
    def update(self, maska):
        if self.typ == "smoke":
            self.lifetime += 1
            if self.lifetime >= self.max_lifetime:
                self.aktivni = False
                return True
        else:
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravitace

            if self.x < 0 or self.x > 1920 or self.y < 0 or self.y > 1080:
                self.aktivni = False
                return True

            self.rect.center = (int(self.x), int(self.y))

            if not hasattr(self, 'collision_surface'):
                self.collision_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(self.collision_surface, self.barva, (self.radius, self.radius), self.radius)
                self.collision_mask = pygame.mask.from_surface(self.collision_surface)

            if maska.overlap(self.collision_mask, (self.rect.x, self.rect.y)):
                self.exploduj()
                return True
        
        return False
    
    def exploduj(self):
        self.aktivni = False
    
    def zkontroluj_kolizi_s_hracem(self, hrac):

        if self.typ == "smoke":
            return False
            
        if self.rect.colliderect(hrac.rect):
            self.exploduj()
            return True
        return False
    
    def vykresli_se(self, screen):
        if self.typ == "smoke" and self.lifetime > self.max_lifetime - 60:
            alpha = 255 * (self.max_lifetime - self.lifetime) // 60
            barva_s_alpha = (self.barva[0], self.barva[1], self.barva[2], alpha)
            
            surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, barva_s_alpha, (self.radius, self.radius), self.radius)
            screen.blit(surface, (int(self.x) - self.radius, int(self.y) - self.radius))
        else:
            pygame.draw.circle(screen, self.barva, (int(self.x), int(self.y)), self.radius)