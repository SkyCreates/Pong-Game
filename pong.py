import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
BALL_SPEED = 6.5    
PADDLE_SPEED = 9
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 105
FONT_SIZE = 40
WINNING_SCORE = 6

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong by Akash Seam')

# Font
font = pygame.font.Font(None, FONT_SIZE)
large_font = pygame.font.Font(None, 2 * FONT_SIZE)

# Clock
clock = pygame.time.Clock()

class Ball:
    """Represents the ball in the game of Pong, handling its movement and drawing."""
    
    def __init__(self):
        """Initialize the ball in the center of the screen with a random direction."""
        self.reset()

    def reset(self):
        """Reset the ball to the center of the screen and assign it a random velocity."""
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = random.choice([-1, 1]) * BALL_SPEED
        self.dy = random.choice([-1, 1]) * BALL_SPEED
        self.radius = 10

    def move(self):
        """Update the ball's position based on its velocity and handle wall collisions."""
        self.x += self.dx
        self.y += self.dy
        # Handle collisions with the top and bottom walls more efficientlyz
        if not (0 <= self.y <= HEIGHT):
            self.dy *= -1
        # Increase speed slightly on paddle collision
        if self.x <= PADDLE_WIDTH or self.x >= WIDTH - PADDLE_WIDTH:
            self.dx *= 1.05  # Increase speed by 5%

    def draw(self):
        """Draw the ball on the screen."""
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

# Paddle class
class Paddle:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.dy = 0

    def move(self):
        self.y += self.dy
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - PADDLE_HEIGHT:
            self.y = HEIGHT - PADDLE_HEIGHT

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

# AI Paddle class
class AIPaddle(Paddle):
    def __init__(self, x, difficulty):
        super().__init__(x)
        self.difficulty = difficulty

    def move(self, ball):
        if self.difficulty == 1:
            if random.random() < 0.4:  # Higher probability of error
                self.dy = PADDLE_SPEED if ball.y > self.y + PADDLE_HEIGHT // 2 else -PADDLE_SPEED
            else:
                self.dy = 0
        elif self.difficulty == 2:
            if random.random() < 0.6:  # Moderate probability of error
                self.dy = PADDLE_SPEED if ball.y > self.y + PADDLE_HEIGHT // 2 else -PADDLE_SPEED
            else:
                self.dy = 0
        elif self.difficulty == 3:
            if random.random() < 0.8:  # Lower probability of error
                self.dy = PADDLE_SPEED if ball.y > self.y + PADDLE_HEIGHT // 2 else -PADDLE_SPEED
            else:
                self.dy = 0
        super().move()

# Draw the score
def draw_score(left_score, right_score):
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 20))
    screen.blit(right_text, (WIDTH * 3 // 4, 20))

# Draw the net
def draw_net():
    for y in range(0, HEIGHT, 20):
        pygame.draw.line(screen, WHITE, (WIDTH // 2, y), (WIDTH // 2, y + 10))

# Display start screen
def start_screen():
    screen.fill(BLACK)
    title_text = large_font.render("PONG", True, WHITE)
    by_text = font.render("by Akash Seam", True, WHITE)
    instruction_text = font.render("Press SPACE to Start", True, WHITE)
    controls_text = font.render("Controls: W and S to move", True, WHITE)
    objective_text = font.render("Objective: First to 6 points wins", True, WHITE)
    player_indicator_text = font.render("You are on the Left", True, WHITE)
    
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(by_text, (WIDTH // 2 - by_text.get_width() // 2, HEIGHT // 4 + 50))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(objective_text, (WIDTH // 2 - objective_text.get_width() // 2, HEIGHT // 2 + 60))
    screen.blit(player_indicator_text, (WIDTH // 2 - player_indicator_text.get_width() // 2, HEIGHT // 2 + 100))
    
    pygame.display.flip()

# Display game over screen
def game_over_screen(left_score):
    screen.fill(BLACK)
    if left_score >= WINNING_SCORE:
        game_over_text = large_font.render("You Win! ", True, WHITE)
    else:
        game_over_text = large_font.render("Game Over", True, WHITE)
    instruction_text = font.render("Press SPACE to Restart or ESC to Exit", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

# Adjust AI difficulty based on score
def adjust_ai_difficulty(left_score, right_score):
    if right_score >= left_score:
        return 1  # Easier AI when player is behind or tied
    if left_score - right_score <= 2:
        return 2  # Moderate AI when player is slightly ahead
    return 3  # Harder AI when player is well ahead

# Ball out of bounds
def handle_ball_out_of_bounds(ball, left_score, right_score, right_paddle):
    if ball.x < 0:  # Player lost a point
        right_score += 1
        ball.reset()
        difficulty = adjust_ai_difficulty(left_score, right_score)
        right_paddle.difficulty = difficulty
    elif ball.x > WIDTH:  # Player scored a pointws
        left_score += 1
        ball.reset()
        difficulty = adjust_ai_difficulty(left_score, right_score)
        right_paddle.difficulty = difficulty
    return left_score, right_score
# Game loop
def game_loop():
    ball = Ball()
    left_paddle = Paddle(10)
    right_paddle = AIPaddle(WIDTH - 20, difficulty=1)
    left_score = 0
    right_score = 0
    difficulty = 1
    game_started = False
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_started or game_over:
                        game_started = True
                        game_over = False
                        ball.reset()
                        left_score = 0
                        right_score = 0
                        difficulty = 1
                        right_paddle.difficulty = difficulty

                if event.key == pygame.K_ESCAPE and game_over:
                    pygame.quit()
                    return

                if event.key == pygame.K_w:
                    left_paddle.dy = -PADDLE_SPEED
                if event.key == pygame.K_s:
                    left_paddle.dy = PADDLE_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    left_paddle.dy = 0

        if game_started and not game_over:
            ball.move()
            left_paddle.move()
            right_paddle.move(ball)

            # Ball collision with paddles
            if ball.x - ball.radius < left_paddle.x + PADDLE_WIDTH and left_paddle.y < ball.y < left_paddle.y + PADDLE_HEIGHT:
                ball.dx = -ball.dx
            if ball.x + ball.radius > right_paddle.x and right_paddle.y < ball.y < right_paddle.y + PADDLE_HEIGHT:
                ball.dx = -ball.dx

            # Handle ball out of bounds
            left_score, right_score = handle_ball_out_of_bounds(ball, left_score, right_score, right_paddle)

            # Check for game over
            if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
                game_over = True

        # Draw everything
        screen.fill(BLACK)
        draw_net()
        ball.draw()
        left_paddle.draw()
        right_paddle.draw()
        draw_score(left_score, right_score)

        if not game_started:
            start_screen()
        elif game_over:
            game_over_screen(left_score)

        pygame.display.flip()
        clock.tick(FPS)

# Run the game loop
if __name__ == "__main__":
    game_loop()
