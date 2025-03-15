import pygame
import math
from delo_hrac import delo

class Hrac():
    def __init__(self, x, y, sirka, vyska, speed, textura, doleva, doprava, nahoru, dolu, textura_delo, 
                 strilej_klavesa="SPACE", standardni_klavesa="1", velky_klavesa="2", rychly_klavesa="3",smoke_klavesa="4"):
        self.speed = speed
        self.rect = pygame.Rect(x, y, sirka, vyska)
        self.image = textura
        self.image = pygame.transform.scale(self.image, (sirka, vyska))
        self.sklon = 0.5
        self.velka_y = 0
        self.na_zemi = False
        self.smer_pohybu = 0  
        self.doleva = True
        self.rect = self.image.get_rect(center=(x, y))
        self.textura_delo = textura_delo
        self.delo = delo(x, y, self.textura_delo)
        self.leva = doleva
        self.prava = doprava
        self.nahoru = nahoru
        self.dolu = dolu
        self.strilej_klavesa = strilej_klavesa
        self.standardni_klavesa = standardni_klavesa
        self.velky_klavesa = velky_klavesa
        self.rychly_klavesa = rychly_klavesa
        self.smoke_klavesa=smoke_klavesa
        self.klavesy_naboju = {
            "standardni": self.standardni_klavesa,
            "velky": self.velky_klavesa,
            "rychly": self.rychly_klavesa,
            "smoke": self.smoke_klavesa
        }
        self.original_textura = textura
        self.uhel = 0
        self.zdravi = 100
        self.zivy = True
        
        # Nové atributy pro power-upy
        self.docasne_efekty = {} 
        self.original_speed = speed 
        self.ma_stit = False 
        self.boost_damage = 1.0  

    def pohni_se(self, klavesa, maska):
        if not self.zivy:
            return
            
        #ukládání pozice
        original_x = self.rect.x
        original_y = self.rect.y

        # nastavení směru pohybu
        self.smer_pohybu = 0
        if len(self.leva) == 1:
            if klavesa[ord(self.leva)]: 
                self.smer_pohybu = -1
                self.rect.x -= self.speed
                self.doleva = False
                
            if klavesa[ord(self.prava)]:
                self.smer_pohybu = 1
                self.rect.x += self.speed
                self.image = self.original_textura
                self.doleva = True
        else:
            if klavesa[getattr(pygame, f'K_{self.leva}')]:
                self.smer_pohybu = -1
                self.rect.x -= self.speed
                self.doleva = False
            
            if klavesa[getattr(pygame, f'K_{self.prava}')]:
                self.smer_pohybu = 1
                self.rect.x += self.speed
                self.image = self.original_textura
                self.doleva = True
            
        if not self.doleva:
            self.zrcadleni_tanku = pygame.transform.flip(self.original_textura, True, False)
            self.image = pygame.transform.rotate(self.zrcadleni_tanku, -self.uhel)
        else:
            self.image = pygame.transform.rotate(self.original_textura, self.uhel)

        #kolize se zemí
        if maska.overlap(pygame.mask.from_surface(self.image), (self.rect.x, self.rect.y)):
            test_y = self.rect.y
            for i in range(int(self.speed * 2)): 
                test_y -= 1
                if not maska.overlap(pygame.mask.from_surface(self.image), (self.rect.x, test_y)):
                    self.rect.y = test_y
                    break
            else:
                self.rect.x = original_x 

        if not self.na_zemi:
            self.velka_y += 0.5
        self.rect.y += self.velka_y

        if maska.overlap(pygame.mask.from_surface(self.image), (self.rect.x, self.rect.y)):
            if self.velka_y > 0: 
                while maska.overlap(pygame.mask.from_surface(self.image), (self.rect.x, self.rect.y)):
                    self.rect.y -= 1
                self.na_zemi = True
                self.velka_y = 0
            else: 
                self.rect.y = original_y
                self.velka_y = 0
 
        if self.na_zemi and self.smer_pohybu != 0:
            self.pohyb_na_sikme_plosine(maska)

        test_rect = self.rect.copy()
        test_rect.y += 1
        if not maska.overlap(pygame.mask.from_surface(self.image), (test_rect.x, test_rect.y)):
            self.na_zemi = False

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.width > 1920:
            self.rect.x = 1920 - self.rect.width
        if self.rect.y + self.rect.height > 1080:
            self.rect.y = 1080 - self.rect.height

    def pohyb_na_sikme_plosine(self, maska):
        #testovací bod před hráčem
        test_ahead = self.rect.copy()
        test_ahead.x += self.smer_pohybu * self.speed
        found_surface = False
        
        for y_offset in range(-int(self.speed * 2), int(self.speed * 2)):
            test_ahead.y = self.rect.y + y_offset
            if maska.overlap(pygame.mask.from_surface(self.image), (test_ahead.x, test_ahead.y)):
                target_y = test_ahead.y - 1 
                
                dy = target_y - self.rect.y
                if abs(dy) > self.speed:
                    dy = self.speed if dy > 0 else -self.speed
                
                self.rect.y += dy
                found_surface = True
                break
        
        if not found_surface:
            self.na_zemi = False
    
    def prijmi_poskozeni(self, poskozeni):
        if "shield" in self.docasne_efekty and self.docasne_efekty["shield"].get("aktivni", False):
            poskozeni *= 0.25
        
        self.zdravi -= poskozeni
        if self.zdravi <= 0:
            self.zdravi = 0
            self.zivy = False
    
    def aktualizace(self, klavesa, maska, nepratele):

        if self.zivy:
            puvodni_damage = {}
            if "damage_boost" in self.docasne_efekty and self.docasne_efekty["damage_boost"].get("aktivni", False):
                # Uložení původních hodnot poškození
                for projektil in self.delo.projektily:
                    puvodni_damage[projektil] = projektil.damage
                    projektil.damage *= 1.5  
            
            self.delo.strilej(klavesa, self.strilej_klavesa)
            self.delo.prepni_naboj(klavesa, self.klavesy_naboju)

            if nepratele:
                self.delo.update_projektily(maska, nepratele)
            else:
                self.delo.update_projektily(maska, [])
            
            # Vrácení původních hodnot poškození
            for projektil, damage in puvodni_damage.items():
                projektil.damage = damage
    
    def vykresli_se(self, screen, maska):
        if self.zivy:

            
            #  vykresli efekt štítu
            if "shield" in self.docasne_efekty and self.docasne_efekty["shield"].get("aktivni", False):
                shield_surface = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
                pygame.draw.ellipse(shield_surface, (0, 100, 255, 120), shield_surface.get_rect())
                screen.blit(shield_surface, (self.rect.x - 10, self.rect.y - 10))
            
            

            if "speed" in self.docasne_efekty:                
                speed_surface = pygame.Surface((20, 10), pygame.SRCALPHA)
                
                smer = -1 if self.doleva else 1
                for i in range(3):
                    alpha = 200 - i * 60
                    pygame.draw.rect(speed_surface, (0, 255, 255, alpha), (i * 5, 0, 5, 10))
                
                if smer == -1:
                    speed_surface = pygame.transform.flip(speed_surface, True, False)
                    screen.blit(speed_surface, (self.rect.right, self.rect.centery - 5))
                else:
                    screen.blit(speed_surface, (self.rect.left - 20, self.rect.centery - 5))

            # Vykreslení ukazatele zdraví
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.rect.width * (self.zdravi / 100), 5))
            self.delo.vykresli_se(screen)

            screen.blit(self.image, self.rect)