import pygame
import math
import time

# 初始化 pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("螺纹加工动画")

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 定义参数
L = 200  # 螺纹长度
Tr = 5  # 进刀量
Tp = 10  # 螺距
Cn = 5  # 切削次数
A = 10  # 螺纹的角度
tailLength = 30  # 退尾长度

# 计算螺纹的斜切半径
tanA = math.tan(math.radians(A))
cr = L * tanA

# 创建刀具
tool_radius = 5
tool_x = WIDTH // 2
tool_y = HEIGHT // 2 - L // 2
tool = pygame.Rect(tool_x, tool_y, tool_radius * 2, tool_radius * 2)

# 设定时间
clock = pygame.time.Clock()

# 进刀、切削、退刀动画的相关参数
progress = 0
cutting = True
has_tail = tailLength > 0
action_stage = "advance"  # 当前动作阶段: advance, cutting, retract

# 动画主循环
running = True
while running:
    screen.fill(WHITE)

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 绘制螺纹路径
    pygame.draw.line(screen, BLUE, (WIDTH // 2, HEIGHT // 2 - L // 2), (WIDTH // 2, HEIGHT // 2 + L // 2), 2)

    # 动画控制：根据阶段更新刀具位置
    if action_stage == "advance":
        # 进刀阶段
        tool.y += Tr  # 模拟进刀
        if tool.y >= HEIGHT // 2 + L // 2:
            action_stage = "cutting"  # 进刀结束，进入切削阶段

    elif action_stage == "cutting":
        # 切削阶段
        for i in range(Cn):
            angle = math.radians(i * Tp)  # 旋转角度
            tool.x = WIDTH // 2 + cr * math.cos(angle)
            tool.y = HEIGHT // 2 + i * Tp
            pygame.draw.circle(screen, RED, tool.center, tool_radius)
        action_stage = "retract"  # 切削结束，进入退刀阶段

    elif action_stage == "retract":
        # 退刀阶段
        if has_tail:
            tool.y -= tailLength  # 退尾动作
            pygame.draw.line(screen, GREEN, (WIDTH // 2, HEIGHT // 2 + L // 2),
                             (WIDTH // 2, HEIGHT // 2 + L // 2 + tailLength), 3)

        action_stage = "done"  # 完成退尾，动画结束

    # 绘制刀具
    pygame.draw.circle(screen, RED, tool.center, tool_radius)

    # 更新显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(15)

    # 停顿，让每个动作可视化
    time.sleep(0.2)

# 退出 pygame
pygame.quit()
