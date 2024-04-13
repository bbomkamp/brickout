import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_GAP = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 36)

# Function to draw the paddle
def draw_paddle(paddle_x):
    pygame.draw.rect(screen, WHITE, (paddle_x, SCREEN_HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to draw the ball
def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

# Function to draw a brick
def draw_brick(brick_x, brick_y, color):
    pygame.draw.rect(screen, color, (brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Function to draw the score
def draw_score(score):
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to initialize the game
def initialize_game():
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_dx = 5 * random.choice([-1, 1])
    ball_dy = -5
    bricks = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            brick_x = col * (BRICK_WIDTH + BRICK_GAP)
            brick_y = row * (BRICK_HEIGHT + BRICK_GAP) + 50
            color = colors[row % len(colors)]  # Choose color based on row
            bricks.append((brick_x, brick_y, color))
    return paddle_x, ball_x, ball_y, ball_dx, ball_dy, bricks

# Function to handle collisions with the paddle
def paddle_collision(ball_x, ball_y, paddle_x):
    return ball_y + BALL_RADIUS >= SCREEN_HEIGHT - PADDLE_HEIGHT and paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH

# Function to handle collisions with the bricks
def brick_collision(ball_x, ball_y, bricks):
    for brick in bricks:
        brick_x, brick_y, _ = brick
        if brick_x <= ball_x <= brick_x + BRICK_WIDTH and brick_y <= ball_y <= brick_y + BRICK_HEIGHT:
            bricks.remove(brick)
            return True
    return False

# Main game loop
def main():
    total_score = 0
    balls_lost = 0
    
    while balls_lost < 3:
        score = 0
        paddle_x, ball_x, ball_y, ball_dx, ball_dy, bricks = initialize_game()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Move the paddle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle_x -= 8 if paddle_x >= 8 else 0  # Prevent going off the left edge
            if keys[pygame.K_RIGHT]:
                paddle_x += 8 if paddle_x <= SCREEN_WIDTH - PADDLE_WIDTH - 8 else 0  # Prevent going off the right edge

            
            # Move the ball
            ball_x += ball_dx
            ball_y += ball_dy
            
            # Check for collisions with walls
            if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
                ball_dx *= -1
            if ball_y <= BALL_RADIUS:
                ball_dy *= -1
            if ball_y >= SCREEN_HEIGHT - BALL_RADIUS:
                # Ball lost, update count and break out of loop
                balls_lost += 1
                break
            
            # Check for collisions with the paddle
            if paddle_collision(ball_x, ball_y, paddle_x):
                ball_dy *= -1
            
            # Check for collisions with the bricks
            if brick_collision(ball_x, ball_y, bricks):
                score += 10
                ball_dy *= -1
            
            # Clear the screen
            screen.fill(BLACK)
            
            # Draw the paddle, ball, bricks, and score
            draw_paddle(paddle_x)
            draw_ball(ball_x, ball_y)
            for brick in bricks:
                draw_brick(*brick)
            draw_score(total_score + score)
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(60)
        
        # Update total score
        total_score += score
    
    pygame.quit()

if __name__ == "__main__":
    main()
