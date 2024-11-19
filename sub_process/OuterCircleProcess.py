import logging
import math

from component.common import P
logger = logging.getLogger(__name__)

class OuterCircle1Process(P):
    def __init__(self, sub_process_type: str, Cn: int, L: float, Tr: float, Cr: float, F: float, **kwargs):
        """
        初始化外圆工艺加工过程的参数。

        参数:
            sub_process_type (str): 子工艺类型。
            Cn (int): 圆圈数量。
            L (float): 长度。
            Tr (float): 过渡半径。
            Cr (float): 退回半径。
            F (float): 进给速度。
        """
        super().__init__(sub_process_type, **kwargs)
        self.sub_process_type = sub_process_type
        self.Cn = Cn  # 圆圈数量
        self.L = L  # 长度
        self.Tr = Tr  # 过渡半径
        self.Cr = Cr  # 退回半径
        self.F = F  # 进给速度
        # 输出当前属性值
        self.print_attributes()

    def print_attributes(self):
        """打印当前对象的属性值。"""
        logger.info("外圆子工艺 属性初始化:")
        logger.info(f"  工艺类型: {self.sub_process_type}")
        logger.info(f"  Cn (int): 圆圈数量: {self.Cn}")
        logger.info(f"  L (float): 长度: {self.L}")
        logger.info(f"  Tr (float): 过渡半径: {self.Tr}")
        logger.info(f"  Cr (float): 退回半径: {self.Cr}")
        logger.info(f"  F (float): 进给速度: {self.F}")

    def generate_gcode(self) -> str:
        """
        根据外圆工艺参数生成 G 代码。

        返回:
            str: 生成的 G 代码。
        """
        gcode = ""

        # 确保 self.Cn 是整数
        try:
            self.Cn = int(self.Cn)
        except ValueError:
            raise ValueError(f"Cn 的值 {self.Cn} 不是有效的整数")

        for a in range(self.Cn):
            if a == 0:
                # 第一圈的 G 代码生成逻辑
                gcode += f"G01 U[{self.Tr} * #521] F{self.F};\n"
                gcode += f"G01 W[{self.L} * #520] F{self.F};\n"
                gcode += f"G00 U[{self.Tr} * #521 * -1] F{self.F};\n"
                gcode += f"G00 W[{self.L} * #520 * -1] F{self.F};\n"

                if self.Cn == 1:
                    gcode += "G00 Z0;\n"  # 返回起始点
                    gcode += "M30;\n"  # 程序结束
            elif a < self.Cn - 1:
                # 中间圈的 G 代码生成逻辑
                gcode += f"G01 U[{self.Tr * 2} * #521] F{self.F};\n"
                gcode += f"G01 W[{self.L} * #520] F{self.F};\n"
                gcode += f"G00 U[{self.Tr} * #521 * -1] F{self.F};\n"
                gcode += f"G00 W[{self.L} * #520 * -1] F{self.F};\n"
            else:
                # 最后一圈的 G 代码生成逻辑
                gcode += f"G01 U[{self.Tr * 2} * #521] F{self.F};\n"
                gcode += f"G01 W[{self.L} * #520] F{self.F};\n"
                gcode += f"G00 U[{self.Cr} * #521 * -1] F{self.F};\n"
                gcode += f"G00 W[{self.L} * #520 * -1] F{self.F};\n"
                gcode += "G00 Z0;\n"  # 返回起始点
                gcode += "M30;\n"  # 程序结束

        return gcode


class OuterCircle2Process(P):
    def __init__(self, sub_process_type: str, Cn: int, Tr: float, F: float, L: float, A: float, xDir: int, zDir: int,
                 G71G73: str, **kwargs):
        """
        初始化外圆弧加工过程的参数。

        参数:
            sub_process_type (str): 子工艺类型。
            Cn (int): 圆圈数量。
            Tr (float): 过渡半径。
            F (float): 进给速度。
            L (float): 长度。
            A (float): 角度（用于计算切割半径）。
            xDir (int): X 轴方向。
            zDir (int): Z 轴方向。
            G71G73 (str): G71 或 G73 切换模式。
        """
        super().__init__(sub_process_type, **kwargs)
        self.sub_process_type = sub_process_type
        self.Cn = Cn
        self.Tr = Tr
        self.F = F
        self.L = L
        self.A = A
        self.xDir = xDir
        self.zDir = zDir
        self.G71G73 = G71G73

    def generate_gcode(self) -> str:
        """
        根据外圆弧加工参数生成 G 代码。

        返回:
            str: 生成的 G 代码。
        """
        gcode = ""
        tanA = math.tan(self.A / 180 * math.pi)
        Cr = self.L * tanA

        # 根据 G71/G73 切换逻辑生成不同的 G 代码
        if self.G71G73 == "G73":
            for a in range(self.Cn):
                if a == 0:
                    # 第一圈的 G 代码生成逻辑
                    gcode += f"G01 U[{self.Tr} * #521] F{self.F};\n"
                    gcode += f"G01 U[{Cr} * #511 * -1] W[{self.L} * #520] F{self.F};\n"
                    gcode += f"G01 U[{self.Tr} * #521 * -1] F{self.F};\n"
                    gcode += f"G01 U[{Cr} * #511] W[{self.L} * #520 * -1] F{self.F * 10};\n"
                elif a < (self.Cn - 1):
                    # 中间圈的 G 代码生成逻辑
                    gcode += f"G01 U[{self.Tr * 2} * #521] F{self.F};\n"
                    gcode += f"G01 U[{Cr} * #511 * -1] W[{self.L} * #520] F{self.F};\n"
                    gcode += f"G00 U[{self.Tr} * #521 * -1] F{self.F};\n"
                    gcode += f"G01 U[{Cr} * #511] W[{self.L} * #520 * -1] F{self.F * 10};\n"
                else:
                    # 最后一圈的 G 代码生成逻辑
                    gcode += f"G01 U[{self.Tr * 2} * #521] F{self.F};\n"
                    gcode += f"G01 U[{Cr} * #511 * -1] W[{self.L} * #520] F{self.F};\n"
                    gcode += f"G00 U[{self.Tr} * #521 * -1] F{self.F};\n"
                    gcode += f"G01 U[{Cr} * #511] W[{self.L} * #520 * -1] F{self.F * 10};\n"
                    gcode += f"G00 U[{self.Tr} * #521 * -1] F{self.F * (a)};\n"  # 为每次循环调整 U 值
                gcode += "M30;\n"  # 程序结束

        elif self.G71G73 == "G71":
            # G71 模式的 G 代码生成逻辑
            gcode += f"G71 U{self.Tr} R{self.Tr / 2} F{self.F};\n"
            gcode += "G71 P80 Q120 U0.2 W0.2 J1 K1;\n"
            gcode += f"N80 G00 U{self.Tr * self.Cn * self.xDir};\n"
            gcode += f"G01 U{self.Tr * self.Cn * -1 * self.xDir} W{self.L * self.zDir};\n"
            gcode += "N120;\n"
            gcode += "M30;\n"  # 程序结束

        return gcode


class OuterCircle3Process(P):
    def __init__(self, sub_process_type: str, R: float, Tr: float, Cn: int, F: float, G2G3: int, PHi1: float, L: float,
                 **kwargs):
        """
        初始化外锥面加工的参数。

        参数:
            sub_process_type (str): 子工艺类型。
            R (float): 半径。
            Tr (float): 过渡半径。
            Cn (int): 圆圈数量。
            F (float): 进给速度。
            G2G3 (int): 1表示G2（顺时针圆弧），3表示G3（逆时针圆弧）。
            PHi1 (float): 第一个角度增量。
            L (float): 长度。
        """
        super().__init__(sub_process_type, **kwargs)
        self.sub_process_type = sub_process_type
        self.R = float(R)  # 确保是浮动类型
        self.Tr = float(Tr)  # 确保是浮动类型
        self.Cn = int(Cn)  # 确保是整数类型
        self.F = float(F)  # 确保是浮动类型
        self.G2G3 = int(G2G3)  # 确保是整数类型
        self.PHi1 = float(PHi1)  # 确保是浮动类型
        self.L = float(L)  # 确保是浮动类型

    def generate_gcode(self) -> str:
        """
        根据外圆3工艺参数生成 G 代码。

        返回:
            str: 生成的 G 代码。
        """
        gcode = []
        delta_x = self.PHi1
        delta_z = self.L
        r = self.R
        tr = self.Tr
        cn = self.Cn
        f = self.F
        g2g3 = self.G2G3

        # G2/G3 模式
        if g2g3 == 1:
            gcode.append("O0300;")
            gcode.append("G28")  # 回原点

            for a in range(cn):
                gcode.append(f"G01 W{-tr} F{f};")

                gcode.append(
                    f"G02 U[{delta_x}] W{delta_z * -1} R{r} F{f};" if g2g3 == 1 else f"G03 U[{delta_x}] W{delta_z * -1} R{r} F{f};")

                if a + 1 == cn:
                    gcode.append(f"G00 W{delta_z + tr * cn};")
                else:
                    gcode.append(f"G00 W{delta_z};")

                gcode.append(f"G00 U[{delta_x * -1}];")

            gcode.append("M30;")  # 程序结束

        else:  # G71 模式
            gcode.append("O0300;")
            gcode.append("G28")  # 回原点
            gcode.append(f"G71 U{tr} R{tr / 2} F{f};")
            gcode.append("G71 P80 Q120 U0.2 W0.2 J1 K1;")
            gcode.append(f"N80 G00 U{tr * cn * -1};")
            gcode.append(
                f"G02 U{tr * cn} W{delta_z * -1} R{r};" if g2g3 == 1 else f"G03 U{tr * cn} W{delta_z * -1} R{r};")
            gcode.append("N120;")
            gcode.append("M30;")  # 程序结束

        return "\n".join(gcode)
