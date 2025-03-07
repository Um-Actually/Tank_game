import pygame
import math
from delo_hrac1 import delo

class Hrac():
    def __init__(self, x, y, sirka, vyska, speed, textura, doleva, doprava, nahoru, dolu, textura_delo, strilej_klavesa="SPACE", zmen_naboj_klavesa="r"):
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
        self.zmen_naboj_klavesa = zmen_naboj_klavesa
        self.original_textura = textura
        self.uhel = 0
        self.zdravi = 100
        self.zivy = True

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

        self.rect.clamp_ip(pygame.Rect(0, 0, 1920, 1080))

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
        self.zdravi -= poskozeni
        if self.zdravi <= 0:
            self.zdravi = 0
            self.zivy = False
    
    def aktualizace(self, klavesa, maska, nepratele):
        # Zpracování střelby
        if self.zivy:
            self.delo.strilej(klavesa, self.strilej_klavesa)
            self.delo.zmen_typ_naboje(klavesa, self.zmen_naboj_klavesa)
            
            # Předáme nepřátele pro kontrolu kolizí s projektily
            if nepratele:
                self.delo.update_projektily(maska, nepratele)
            else:
                self.delo.update_projektily(maska, [])

    def vykresli_se(self, screen, maska):
        if self.zivy:
            self.delo.vykresli_se(screen)
            screen.blit(self.image, self.rect)
            
            # Vykreslení ukazatele zdraví
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.rect.width * (self.zdravi / 100), 5))