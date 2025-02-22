import pygame
import random
import math
from hrac import Hrac


velikost_okna_x = 1280
velikost_okna_y = 720
screen = pygame.display.set_mode((velikost_okna_x, velikost_okna_y))

left_h1="a"
up_h1="w"
down_h1="s"
right_h1="d"

left_h2="LEFT"
up_h2="UP"
down_h2="DOWN"
right_h2="RIGHT"

t_1_les=pygame.image.load("tank_A_textury/Tank_A_les.png")
t_1_poust=pygame.image.load("tank_A_textury/Tank_A_poust.png")
t_1_zima=pygame.image.load("tank_A_textury/Tank_A_zima.png")

t_2_les=("tank_B_textury/Tank_B_les.png")
t_2_poust=("tank_B_textury/Tank_B_poust.png")
t_2_zima=("tank_B_textury/Tank_B_zima.png")
# Načítání pozadí a masky
zem = pygame.image.load("./zem_textury/pozadi_chozeni_les.png").convert_alpha()
zem_rect = zem.get_rect()
zem_mask = pygame.mask.from_surface(zem)

# Vytvoření hráčů
hrac = Hrac(velikost_okna_x // 2, 0, 120, 80, 5,(random.choice([t_1_les,t_1_poust,t_1_zima])),left_h1,right_h1,up_h1,down_h1)
hrac2 = Hrac(velikost_okna_x // 2, 0, 120, 80, 5,(random.choice([t_1_les,t_1_poust,t_1_zima])),left_h2,right_h2,up_h2,down_h2)

clock = pygame.time.Clock()
status = True

while status:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False

    # Aktualizace hráčů
    klavesa = pygame.key.get_pressed()
    hrac.pohni_se(klavesa, zem_mask)
    hrac.delo.naklon(klavesa, up_h1, down_h1)
    hrac.delo.aktulizace_pozice(hrac.rect.centerx, hrac.rect.centery, hrac.doleva)

    hrac2.pohni_se(klavesa, zem_mask)
    hrac2.delo.naklon(klavesa, up_h2, down_h2)
    hrac2.delo.aktulizace_pozice(hrac2.rect.centerx, hrac2.rect.centery, hrac2.doleva)

    # Vykreslování
    screen.fill((0, 100, 240))
    screen.blit(zem, (0, 0))
    hrac.delo.vykresli_se(screen)
    hrac.vykresli_se(screen, zem_mask)
    hrac2.vykresli_se(screen, zem_mask)
   
    pygame.display.update()

pygame.quit()