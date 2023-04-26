import sys
import pygame
import random

# Initialize pygame
pygame.init()

# Define game variables
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Mario Game")
clock = pygame.time.Clock()

background_image_path = 'mario_backg.png'


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("mario.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, HEIGHT - 150  # Initial position
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_y = 1  # Gravity
        self.on_ground = False

    def update(self, platforms):
        self.handle_input()
        self.velocity_y += self.acceleration_y
        self.rect.y += self.velocity_y

        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.velocity_y > 0:
                self.rect.y = platform.rect.y - self.rect.height
                self.velocity_y = 0
                self.on_ground = True

        self.rect.x += self.velocity_x

        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.velocity_x > 0:
                self.rect.x = platform.rect.x - self.rect.width
            elif self.velocity_x < 0:
                self.rect.x = platform.rect.x + platform.rect.width

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.velocity_x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = 5
        else:
            self.velocity_x = 0

        if keys[pygame.K_UP] and self.on_ground:
            self.velocity_y = -24
            self.on_ground = False

class Background:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert()
        self.image_width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.image_width

    def update(self, player_velocity_x):
        if player_velocity_x < 0:
            # Scroll to the right when Mario moves to the left
            speed = -player_velocity_x
            self.x1 += speed
            self.x2 += speed
        elif player_velocity_x > 0:
            # Scroll to the left when Mario moves to the right
            speed = player_velocity_x
            self.x1 -= speed
            self.x2 -= speed

        if self.x1 <= -self.image_width:
            self.x1 = self.image_width

        if self.x2 <= -self.image_width:
            self.x2 = self.image_width

        if self.x1 >= self.image_width:
            self.x1 = -self.image_width

        if self.x2 >= self.image_width:
            self.x2 = -self.image_width

    def draw(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))  # Fill with red color for visibility
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player_velocity_x):
        self.rect.x -= player_velocity_x

        # Check if the obstacle is off the screen and reposition it
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH + random.randint(100, 300)
            self.rect.y = random.randint(HEIGHT // 2, HEIGHT - 150)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 128, 0))  # Fill with green color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        self.running = True
        self.game_over = False

    def update(self, player):
        if player.rect.y > HEIGHT:
            self.game_over = True
            self.running = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def reset(self):
        self.running = True
        self.game_over = False


def main():
    # Create instances of Player, Platform, and Game classes
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    platforms = pygame.sprite.Group()
    ground = Platform(0, HEIGHT - 50, WIDTH, 50)
    platform1 = Platform(200, 300, 150, 20)
    platform2 = Platform(400, 200, 150, 20)
    platforms.add(ground, platform1, platform2)


    bg = Background(background_image_path)  # Adjust speed as needed


    game = Game()

    obstacles = pygame.sprite.Group()
    for i in range(3):  # Create 3 obstacles
        obstacle = Obstacle(WIDTH + i * 200, random.randint(HEIGHT // 2, HEIGHT - 150), 50, 50)
        obstacles.add(obstacle)

    # Create the game loop
    while game.running:
        # Handle events
        game.handle_input()

        # Update the game state
        player.update(platforms)
        game.update(player)
        bg.update(player.velocity_x)
        obstacles.update(player.velocity_x)  # Update obstacles

        # Render the game
        bg.draw(screen)
        all_sprites.draw(screen)
        platforms.draw(screen)
        obstacles.draw(screen)  # Draw obstacles
        pygame.display.flip()
        clock.tick(FPS)




    if game.game_over:
        print("Game over!")

if __name__ == "__main__":
    main()



