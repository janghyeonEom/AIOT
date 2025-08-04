import pygame
import sys
import random

# 게임 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)

# 게임 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_SIZE = 15
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 6
BRICK_COLS = 10

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.choice([-4, 4])
        self.dy = -4
        self.size = BALL_SIZE
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)
    
    def bounce_x(self):
        self.dx = -self.dx
    
    def bounce_y(self):
        self.dy = -self.dy

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = 8
    
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
    
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = color
        self.destroyed = False
    
    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("벽돌깨기 게임")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
    
    def reset_game(self):
        # 공 생성
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        # 패들 생성
        self.paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30)
        
        # 벽돌 생성
        self.bricks = []
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * (BRICK_WIDTH + 5) + 40
                y = row * (BRICK_HEIGHT + 5) + 50
                color = colors[row]
                self.bricks.append(Brick(x, y, color))
        
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_won = False
    
    def handle_collisions(self):
        # 벽과의 충돌
        if self.ball.x <= self.ball.size or self.ball.x >= SCREEN_WIDTH - self.ball.size:
            self.ball.bounce_x()
        
        if self.ball.y <= self.ball.size:
            self.ball.bounce_y()
        
        # 바닥에 떨어짐
        if self.ball.y >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                # 공 리셋
                self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        # 패들과의 충돌
        ball_rect = pygame.Rect(self.ball.x - self.ball.size, self.ball.y - self.ball.size, 
                               self.ball.size * 2, self.ball.size * 2)
        paddle_rect = self.paddle.get_rect()
        
        if ball_rect.colliderect(paddle_rect) and self.ball.dy > 0:
            self.ball.bounce_y()
            # 패들의 어느 부분에 맞았는지에 따라 공의 방향 조정
            hit_pos = (self.ball.x - self.paddle.x) / self.paddle.width
            self.ball.dx = (hit_pos - 0.5) * 8
        
        # 벽돌과의 충돌
        for brick in self.bricks:
            if not brick.destroyed:
                brick_rect = brick.get_rect()
                if ball_rect.colliderect(brick_rect):
                    brick.destroyed = True
                    self.score += 10
                    self.ball.bounce_y()
                    break
        
        # 모든 벽돌이 파괴되었는지 확인
        if all(brick.destroyed for brick in self.bricks):
            self.game_won = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # 게임 객체들 그리기
        self.ball.draw(self.screen)
        self.paddle.draw(self.screen)
        
        for brick in self.bricks:
            brick.draw(self.screen)
        
        # UI 그리기
        score_text = self.small_font.render(f"점수: {self.score}", True, WHITE)
        lives_text = self.small_font.render(f"생명: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 35))
        
        # 게임 오버 또는 승리 메시지
        if self.game_over:
            game_over_text = self.font.render("게임 오버! R키를 눌러 다시 시작", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        elif self.game_won:
            win_text = self.font.render("축하합니다! 승리! R키를 눌러 다시 시작", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(win_text, text_rect)
        
        # 조작법 안내
        if not self.game_over and not self.game_won:
            help_text = self.small_font.render("← → 키로 패들 조작, ESC로 종료", True, WHITE)
            self.screen.blit(help_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 25))
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and (self.game_over or self.game_won):
                        self.reset_game()
            
            # 키 입력 처리 (연속 입력)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move_left()
            if keys[pygame.K_RIGHT]:
                self.paddle.move_right()
            
            # 게임 로직 업데이트
            if not self.game_over and not self.game_won:
                self.ball.move()
                self.handle_collisions()
            
            # 화면 그리기
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"게임 실행 중 오류가 발생했습니다: {e}")
        print("pygame이 설치되어 있는지 확인해주세요: pip install pygame")