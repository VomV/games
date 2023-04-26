import sys
import pygame
import random

# Initialize pygame
pygame.init()

# Define game variables
WIDTH = 640
HEIGHT = 480
CELL_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):  
        self.positions = [(WIDTH // 2, HEIGHT // 2)]  # Initial snake position
        self.direction = (0, -CELL_SIZE)  # Initial snake direction (up)
        self.grow = False

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.positions.insert(0, new_head)

        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        dir_x, dir_y = self.direction
        new_dir_x, new_dir_y = new_direction

        # Prevents the snake from moving in the opposite direction
        if (dir_x, dir_y) != (-new_dir_x, -new_dir_y):
            self.direction = new_direction

    def grow_snake(self):
        self.grow = True

    def collides_with_self(self):
        head = self.positions[0]
        return head in self.positions[1:]

    def draw(self, screen):
        for segment in self.positions:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        return (x, y)

    def respawn(self, snake_positions):
        while True:
            self.position = self.generate_position()
            if self.position not in snake_positions:
                break

    def draw(self, screen):
        pygame.draw.rect(screen, RED, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))


class Game:
    def __init__(self, snake, food):
        self.snake = snake
        self.food = food
        self.score = 0
        self.game_over = False

    def update(self):
        self.snake.move()

        # Check if the snake collides with the food
        if self.snake.positions[0] == self.food.position:
            self.snake.grow_snake()
            self.food.respawn(self.snake.positions)
            self.score += 1

        # Check if the snake collides with the screen boundaries
        head_x, head_y = self.snake.positions[0]
        if head_x < 0 or head_y < 0 or head_x >= WIDTH or head_y >= HEIGHT:
            self.game_over = True

        # Check if the snake collides with itself
        if self.snake.collides_with_self():
            self.game_over = True

    def draw(self, screen):
        screen.fill(BLACK)
        self.snake.draw(screen)
        self.food.draw(screen)
        self.draw_score(screen)

    def draw_score(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(text, (10, 10))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.change_direction((0, -CELL_SIZE))
            elif event.key == pygame.K_DOWN:
                self.snake.change_direction((0, CELL_SIZE))
            elif event.key == pygame.K_LEFT:
                self.snake.change_direction((-CELL_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                self.snake.change_direction((CELL_SIZE, 0))


def main():
    snake = Snake()
    food = Food()
    game = Game(snake, food)

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_input(event)

        game.update()
        game.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
