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
        
        # Nastavení vlastností podle typu náboje
        if typ == "standardni":
            self.damage = 20
            self.radius = 5
            self.barva = (255, 0, 0)  
        elif typ == "velky":
            self.damage = 40
            self.radius = 8
            self.barva = (255, 255, 0) 
            self.rychlost= rychlost*0.75
        elif typ == "rychly":
            self.damage = 10
            self.radius = 3
            self.rychlost = rychlost * 1.5
            self.barva = (0, 255, 255)  
        
        # Výpočet počáteční rychlosti ve složkách
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
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravitace
        self.rect.center = (self.x, self.y)
        
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, self.barva, (self.radius, self.radius), self.radius)
        
        if maska.overlap(pygame.mask.from_surface(surface), (self.rect.x, self.rect.y)):
            self.exploduj()
            return True
        if self.x < 0 or self.x > 1920 or self.y < 0 or self.y > 1080:
            self.aktivni = False
            return True
            
        return False
    def exploduj(self):
        # Zde může být kód pro efekt exploze
        self.aktivni = False
    
    def zkontroluj_kolizi_s_hracem(self, hrac):
        if self.rect.colliderect(hrac.rect):
            self.exploduj()
            return True
        return False
    
    def vykresli_se(self, screen):
        pygame.draw.circle(screen, self.barva, (int(self.x), int(self.y)), self.radius)