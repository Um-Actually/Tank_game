import pygame
from hrac import Hrac  # Import třídy Hrac ze souboru hrac.py
from hrac2 import Hrac2
# Inicializace pygame
pygame.init()

# Okno
velikost_okna_x = 800
velikost_okna_y = 600
screen = pygame.display.set_mode((velikost_okna_x, velikost_okna_y))

# Načítání pozadí a masky
zem = pygame.image.load("zakrivena_cara_na_zemi.png").convert_alpha()
zem_rect = zem.get_rect()
zem_mask = pygame.mask.from_surface(zem)

# Vytvoření povrchu pro masku
mask_surface = pygame.Surface(zem.get_size())
mask_surface.fill((0, 0, 0))
mask_surface.blit(zem, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)


hrac = Hrac(velikost_okna_x // 2, 0, 50, 50, 5)
hrac2= Hrac2(velikost_okna_x/2, 0, 50, 50, 5)
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
    hrac2.pohni_se(klavesa,zem_mask)

    # vykreslování
    screen.fill((0, 0, 0))
    screen.blit(mask_surface, (0, 0))  
    hrac.vykresli_se(screen)  
    hrac2.vykresli_se(screen)

    pygame.display.update()

pygame.quit()
