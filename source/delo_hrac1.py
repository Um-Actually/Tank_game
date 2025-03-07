import pygame
from munice import Projektil

class delo():
    def __init__(self, x, y, textura):
        #dělo
        self.x = x
        self.y = y
        self.uhel = 0
        self.rotace = 1
        self.image = textura
        self.image = pygame.transform.scale(self.image, (120, 6))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.midleft = (x, y)
        self.vpravo = True
        self.posun = 6
        self.posun2=45
        #střílení
        self.cooldown = 0
        self.max_cooldown = 60 
        self.projektily = []
        self.aktualni_typ_naboje = "standardni"
        self.typy_naboju = ["standardni", "velky", "rychly"]
        self.index_typu_naboje = 0
        
        # Přidání omezené munice pro každý typ náboje
        self.munice = {"standardni": 7, "velky": 2, "rychly": 10}
    
    def naklon(self, klavesa, nahoru_klavesa, dolu_klavesa):
        # naklánění děla
        if len(nahoru_klavesa) == 1:
            if klavesa[ord(nahoru_klavesa)]:
                self.uhel += self.rotace
            if klavesa[ord(dolu_klavesa)]:
                self.uhel -= self.rotace
        else:
            if klavesa[getattr(pygame, f'K_{nahoru_klavesa}')]:
                self.uhel += self.rotace
            if klavesa[getattr(pygame, f'K_{dolu_klavesa}')]:
                self.uhel -= self.rotace
        self.uhel = max(-10, min(50, self.uhel))
               
        # otáčení děla 
        if not self.vpravo:
            self.zrcadleni_dela = pygame.transform.flip(self.original_image, True, False)
            self.image = pygame.transform.rotate(self.zrcadleni_dela, -self.uhel)
            self.rect = self.image.get_rect(midright=(self.x, self.y))
        else:
            self.image = pygame.transform.rotate(self.original_image, self.uhel)
            self.rect = self.image.get_rect(midleft=(self.x, self.y))
    
    def strilej(self, klavesa, strelba_klavesa):
        # Aktualizace cooldownu
        if self.cooldown > 0:
            self.cooldown -= 1
        
        stisknuto = False
        if len(strelba_klavesa) == 1:
            stisknuto = klavesa[ord(strelba_klavesa)]
        else:
            stisknuto = klavesa[getattr(pygame, f'K_{strelba_klavesa}')]
            
        if stisknuto and self.cooldown == 0 and self.munice[self.aktualni_typ_naboje] > 0:
            if self.vpravo:
                pozice_x = self.rect.right
            else:
                pozice_x = self.rect.left
            
            novy_projektil = Projektil(
                pozice_x, 
                self.rect.centery, 
                self.uhel, 
                self.vpravo, 
                17,
                self.aktualni_typ_naboje
            )
            
            self.projektily.append(novy_projektil)
            self.munice[self.aktualni_typ_naboje] -= 1
            self.cooldown = self.max_cooldown
            return True
        return False
    
    def zmen_typ_naboje(self, klavesa, zmena_klavesa):
        stisknuto = False
        if len(zmena_klavesa) == 1:
            stisknuto = klavesa[ord(zmena_klavesa)]
        else:
            stisknuto = klavesa[getattr(pygame, f'K_{zmena_klavesa}')]
            
        if stisknuto and len(self.projektily) == 0:  
            # Změna typu náboje
            self.index_typu_naboje = (self.index_typu_naboje + 1) % len(self.typy_naboju)
            self.aktualni_typ_naboje = self.typy_naboju[self.index_typu_naboje]
            return True
        return False
    
    def aktualizace_pozice(self, hrac_x, hrac_y, smer_vpravo=True):
        if smer_vpravo:
            self.x = hrac_x - self.posun2
        else:
            self.x = hrac_x + self.posun2
        self.y = hrac_y - self.posun
        self.vpravo = smer_vpravo
        if self.vpravo:
            self.rect.midleft = (self.x, self.y)
        else:
            self.rect.midright = (self.x, self.y)
    
    def update_projektily(self, maska, nepratele):
        projektily_ke_smazani = []
        for i, projektil in enumerate(self.projektily):
            kolize = projektil.update(maska)
            for nepritel in nepratele:
                if projektil.zkontroluj_kolizi_s_hracem(nepritel):
                    nepritel.prijmi_poskozeni(projektil.damage)
            if not projektil.aktivni or kolize:
                projektily_ke_smazani.append(i)
        for i in sorted(projektily_ke_smazani, reverse=True):
            self.projektily.pop(i)
    
    def vykresli_se(self, screen):
        # Vykreslení děla
        screen.blit(self.image, self.rect)
        # Vykreslení projektilů
        for projektil in self.projektily:
            projektil.vykresli_se(screen)
        
        if self.cooldown > 0:
            pygame.draw.rect(screen, (255, 0, 0), (self.x - 20, self.y - 30, 40 * (self.cooldown / self.max_cooldown), 5))
        
        font = pygame.font.SysFont(None, 24)
        typ_text = font.render(f'{self.aktualni_typ_naboje}: {self.munice[self.aktualni_typ_naboje]}', True, (255, 255, 255))
        if self.vpravo:
            screen.blit(typ_text, (self.x - 20, self.y - 40))
        else:
            screen.blit(typ_text, (self.x - 80, self.y - 40))
