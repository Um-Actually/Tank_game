import pygame
import random
import math

class PowerUp:
    def __init__(self, x, y, typ, trvani=10, textura=None):
        self.x = x
        self.y = y
        self.typ = typ
        self.trvani = trvani  
        self.aktivni = True
        self.sebrany = False
        self.cas_sebrani = 0
        
        self.sirka = 30
        self.vyska = 30
        
        self.rect = pygame.Rect(x - self.sirka//2, y - self.vyska//2, self.sirka, self.vyska)
        
        self.offset_y = 0
        self.animace_smer = 1
        self.animace_rychlost = 0.5
        
        # Nastavení textury nebo výchozí barvy
        self.textura = textura
        self.barva = self.ziskej_barvu_podle_typu()
        
        # Vytvoření surface pro power-up pokud nemá texturu
        if self.textura is None:
            self.surface = pygame.Surface((self.sirka, self.vyska), pygame.SRCALPHA)
    
    def ziskej_barvu_podle_typu(self):
        # Barvy podle typu power-upu
        barvy = {
            "health": (0, 255, 0),         # Zelená pro zdraví
            "ammo": (255, 255, 0),         # Žlutá pro munici
            "speed": (0, 255, 255),        # Azurová pro rychlost
            "shield": (0, 0, 255),         # Modrá pro štít
            "damage": (255, 0, 0),         # Červená pro zvýšení poškození
            "rapid_fire": (255, 165, 0),   # Oranžová pro rychlopalbu
            "jump": (128, 0, 128)          # Fialová pro vysoký skok
        }
        return barvy.get(self.typ, (255, 255, 255))  # Bílá jako výchozí
    
    def update(self, cas):
        if not self.aktivni:
            return False
            
        self.offset_y += self.animace_rychlost * self.animace_smer
        if abs(self.offset_y) > 5:
            self.animace_smer *= -1
            
        self.rect.center = (self.x, self.y + self.offset_y)
        
        if self.sebrany:
            if cas - self.cas_sebrani > self.trvani * 1000:  # Převod na milisekundy
                self.aktivni = False
                return False
        
        return True
        
    def vykresli_se(self, screen):
        if not self.aktivni or self.sebrany:
            return
            
        if self.textura is not None:
            screen.blit(self.textura, self.rect)
        else:
            # Vykreslení základního tvaru podle typu power-upu
            if self.typ == "health":
                # Kříž pro zdraví
                pygame.draw.rect(self.surface, self.barva, (10, 5, 10, 20))
                pygame.draw.rect(self.surface, self.barva, (5, 10, 20, 10))
            elif self.typ == "ammo":
                # Kulka pro munici
                pygame.draw.polygon(self.surface, self.barva, [(15, 5), (25, 15), (15, 25), (5, 15)])
            elif self.typ == "speed":
                # Blesk pro rychlost
                pygame.draw.polygon(self.surface, self.barva, [(15, 5), (20, 13), (25, 10), (15, 25), (10, 17), (5, 20)])
            elif self.typ == "shield":
                # Štít
                pygame.draw.circle(self.surface, self.barva, (15, 15), 12, 3)
            elif self.typ == "damage":
                # Symbol poškození
                pygame.draw.polygon(self.surface, self.barva, [(5, 5), (25, 5), (15, 15), (25, 25), (5, 25), (15, 15)])
            elif self.typ == "rapid_fire":
                # Tři kulky pro rychlopalbu
                for i in range(3):
                    pygame.draw.circle(self.surface, self.barva, (10 + i*5, 15), 3)
            elif self.typ == "jump":
                # Šipka nahoru pro skok
                pygame.draw.polygon(self.surface, self.barva, [(15, 5), (25, 15), (20, 15), (20, 25), (10, 25), (10, 15), (5, 15)])
            else:
                # Výchozí kruh
                pygame.draw.circle(self.surface, self.barva, (15, 15), 10)
                
            screen.blit(self.surface, self.rect)
            
    def kolize_s_hracem(self, hrac):
        if not self.aktivni or self.sebrany:
            return False
            
        if self.rect.colliderect(hrac.rect):
            self.sebrani(hrac)
            return True
        return False
        
    def sebrani(self, hrac):
        self.sebrany = True
        self.cas_sebrani = pygame.time.get_ticks()
        self.aplikuj_efekt(hrac)
    
    def aplikuj_efekt(self, hrac):
        # Aplikace efektu power-upu podle typu
        if self.typ == "health":
            hrac.zdravi = min(100, hrac.zdravi + 30) 
        
        elif self.typ == "ammo":
            # Přidání munice do všech typů nábojů
            for typ_naboje in hrac.delo.munice:
                hrac.delo.munice[typ_naboje] += 1
        
        elif self.typ == "speed":
            hrac.docasne_efekty = hrac.docasne_efekty if hasattr(hrac, 'docasne_efekty') else {}
            hrac.docasne_efekty["speed"] = {
                "puvodni_hodnota": hrac.speed,
                "nova_hodnota": hrac.speed * 1.5,
                "konec": self.cas_sebrani + self.trvani * 1000
            }
            hrac.speed = hrac.docasne_efekty["speed"]["nova_hodnota"]
        
        elif self.typ == "shield":
            # Dočasná nesmrtelnost nebo snížení poškození
            hrac.docasne_efekty = hrac.docasne_efekty if hasattr(hrac, 'docasne_efekty') else {}
            hrac.docasne_efekty["shield"] = {
                "aktivni": True,
                "konec": self.cas_sebrani + self.trvani * 1000
            }
        
        elif self.typ == "damage":
            # Dočasné zvýšení poškození
            hrac.docasne_efekty = hrac.docasne_efekty if hasattr(hrac, 'docasne_efekty') else {}
            hrac.docasne_efekty["damage_boost"] = {
                "aktivni": True,
                "konec": self.cas_sebrani + self.trvani * 1000
            }
        
        elif self.typ == "rapid_fire":
            # Dočasné snížení cooldownu střelby
            hrac.docasne_efekty = hrac.docasne_efekty if hasattr(hrac, 'docasne_efekty') else {}
            hrac.docasne_efekty["rapid_fire"] = {
                "puvodni_hodnota": hrac.delo.max_cooldown,
                "nova_hodnota": hrac.delo.max_cooldown // 2,
                "konec": self.cas_sebrani + self.trvani * 1000
            }
            hrac.delo.max_cooldown = hrac.docasne_efekty["rapid_fire"]["nova_hodnota"]
        
        elif self.typ == "jump":
            if hrac.na_zemi:
                hrac.velka_y = -25
            else:
                hrac.velka_y = -50
            hrac.na_zemi = False
class PowerUpManager:
    def __init__(self, max_power_ups=5, pravdepodobnost_spawnu=0.005, textury=None):
        self.power_ups = []
        self.max_power_ups = max_power_ups
        self.pravdepodobnost_spawnu = pravdepodobnost_spawnu
        self.textury = textury or {} 
        self.typy_power_upů = [
            "health", "ammo", "speed", "shield", 
            "damage", "rapid_fire", "jump"
        ]
        self.cas = 0
        
    def update(self, hraci, maska, velikost_okna_x, velikost_okna_y):
        self.cas = pygame.time.get_ticks()

        self.power_ups = [pu for pu in self.power_ups if pu.update(self.cas)]
        
        # Kontrola kolizí s hráči
        for power_up in self.power_ups:
            for hrac in hraci:
                if hrac.zivy and power_up.kolize_s_hracem(hrac):
                    break 

        if len([pu for pu in self.power_ups if not pu.sebrany]) < self.max_power_ups:
            if random.random() < self.pravdepodobnost_spawnu:
                self.spawn_power_up(maska, velikost_okna_x, velikost_okna_y)
    
    def vykresli_se(self, screen):
        for power_up in self.power_ups:
            power_up.vykresli_se(screen)
    

    def spawn_power_up(self, maska, velikost_okna_x, velikost_okna_y):

        max_pokusy = 5
        for _ in range(max_pokusy):
            x = random.randint(50, velikost_okna_x - 50)
            y = 50  
            typ = random.choice(self.typy_power_upů)
            textura = self.textury.get(typ)

            krok = 10 
            while y < velikost_okna_y - 50:
                if maska.get_at((x, y)):
                    while y > 0 and maska.get_at((x, y-1)):
                        y -= 1
                    break
                y += krok

                if y > velikost_okna_y - 200:
                    krok = 2

            if y < velikost_okna_y - 50:
                power_up = PowerUp(x, y - 20, typ, trvani=random.randint(5, 15), textura=textura)
                self.power_ups.append(power_up)
                return True
        
        return False 
    def aktualizuj_docasne_efekty(self, hraci):
        for hrac in hraci:
            if not hasattr(hrac, 'docasne_efekty'):
                hrac.docasne_efekty = {}
            efekty_ke_smazani = []

            for efekt, data in hrac.docasne_efekty.items():
                if self.cas >= data.get("konec", 0):
                    if efekt == "speed":
                        hrac.speed = data["puvodni_hodnota"]
                    elif efekt == "rapid_fire":
                        hrac.delo.max_cooldown = data["puvodni_hodnota"]
                    
                    efekty_ke_smazani.append(efekt)

            for efekt in efekty_ke_smazani:
                del hrac.docasne_efekty[efekt]
    
    def ma_efekt(self, hrac, efekt):
        if hasattr(hrac, 'docasne_efekty') and efekt in hrac.docasne_efekty:
            return hrac.docasne_efekty[efekt].get("aktivni", False)
        return False
    
    def nacti_textury(self, cesty_k_texturam):
        for typ, cesta in cesty_k_texturam.items():
            try:
                textura = pygame.image.load(cesta).convert_alpha()
                textura = pygame.transform.scale(textura, (30, 30)) 
                self.textury[typ] = textura
            except pygame.error:
                print(f"Nepodařilo se načíst texturu pro power-up typu {typ}: {cesta}")