import pygame
import random
import math
from hrac import Hrac


velikost_okna_x = 1280
velikost_okna_y = 720
screen = pygame.display.set_mode((velikost_okna_x, velikost_okna_y))
pygame.display.set_caption("Tank Battle")

# Klávesy pro ovládání hráčů
left_h1 = "a"
up_h1 = "w"
down_h1 = "s"
right_h1 = "d"
fire_h1 = "SPACE" 
switch_h1 = "e"    

left_h2 = "LEFT"
up_h2 = "UP"
down_h2 = "DOWN"
right_h2 = "RIGHT"
fire_h2 = "KP0"    # Klávesa pro střelbu (numerická klávesnice 0)
switch_h2 = "KP_PERIOD"  # Klávesa pro změnu typu náboje (numerická klávesnice tečka)

# Načítání textur tanků
t_1_les = pygame.image.load("tank_A_textury/Tank_A_les.png")
t_1_poust = pygame.image.load("tank_A_textury/Tank_A_poust.png")
t_1_zima = pygame.image.load("tank_A_textury/Tank_A_zima.png")

t_2_les = pygame.image.load("tank_B_textury/Tank_B_les_zrcadlove.png")
t_2_poust = pygame.image.load("tank_B_textury/Tank_B_poust_zrcadlove.png")
t_2_zima = pygame.image.load("tank_B_textury/Tank_B_zima_zrcadlove.png")

# Načítání textur děl
d_1_les = pygame.image.load("tank_A_textury/delo_tank_A_les.png")
d_1_poust = pygame.image.load("tank_A_textury/delo_tank_A_poust.png")
d_1_zima = pygame.image.load("tank_A_textury/delo_tank_A_zima.png")

d_2_les = pygame.image.load("tank_B_textury/delo_tank_B_les.png")
d_2_poust = pygame.image.load("tank_B_textury/delo_tank_B_poust.png")
d_2_zima = pygame.image.load("tank_B_textury/delo_tank_B_zima.png")

# Náhodný výběr textur pro hráče 1
textura_hrac1 = random.choice([t_1_les, t_1_poust, t_1_zima])
if textura_hrac1 == t_1_les:
    textura_delo1 = d_1_les
elif textura_hrac1 == t_1_poust:
    textura_delo1 = d_1_poust
else:
    textura_delo1 = d_1_zima

# Náhodný výběr textur pro hráče 2
textura_hrac2 = random.choice([t_2_les, t_2_poust, t_2_zima])
if textura_hrac2 == t_2_les:
    textura_delo2 = d_2_les
elif textura_hrac2 == t_2_poust:
    textura_delo2 = d_2_poust
else:
    textura_delo2 = d_2_zima

# Načítání pozadí a masky
zem = pygame.image.load("./zem_textury/zem_chozeni_zima.png").convert_alpha()
zem_rect = zem.get_rect()
zem_mask = pygame.mask.from_surface(zem)

# Vytvoření hráčů
hrac = Hrac(velikost_okna_x // 4, 0, 120, 80, 2, textura_hrac1, left_h1, right_h1, up_h1, down_h1, textura_delo1, fire_h1, switch_h1)
hrac2 = Hrac(velikost_okna_x * 3 // 4, 0, 120, 80, 2, textura_hrac2, left_h2, right_h2, up_h2, down_h2, textura_delo2, fire_h2, switch_h2)

# Inicializace fontu 
pygame.font.init()
font = pygame.font.SysFont(None, 36)

# Stav hry
hra_bezi = True
konec_hry = False
winner = None

clock = pygame.time.Clock()
status = True

while status:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
        elif event.type == pygame.KEYDOWN and konec_hry:
            if event.key == pygame.K_r:
                # Restart hry
                hrac.zdravi = 100
                hrac.zivy = True
                hrac2.zdravi = 100
                hrac2.zivy = True 
                konec_hry = False
                winner = None

    klavesa = pygame.key.get_pressed()
    
    if not konec_hry:
        # Seznam nepřátel pro každého hráče
        nepratele_hrac1 = [hrac2]
        nepratele_hrac2 = [hrac]
        
        # Pohyb a aktualizace hráčů
        hrac.pohni_se(klavesa, zem_mask)
        hrac.delo.naklon(klavesa, up_h1, down_h1)
        hrac.delo.aktulizace_pozice(hrac.rect.centerx, hrac.rect.centery, hrac.doleva)
        hrac.aktualizace(klavesa, zem_mask, nepratele_hrac1)
        
        hrac2.pohni_se(klavesa, zem_mask)
        hrac2.delo.naklon(klavesa, up_h2, down_h2)
        hrac2.delo.aktulizace_pozice(hrac2.rect.centerx, hrac2.rect.centery, hrac2.doleva)
        hrac2.aktualizace(klavesa, zem_mask, nepratele_hrac2)
        
        # Kontrola kolizí projektilů s hráči
        for projektil in hrac.delo.projektily:
            if projektil.zkontroluj_kolizi_s_hracem(hrac2):
                hrac2.prijmi_poskozeni(projektil.damage)
        
        for projektil in hrac2.delo.projektily:
            if projektil.zkontroluj_kolizi_s_hracem(hrac):
                hrac.prijmi_poskozeni(projektil.damage)
        
        # Kontrola konce hry
        if not hrac.zivy:
            konec_hry = True
            winner = "Hráč 2"
        elif not hrac2.zivy:
            konec_hry = True
            winner = "Hráč 1"

    # Vykreslování
    screen.fill((0, 100, 240))
    screen.blit(zem, (0, 0))
    
    # Vykreslení hráčů
    hrac.vykresli_se(screen, zem_mask)
    hrac2.vykresli_se(screen, zem_mask)
    pygame.display.update()