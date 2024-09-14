import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker')

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)

BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE]  # Different colors for each row
ROW_POINTS = [50, 40, 30, 20, 10]  # Points for each row, higher for rows at the top

# Set up paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 12

# Set up ball
BALL_RADIUS = 10
BALL_SPEED_X = 4
BALL_SPEED_Y = -6  # Increased speed for more responsive gameplay

# Set up bricks
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 50
BRICK_OFFSET_LEFT = 35

# Set up font
FONT = pygame.font.SysFont('Arial', 24)
BIG_FONT = pygame.font.SysFont('Arial', 48)

# Define the paddle class
class Paddle:
    def __init__(self):
        self.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
        self.speed = PADDLE_SPEED

    def move(self, direction):
        if direction == 'left' and self.x > 0:
            self.x -= self.speed
        if direction == 'right' and self.x < SCREEN_WIDTH - PADDLE_WIDTH:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Define the ball class
class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = BALL_RADIUS
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.radius * 2:
            self.speed_x *= -1
        if self.y <= 0:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

    def collide_with_paddle(self, paddle):
        if self.y + self.radius >= paddle.y and paddle.x <= self.x <= paddle.x + PADDLE_WIDTH:
            hit_pos = (self.x - paddle.x) / PADDLE_WIDTH
            self.speed_x = BALL_SPEED_X * (hit_pos - 0.5) * 2  # Adjust speed based on hit position
            self.speed_y *= -1

    def collide_with_brick(self, brick):
        if brick.x <= self.x <= brick.x + BRICK_WIDTH and brick.y <= self.y <= brick.y + BRICK_HEIGHT:
            return True
        return False

# Define the brick class
class Brick:
    def __init__(self, x, y, color, points):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.alive = True
        self.color = color
        self.points = points

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Create bricks
def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick_x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
            brick_y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
            color = BRICK_COLORS[row % len(BRICK_COLORS)]  # Assign color based on row
            points = ROW_POINTS[row % len(ROW_POINTS)]  # Assign points based on row
            bricks.append(Brick(brick_x, brick_y, color, points))
    return bricks

# Draw the welcome screen with a Start button
def draw_welcome_screen():
    screen.fill(BLACK)
    title_text = BIG_FONT.render("Brick Breaker", True, WHITE)
    start_text = FONT.render("Click to Start", True, WHITE)
    
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    
    pygame.display.flip()

# Main game loop
def game_loop():
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    score = 0
    lives = 3  # Set initial number of lives
    
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move('left')
        if keys[pygame.K_RIGHT]:
            paddle.move('right')

        # Move ball
        ball.move()

        # Check for paddle collision
        ball.collide_with_paddle(paddle)

        # Check for brick collision
        for brick in bricks:
            if brick.alive and ball.collide_with_brick(brick):
                ball.speed_y *= -1
                brick.alive = False
                score += brick.points
                break

        # Check for losing condition (ball goes below screen)
        if ball.y > SCREEN_HEIGHT:
            lives -= 1
            if lives > 0:
                # Reset ball position after losing a life
                ball = Ball()
            else:
                return  # End game when lives reach zero

        # Draw paddle, ball, and bricks
        paddle.draw(screen)
        ball.draw(screen)

        for brick in bricks:
            brick.draw(screen)

        # Display score and lives
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        lives_text = FONT.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

        pygame.display.flip()
        clock.tick(60)

# Run the game with welcome screen
def main():
    in_menu = True
    
    while True:
        if in_menu:
            draw_welcome_screen()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False  # Start the game when mouse is clicked

            in_menu = False
            game_loop()
            in_menu = True  # After game over, return to menu

if __name__ == "__main__":
    main()
