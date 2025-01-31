import pygame
import math

# Inicializace pygame
pygame.init()

# Velikost obrázku
velikost_okna_x = 800
velikost_okna_y = 600

# Vytvoření průhledného povrchu
obrazek_surface = pygame.Surface((velikost_okna_x, velikost_okna_y), pygame.SRCALPHA)
obrazek_surface.fill((0, 0, 0, 0))  # Nastavení pozadí na průhledné

# Parametry zakřivené čáry (polokruh)
start_angle = 0
end_angle = math.pi  # Polovina kruhu
radius = 300
center_x = velikost_okna_x //2 
center_y = velikost_okna_y - 1  # Posunuto dolů (blízko spodní části okna)

# Kreslení zakřivené čáry (polokruh) na zemi (spodní část okna)
pygame.draw.arc(obrazek_surface, (255, 255, 255), 
                (center_x - radius, center_y - radius, 2 * radius, 2 * radius), 
                start_angle, end_angle, 5)

# Uložení povrchu jako PNG obrázku s průhledným pozadím
pygame.image.save(obrazek_surface, "zakrivena_cara_na_zemi.png")

# Ukončení pygame
pygame.quit()
