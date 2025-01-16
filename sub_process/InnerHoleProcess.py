import math

from component.common import P


class InnerHole1Process(P):
    """
    处理内孔加工的 G 代码生成类。

    该类用于生成内孔加工的 G 代码，根据不同的加工参数生成相应的 G 代码指令。

    参数:
    - Cn (int): 进刀次数，表示内孔加工的进刀次数（必选）。
    - L (float): 加工长度（必选）。
    - Tr (float): 进刀深度（必选）。
    - Cr (float): 最后一次进刀的退刀量（必选）。
    - F (float): 进给速度，单位 mm/min（必选）。
    - **kwargs (dict): 其他工艺相关参数，继承父类 `P` 使用。

    方法:
    - generate_gcode(): 根据传入的参数生成相应的 G 代码字符串。
    """

    def __init__(self, sub_process_type: str, Cn: int, L: float, Tr: float, Cr: float, F: float, **kwargs):
        """
        初始化中心孔加工 G 代码生成器。

        参数:
        - Cn (int): 进刀次数（必选）。
        - L (float): 加工长度（必选）。
        - Tr (float): 进刀深度（必选）。
        - Cr (float): 最后一次进刀的退刀量（必选）。
        - F (float): 进给速度（必选）。
        - **kwargs (dict): 其他工艺相关参数（可选）。
        """
        super().__init__(sub_process_type, **kwargs)
        self.Cn = int(Cn)
        self.L = float(L)
        self.Tr = float(Tr)
        self.Cr = float(Cr)
        self.F = float(F)

    def generate_gcode(self) -> str:
        """
        生成内孔加工的 G 代码。

        根据进刀次数、进刀深度、进给速度等参数生成相应的 G 代码指令，并将其返回为字符串。

        返回:
        - str: 生成的 G 代码字符串。
        """
        gcode = []
        for a in range(self.Cn):
            if a == 0:
                # Header and start
                gcode.append("O200;")
                gcode.append("G28")  # Home the machine
                gcode.append(f"G01 U[{self.Tr} * #521] F{self.F};")
                gcode.append(f"G01 W[{self.L} * #520] F{self.F};")
                gcode.append(f"G00 U[{self.Tr} * #521 * -1] F{self.F};")
                gcode.append(f"G00 W[{self.L} * #520 * -1] F{self.F};")
                if self.Cn == 1:
                    gcode.append("M30;")  # End of program
            elif a < (self.Cn - 1):
                gcode.append(f"G01 U[{self.Tr * 2} * #521] F{self.F};")
                gcode.append(f"G01 W[{self.L} * #520] F{self.F};")
                gcode.append(f"G00 U[{self.Tr} * #521 * -1] F{self.F};")
                gcode.append(f"G00 W[{self.L} * #520 * -1] F{self.F};")
            else:
                gcode.append(f"G01 U[{self.Tr * 2} * #521] F{self.F};")
                gcode.append(f"G01 W[{self.L} * #520] F{self.F};")
                gcode.append(f"G00 U[{self.Cr} * #521 * -1] F{self.F};")
                gcode.append(f"G00 W[{self.L} * #520 * -1] F{self.F};")
                gcode.append("M30;")  # End of program

        return "\n".join(gcode)


class InnerHole2Process(P):
    """
    处理内孔加工（G71 和 G73）的 G 代码生成类。

    该类用于根据不同的加工参数生成相应的 G 代码指令，支持 G71 和 G73 模式的内孔加工。

    方法:
    - generate_gcode(): 根据传入的参数生成相应的 G 代码字符串。
    """

    def __init__(self, sub_process_type: str, Cn: int, L: float, Tr: float, F: float, A: float, xDir: int, zDir: int,
                 G71G73: int,
                 **kwargs):
        """
        初始化内锥面加工 G 代码生成器。

        参数:
        - Cn (int): 进刀次数（必选）。
        - L (float): 加工长度（必选）。
        - Tr (float): 进刀深度（必选）。
        - F (float): 进给速度（必选）。
        - A (float): 锥度角度（必选）。
        - xDir (int): X 轴方向（必选）。
        - zDir (int): Z 轴方向（必选）。
        - G71G73 (str): 加工模式（必选）。
        - **kwargs (dict): 其他工艺相关参数（可选）。
        """
        super().__init__(sub_process_type, **kwargs)
        self.Cn = int(Cn)
        self.L = float(L)
        self.Tr = float(Tr)
        self.F = float(F)
        self.A = float(A)
        self.xDir = int(xDir)
        self.zDir = int(zDir)
        self.G71G73 = G71G73

    def generate_gcode(self) -> str:
        """
        生成内锥面工艺加工的 G 代码。

        根据加工模式（G71 或 G73）以及进刀次数、进刀深度等参数生成相应的 G 代码。

        返回:
        - str: 生成的 G 代码字符串。
        """
        gcode = []
        tanA = math.tan(math.radians(self.A))  # 锥度角度转弧度后计算正切
        Cr = self.L * tanA

        if self.G71G73 == 'G73':  # G73 加工模式
            for a in range(self.Cn):
                if a == 0:
                    gcode.append("O200")
                    gcode.append("G28")  # 复位
                    gcode.append(f"G01 U[{self.Tr} * #521] F{self.F};")
                    gcode.append(f"G01 U[{Cr} * #511 * -1] W[{self.L} * #520] F{self.F};")
                    gcode.append(f"G00 U[{self.Tr} * #521 * -1] F{self.F};")
                    gcode.append(f"G01 U[{Cr} * #511] W[{self.L} * #520 * -1] F{self.F * 10};")
                    if self.Cn == 1:
                        gcode.append("M30;")  # 结束
                elif a < (self.Cn - 1):
                    gcode.append(f"G01 U[{self.Tr * 2} * #521] F{self.F};")
                    gcode.append(f"G01 U[{Cr} * #511 * -1] W[{self.L} * #520] F{self.F};")
                    gcode.append(f"G00 U[{self.Tr} * #521 * -1] F{self.F};")
                    gcode.append(f"G01 U[{Cr} * #511] W[{self.L} * #520 * -1] F{self.F * 10};")
                else:
                    gcode.append(f"G01 U[{self.Tr * 2} * #521] F{self.F};")
                    gcode.append(f"G01 U[{Cr} * #511 * -1] W[{self.L} * #520] F{self.F};")
                    gcode.append(f"G00 U[{self.Tr} * #521 * -1] F{self.F};")
                    gcode.append(f"G01 U[{Cr} * #511] W[{self.L} * #520 * -1] F{self.F * 10};")
                    gcode.append(f"G00 U[{self.Tr * (self.Cn - 1)} * #521 * -1] F{self.F};")
                    gcode.append("M30;")  # 结束

        elif self.G71G73 == 'G71':  # G71 加工模式
            gcode.append("O200;")
            gcode.append("G28")  # 复位
            gcode.append(f"G71 U{self.Tr} R{self.Tr / 2} F{self.F};")
            gcode.append("G71 P80 Q120 U0.2 W0.2 J1 K1;")
            gcode.append(f"N80 G00 U{self.Tr * self.Cn * self.xDir};")
            gcode.append(f"G01 U{self.Tr * self.Cn * -1 * self.xDir} W{self.L * self.zDir};")
            gcode.append("N120;")
            gcode.append("M30;")  # 结束

        return "\n".join(gcode)


class InnerHole3Process(P):
    """
    处理内孔切槽的 G 代码生成类。

    该类用于根据不同的加工参数生成相应的 G 代码指令。
    方法:
    - generate_gcode(): 根据传入的参数生成相应的 G 代码字符串。
    """

    def __init__(self, sub_process_type: str, W: float, Tw: float, Cn: int, Lr: float, Tr: float, F: float,  **kwargs):
        """
        初始化内槽 G 代码生成器。

        参数:
        - W (float): 开口宽度（必选）。
        - Tw (float): 切槽刀具宽度（必选）。
        - Cn (int): 切槽次数（必选）。
        - Lr (float): 切槽深度（必选）。
        - Tr (float): 进刀深度（必选）。
        - F (float): 进给速度（必选）。
        """
        super().__init__(sub_process_type, **kwargs)
        self.W = float(W)
        self.Tw = float(Tw)
        self.Cn = int(Cn)
        self.Lr = float(Lr)
        self.Tr = float(Tr)
        self.F = float(F)
    def generate_gcode(self) -> str:
        """
        生成内槽的 G 代码。

        根据切槽的开口宽度、刀具宽度、切槽次数等参数生成相应的 G 代码。

        返回:
        - str: 生成的 G 代码字符串。
        """
        gcode = []
        Wn = int(self.W // self.Tw)  # 切槽次数（刀具宽度整除）
        remainW = self.W % self.Tw  # 剩余宽度
        if remainW != 0:
            Wn += 1  # 如果有剩余宽度，增加一次切槽

        if self.W < self.Tw:
            gcode.append("warning: The opening width is less than the tool width")
        else:
            for w in range(Wn):
                for a in range(self.Cn):
                    if a == 0:
                        gcode.append("O200;")
                        gcode.append("G28")  # 复位
                        gcode.append(f"G01 U[{self.Tr} * #520] F{self.F};")
                        gcode.append(f"G00 U[{self.Tr} * #520 * -1] F{self.F};")
                        if self.Cn == 1 and w == Wn - 1:
                            gcode.append("M30;")  # 结束
                    elif a < (self.Cn - 1):
                        gcode.append(f"G01 U[{self.Tr * 2} * #520] F{self.F};")
                        gcode.append(f"G00 U[{self.Tr} * #520 * -1] F{self.F};")
                    else:
                        gcode.append(f"G01 U[{self.Tr * 2} * #520] F{self.F};")
                        gcode.append(f"G00 U[{self.Lr} * #520 * -1] F{self.F};")

                if w < Wn - 2:
                    gcode.append(f"G00 W[{self.Tw * -1}] F{self.F};")
                elif w < Wn - 1:
                    if remainW != 0:
                        gcode.append(f"G00 W[{remainW * -1}] F{self.F};")
                    else:
                        gcode.append(f"G00 W[{self.Tw * -1}] F{self.F};")
                else:
                    gcode.append(f"G00 W[{self.W - self.Tw}] F{self.F};")
                    gcode.append("M30;")  # 结束

        return "\n".join(gcode)


class InnerHole4Process(P):
    """
    处理内孔切割的 G 代码生成类。

    该类用于根据不同的加工参数生成相应的 G 代码指令。

    方法:
    - generate_gcode(): 根据传入的参数生成相应的 G 代码字符串。
    """

    def __init__(self, sub_process_type: str,  R: float, Tr: float, Cn: int, F: float, G2G3: int, PHi1: float, L: float,
                 **kwargs):
        """
        初始化内弧 G 代码生成器。

        参数:
        - R (float): 半径（必选）。
        - Tr (float): 每次进刀量（必选）。
        - Cn (int): 进刀次数（必选）。
        - F (float): 进给速度（必选）。
        - G2G3 (int): 切割方式，0表示顺时针(G02)，1表示逆时针(G03)。
        - PHi1 (float): X轴的增量位置（必选）。
        - L (float): Z轴的增量位置（必选）。
        """
        super().__init__(sub_process_type, **kwargs)
        self.R = float(R)
        self.Tr = float(Tr)
        self.Cn = int(Cn)
        self.F = float(F)
        self.G2G3 = int(G2G3)
        self.PHi1 = float(PHi1)
        self.L = float(L)

    def generate_gcode(self) -> str:
        """
        生成内弧的 G 代码。

        根据切割参数生成相应的 G 代码，包括顺时针或逆时针的切圆弧指令。

        返回:
        - str: 生成的 G 代码字符串。
        """
        gcode = []
        delta_x = self.PHi1
        delta_z = self.L

        if self.G2G3 == 0:  # 顺时针切割 G02
            gcode.append("O0300;")
            gcode.append("G28")  # 复位

            for a in range(self.Cn):
                # 左进刀
                gcode.append(f"G01 W{-self.Tr} F{self.F};")
                # 切圆弧
                gcode.append(f"G02 U[{delta_x * -1}] W{delta_z * -1} R{self.R} F{self.F};")
                # Z轴退刀
                if a + 1 == self.Cn:  # 最后一刀，退刀到起点
                    gcode.append(f"G00 W{delta_z + self.Tr * self.Cn};")
                else:  # 正常退刀
                    gcode.append(f"G00 W{delta_z};")
                # X轴退刀
                gcode.append(f"G00 U[{delta_x}];")

            gcode.append("M30;")  # 结束
        else:  # 逆时针切割 G03
            gcode.append("O0300;")
            gcode.append("G28")  # 复位

            for a in range(self.Cn):
                # 左进刀
                gcode.append(f"G01 W{-self.Tr} F{self.F};")
                # 切圆弧
                gcode.append(f"G03 U[{delta_x * -1}] W{delta_z * -1} R{self.R} F{self.F};")
                # Z轴退刀
                if a + 1 == self.Cn:  # 最后一刀，退刀到起点
                    gcode.append(f"G00 W{delta_z + self.Tr * self.Cn};")
                else:  # 正常退刀
                    gcode.append(f"G00 W{delta_z};")
                # X轴退刀
                gcode.append(f"G00 U[{delta_x}];")

            gcode.append("M30;")  # 结束

        return "\n".join(gcode)


class InnerHole5Process(P):
    """
    处理内孔切割的 G 代码生成类，主要用于根据不同的参数生成 `innerHole5` 的 G 代码指令。

    参数:
    - Cn (int): 进刀次数（必选）。
    - deltaT (float): 每次进刀的增量（必选）。
    - F (float): 进给速度（必选）。
    - BT (float): 退刀时的增量（必选）。
    - L (float): 最终的退刀位置（必选）。

    方法:
    - generate_gcode(): 根据传入的参数生成相应的 G 代码字符串。
    """

    def __init__(self, sub_process_type: str, Cn: int, deltaT: float, F: float, BT: float, L: float,  **kwargs):
        """
        初始化内圆 G 代码生成器。

        参数:
        - Cn (int): 进刀次数（必选）。
        - deltaT (float): 每次进刀的增量（必选）。
        - F (float): 进给速度（必选）。
        - BT (float): 退刀时的增量（必选）。
        - L (float): 最终的退刀位置（必选）。
        """
        super().__init__(sub_process_type, **kwargs)
        self.Cn = int(Cn)
        self.deltaT = float(deltaT)
        self.F = float(F)
        self.BT = float(BT)
        self.L = float(L)

    def generate_gcode(self) -> str:
        """
        生成内圆的 G 代码。

        根据切割参数生成相应的 G 代码。

        返回:
        - str: 生成的 G 代码字符串。
        """
        gcode = []
        for a in range(self.Cn):
            if a == 0:
                gcode.append("O200;")  # 第一刀开始
                gcode.append("G28")  # 复位

                # 进刀
                gcode.append(f"G01 W[{self.deltaT} * #521] F{self.F};")

                # 退刀
                if self.Cn == 1:
                    gcode.append(f"G00 W[{self.deltaT} * #521 * -1] F{self.F};")
                else:
                    gcode.append(f"G00 W[{self.BT} * #521 * -1] F{self.F};")

                if self.Cn == 1:
                    gcode.append("M30;")  # 结束
            elif a < (self.Cn - 1):
                # 中间刀
                gcode.append(f"G01 W[{(self.deltaT + self.BT)} * #521] F{self.F};")
                gcode.append(f"G00 W[{self.BT} * #521 * -1] F{self.F};")
            else:
                # 最后一刀
                gcode.append(f"G01 W[{(self.deltaT + self.BT)} * #521] F{self.F};")
                gcode.append(f"G00 W[{self.L} * #521 * -1] F{self.F};")
                gcode.append("M30;")  # 结束

        return "\n".join(gcode)
