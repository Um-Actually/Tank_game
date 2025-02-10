import pygame
import math


class Hrac2():
    def __init__(self, x, y, sirka, vyska, speed):
        self.speed = speed
        self.rect = pygame.Rect(x, y, sirka, vyska)
        self.image = pygame.image.load("tank_B_textury/Tank_B_les.png")
        self.image = pygame.transform.scale(self.image, (sirka, vyska))
        self.sklon = 0.5
        self.velka_y = 0
        self.na_zemi = False
        self.smer_pohybu = 0  

    def pohni_se(self, klavesa, maska):
        #ukládání pozice
        original_x = self.rect.x
        original_y = self.rect.y

        # nastavení směru pohybu
        self.smer_pohybu = 0
        if klavesa[pygame.K_LEFT]:
            self.smer_pohybu = -1
            self.rect.x -= self.speed
            self.image = pygame.image.load("tank_B_textury/Tank_B_les.png")
        if klavesa[pygame.K_RIGHT]:
            self.smer_pohybu = 1
            self.rect.x += self.speed
            self.image = pygame.image.load("tank_B_textury/Tank_B_les_zrcadlove.png")
       #kolize se zemí
        if maska.overlap(pygame.mask.from_surface(self.image), (self.rect.x, self.rect.y)):
            test_y = self.rect.y
            # hledání cesty aby mohl na horu
            for i in range(int(self.speed * 2)): 
                test_y -= 1
                if not maska.overlap(pygame.mask.from_surface(self.image), (self.rect.x, test_y)):
                    self.rect.y = test_y
                    break
            else:
                self.rect.x = original_x   #když nenajde vrátí se zpět
       
        # gravitace když není na zemi
        if not self.na_zemi:
            self.velka_y += 0.5
        self.rect.y += self.velka_y
        #kontrola kolize při pádu
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

        self.rect.clamp_ip(pygame.Rect(0, 0, 1280, 720))

    def pohyb_na_sikme_plosine(self, maska):
        #testovací bod před hráčem
        test_ahead = self.rect.copy()
        test_ahead.x += self.smer_pohybu * self.speed
        found_surface = False
        #hledá povrch nad nebo pod hráčem
        for y_offset in range(-int(self.speed * 2), int(self.speed * 2)):
            test_ahead.y = self.rect.y + y_offset
            if maska.overlap(pygame.mask.from_surface(self.image), (test_ahead.x, test_ahead.y)):
                target_y = test_ahead.y - 1 
                #plynulí přechod na novou výšku
                dy = target_y - self.rect.y
                if abs(dy) > self.speed:
                    dy = self.speed if dy > 0 else -self.speed
                
                self.rect.y += dy
                found_surface = True
                break
        
        if not found_surface:
            self.na_zemi = False

    def vykresli_se(self, screen, maska):
        screen.blit(self.image, self.rect)