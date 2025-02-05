import pygame
from hrac import Hrac  
from hrac2 import Hrac2  

# Inicializace pygame
pygame.init()

# Okno
velikost_okna_x = 1280
velikost_okna_y = 720
screen = pygame.display.set_mode((velikost_okna_x, velikost_okna_y))

# Načítání pozadí a masky
zem = pygame.image.load("./zem_textury/pozadi_chozeni_les.png").convert_alpha()
zem_rect = zem.get_rect()
zem_mask = pygame.mask.from_surface(zem)

# Vytvoření povrchu pro masku
mask_surface = pygame.Surface(zem.get_size())
mask_surface.fill((0, 0, 0))
mask_surface.blit(zem, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)

# Načtení textur pro hráče
hrac = Hrac(velikost_okna_x // 2, 0, 120, 80, 5)  
hrac2 = Hrac2(velikost_okna_x / 2, 0, 120, 80, 5)

# FPS limit
clock = pygame.time.Clock()
status = True

while status:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False

    # Pohyb hráče
    klavesa = pygame.key.get_pressed()
    hrac.pohni_se(klavesa, zem_mask)
    hrac2.pohni_se(klavesa, zem_mask)

    # Pohyb po šikmé plošině
    hrac.pohyb_na_sikme_plosine(zem_mask)
    hrac2.pohyb_na_sikme_plosine(zem_mask)

    # Vykreslování
    screen.fill((0, 0, 0))
    screen.blit(mask_surface, (0, 0))  
    hrac.vykresli_se(screen)  
    hrac2.vykresli_se(screen)

    pygame.display.update()

pygame.quit()

  