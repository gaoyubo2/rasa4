import math
import re

from component.common import P


class Chamfer1Process(P):
    """
    用于生成外圆角倒角1的GCode，支持G71和G73模式下的GCode生成。
    """

    def __init__(self, sub_process_type: str, R: float, Tr: float, Cn: int, F: float, G2G3: int, PHi1: float, L: float,
                 G71G73: int,
                 **kwargs):
        """
        初始化外圆角倒角加工过程的参数。

        参数:
            R (float): 圆弧半径。
            Tr (float): 每次进刀量。
            Cn (int): 进刀次数。
            F (float): 进给速度。
            G2G3 (int): 切圆弧方向（0 表示 G02，1 表示 G03）。
            PHi1 (float): 终点的X轴增量位置（用于G73模式）。
            L (float): 终点的Z轴增量位置。
            G71G73 (int): 加工模式（G71 或 G73）。
        """
        super().__init__(sub_process_type, **kwargs)
        # 转化为适当的类型
        self.R = float(R)  # 转化为浮动数
        self.Tr = float(Tr)  # 转化为浮动数
        self.Cn = int(re.search(r'\d+', str(Cn)).group())  # 提取第一个出现的数字，并转为整数
        self.F = float(F)  # 转化为浮动数
        self.G2G3 = int(G2G3)  # 转化为整数
        self.PHi1 = float(PHi1)  # 转化为浮动数
        self.L = float(L)  # 转化为浮动数
        self.G71G73 = int(G71G73)  # 转化为整数

    def generate_gcode(self) -> str:
        """
        根据倒角加工参数生成GCode。

        返回:
            str: 生成的GCode字符串。
        """
        gcode = []
        delta_x = self.PHi1
        delta_z = self.L
        tr = self.Tr
        f = self.F
        r = self.R
        cn = self.Cn
        g2g3 = self.G2G3
        mode = self.G71G73

        if mode == 73:  # G73模式
            gcode.append("O0300;")
            for a in range(cn):
                # 左进刀
                gcode.append(f"G01 W{-tr} F{f}")

                # 切圆弧
                if g2g3 == 1:
                    gcode.append(f"G02 U[{delta_x}] W{-delta_z} R{r} F{f}")
                else:
                    gcode.append(f"G03 U[{delta_x}] W{-delta_z} R{r} F{f}")

                # Z轴退刀
                if a + 1 == cn:  # 最后一刀，退刀到起点
                    gcode.append(f"G00 W{delta_z + tr * cn}")
                else:
                    gcode.append(f"G00 W{delta_z}")

                # X轴退刀
                gcode.append(f"G00 U[{delta_x * -1}]")

            gcode.append("G00 G28;")  # 返回机器起点
            gcode.append("M30;")

        else:  # G71模式
            gcode.append("O0300;")
            gcode.append("G00 G28")  # 初始化
            gcode.append(f"G71 U{tr} R{tr / 2} F{f}")
            gcode.append("G71 P80 Q120 U0.2 W0.2 J1 K1")

            # 进刀
            gcode.append(f"N80 G00 U{-tr * cn}")

            # 切圆弧
            if g2g3 == 0:
                gcode.append(f"G02 U{tr * cn} W{-delta_z} R{r}")
            else:
                gcode.append(f"G03 U{tr * cn} W{-delta_z} R{r}")

            gcode.append("N120")
            gcode.append("G00 G28")  # 返回机器起点
            gcode.append("M30;")

        return "\n".join(gcode)


class Chamfer2Process(P):
    """
    用于生成外倒角的GCode，支持G71和G73模式下的GCode生成。
    """

    def __init__(self, sub_process_type: str, Cn: int, Tr: float, F: float, L: float, A: float, xDir: int, zDir: int,
                 G71G73: int,
                 **kwargs):
        """
        初始化外倒角加工过程的参数。

        参数:
            Cn (int): 进刀次数。
            Tr (float): 每次进刀量。
            F (float): 进给速度。
            L (float): 长度。
            A (float): 倒角角度。
            xDir (int): X轴方向。
            zDir (int): Z轴方向。
            G71G73 (int): 加工模式（G71 或 G73）。
        """
        super().__init__(sub_process_type, **kwargs)
        # 提取Cn中的整数部分
        self.Cn = int(re.search(r'\d+', str(Cn)).group())  # 提取第一个出现的数字，并转为整数
        # 提取xDir中的整数部分
        self.xDir = int(re.search(r'\d+', str(xDir)).group())
        # 提取zDir中的整数部分
        self.zDir = int(re.search(r'\d+', str(zDir)).group())
        # 提取G71G73中的整数部分
        self.G71G73 = int(re.search(r'\d+', str(G71G73)).group())
        # 转换为浮动数
        self.Tr = float(Tr)
        self.F = float(F)
        self.L = float(L)
        self.A = float(A)

    def generate_gcode(self) -> str:
        """
        根据倒角加工参数生成GCode。

        返回:
            str: 生成的GCode字符串。
        """
        gcode = []
        cn = self.Cn
        tr = self.Tr
        f = self.F
        l = self.L
        tanA = math.tan(self.A / 180 * math.pi)
        cr = l * tanA
        x_dir = self.xDir
        z_dir = self.zDir

        if self.G71G73 == 73:  # G73模式
            gcode.append("O200;")
            num = 1
            for a in range(cn):
                if a == 0:
                    gcode.append(f"G01 U[{tr} * #521] F{f}")
                    gcode.append(f"G01 U[{cr} * #521 * #511 * -1] W[{l} * #520] F{f}")
                    gcode.append(f"G00 U[{tr} * #521 * -1] F{f}")
                    gcode.append(f"G01 U[{cr} * #521 * #511] W[{l} * #520 * -1] F{f * 10}")
                    if cn == 1:
                        gcode.append("G00 G28;")  # 返回起点
                        gcode.append("M30;")
                    num += 1
                elif a < cn - 1:
                    gcode.append(f"G01 U[{tr * 2} * #521] F{f}")
                    gcode.append(f"G01 U[{cr} * #521 * #511 * -1] W[{l} * #520] F{f}")
                    gcode.append(f"G00 U[{tr} * #521 * -1] F{f}")
                    gcode.append(f"G01 U[{cr} * #521 * #511] W[{l} * #520 * -1] F{f * 10}")
                    num += 1
                else:
                    gcode.append(f"G01 U[{tr * 2} * #521] F{f}")
                    gcode.append(f"G01 U[{cr} * #521 * #511 * -1] W[{l} * #520] F{f}")
                    gcode.append(f"G00 U[{tr} * #521 * -1] F{f}")
                    gcode.append(f"G01 U[{cr} * #521 * #511] W[{l} * #520 * -1] F{f * 10}")
                    gcode.append(f"G00 U[{tr * (num - 1)} * #521 * -1] F{f}")
                    gcode.append("G00 G28;")  # 返回起点
                    gcode.append("M30;")

        elif self.G71G73 == 71:  # G71模式
            gcode.append("O200;")
            gcode.append("G00 G28")  # 初始化
            gcode.append(f"G71 U{tr} R{tr / 2} F{f}")
            gcode.append("G71 P80 Q120 U0.2 W0.2 J1 K1")
            gcode.append(f"N80 G00 U{tr * cn * x_dir}")
            gcode.append(f"G01 U{tr * cn * -1 * x_dir} W{l * z_dir}")
            gcode.append("N120")
            gcode.append("G00 G28")  # 返回起点
            gcode.append("M30;")

        return "\n".join(gcode)


class Chamfer3Process(P):
    """
    用于生成内圆角倒角的GCode，支持G71和G73模式下的GCode生成。
    """

    def __init__(self, sub_process_type: str, R: float, Tr: float, Cn: int, F: float, G2G3: int, PHi1: float, L: float,
                 G71G73: int,
                 **kwargs):
        """
        初始化内圆角倒角加工过程的参数。

        参数:
            R (float): 圆弧半径。
            Tr (float): 每次进刀量。
            Cn (int): 进刀次数。
            F (float): 进给速度。
            G2G3 (int): 圆弧方向，1表示G02，0表示G03。
            PHi1 (float): 终点增量位置X。
            L (float): 终点增量位置Z。
            G71G73 (int): 加工模式（G71 或 G73）。
        """
        super().__init__(sub_process_type, **kwargs)
        self.R = float(R)
        self.Tr = float(Tr)
        self.Cn = int(re.search(r'\d+', str(Cn)).group())
        self.F = float(F)
        self.G2G3 = int(re.search(r'\d+', str(G2G3)).group())
        self.PHi1 = float(PHi1)
        self.L = float(L)
        self.G71G73 = int(re.search(r'\d+', str(G71G73)).group())

    def generate_gcode(self) -> str:
        """
        根据倒角加工参数生成GCode。

        返回:
            str: 生成的GCode字符串。
        """
        gcode = []
        r = self.R
        tr = self.Tr
        cn = self.Cn
        f = self.F
        g2g3 = self.G2G3
        delta_x = self.PHi1
        delta_z = self.L

        if self.G71G73 == 73:  # G73模式
            gcode.append("O0300;")
            for a in range(cn):
                # 左进刀
                gcode.append(f"G01 W{-tr} F{f}")
                # 切圆弧
                if g2g3 == 1:
                    gcode.append(f"G02 U[{delta_x * -1}] W{-delta_z} R{r} F{f}")
                else:
                    gcode.append(f"G03 U[{delta_x * -1}] W{-delta_z} R{r} F{f}")
                # Z轴退刀
                if a + 1 == cn:  # 最后一刀，退刀到起点
                    gcode.append(f"G00 W{delta_z + tr * cn}")
                else:  # 正常退刀
                    gcode.append(f"G00 W{delta_z}")
                # X轴退刀
                gcode.append(f"G00 U[{delta_x}]")

            gcode.append("G00 G28;")  # 返回起点
            gcode.append("M30;")

        else:  # G71模式
            gcode.append("O0300;")
            gcode.append("G00 G28")  # 初始化
            gcode.append(f"G71 U{tr} R{tr / 2} F{f}")
            gcode.append("G71 P80 Q120 U0.2 W0.2 J1 K1")
            gcode.append(f"N80 G00 U{tr * cn}")
            if g2g3 == 0:
                gcode.append(f"G02 U{-tr * cn} W{-delta_z} R{r}")
            elif g2g3 == 1:
                gcode.append(f"G03 U{-tr * cn} W{-delta_z} R{r}")
            gcode.append("N120")
            gcode.append("G00 G28")  # 返回起点
            gcode.append("M30;")

        return "\n".join(gcode)


class Chamfer4Process(P):
    """
    用于生成内倒角的GCode，支持G71和G73模式下的GCode生成。
    """

    def __init__(self, sub_process_type: str, Cn: int, Tr: float, L: float, F: float, A: float, xDir: int, zDir: int,
                 G71G73: int,
                 **kwargs):
        """
        初始化内倒角加工过程的参数。

        参数:
            Cn (int): 进刀次数。
            Tr (float): 每次进刀量。
            L (float): 长度。
            F (float): 进给速度。
            A (float): 倒角角度。
            xDir (int): X轴方向。
            zDir (int): Z轴方向。
            G71G73 (int): 加工模式（G71 或 G73）。
        """
        super().__init__(sub_process_type, **kwargs)
        self.Cn = int(re.search(r'\d+', str(Cn)).group())
        self.Tr = float(Tr)
        self.L = float(L)
        self.F = float(F)
        self.A = float(A)
        self.xDir = int(re.search(r'\d+', str(xDir)).group())
        self.zDir = int(re.search(r'\d+', str(zDir)).group())
        self.G71G73 = int(re.search(r'\d+', str(G71G73)).group())

    def generate_gcode(self) -> str:
        """
        根据倒角加工参数生成GCode。

        返回:
            str: 生成的GCode字符串。
        """
        gcode = []
        num = 1
        tanA = math.tan(self.A / 180 * math.pi)
        cr = self.L * tanA

        if self.G71G73 == 73:  # G73模式
            gcode.append("O200;")
            for a in range(self.Cn):
                if a == 0:
                    gcode.append(f"G01 U[{self.Tr} * #521] F{self.F};")
                    gcode.append(f"G01 U[{cr} * #521 * #511 * -1] W[{self.L} * #520] F{self.F};")
                    gcode.append(f"G00 U[{self.Tr} * #521 * -1] F{self.F};")
                    gcode.append(f"G01 U[{cr} * #521 * #511] W[{self.L} * #520 * -1] F{self.F * 10};")
                    if self.Cn == 1:
                        gcode.append("G00 G28;")  # 返回起点
                        gcode.append("M30;")
                    num += 1
                elif a < (self.Cn - 1):
                    gcode.append(f"G01 U[{self.Tr * 2} * #521] F{self.F};")
                    gcode.append(f"G01 U[{cr} * #521 * #511 * -1] W[{self.L} * #520] F{self.F};") 
                    gcode.append(f"G00 U[{self.Tr} * #521 * -1] F{self.F};")
                    gcode.append(f"G01 U[{cr} * #521 * #511] W[{self.L} * #520 * -1] F{self.F * 10};")
                    num += 1
                else:
                    gcode.append(f"G01 U[{self.Tr * 2} * #521] F{self.F};")
                    gcode.append(f"G01 U[{cr} * #521 * #511 * -1] W[{self.L} * #520] F{self.F};")
                    gcode.append(f"G00 U[{self.Tr} * #521 * -1] F{self.F};")
                    gcode.append(f"G01 U[{cr} * #521 * #511] W[{self.L} * #520 * -1] F{self.F * 10};")
                    gcode.append(f"G00 U[{self.Tr * (num - 1)} * #521 * -1] F{self.F};")
                    gcode.append("G00 G28;")  # 返回起点
                    gcode.append("M30;")

        elif self.G71G73 == 71:  # G71模式
            gcode.append("O200;")
            gcode.append("G00 G28;")  # 初始化
            gcode.append(f"G71 U{self.Tr} R{self.Tr / 2} F{self.F};")
            gcode.append("G71 P80 Q120 U0.2 W0.2 J1 K1;")
            gcode.append(f"N80 G00 U{self.Tr * self.Cn * self.xDir};")
            gcode.append(f"G01 U{self.Tr * self.Cn * -1 * self.xDir} W{self.L * self.zDir};")
            gcode.append("N120;")
            gcode.append("G00 G28;")  # 返回起点
            gcode.append("M30;")

        return "\n".join(gcode)
