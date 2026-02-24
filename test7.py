import pygame
import random
import sys
import math

# --- 初始化 Pygame ---
pygame.init()

# --- 游戏配置常量 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 150  # 每个地鼠洞的大小
GRID_ROWS = 2
GRID_COLS = 3
GAME_DURATION = 30  # 游戏时长（秒）

# 颜色定义 (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)       # 地鼠颜色
DARK_GREEN = (34, 139, 34)  # 背景色
HOLE_COLOR = (60, 40, 20)   # 洞的颜色
RED = (220, 20, 60)         # 锤子颜色

# 设置屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python 打地鼠 (鼠标点击版)")
clock = pygame.time.Clock()

# --- 字体设置 ---
# 尝试获取系统字体，如果失败则使用默认字体
try:
    font = pygame.font.SysFont("simhei", 32)  # Windows 常用黑体
    score_font = pygame.font.SysFont("arial", 48, bold=True)
except:
    font = pygame.font.Font(None, 32)
    score_font = pygame.font.Font(None, 48)

class Mole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.is_up = False
        self.timer = 0
        self.stay_time = 0 # 地鼠停留的时间

    def draw(self, surface):
        # 1. 画洞 (深色椭圆)
        hole_rect = pygame.Rect(self.x + 10, self.y + 80, GRID_SIZE - 20, GRID_SIZE - 80)
        pygame.draw.ellipse(surface, HOLE_COLOR, hole_rect)

        # 2. 如果地鼠升起，画地鼠
        if self.is_up:
            # 身体 (半圆)
            mole_rect = pygame.Rect(self.x + 20, self.y + 40, GRID_SIZE - 40, GRID_SIZE - 50)
            pygame.draw.circle(surface, BROWN, mole_rect.center, mole_rect.width // 2)
            
            # 眼睛
            eye_radius = 5
            pygame.draw.circle(surface, BLACK, (self.x + 50, self.y + 70), eye_radius)
            pygame.draw.circle(surface, BLACK, (self.x + 100, self.y + 70), eye_radius)
            
            # 鼻子
            pygame.draw.ellipse(surface, BLACK, (self.x + 65, self.y + 85, 20, 15))
            
            # 嘴巴 (线条)
            pygame.draw.arc(surface, BLACK, (self.x + 60, self.y + 90, 30, 20), 3.14, 6.28, 2)

    def pop_up(self):
        if not self.is_up:
            self.is_up = True
            # 随机停留时间 40 到 100 帧 (约0.7秒到1.6秒)
            self.stay_time = random.randint(40, 100) 

    def whack(self, mouse_pos):
        # 检查鼠标点击是否在升起的地鼠范围内
        if self.is_up and self.rect.collidepoint(mouse_pos):
            self.is_up = False # 打中后立即下去
            return True
        return False

    def update(self):
        if self.is_up:
            self.timer += 1
            if self.timer >= self.stay_time:
                self.is_up = False
                self.timer = 0

def draw_hammer(surface, pos, is_clicking):
    # 简单的锤子绘制逻辑
    mx, my = pos
    handle_color = (160, 82, 45)
    
    # 如果点击中，锤子旋转一点
    angle = 0
    if is_clicking:
        angle = -45
    
    # 创建一个临时的 Surface 用于旋转
    hammer_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
    
    # 画锤柄
    pygame.draw.rect(hammer_surf, handle_color, (45, 40, 10, 60))
    # 画锤头
    pygame.draw.rect(hammer_surf, (100, 100, 100), (20, 20, 60, 30))
    pygame.draw.rect(hammer_surf, RED, (20, 20, 60, 10)) # 锤头红色装饰

    # 旋转
    rotated_hammer = pygame.transform.rotate(hammer_surf, angle)
    
    # 获取新的矩形并设置中心为鼠标位置
    new_rect = rotated_hammer.get_rect(center=(mx, my))
    
    surface.blit(rotated_hammer, new_rect)
    
    # 隐藏系统鼠标，使用自定义图形
    pygame.mouse.set_visible(False)

def main():
    # 计算网格居中位置
    start_x = (SCREEN_WIDTH - (GRID_COLS * GRID_SIZE)) // 2
    start_y = (SCREEN_HEIGHT - (GRID_ROWS * GRID_SIZE)) // 2 + 50

    # 创建地鼠列表
    moles = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = start_x + col * GRID_SIZE
            y = start_y + row * GRID_SIZE
            moles.append(Mole(x, y))

    score = 0
    start_ticks = pygame.time.get_ticks() # 记录开始时间（毫秒）
    
    # 控制地鼠出现的频率
    pop_event = pygame.USEREVENT + 1
    pygame.time.set_timer(pop_event, 800) # 每800毫秒尝试冒出一只地鼠

    running = True
    while running:
        # 1. 计算剩余时间
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, GAME_DURATION - seconds_passed)

        if time_left == 0:
            running = False # 时间到，结束循环

        # 2. 事件处理
        mouse_click_pos = None
        is_clicking = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pop_event:
                # 随机选择一个地鼠冒出来
                random.choice(moles).pop_up()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 左键点击
                    is_clicking = True
                    mouse_click_pos = event.pos
                    # 检查是否打中地鼠
                    for mole in moles:
                        if mole.whack(mouse_click_pos):
                            score += 1

        # 3. 绘制背景
        screen.fill(DARK_GREEN)

        # 4. 绘制 UI (分数和时间)
        score_text = score_font.render(f"得分: {score}", True, WHITE)
        time_text = font.render(f"时间: {int(time_left)}", True, WHITE)
        screen.blit(score_text, (20, 20))
        screen.blit(time_text, (SCREEN_WIDTH - 150, 30))

        # 5. 更新并绘制地鼠
        for mole in moles:
            mole.update()
            mole.draw(screen)

        # 6. 绘制自定义锤子 (跟随鼠标)
        draw_hammer(screen, pygame.mouse.get_pos(), is_clicking)

        # 7. 刷新屏幕
        pygame.display.flip()
        clock.tick(60) # 锁定 60 帧

    # --- 游戏结束画面 ---
    game_over = True
    while game_over:
        screen.fill(BLACK)
        end_text = score_font.render("游戏结束!", True, WHITE)
        final_score_text = font.render(f"最终得分: {score}", True, WHITE)
        restart_text = font.render("按空格键重新开始，ESC键退出", True, WHITE)
        
        screen.blit(end_text, (SCREEN_WIDTH//2 - end_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
        screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 60))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    main() # 递归调用重启游戏

if __name__ == "__main__":
    main()
