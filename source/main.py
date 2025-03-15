import pygame
import random
import math
from hrac import Hrac
from power_upy import PowerUpManager
from delo_hrac import delo
hlavni_smycka=True
velikost_okna_x = 1920
velikost_okna_y = 1080
screen = pygame.display.set_mode((velikost_okna_x, velikost_okna_y))
pygame.display.set_caption("war of tanks")

# Klávesy pro ovládání hráčů
left_h1 = "a"
up_h1 = "w"
down_h1 = "s"
right_h1 = "d"
fire_h1 = "SPACE"        
std_h1 = "1"             
velky_h1 = "2"           
rychly_h1 = "3"        
smoke_h1=  "4"

left_h2 = "LEFT"
up_h2 = "UP"
down_h2 = "DOWN"
right_h2 = "RIGHT"
fire_h2 = "KP0"          
std_h2 = "KP1"           
velky_h2 = "KP2"         
rychly_h2 = "KP3"      
smoke_h2= "KP4"   

exit_=pygame.image.load("tlacitka/exit.png").convert_alpha()
start=pygame.image.load("tlacitka/start.png").convert_alpha()
menu_button=pygame.image.load("tlacitka/menu_button.png").convert_alpha()
menu_pozadi=pygame.image.load("tlacitka/menu_pozadi.png").convert_alpha()
tlacitko_on=pygame.image.load("tlacitka/on.png").convert_alpha()
tlacitko_off=pygame.image.load("tlacitka/off.png").convert_alpha()
tlacitko_tanky_velky=pygame.image.load("tlacitka/tlacitko_tank_velky.png").convert_alpha()
tlacitko_tanky=pygame.image.load("tlacitka/tlacitko_tanky.png").convert_alpha()
tlacitko_les=pygame.image.load("tlacitka/tlacitko_les.png").convert_alpha()
tlacitko_poust=pygame.image.load("tlacitka/tlacitko_poust.png").convert_alpha()
tlacitko_zima=pygame.image.load("tlacitka/tlacitko_zima.png").convert_alpha()
tlacitko_maskovani=tlacitko_off
# Načítání textur tanků
t_1_les = pygame.image.load("tank_A_textury/Tank_A_les.png").convert_alpha()
t_1_poust = pygame.image.load("tank_A_textury/Tank_A_poust.png").convert_alpha()
t_1_zima = pygame.image.load("tank_A_textury/Tank_A_zima.png").convert_alpha()

t_2_les = pygame.image.load("tank_B_textury/Tank_B_les_zrcadlove.png").convert_alpha()
t_2_poust = pygame.image.load("tank_B_textury/Tank_B_poust_zrcadlove.png").convert_alpha()
t_2_zima = pygame.image.load("tank_B_textury/Tank_B_zima_zrcadlove.png").convert_alpha()

# Načítání textur děl
d_1_les = pygame.image.load("tank_A_textury/delo_tank_A_les.png").convert_alpha()
d_1_poust = pygame.image.load("tank_A_textury/delo_tank_A_poust.png").convert_alpha()
d_1_zima = pygame.image.load("tank_A_textury/delo_tank_A_zima.png").convert_alpha()

d_2_les = pygame.image.load("tank_B_textury/delo_tank_B_les.png").convert_alpha()
d_2_poust = pygame.image.load("tank_B_textury/delo_tank_B_poust.png").convert_alpha()
d_2_zima = pygame.image.load("tank_B_textury/delo_tank_B_zima.png").convert_alpha()

zem_les=pygame.image.load("./zem_textury/zem_chozeni_les.png").convert_alpha()
zem_poust=pygame.image.load("./zem_textury/zem_chozeni_poust.png").convert_alpha()
zem_zima=pygame.image.load("./zem_textury/zem_chozeni_zima.png").convert_alpha()

textura_hrac1=t_1_les
textura_hrac2=t_2_les
textura_delo1=d_1_les
textura_delo2=d_2_les
maskovani_1="les"
maskovani_2="les"
pozadi="les"
# Načítání pozadí a masky
zem = zem_les
zem_rect = zem.get_rect()
zem_mask = pygame.mask.from_surface(zem)

pygame.font.init()
font = pygame.font.SysFont(None, 36)

try:

    power_up_textury = {
        "health": "powerup_textury/health.png",
        "ammo": "powerup_textury/ammo.png",
        "speed": "powerup_textury/speed.png",
        "shield": "powerup_textury/shield.png",
        "damage": "powerup_textury/damage.png",
        "rapid_fire": "powerup_textury/rapid_fire.png",
        "jump": "powerup_textury/jump.png"
    }
    power_up_manager = PowerUpManager(max_power_ups=5, pravdepodobnost_spawnu=0.01)
    power_up_manager.nacti_textury(power_up_textury)
except Exception as e:
    print(f"Chyba při načítání power-upů: {e}")

    power_up_manager = PowerUpManager(max_power_ups=5, pravdepodobnost_spawnu=0.01)


tlacitko_1=pygame.Rect((velikost_okna_x/2 - 100, velikost_okna_y/2 - 50, 200, 100))
tlacitko_2=pygame.Rect((velikost_okna_x/2 - 100, velikost_okna_y/2 + 75, 200, 100))
tlacitko_3=pygame.Rect((velikost_okna_x/2 - 100, velikost_okna_y/2 + 200, 200, 100))

hrac1_tlacitko_1=pygame.Rect((0 + 100, velikost_okna_y/2 - 50, 200, 100))
hrac1_tlacitko_2=pygame.Rect((0 + 100, velikost_okna_y/2 + 75, 200, 100))
hrac1_tlacitko_3=pygame.Rect((0 + 100, velikost_okna_y/2 + 200, 200, 100))

hrac2_tlacitko_1=pygame.Rect((velikost_okna_x - 300, velikost_okna_y/2 - 50, 200, 100))
hrac2_tlacitko_2=pygame.Rect((velikost_okna_x - 300, velikost_okna_y/2 + 75, 200, 100))
hrac2_tlacitko_3=pygame.Rect((velikost_okna_x - 300, velikost_okna_y/2 + 200, 200, 100))

mapa_tlacitko_1=pygame.Rect((velikost_okna_x/2-350, 50 , 200, 100))
mapa_tlacitko_2=pygame.Rect((velikost_okna_x/2-100 , 50 , 200, 100))
mapa_tlacitko_3=pygame.Rect((velikost_okna_x/2+150, 50 , 200, 100))
maskovani_tlacitko=pygame.Rect((velikost_okna_x/2-100, velikost_okna_y-200 , 200, 100))
hlavni_smycka=True
maskovani=False


while hlavni_smycka:
    status = False
    menu_skiny=False
    menu=True
    hrac = Hrac(velikost_okna_x // 4, 0, 120, 80, 2, textura_hrac1, 
            left_h1, right_h1, up_h1, down_h1, textura_delo1, 
            fire_h1, std_h1, velky_h1, rychly_h1, smoke_h1)

    hrac2 = Hrac(velikost_okna_x * 3 // 4, 0, 120, 80, 2, textura_hrac2, 
            left_h2, right_h2, up_h2, down_h2, textura_delo2, 
            fire_h2, std_h2, velky_h2, rychly_h2 ,smoke_h2)
    while menu:
        pozice_mys= pygame.mouse.get_pos()
        mys_nad_tlacitkem_1=tlacitko_1.collidepoint(pozice_mys)
        mys_nad_tlacitkem_2=tlacitko_2.collidepoint(pozice_mys)
        mys_nad_tlacitkem_3=tlacitko_3.collidepoint(pozice_mys)

        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                hlavni_smycka = False

            elif udalost.type==pygame.MOUSEBUTTONDOWN:
                if mys_nad_tlacitkem_1:
                    status=True
                    menu=False
                    menu_skiny=False
                elif mys_nad_tlacitkem_2:
                    menu_skiny=True
                    menu=False
                elif mys_nad_tlacitkem_3:
                    status=False
                    menu=False
                    hlavni_smycka = False

        screen.fill((0, 255, 255))
        screen.blit(menu_pozadi,(0,0))
        screen.blit(exit_,(velikost_okna_x/2 - 100, velikost_okna_y/2 + 200, 200, 100))
        screen.blit(start,(velikost_okna_x/2 - 100, velikost_okna_y/2 - 50))
        screen.blit(menu_button,(velikost_okna_x/2 - 100, velikost_okna_y/2 + 75, 200, 100))
        pygame.display.flip()

    while menu_skiny:
        pozice_mys= pygame.mouse.get_pos()
        hrac1_mys_nad_tlacitkem_1=hrac1_tlacitko_1.collidepoint(pozice_mys)
        hrac1_mys_nad_tlacitkem_2=hrac1_tlacitko_2.collidepoint(pozice_mys)
        hrac1_mys_nad_tlacitkem_3=hrac1_tlacitko_3.collidepoint(pozice_mys)

        hrac2_mys_nad_tlacitkem_1=hrac2_tlacitko_1.collidepoint(pozice_mys)
        hrac2_mys_nad_tlacitkem_2=hrac2_tlacitko_2.collidepoint(pozice_mys)
        hrac2_mys_nad_tlacitkem_3=hrac2_tlacitko_3.collidepoint(pozice_mys)

        mapa_mys_nad_tlacitkem_1=mapa_tlacitko_1.collidepoint(pozice_mys)
        mapa_mys_nad_tlacitkem_2=mapa_tlacitko_2.collidepoint(pozice_mys)
        mapa_mys_nad_tlacitkem_3=mapa_tlacitko_3.collidepoint(pozice_mys)

        maskovani_mys_nad_tlacitkem=maskovani_tlacitko.collidepoint(pozice_mys)

        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                menu = False
            elif udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_ESCAPE:
                    menu_skiny=False
                    menu = True
                    status=False

            elif udalost.type==pygame.MOUSEBUTTONDOWN:
                if hrac1_mys_nad_tlacitkem_1:
                    textura_hrac1=t_1_les
                    textura_delo1=d_1_les
                    maskovani_1="les"
                elif hrac1_mys_nad_tlacitkem_2:
                    textura_hrac1=t_1_poust
                    textura_delo1=d_1_poust
                    maskovani_1="poust"
                elif hrac1_mys_nad_tlacitkem_3:
                    textura_hrac1=t_1_zima
                    textura_delo1=d_1_zima
                    maskovani_1="zima"
                elif hrac2_mys_nad_tlacitkem_1:
                    textura_hrac2=t_2_les
                    textura_delo2=d_2_les
                    maskovani_2="les"
                elif hrac2_mys_nad_tlacitkem_2:
                    textura_hrac2=t_2_poust
                    textura_delo2=d_2_poust
                    maskovani_2="poust"
                elif hrac2_mys_nad_tlacitkem_3:
                    textura_hrac2=t_2_zima
                    textura_delo2=d_2_zima
                    maskovani_2="zima"
                elif mapa_mys_nad_tlacitkem_1:
                    zem=zem_les
                    pozadi="les"
                elif mapa_mys_nad_tlacitkem_2:
                    zem=zem_poust
                    pozadi="poust"
                elif mapa_mys_nad_tlacitkem_3:
                    zem=zem_zima
                    pozadi="zima"
                elif maskovani_mys_nad_tlacitkem:
                    if maskovani==False:
                        maskovani=True
                        tlacitko_maskovani=tlacitko_on
                    else:
                        maskovani=False
                        tlacitko_maskovani=tlacitko_off

        screen.fill((0, 255, 255))
        screen.blit(zem,(0,0))
        screen.blit(tlacitko_les,(velikost_okna_x/2+150, 50))
        screen.blit(tlacitko_poust,(velikost_okna_x/2-100 , 50))
        screen.blit(tlacitko_zima,(velikost_okna_x/2-350, 50))

        screen.blit(tlacitko_maskovani,(velikost_okna_x/2-100, velikost_okna_y-200 ))
        screen.blit(tlacitko_tanky,(velikost_okna_x - 300, velikost_okna_y/2 - 50))
        screen.blit(tlacitko_tanky,(velikost_okna_x - 300, velikost_okna_y/2 + 75))
        screen.blit(tlacitko_tanky,(velikost_okna_x - 300, velikost_okna_y/2 + 200))

        screen.blit(pygame.transform.flip(d_2_les, True, False),(velikost_okna_x - 273, velikost_okna_y/2 - 15, 200, 100))
        screen.blit(pygame.transform.flip(d_2_poust, True, False),(velikost_okna_x - 273, velikost_okna_y/2 + 110, 200, 100))
        screen.blit(pygame.transform.flip(d_2_zima, True, False),(velikost_okna_x - 273, velikost_okna_y/2 + 235, 200, 100))
        screen.blit(pygame.transform.flip(t_2_les, True, False),(velikost_okna_x - 273, velikost_okna_y/2 - 45, 200, 100))
        screen.blit(pygame.transform.flip(t_2_poust, True, False),(velikost_okna_x - 273, velikost_okna_y/2 + 80, 200, 100))
        screen.blit(pygame.transform.flip(t_2_zima, True, False),(velikost_okna_x - 273, velikost_okna_y/2 + 205, 200, 100))
        
        screen.blit(tlacitko_tanky,(100, velikost_okna_y/2 - 50, 200, 100))
        screen.blit(tlacitko_tanky,(0 + 100, velikost_okna_y/2 + 75, 200, 100))
        screen.blit(tlacitko_tanky,(0 + 100, velikost_okna_y/2 + 200, 200, 100))
    
        screen.blit(d_1_les, (0 + 145, velikost_okna_y / 2 - 3))
        screen.blit(d_1_poust, (0 + 145, velikost_okna_y / 2 + 117))
        screen.blit(d_1_zima, (0 + 145, velikost_okna_y / 2 + 242))
        screen.blit(t_1_les, (0 + 145, velikost_okna_y / 2 - 35))
        screen.blit(t_1_poust, (0 + 145, velikost_okna_y / 2 + 90))
        screen.blit(t_1_zima, (0 + 145, velikost_okna_y / 2 + 215))

        screen.blit(tlacitko_tanky_velky, (velikost_okna_x/2 -650, velikost_okna_y/2 -15))
        screen.blit(pygame.transform.scale(textura_delo1, (320, 18)),(velikost_okna_x/2 -630, velikost_okna_y/2 +92, 320, 280))
        screen.blit(pygame.transform.scale(textura_hrac1, (320, 280)),(velikost_okna_x/2 -650, velikost_okna_y/2 -12, 320, 280))

        screen.blit(tlacitko_tanky_velky, (velikost_okna_x/2 + 300, velikost_okna_y/2 -15, 350, 280))
        screen.blit(pygame.transform.scale((pygame.transform.flip(textura_delo2, True, False)), (320, 18)),(velikost_okna_x/2 + 310, velikost_okna_y/2 +92, 320, 280))
        screen.blit(pygame.transform.scale((pygame.transform.flip(textura_hrac2, True, False)), (320, 280)),(velikost_okna_x/2 + 330, velikost_okna_y/2 -15, 320, 280))


        pygame.display.flip()


    hrac = Hrac(velikost_okna_x // 4, 0, 120, 80, 2, textura_hrac1, 
            left_h1, right_h1, up_h1, down_h1, textura_delo1, 
            fire_h1, std_h1, velky_h1, rychly_h1, smoke_h1)

    hrac2 = Hrac(velikost_okna_x * 3 // 4, 0, 120, 80, 2, textura_hrac2, 
            left_h2, right_h2, up_h2, down_h2, textura_delo2, 
            fire_h2, std_h2, velky_h2, rychly_h2 ,smoke_h2)

    zem_rect = zem.get_rect()
    zem_mask = pygame.mask.from_surface(zem)

    konec_hry = False
    winner = None
    clock = pygame.time.Clock()

    while status:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = True
                    menu_skiny=False
                    status=False
                    power_up_manager.power_ups = []
                if konec_hry:
                    if event.key == pygame.K_r:
                        # Restart hry
                        hrac.zdravi = 100
                        hrac.zivy = True
                        hrac.docasne_efekty = {} 
                        hrac.speed = hrac.original_speed
                        hrac.delo.munice={"standardni": 7, "velky": 2, "rychly": 10,"smoke":12}
                        
                        hrac2.zdravi = 100
                        hrac2.zivy = True 
                        hrac2.docasne_efekty = {}  
                        hrac2.speed = hrac2.original_speed
                        hrac2.delo.munice={"standardni": 7, "velky": 2, "rychly": 10,"smoke":12}
                        power_up_manager.power_ups = []
                        
                        konec_hry = False
                        winner = None


        klavesa = pygame.key.get_pressed()
        
        if not konec_hry:
            # Seznam nepřátel pro každého hráče
            nepratele_hrac1 = [hrac2]
            nepratele_hrac2 = [hrac]
            
            # Aktualizace power-upů
            power_up_manager.update([hrac, hrac2], zem_mask, velikost_okna_x, velikost_okna_y)
            power_up_manager.aktualizuj_docasne_efekty([hrac, hrac2])
            
            # Pohyb a aktualizace hráčů
            hrac.pohni_se(klavesa, zem_mask)
            hrac.delo.naklon(klavesa, up_h1, down_h1)
            hrac.delo.aktualizace_pozice(hrac.rect.centerx, hrac.rect.centery, hrac.doleva)
            hrac.aktualizace(klavesa, zem_mask, nepratele_hrac1)
            
            hrac2.pohni_se(klavesa, zem_mask)
            hrac2.delo.naklon(klavesa, up_h2, down_h2)
            hrac2.delo.aktualizace_pozice(hrac2.rect.centerx, hrac2.rect.centery, hrac2.doleva)
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
        
        # Vykreslení power-upů
        power_up_manager.vykresli_se(screen)
        if maskovani:
            if maskovani_1==pozadi:
                if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_SPACE]:
                    hrac.vykresli_se(screen, zem_mask)
                    hrac.delo.vykresleni_naboju(screen)
            else:
                hrac.vykresli_se(screen, zem_mask)
                hrac.delo.vykresleni_naboju(screen)
            if maskovani_2==pozadi:        
                if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_KP0]:
                    hrac2.vykresli_se(screen, zem_mask)

            else:
                hrac2.vykresli_se(screen, zem_mask)

            hrac2.delo.vykresleni_naboju(screen)
            hrac.delo.vykresleni_naboju(screen)
        if  maskovani==False:   
            hrac.vykresli_se(screen, zem_mask)
            hrac2.vykresli_se(screen, zem_mask)
            hrac.delo.vykresleni_naboju(screen)
            hrac2.delo.vykresleni_naboju(screen)
        # Vykreslení informací o vítězi
        if konec_hry:
            win_text = font.render(f'Vítěz: {winner}', True, (255, 255, 255))
            restart_text = font.render('Stiskni R pro restart', True, (255, 255, 255))
            screen.blit(win_text, (velikost_okna_x // 2 - 150, 50))
            screen.blit(restart_text, (velikost_okna_x // 2 - 150, 100))
        screen.blit(zem, (0, 0))
            
        pygame.display.flip()
    