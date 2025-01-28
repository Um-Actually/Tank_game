import pygame
from hrac import Hrac

# Inicializace Pygame
pygame.init()

# Okno
velikost_okna_x = 800
velikost_okna_y = 600
screen = pygame.display.set_mode((velikost_okna_x, velikost_okna_y))

# Hráč
rozmer_hrace_x = 50
rozmer_hrace_y = 50
ryclost_hrace = 5
hrac = Hrac(velikost_okna_x / 2, velikost_okna_y / 2, rozmer_hrace_x, rozmer_hrace_y, ryclost_hrace)

# Limit FPS
clock = pygame.time.Clock()

# Načítání obrázku a masky
zem = pygame.image.load("Testovaci_pozadi.png").convert_alpha()
zem_rect = zem.get_rect()
zem_mask = pygame.mask.from_surface(zem)

# Vytvoření povrchu pro masku (bílé části tam, kde je maska)
mask_surface = pygame.Surface(zem.get_size())
mask_surface.fill((0, 0, 0))  # Nastavení černého pozadí

# Převod masky na viditelný formát (bílé části pro neprůhledné oblasti)
for x in range(zem_mask.get_width()):
    for y in range(zem_mask.get_height()):
        if zem_mask.get_at((x, y)):
            mask_surface.set_at((x, y), (255, 255, 255))  # Bílá pro neprůhledné části

status = True
while status:
    clock.tick(60)  # FPS limit

    # Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
    
    # Pohyb hráče
    klavesa = pygame.key.get_pressed()
    hrac.pohni_se(klavesa)        

    # Vyplnění obrazovky černou barvou
    screen.fill((0, 0, 0))

    # Zobrazení masky
    screen.blit(mask_surface, (0, 0))

    # Vykreslení hráče
    hrac.vykresli_se(screen)

    # Aktualizace obrazovky
    pygame.display.update()

pygame.quit()
