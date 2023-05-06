import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Princess Dress-Up Game")

# Load images
princess_base = pygame.image.load("princess_base.png")
dress1 = pygame.image.load("dress_1.jpeg")
dress2 = pygame.image.load("dress_2.jpeg")
dress3 = pygame.image.load("dress_3.jpeg")
dresses = [dress1, dress2, dress3]

# Variables
selected_dress = None

def draw():
    screen.fill((255, 255, 255))
    screen.blit(princess_base, (WIDTH // 2 - princess_base.get_width() // 2, HEIGHT // 2 - princess_base.get_height() // 2))
    
    if selected_dress is not None:
        screen.blit(selected_dress, (WIDTH // 2 - selected_dress.get_width() // 2, HEIGHT // 2 - selected_dress.get_height() // 2))
    
    for i, dress in enumerate(dresses):
        screen.blit(dress, (20 + (i * (dress.get_width() + 10)), 20))

    pygame.display.update()

def main():
    global selected_dress

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for i, dress in enumerate(dresses):
                    dress_rect = pygame.Rect(20 + (i * (dress.get_width() + 10)), 20, dress.get_width(), dress.get_height())
                    if dress_rect.collidepoint(mouse_x, mouse_y):
                        selected_dress = dress

        draw()

if __name__ == "__main__":
    main()
