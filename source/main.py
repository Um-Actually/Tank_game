import pygame

velikost_okna_x=800
velikost_okna_y=600
screen= pygame.display.set_mode((velikost_okna_x, velikost_okna_y))


status=True
while status:
    # vypínání okna
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            status = False
    #barva pozadí + aktulizace pozadí
    screen.fill((255,255,255))
    pygame.display.update()

pygame.quit()