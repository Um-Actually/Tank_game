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
        self.typy_naboju = ["standardni", "velky", "rychly","smoke"]
        self.index_typu_naboje = 0
        
        # Přidání omezené munice pro každý typ náboje
        self.munice = {"standardni": 7, "velky": 2, "rychly": 10,"smoke":12}
    
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
        self.uhel = max(-20, min(50, self.uhel))
               
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
    
    def nastav_typ_naboje(self, typ_naboje):
        if typ_naboje in self.typy_naboju:
            self.aktualni_typ_naboje = typ_naboje
            self.index_typu_naboje = self.typy_naboju.index(typ_naboje)
            return True
        return False
    
    def prepni_naboj(self, klavesa, klavesy_naboju):

        for typ_naboje, klavesa_pro_naboj in klavesy_naboju.items():
            stisknuto = False
            if len(klavesa_pro_naboj) == 1:
                stisknuto = klavesa[ord(klavesa_pro_naboj)]
            else:
                stisknuto = klavesa[getattr(pygame, f'K_{klavesa_pro_naboj}')]
                
            if stisknuto and typ_naboje in self.typy_naboju:
                self.aktualni_typ_naboje = typ_naboje
                self.index_typu_naboje = self.typy_naboju.index(typ_naboje)
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
 
            if projektil.aktivni:
                for nepritel in nepratele:
                    if nepritel.zivy and projektil.zkontroluj_kolizi_s_hracem(nepritel):
                        nepritel.prijmi_poskozeni(projektil.damage)
                        break  
            
            if not projektil.aktivni or kolize:
                projektily_ke_smazani.append(i)

        for i in sorted(projektily_ke_smazani, reverse=True):
            self.projektily.pop(i)
    def vykresli_se(self, screen):
        screen.blit(self.image, self.rect)
   
    def vykresleni_naboju(self,screen):
        if self.cooldown > 0:
            pygame.draw.rect(screen, (255, 0, 0), (self.x - 20, self.y - 30, 40 * (self.cooldown / self.max_cooldown), 5))
        
        font = pygame.font.SysFont(None, 24)
        typ_text = font.render(f'{self.aktualni_typ_naboje}: {self.munice[self.aktualni_typ_naboje]}', True, (255, 255, 255))
        if self.vpravo:
            screen.blit(typ_text, (self.x - 20, self.y - 40))
        else:
            screen.blit(typ_text, (self.x - 80, self.y - 40))
        for projektil in self.projektily:
            projektil.vykresli_se(screen)