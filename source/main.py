import pygame
from hrac import Hrac
#okno
velikost_okna_x = 800
velikost_okna_y = 600
screen = pygame.display.set_mode((velikost_okna_x, velikost_okna_y))

#hrac
rozmer_hrace_x=50
rozmer_hrace_y=50
ryclost_hrace=5

hrac=Hrac(velikost_okna_x/2,velikost_okna_y/2,rozmer_hrace_x,rozmer_hrace_y,ryclost_hrace)
#limit FPS
clock=pygame.time.Clock()
# Načítání obrázku a masky
zem = pygame.image.load("Testovaci_pozadi.png").convert_alpha()
zem_rect = zem.get_rect()
zem_mask = pygame.mask.from_surface(zem)

# Vytvoření povrchu pro masku (bílé části tam, kde je maska)
mask_surface = pygame.Surface(zem.get_size())
mask_surface.fill((0, 0, 0))  # Nastavení černého pozadí
mask_surface.blit(zem, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)

status = True
while status:
    clock.tick(60)
    # Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
    
    #pohyb hráče
    klavesa = pygame.key.get_pressed()
    hrac.pohni_se(klavesa)        

    screen.fill((0, 0, 0))
    screen.blit(mask_surface, (0, 0))
    hrac.vykresli_se(screen)

    pygame.display.update()

pygame.quit()
