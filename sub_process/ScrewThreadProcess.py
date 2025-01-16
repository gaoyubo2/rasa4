import math
import re

from component.common import P
import math

SQRT_2 = 1.4142135623730950


class ScrewThread1Process(P):
    """
    该类用于生成外直螺纹加工的 GCode，基于提供的工艺参数生成相应的 GCode。
    """

    def __init__(self, sub_process_type: str, L: float, Tr: float, Tp: float, Cn: int, Cr: float, multi_head: int,
                 tailLength: float,
                 cuttingDepthSelection: float, **kwargs):
        """
        初始化外直螺纹加工过程的参数。

        参数:
            L (float): 螺纹加工的长度。
            Tr (float): 进刀量。
            Tp (float): 螺距。
            Cn (int): 螺纹加工的切削次数。
            Cr (float): 螺纹的根部直径。
            multi_head (int): 多头加工数量。
            tailLength (float): 退尾长度，单位是螺距个数。
            cuttingDepthSelection (float): 切削深度选择，用于决定等距或递减进刀。
        """
        super().__init__(sub_process_type, **kwargs)
        self.L = float(L)
        self.Tr = float(Tr)
        self.Tp = float(Tp)
        self.Cn = int(re.search(r'\d+', str(Cn)).group())
        self.Cr = float(Cr)
        self.multi_head = int(re.search(r'\d+', str(multi_head)).group())
        self.tailLength = float(tailLength)
        self.cuttingDepthSelection = float(cuttingDepthSelection)

    def generate_gcode(self) -> str:
        """
        根据工艺参数生成螺纹加工的 GCode。

        返回:
            str: 生成的 GCode 字符串。
        """
        gcode = []
        tr = self.Tr  # 进刀量
        f = self.Tp  # 螺距
        cn = self.Cn  # 切削次数
        cr = self.Cr  # 螺纹根部直径
        m_h = self.multi_head  # 多头加工数量
        tail_z = self.tailLength  # 退尾长度
        cutting_depth_selection = self.cuttingDepthSelection  # 切削深度选择

        # 多头加工时，每个头对应的角度
        m_h_angle = 360 / m_h
        tr_calc = 0  # 进刀量
        mid_val = 0  # 中间变量

        # 判断是否有退尾
        have_tail = 0 if tail_z < 0.1 else 1
        if have_tail:
            tail_z = tail_z * f  # 长轴退尾量计算

        # 初始化q和textHeadFlag
        q = 0

        # 生成G-code头部
        gcode.append("O200;")
        gcode.append("G28")  # 返回机器原点

        # 如果没有退尾，直接设置为0
        if have_tail == 0:
            gcode.append(f"G01 U{tr * -1} F{f}")  # 进刀
        else:
            gcode.append(f"G01 U{tr * -1} F{f}")  # 进刀并有退尾

        for m in range(m_h):  # 多头循环
            q = m_h_angle * m
            mid_val = 0
            for a in range(cn):
                if cutting_depth_selection < 0.5:  # 等距进刀
                    tr_calc = tr * (a + 1) * -1
                else:  # 递减进刀
                    tr_calc = tr_calc / SQRT_2 + mid_val
                    mid_val = tr_calc
                    if a + 1 == cn:
                        tr_calc = cr * -1

                # 进刀
                gcode.append(f"G01 U{tr_calc} F{f}")

                # 切螺纹
                gcode.append(f"G32 W[{self.L} * #520] F{f} Q{q * 1000}")

                # X退刀
                gcode.append(f"G00 U{tr * -1 + tr}")

                # Z退刀
                gcode.append(f"G00 W[{self.L} * #520 * -1]")

                # X向上归位到起始点
                gcode.append(f"G00 U{tr * -1}")

        # 结束部分
        gcode.append("M30;")  # 程序结束

        return "\n".join(gcode)  # 返回生成的 GCode 字符串


class ScrewThread2Process(P):
    """
    该类用于生成外锥（管）螺纹加工的 GCode，基于提供的工艺参数生成相应的 GCode。
    """

    def __init__(self, sub_process_type: str, L: float, Tr: float, Tp: float, Cn: int, A: float, tailLength: float,
                 startA: float,
                 **kwargs):
        """
        初始化外锥（管）螺纹加工过程的参数。

        参数:
            L (float): 螺纹加工的长度。
            Tr (float): 进刀量。
            Tp (float): 螺距。
            Cn (int): 螺纹加工的切削次数。
            A (float): 螺纹的角度（以度为单位）。
            tailLength (float): 退尾长度，单位是螺距个数。
            startA (float): 起始角度。
        """
        super().__init__(sub_process_type, **kwargs)
        self.L = float(L)
        self.Tr = float(Tr)
        self.Tp = float(Tp)
        self.Cn = int(re.search(r'\d+', str(Cn)).group())
        self.A = float(A)
        self.tailLength = float(tailLength)
        self.startA = float(startA)

    def generate_gcode(self) -> str:
        """
        根据工艺参数生成螺纹加工的 GCode。

        返回:
            str: 生成的 GCode 字符串。
        """
        gcode = []
        tr = self.Tr  # 进刀量
        f = self.Tp  # 螺距
        cn = self.Cn  # 切削次数
        A = self.A  # 螺纹角度
        l = self.L  # 螺纹长度
        tanA = math.tan(math.radians(A))  # 转换角度为弧度，并计算tan值
        cr = l * tanA  # 计算螺纹的根部直径
        q = self.startA  # 起始角度

        tail_z = self.tailLength  # 退尾长度
        cutting_depth_selection = self.Tp  # 切削深度选择，用于决定等距或递减进刀

        # 判断是否有退尾
        have_tail = 0 if tail_z < 0.1 else 1
        if have_tail:
            tail_z = tail_z * f  # 长轴退尾量计算

        # 初始化
        gcode.append("O200;")
        gcode.append("G28")  # 返回机器原点

        # 生成G-code主循环
        if have_tail == 0:  # 没有退尾
            for a in range(cn):
                # 进刀
                gcode.append(f"G01 U{tr * (a + 1) * -1} F{f}")

                # 切螺纹
                gcode.append(f"G32 U[{cr} * #511] W[{l} * #520] F{f} Q{q * 1000}")

                # X退刀
                gcode.append(f"G00 U{tr * (a + 2)}")

                # 斜向上退刀
                gcode.append(f"G01 U[{cr} * #511 * -1] W[{l} * #520 * -1] F{f * 10}")

                # X向上归位到起始点
                gcode.append(f"G00 U{tr * -1}")
        else:  # 有退尾的情况
            for a in range(cn):
                # 进刀
                gcode.append(f"G01 U{tr * (a + 1) * -1} F{f}")

                # 切螺纹
                gcode.append(f"G32 U[{cr} * #511] W[{l} * #520] F{f} Q{q * 1000} J[{tr * (a + 1)} / #511] K{tail_z}")

                # X退刀
                gcode.append(f"G00 U{tr}")

                # 斜向上退刀
                gcode.append(f"G01 U[{cr} * #511 * -1] W[{l} * #520 * -1] F{f * 10}")

                # X向上归位到起始点
                gcode.append(f"G00 U{tr * -1}")

        # 结束部分
        gcode.append("M30;")  # 程序结束

        return "\n".join(gcode)  # 返回生成的 GCode 字符串


class ScrewThread3Process(P):
    """
    该类用于生成内直螺纹加工的 GCode，基于提供的工艺参数生成相应的 GCode。
    """

    def __init__(self, sub_process_type: str, L: float, Tr: float, Tp: float, Cn: int, startA: float, tailLength: float,
                 **kwargs):
        """
        初始化内直螺纹加工过程的参数。

        参数:
            L (float): 螺纹加工的长度。
            Tr (float): 进刀量。
            Tp (float): 螺距。
            Cn (int): 螺纹加工的切削次数。
            startA (float): 起始角度。
            tailLength (float): 退尾长度，单位是螺距个数。
        """
        super().__init__(sub_process_type, **kwargs)
        self.L = float(L)
        self.Tr = float(Tr)
        self.Tp = float(Tp)
        self.Cn = int(re.search(r'\d+', str(Cn)).group())
        self.startA = float(startA)
        self.tailLength = float(tailLength)

    def generate_gcode(self) -> str:
        """
        根据工艺参数生成螺纹加工的 GCode。

        返回:
            str: 生成的 GCode 字符串。
        """
        gcode = []
        tr = self.Tr  # 进刀量
        f = self.Tp  # 螺距
        cn = self.Cn  # 切削次数
        q = self.startA  # 起始角度

        tail_z = self.tailLength  # 退尾长度
        have_tail = 0 if tail_z < 0.1 else 1  # 判断是否有退尾

        # 如果有退尾，退尾长度是螺距乘以退尾的数量
        if have_tail:
            tail_z = tail_z * f  # 长轴退尾量计算

        # 初始化 GCode
        gcode.append("O200;")
        gcode.append("G28")  # 返回机器原点

        # 生成G-code主循环
        if have_tail == 0:  # 没有退尾
            for a in range(cn):
                # 进刀
                gcode.append(f"G01 U{tr * (a + 1)} F{f}")

                # 切螺纹
                gcode.append(f"G32 W[{self.L} * #520] F{f} Q{q * 1000}")

                # X退刀
                gcode.append(f"G00 U{tr * (a + 2) * -1} F{f}")

                # Z退刀
                gcode.append(f"G00 W[{self.L} * #520 * -1]")

                # X向下归位到起始点
                gcode.append(f"G00 U{tr}")

        else:  # 有退尾的情况
            for a in range(cn):
                # 进刀
                gcode.append(f"G01 U{tr * (a + 1)} F{f}")

                # 切螺纹
                gcode.append(f"G32 W[{self.L} * #520] F{f} Q{q * 1000} J[{tr * (a + 1) * -1}] K{tail_z}")

                # X退刀
                gcode.append(f"G00 U{tr * -1}")

                # Z退刀
                gcode.append(f"G00 W[{self.L} * #520 * -1]")

                # X向下归位到起始点
                gcode.append(f"G00 U{tr}")

        # 结束部分
        gcode.append("M30;")  # 程序结束

        return "\n".join(gcode)  # 返回生成的 GCode 字符串


class ScrewThread4Process(P):
    """
    用于生成内锥（管）螺纹加工的 GCode，基于提供的加工参数生成相应的 GCode。
    """

    def __init__(self, sub_process_type: str, L: float, Tr: float, Tp: float, Cn: int, startA: float, A: float,
                 tailLength: float,
                 **kwargs):
        """
        初始化内锥（管）螺纹加工过程的参数。

        参数:
            L (float): 螺纹长度。
            Tr (float): 进刀量。
            Tp (float): 螺距。
            Cn (int): 螺纹加工的切削次数。
            startA (float): 起始角度。
            A (float): 角度，用于计算螺纹的倾斜量。
            tailLength (float): 退尾长度，以螺距为单位，可以是小数。
        """
        super().__init__(sub_process_type, **kwargs)
        self.L = float(L)
        self.Tr = float(Tr)
        self.Tp = float(Tp)
        self.Cn = int(re.search(r'\d+', str(Cn)).group())
        self.startA = float(startA)
        self.A = float(A)
        self.tailLength = float(tailLength)

    def generate_gcode(self) -> str:
        """
        根据工艺参数生成内锥（管）螺纹加工的 GCode。

        返回:
            str: 生成的 GCode 字符串。
        """
        gcode = []
        tr = self.Tr
        f = self.Tp
        cn = self.Cn
        tanA = math.tan(math.radians(self.A))
        cr = self.L * tanA
        q = self.startA

        tail_z = self.tailLength  # 退尾长度
        have_tail = 0 if tail_z < 0.1 else 1  # 判断是否有退尾

        # 如果有退尾，退尾长度是螺距乘以退尾的数量
        if have_tail:
            tail_z = tail_z * f  # 长轴退尾量计算

        # 初始化 GCode
        gcode.append("O200;")
        gcode.append("G28")  # 返回机器原点

        # 主循环生成G-code
        if have_tail == 0:  # 没有退尾
            for a in range(cn):
                # 进刀下
                gcode.append(f"G01 U{tr * (a + 1)} F{f}")

                # 切螺纹
                gcode.append(f"G32 U[{cr} * #511 * -1] W[{self.L} * #520] F{f} Q{q * 1000}")

                # X退刀
                gcode.append(f"G00 U{tr * (a + 2) * -1}")

                # 斜向下退刀
                gcode.append(f"G01 U[{cr} * #511] W[{self.L} * #520 * -1] F{f * 10}")

                # X向下归位到起始点
                gcode.append(f"G00 U{tr}")

        else:  # 有退尾的情况
            for a in range(cn):
                # 进刀
                gcode.append(f"G01 U{tr * (a + 1)} F{f}")

                # 切螺纹
                gcode.append(
                    f"G32 U[{cr} * #511 * -1] W[{self.L} * #520] F{f} Q{q * 1000} J[{tr * (a + 1) * -1} / #511] K{tail_z}")

                # X退刀
                gcode.append(f"G00 U{tr * -1}")

                # 斜向下退刀
                gcode.append(f"G01 U[{cr} * #511] W[{self.L} * #520 * -1] F{f * 10}")

                # X向上归位到起始点
                gcode.append(f"G00 U{tr}")

        # 结束部分
        gcode.append("M30;")  # 程序结束

        return "\n".join(gcode)  # 返回生成的 GCode 字符串
