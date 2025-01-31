import pygame

# Inicializace Pygame
pygame.init()

# Nastavení okna
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hill Climb Racing - Mapa pomocí masek")

# Barvy
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Třída pro vozidlo
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 30))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.5
        self.lift = -15

    def update(self):
        self.velocity_y += self.gravity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Omezíme pohyb na obrazovce
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.velocity_y = 0
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity_y = 0

    def jump(self):
        self.velocity_y = self.lift

    def move(self, direction):
        if direction == "left":
            self.velocity_x = -5
        elif direction == "right":
            self.velocity_x = 5
        else:
            self.velocity_x = 0

# Třída pro mapu (terén)
class Map(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load("zakrivena_cara_na_zemi.png").convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = screen_height  # mapu umístíme na spodní část obrazovky
        self.mask = pygame.mask.from_surface(self.image)  # Maska pro detekci kolizí

    def update(self):
        # Tato metoda by mohla posouvat mapu, pokud ji chceš pohybovat
        pass

# Hlavní cyklus hry
def main():
    vehicle = Vehicle(100, screen_height - 100)
    terrain_map = Map("map.png")  # Zde vložíš cestu k obrázku s mapou

    all_sprites = pygame.sprite.Group()
    all_sprites.add(vehicle, terrain_map)

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    vehicle.move("left")
                elif event.key == pygame.K_RIGHT:
                    vehicle.move("right")
                elif event.key == pygame.K_SPACE:
                    vehicle.jump()

        # Aktualizace objektů
        all_sprites.update()

        # Detekce kolizí mezi vozidlem a mapou (masky)
        if pygame.sprite.collide_mask(vehicle, terrain_map):
            vehicle.velocity_y = 0
            vehicle.rect.bottom = terrain_map.rect.top

        # Kreslení objektů
        all_sprites.draw(screen)

        # Aktualizace obrazovky
        pygame.display.flip()

        # Ovládání FPS
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
