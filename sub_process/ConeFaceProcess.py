import math
import re

from component.common import P


class ConeFace1Process(P):
    """
    该类用于生成锥形面加工的 GCode，基于提供的工艺参数生成相应的 GCode。
    """

    def __init__(self, sub_process_type: str, Tr: float, F: float, L: float, Cn: int, A: float, xDir: int, zDir: int,
                 G71G73: str,
                 **kwargs):
        """
        初始化外反锥面加工过程的参数。

        参数:
            Tr (float): 刀具半径或偏移量。
            F (float): 进给速率。
            L (float): 切割长度。
            Cn (int): 切割次数（即工序的循环次数）。
            A (float): 锥形面的角度，单位为度。
            xDir (int): X轴的方向 (-1 表示负向，1 表示正向)。
            zDir (int): Z轴的方向 (-1 表示负向，1 表示正向)。
            G71G73 (str): GCode模式，'G73' 表示深孔钻削，'G71' 表示粗加工模式。
        """
        super().__init__(sub_process_type, **kwargs)
        self.Tr = float(Tr)
        self.F = float(F)
        self.L = float(L)
        self.Cn = int(re.search(r'\d+', str(Cn)).group())
        self.A = float(A)
        self.xDir = int(re.search(r'\d+', str(xDir)).group())
        self.zDir = int(re.search(r'\d+', str(zDir)).group())
        self.G71G73 = str(G71G73)

    def generate_gcode(self) -> str:
        """
        根据工艺参数生成外反锥面加工的 GCode。

        返回:
            str: 生成的 GCode 字符串。
        """
        gcode = []
        tanA = math.tan(self.A / 180 * math.pi)  # 计算锥形角度的切线值
        Cr = self.L * tanA  # 计算锥形面的半径
        tr = self.Tr  # 刀具半径
        f = self.F  # 进给速率
        cn = self.Cn  # 切割次数
        xDir = self.xDir  # X轴方向
        zDir = self.zDir  # Z轴方向
        g71g73 = self.G71G73  # GCode模式

        num = 1  # 初始化循环次数

        if g71g73 == 'G73':  # 如果使用 G73 模式（深孔钻削）
            for a in range(cn):
                if a == 0:
                    gcode.append("O200;")  # 程序开始
                    gcode.append("G28")  # 返回机器原点
                    gcode.append(f"G01 U[{tr} * #521] F{f};")  # 进给运动
                    gcode.append(f"G01 U[{Cr} * #511 * -1] W[{self.L} * #520] F{f};")  # 切削运动
                    gcode.append(f"G00 U[{tr} * #521 * -1] F{f};")  # 快速退刀
                    gcode.append(f"G01 U[{Cr} * #511] W[{self.L} * #520 * -1] F{f * 10};")  # 加速进给切削
                    if cn == 1:
                        gcode.append("G00 U0;")  # 返回到起始位置
                        gcode.append("M30;")  # 程序结束
                    num += 1
                elif a < (cn - 1):
                    gcode.append(f"G01 U[{tr * 2}] F{f};")
                    gcode.append(f"G01 U[{Cr} * #511 * -1] W[{self.L} * #520] F{f};")
                    gcode.append(f"G00 U[{tr} * #521 * -1] F{f};")
                    gcode.append(f"G01 U[{Cr} * #511] W[{self.L} * #520 * -1] F{f * 10};")
                    num += 1
                else:
                    gcode.append(f"G01 U[{tr * 2}] F{f};")
                    gcode.append(f"G01 U[{Cr} * #511 * -1] W[{self.L} * #520] F{f};")
                    gcode.append(f"G00 U[{tr} * #521 * -1] F{f};")
                    gcode.append(f"G01 U[{Cr} * #511] W[{self.L} * #520 * -1] F{f * 10};")
                    gcode.append(f"G00 U[{tr} * #521 * -1] F{f};")
                    gcode.append("G00 U0;")  # 返回到起始位置
                    gcode.append("M30;")  # 程序结束

        elif g71g73 == 'G71':  # 如果使用 G71 模式（粗加工）
            gcode.append("O200;")  # 程序开始
            gcode.append("G28")  # 返回机器原点
            gcode.append(f"G71 U{tr} R{tr / 2} F{f};")  # 粗加工块
            gcode.append("G71 P80 Q120 U0.2 W0.2 J1 K1;")
            gcode.append(f"N80 G00 U{tr * cn * xDir};")  # 移动到起始位置
            gcode.append(f"G01 U{tr * cn * -1 * xDir} W{self.L * zDir};")  # 切削运动
            gcode.append("N120;")  # 结束粗加工块
            gcode.append("M30;")  # 程序结束

        return "\n".join(gcode)  # 返回生成的 GCode 字符串


class ConeFace2Process(P):
    """
    该类用于内反锥面加工的 GCode，基于提供的工艺参数生成相应的 GCode。
    """

    def __init__(self, sub_process_type: str, Tr: float, F: float, L: float, Cn: int, A: float, Cr: float, xDir: int,
                 zDir: int, G71G73: str, **kwargs):
        """
        初始化内反锥面加工过程的参数。

        参数:
            Tr (float): 刀具半径或偏移量。
            F (float): 进给速率。
            L (float): 切割长度。
            Cn (int): 切割次数（即工序的循环次数）。
            A (float): 锥形面的角度，单位为度。
            Cr (float): 锥形面的半径。
            G71G73 (str): GCode模式，'G73' 表示深孔钻削，'G71' 表示粗加工模式。
        """
        super().__init__(sub_process_type, **kwargs)
        self.sub_process_type = sub_process_type
        self.Tr = float(Tr)
        self.F = float(F)
        self.L = float(L)
        self.Cn = int(re.search(r'\d+', str(Cn)).group())
        self.A = float(A)
        self.Cr = float(Cr)
        self.G71G73 = str(G71G73)

    def generate_gcode(self) -> str:
        """
        根据工艺参数生成内反锥面加工的 GCode。

        参数:
            textHeadFlag (bool): 是否输出头部标记。

        返回:
            str: 生成的 GCode 字符串。
        """
        gcode = []
        tanA = math.tan(self.A / 180 * math.pi)  # 计算锥形角度的切线值
        Cr = self.L * tanA  # 计算锥形面的半径
        Tr = self.Tr  # 刀具半径
        F = self.F  # 进给速率
        Cn = self.Cn  # 切割次数
        G71G73 = self.G71G73  # GCode模式
        Num = 1  # 初始化循环次数

        if G71G73 == 'G73':  # 如果使用 G73 模式（深孔钻削）
            for a in range(Cn):
                if a == 0:
                    gcode.append("O200")
                    gcode.append("G28")  # 返回机器原点
                    gcode.append(f"G01 U{Tr * -1} F{F}")
                    gcode.append(f"G01 U{Cr * -1} W{self.L * -1} F{F}")
                    gcode.append(f"G00 U{Tr} F{F}")
                    gcode.append(f"G01 U{Cr} W{self.L} F{F * 10}")
                    if Cn == 1:
                        gcode.append("G00 U0")  # 返回到起始位置
                        gcode.append("M30")  # 程序结束
                    Num += 1
                elif a < (Cn - 1):
                    gcode.append(f"G01 U{Tr * -2} F{F}")
                    gcode.append(f"G01 U{Cr * -1} W{self.L * -1} F{F}")
                    gcode.append(f"G00 U{Tr} F{F}")
                    gcode.append(f"G01 U{Cr} W{self.L} F{F * 10}")
                    Num += 1
                else:
                    gcode.append(f"G01 U{Tr * -2} F{F}")
                    gcode.append(f"G01 U{Cr * -1} W{self.L * -1} F{F}")
                    gcode.append(f"G00 U{Tr} F{F}")
                    gcode.append(f"G01 U{Cr} W{self.L} F{F * 10}")
                    gcode.append(f"G00 U{Tr * (Num - 1)} F{F}")
                    gcode.append("G00 U0")  # 返回到起始位置
                    gcode.append("M30")  # 程序结束

        elif G71G73 == 'G71':  # 如果使用 G71 模式（粗加工）
            gcode.append("O200")
            gcode.append("G28")  # 返回机器原点
            gcode.append(f"G71 U{Tr} R{Tr / 2} F{F}")
            gcode.append("G71 P80 Q120 U0.2 W0.2 J1 K1")
            gcode.append(f"N80 G00 U{Tr * Cn * -1}")
            gcode.append(f"G01 U{Cr} W{self.L}")
            gcode.append("N120")
            gcode.append("M30")  # 程序结束

        return "\n".join(gcode)  # 返回生成的 GCode 字符串


class ConeFace3Process(P):
    """
    该类用于生成外正锥面加工的 GCode，基于提供的工艺参数生成相应的 GCode。
    """

    def __init__(self, sub_process_type: str, Tr: float, F: float, L: float, Cn: int, A: float, Cr: float, Cr1: float,
                 xDir: int, zDir: int,
                 G71G73: str, **kwargs):
        """
        初始化锥面加工过程的参数。

        参数:
            Tr (float): 刀具半径或偏移量。
            F (float): 进给速率。
            L (float): 切割长度。
            Cn (int): 切割次数（即工序的循环次数）。
            A (float): 锥形面的角度，单位为度。
            Cr (float): 锥形面的半径。
            Cr1 (float): 锥形面的另一个半径。
            G71G73 (str): GCode模式，'G73' 表示深孔钻削，'G71' 表示粗加工模式。
        """
        super().__init__(sub_process_type, **kwargs)
        self.Tr = float(Tr)
        self.F = float(F)
        self.L = float(L)
        self.Cn = int(re.search(r'\d+', str(Cn)).group())
        self.A = float(A)
        self.Cr = float(Cr)
        self.Cr1 = float(Cr1)
        self.xDir = int(re.search(r'\d+', str(xDir)).group())
        self.zDir = int(re.search(r'\d+', str(zDir)).group())
        self.G71G73 = str(G71G73)

    def generate_gcode(self) -> str:
        """
        根据工艺参数生成第三种锥形面加工的 GCode。

        返回:
            str: 生成的 GCode 字符串。
        """
        gcode = []
        tanA = math.tan(self.A / 180 * math.pi)  # 计算锥形角度的切线值
        Cr = self.L * tanA  # 计算锥形面的半径
        Tr = self.Tr  # 刀具半径
        F = self.F  # 进给速率
        Cn = self.Cn  # 切割次数
        G71G73 = self.G71G73  # GCode模式
        Num = 1  # 初始化循环次数

        if G71G73 == 'G73':  # 如果使用 G73 模式（深孔钻削）
            for a in range(Cn):
                if a == 0:
                    gcode.append("O200;")
                    gcode.append("G28")  # 返回机器原点
                    gcode.append(f"G01 U{Tr * -1} F{F}")
                    gcode.append(f"G01 U{Cr * -1} W{self.L * -1} F{F}")
                    gcode.append(f"G00 U{Tr} F{F}")
                    gcode.append(f"G00 U{Cr * -1} W{self.L * -1} F{F}")
                    if Cn == 1:
                        gcode.append("M30;")  # 程序结束
                    Num += 1
                elif a < (Cn - 1):
                    gcode.append(f"G01 U{Tr * 2} F{F}")
                    gcode.append(f"G01 U{Cr * -1} W{self.L} F{F}")
                    gcode.append(f"G00 U{Tr} F{F}")
                    gcode.append(f"G00 U{Cr * -1} W{self.L * -1} F{F}")
                    Num += 1
                else:
                    gcode.append(f"G01 U{Tr * 2} F{F}")
                    gcode.append(f"G01 U{Cr * -1} W{self.L} F{F}")
                    gcode.append(f"G00 U{Tr} F{F}")
                    gcode.append(f"G00 U{Cr * -1} W{self.L * -1} F{F}")
                    gcode.append(f"G00 U{Tr * (Cn - 1)} F{F}")
                    gcode.append("M30;")  # 程序结束

        elif G71G73 == 'G71':  # 如果使用 G71 模式（粗加工）
            gcode.append("O200;")
            gcode.append("G28")  # 返回机器原点
            gcode.append(f"G71 U{Tr} R{Tr / 2} F{F}")
            gcode.append("G71 P80 Q120 U0.2 W0.2 J1 K1")
            gcode.append(f"N80 G00 U{self.Cr1 * self.xDir}")
            gcode.append(f"G01 U{self.Cr1 * self.xDir * -1} W{self.L * self.zDir}")
            gcode.append("N120")
            gcode.append("M30;")  # 程序结束

        return "\n".join(gcode)  # 返回生成的 GCode 字符串


class ConeFace4Process(P):
    """
    该类用于生成内正锥面锥形面加工的 GCode，基于提供的工艺参数生成相应的 GCode。
    """

    def __init__(self, sub_process_type: str, Tr: float, F: float, L: float, Cn: int, A: float, xDir: int, zDir: int,
                 **kwargs):
        """
        初始化锥面加工过程的参数。

        参数:
            Tr (float): 刀具半径或偏移量。
            F (float): 进给速率。
            L (float): 切割长度。
            Cn (int): 切割次数（即工序的循环次数）。
            A (float): 锥形面的角度，单位为度。
            xDir (int): X轴的方向 (-1 表示负向，1 表示正向)。
            zDir (int): Z轴的方向 (-1 表示负向，1 表示正向)。
        """
        super().__init__(sub_process_type, **kwargs)
        self.Tr = float(Tr)
        self.F = float(F)
        self.L = float(L)
        self.Cn = int(re.search(r'\d+', str(Cn)).group())
        self.A = float(A)
        self.xDir = int(re.search(r'\d+', str(xDir)).group())
        self.zDir = int(re.search(r'\d+', str(zDir)).group())

    def generate_gcode(self) -> str:
        """
        根据工艺参数生成第四种锥形面加工的 GCode。

        返回:
            str: 生成的 GCode 字符串。
        """
        gcode = []
        tanA = math.tan(self.A / 180 * math.pi)  # 计算锥形角度的切线值
        Cr = self.L * tanA  # 计算锥形面的半径
        Tr = self.Tr  # 刀具半径
        F = self.F  # 进给速率
        Cn = self.Cn  # 切割次数

        Num = 1  # 初始化循环次数

        for a in range(Cn):
            if a == 0:
                gcode.append("O200;")
                gcode.append("G28")  # 返回机器原点
                gcode.append(f"G01 U{Tr} F{F}")
                gcode.append(f"G01 U{Cr} W{self.L * -1} F{F}")
                gcode.append(f"G00 U{Tr * -1} F{F}")
                gcode.append(f"G01 U{Cr * -1} W{self.L} F{F * 10}")
                if Cn == 1:
                    gcode.append("M30;")  # 程序结束
                Num += 1
            elif a < (Cn - 1):
                gcode.append(f"G01 U{Tr * 2} F{F}")
                gcode.append(f"G01 U{Cr} W{self.L * -1} F{F}")
                gcode.append(f"G00 U{Tr * -1} F{F}")
                gcode.append(f"G01 U{Cr * -1} W{self.L} F{F * 10}")
                Num += 1
            else:
                gcode.append(f"G01 U{Tr * 2} F{F}")
                gcode.append(f"G01 U{Cr} W{self.L * -1} F{F}")
                gcode.append(f"G00 U{Tr * -1} F{F}")
                gcode.append(f"G01 U{Cr * -1} W{self.L} F{F * 10}")
                gcode.append(f"G00 U{Tr * (Num - 1) * -1} F{F}")
                gcode.append("M30;")  # 程序结束

        return "\n".join(gcode)  # 返回生成的 GCode 字符串
