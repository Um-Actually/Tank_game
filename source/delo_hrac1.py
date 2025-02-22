import pygame

class delo():
    def __init__(self,x,y,textura):
        self.x=x
        self.y=y
        self.uhel=0
        self.rotace=1
        self.image=textura
        self.image=pygame.transform.scale(self.image, (60, 5))
        self.original_image=self.image
        self.rect = self.image.get_rect()
        self.rect.midleft=(x,y)
        self.vpravo=True
        self.posun=6
    

    def naklon(self,klavesa,nahoru_klavesa, dolu_klavesa):
        # naklánění děla
        if len(nahoru_klavesa)==1:
            if klavesa[ord(nahoru_klavesa)]:
                self.uhel += self.rotace
            if klavesa[ord(dolu_klavesa)]:
                self.uhel -= self.rotace
 
        else:
            if klavesa[getattr(pygame,f'K_{nahoru_klavesa}')]:
                self.uhel += self.rotace
                print(self.uhel)
            if klavesa[getattr(pygame,f'K_{dolu_klavesa}')]:
                self.uhel -= self.rotace
                print(self.uhel)
        self.uhel = max(-10, min(70, self.uhel))
               
        # otáčení děla 
        if not self.vpravo:
            self.zrcadleni_dela=pygame.transform.flip(self.original_image, True, False)
            self.image = pygame.transform.rotate(self.zrcadleni_dela, -self.uhel)
            self.rect = self.image.get_rect(midright=(self.x, self.y))
        else:
            self.image = pygame.transform.rotate(self.original_image, self.uhel)
            self.rect = self.image.get_rect(midright=(self.x, self.y))
        
    def aktulizace_pozice(self,hrac_x,hrac_y, smer_vpravo=True):
        self.x = hrac_x
        self.y = hrac_y - self.posun
        self.vpravo = smer_vpravo
        self.rect.center = (self.x, self.y)

    def vykresli_se(self,screen):
        screen.blit(self.image, self.rect)    