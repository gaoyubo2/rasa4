import pygame
import numpy as np

# 初始化 Pygame
pygame.init()

# 设置窗口尺寸
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("G-code 3D Animation with Parameters")

# 颜色定义
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# 假设 G-code 解析后的参数
sub_process_type = "外圆加工"  # 子工艺类型
R = 2.5  # 半径
Tr = 1.0  # 过渡半径
Cn = 3  # 圆圈数量
F = 1000.0  # 进给速度
G2G3 = 1  # 1表示G2（顺时针圆弧），3表示G3（逆时针圆弧）
PHi1 = 15.0  # 第一个角度增量
L = 100.0  # 长度
W = 100.0  # 切削深度

N_frames = 100  # 动画帧数
U = 20.0  # 移动的 U 轴距离

# 生成外圆轨迹
theta = np.linspace(0, 2 * np.pi, N_frames)
X = R * np.cos(theta)  # 圆形 X 坐标
Y = R * np.sin(theta)  # 圆形 Y 坐标
Z = np.linspace(0, L, N_frames)  # 切削深度（从 0 到 L）

# 转换为屏幕坐标
def convert_to_screen_coords(x, y, z):
    scale = 100  # 缩放因子
    return int(x * scale + WIDTH // 2), int(y * scale + HEIGHT // 2)

# 初始化字体
font = pygame.font.SysFont("Arial", 20)

# 主循环
running = True
clock = pygame.time.Clock()
frame = 0

# 存储轨迹点
trajectory_points = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景
    screen.fill(WHITE)

    # 更新当前帧的轨迹点
    x_screen, y_screen = convert_to_screen_coords(X[frame], Y[frame], Z[frame])
    trajectory_points.append((x_screen, y_screen))

    # 绘制完整的切削轨迹
    if len(trajectory_points) > 1:
        pygame.draw.lines(screen, BLUE, False, trajectory_points, 2)  # 画轨迹线

    # 绘制当前帧的点（如果需要突出显示当前点）
    pygame.draw.circle(screen, RED, (x_screen, y_screen), 5)

    # 绘制半径标注
    radius_x, radius_y = convert_to_screen_coords(R, 0, 0)  # 半径的终点坐标
    pygame.draw.line(screen, GREEN, (WIDTH // 2, HEIGHT // 2), (radius_x, radius_y), 2)  # 绘制半径线
    radius_text = font.render(f"R = {R}", True, GREEN)
    screen.blit(radius_text, (radius_x + 10, radius_y - 10))  # 半径文字标注

    # 进给速度标注
    feed_text = font.render(f"F = {F}", True, BLACK)
    screen.blit(feed_text, (10, HEIGHT - 30))  # 在屏幕下方标注进给速度

    # 过渡半径标注
    transition_text = font.render(f"Tr = {Tr}", True, BLACK)
    screen.blit(transition_text, (10, HEIGHT - 60))  # 在屏幕下方标注过渡半径

    # 标注圆圈数量
    circle_count_text = font.render(f"Cn = {Cn}", True, BLACK)
    screen.blit(circle_count_text, (10, HEIGHT - 90))  # 在屏幕下方标注圆圈数量

    # 绘制进给速度的箭头
    feed_arrow_end_x = WIDTH // 2 + F / 100  # 控制箭头长度
    feed_arrow_end_y = HEIGHT // 2
    pygame.draw.line(screen, BLUE, (WIDTH // 2, HEIGHT // 2), (feed_arrow_end_x, feed_arrow_end_y), 2)
    pygame.draw.polygon(screen, BLUE, [(feed_arrow_end_x, feed_arrow_end_y),
                                      (feed_arrow_end_x - 5, feed_arrow_end_y - 5),
                                      (feed_arrow_end_x - 5, feed_arrow_end_y + 5)])  # 绘制箭头

    # 动态标注其他参数：G2G3（顺时针/逆时针）
    direction_text = f"G2G3: {'G2 (Clockwise)' if G2G3 == 1 else 'G3 (Counter-clockwise)'}"
    direction_surface = font.render(direction_text, True, BLACK)
    screen.blit(direction_surface, (WIDTH - 250, 10))

    # 更新帧
    frame = (frame + 1) % N_frames

    # 刷新显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(30)  # 30帧每秒

# 退出 Pygame
pygame.quit()
