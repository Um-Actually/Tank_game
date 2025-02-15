import pygame

class delo():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.uhel=0
        self.rotace=1
        self.image=pygame.image.load("tank_A_textury/delo_tank_A_les.png")
        self.image=pygame.transform.scale(self.image, (120, 80))
        self.original_image=self.image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.smer_vpravo=True
    def naklon(self,klavesa):

        # měnění úhlu pro otáčení děla
        if klavesa [pygame.K_w]:
            self.uhel+=self.rotace
        if klavesa [pygame.K_s]:
            self.uhel-=self.rotace
        self.uhel = max(-10, min(70, self.uhel))
        # otáčení děla 
        self.image = pygame.transform.rotate(self.original_image, self.uhel)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def aktulizace_pozice(self,hrac_x,hrac_y):
        self.x = hrac_x
        self.y = hrac_y 
        self.rect.center = (self.x, self.y)

    def vykresli_se(self,screen):
        screen.blit(self.image, self.rect)        