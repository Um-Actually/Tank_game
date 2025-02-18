import pygame
import math
from hrac import Hrac
from hrac2 import Hrac2

velikost_okna_x = 1280
velikost_okna_y = 720
screen = pygame.display.set_mode((velikost_okna_x, velikost_okna_y))

# Načítání pozadí a masky
zem = pygame.image.load("./zem_textury/pozadi_chozeni_les.png").convert_alpha()
zem_rect = zem.get_rect()
zem_mask = pygame.mask.from_surface(zem)

# Vytvoření hráčů
hrac = Hrac(velikost_okna_x // 2, 0, 120, 80, 5)
hrac2 = Hrac2(velikost_okna_x // 2, 0, 120, 80, 5)

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
    hrac.delo.naklon(klavesa)
    hrac.delo.aktulizace_pozice(hrac.rect.centerx, hrac.rect.centery, not hrac.doleva)
    hrac2.pohni_se(klavesa, zem_mask)

    # Vykreslování
    screen.fill((0, 100, 240))
    screen.blit(zem, (0, 0))
    hrac.delo.vykresli_se(screen)
    hrac.vykresli_se(screen, zem_mask)
    hrac2.vykresli_se(screen, zem_mask)
   
    pygame.display.update()

pygame.quit()