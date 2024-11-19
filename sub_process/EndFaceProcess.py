from component.common import P


class EndFace1Process(P):
    """
    处理端面工艺（End Face Process）的 G 代码生成类。

    该类用于生成端面加工的 G 代码，根据不同的加工参数生成相应的 G 代码指令，支持 G71 和 G73 模式。

    方法:
    - generate_gcode(): 根据传入的参数生成相应的 G 代码，支持 G71 和 G73 两种模式，返回生成的 G 代码字符串。

    使用工艺:
    - 该类适用于端面加工（End Face Processing），常用于车床等数控机床的加工程序生成。
    """

    def __init__(self, sub_process_type: str, Cn: int, Lr: float, deltaT: float, CT: float, F: float, **kwargs):
        """
        初始化端面工艺类。

        参数:
        - process_type (str): 工艺类型，必选，决定工艺处理的方式。
        - Cn (int): 进刀次数，必选，表示进刀轮数。
        - Lr (float): 退刀量，必选，表示每次退刀的距离。
        - deltaT (float): 进刀量，必选，表示每次进刀的深度。
        - CT (float): 最后一次进刀的退刀量，必选。
        - F (float): 进给速度，必选，单位为 mm/min。
        - **kwargs (dict): 可选的其他参数，由父类 `P` 处理。

        """
        super().__init__(sub_process_type, **kwargs)
        self.Cn = Cn
        self.Lr = Lr
        self.deltaT = deltaT
        self.CT = CT
        self.F = F

    def generate_gcode(self) -> str:
        """
        生成端面加工的 G 代码。
        """
        gcode = []
        Cn = self.Cn
        Lr = self.Lr
        deltaT = self.deltaT
        CT = self.CT
        F = self.F

        for a in range(Cn):
            if a == 0:
                gcode.append("O200;")
                gcode.append("G28")  # Home the machine

                gcode.append(f"G01 W[{deltaT} * #521] F{F};")
                gcode.append(f"G01 U[{Lr} * #520] F{F};")
                gcode.append(f"G00 W[{deltaT} * #521 * -1] F{F};")
                gcode.append(f"G00 U[{Lr} * #520 * -1] F{F};")

                if Cn == 1:
                    gcode.append("M30;")  # End of program

            elif a < Cn - 1:
                gcode.append(f"G01 W[{deltaT * 2} * #521] F{F};")
                gcode.append(f"G01 U[{Lr} * #520] F{F};")
                gcode.append(f"G00 W[{deltaT} * #521 * -1] F{F};")
                gcode.append(f"G00 U[{Lr} * #520 * -1] F{F};")

            else:  # Last iteration
                gcode.append(f"G01 W[{deltaT * 2} * #521] F{F};")
                gcode.append(f"G01 U[{Lr} * #520] F{F};")
                gcode.append(f"G00 W[{CT} * #521 * -1] F{F};")
                gcode.append(f"G00 U[{Lr} * #520 * -1] F{F};")
                gcode.append("M30;")  # End of program

        return "\n".join(gcode)


class EndFace2Process(P):
    """
    处理端面工艺（End Face Process）第二种方式的 G 代码生成类。

    该类用于生成端面加工的 G 代码，根据不同的加工参数生成相应的 G 代码指令。
    支持 G71 和 G73 模式，根据进刀次数、宽度、进给速度等参数生成相应的 G 代码。

    参数:
    - W (float): 加工宽度，表示端面加工的总宽度（必选）。
    - Tw (float): 刀具宽度，表示每次加工的切削宽度（必选）。
    - Cn (int): 进刀次数，表示端面加工的进刀次数（必选）。
    - Lr (float): 退刀量，表示每次退刀的距离（必选）。
    - Tr (float): 每次进刀的深度（必选）。
    - F (float): 进给速度，单位 mm/min（必选）。
    - **kwargs (dict): 其他工艺相关参数，继承父类 `P` 使用。

    方法:
    - generate_gcode(): 根据传入的参数生成相应的 G 代码字符串。
    """

    def __init__(self,sub_process_type: str, W: float, Tw: float, Cn: int, Lr: float, Tr: float, F: float, **kwargs):
        """
        初始化端面加工 G 代码生成器。

        参数:
        - W (float): 加工宽度（必选）。
        - Tw (float): 刀具宽度（必选）。
        - Cn (int): 进刀次数（必选）。
        - Lr (float): 退刀量（必选）。
        - Tr (float): 每次进刀的深度（必选）。
        - F (float): 进给速度（必选）。
        - **kwargs (dict): 其他工艺相关参数（可选）。
        """
        super().__init__(sub_process_type, **kwargs)
        self.W = W
        self.Tw = Tw
        self.Cn = Cn
        self.Lr = Lr
        self.Tr = Tr
        self.F = F

    def generate_gcode(self) -> str:
        """
        生成端面加工的 G 代码。

        根据进刀次数、退刀量、进给速度等参数生成相应的 G 代码指令，并将其返回为字符串。

        返回:
        - str: 生成的 G 代码字符串。
        """
        gcode = []
        Wn = int(self.W / self.Tw)
        remainW = self.W % self.Tw

        if remainW != 0:
            Wn += 1

        for w in range(Wn):
            for a in range(self.Cn):
                if a == 0:
                    # Header and start
                    gcode.append("O200;")
                    gcode.append("G28")  # Home the machine
                    gcode.append(f"G01 U[{self.Tr} * #520] F{self.F};")
                    gcode.append(f"G00 U[{self.Tr} * #520 * -1] F{self.F};")
                    if self.Cn == 1 and w == Wn - 1:
                        gcode.append("M30;")  # End of program
                elif a < (self.Cn - 1):
                    gcode.append(f"G01 U[{self.Tr * 2} * #520] F{self.F};")
                    gcode.append(f"G00 U[{self.Tr} * #520 * -1] F{self.F};")
                else:
                    gcode.append(f"G01 U[{self.Tr * 2} * #520] F{self.F};")
                    gcode.append(f"G00 U[{self.Lr} * #520 * -1] F{self.F};")

            if w < Wn - 2:
                gcode.append(f"G00 W[{-self.Tw}] F{self.F};")
            elif w < Wn - 1:
                if remainW != 0:
                    gcode.append(f"G00 W[{-remainW}] F{self.F};")
                else:
                    gcode.append(f"G00 W[{-self.Tw}] F{self.F};")
            else:
                gcode.append(f"G00 W[{self.W - self.Tw}] F{self.F};")
                gcode.append("M30;")  # End of program

        return "\n".join(gcode)


class EndFace3Process(P):
    """
    处理端面工艺（End Face Process）第三种方式的 G 代码生成类。

    该类用于生成端面加工的 G 代码，根据不同的加工参数生成相应的 G 代码指令。
    支持 G71 和 G73 模式，根据进刀次数、进给速度等参数生成相应的 G 代码。

    参数:
    - Cn (int): 进刀次数，表示端面加工的进刀次数（必选）。
    - Lr (float): 退刀量，表示每次退刀的距离（必选）。
    - deltaT (float): 每次进刀的深度（必选）。
    - CT (float): 最后一次进刀的退刀量（必选）。
    - F (float): 进给速度，单位 mm/min（必选）。
    - **kwargs (dict): 其他工艺相关参数，继承父类 `P` 使用。

    方法:
    - generate_gcode(): 根据传入的参数生成相应的 G 代码字符串。
    """

    def __init__(self, sub_process_type: str, Cn: int, Lr: float, deltaT: float, CT: float, F: float,  **kwargs):
        """
        初始化端面加工 G 代码生成器。

        参数:
        - Cn (int): 进刀次数（必选）。
        - Lr (float): 退刀量（必选）。
        - deltaT (float): 每次进刀的深度（必选）。
        - CT (float): 最后一次进刀的退刀量（必选）。
        - F (float): 进给速度（必选）。
        - **kwargs (dict): 其他工艺相关参数（可选）。
        """
        super().__init__(sub_process_type, **kwargs)
        self.Cn = Cn
        self.Lr = Lr
        self.deltaT = deltaT
        self.CT = CT
        self.F = F

    def generate_gcode(self) -> str:
        """
        生成端面加工的 G 代码。

        根据进刀次数、退刀量、进给速度等参数生成相应的 G 代码指令，并将其返回为字符串。

        返回:
        - str: 生成的 G 代码字符串。
        """
        gcode = []
        for a in range(self.Cn):
            if a == 0:
                # Header and start
                gcode.append("O200;")
                gcode.append("G28")  # Home the machine
                gcode.append(f"G01 W[{self.deltaT} * #521] F{self.F};")
                gcode.append(f"G01 U[{self.Lr} * #520] F{self.F};")
                gcode.append(f"G00 W[{self.deltaT} * #521 * -1] F{self.F};")
                gcode.append(f"G00 U[{self.Lr} * #520 * -1] F{self.F};")
                if self.Cn == 1:
                    gcode.append("M30;")  # End of program
            elif a < (self.Cn - 1):
                gcode.append(f"G01 W[{self.deltaT * 2} * #521] F{self.F};")
                gcode.append(f"G01 U[{self.Lr} * #520] F{self.F};")
                gcode.append(f"G00 W[{self.deltaT} * #521 * -1] F{self.F};")
                gcode.append(f"G00 U[{self.Lr} * #520 * -1] F{self.F};")
            else:
                gcode.append(f"G01 W[{self.deltaT * 2} * #521] F{self.F};")
                gcode.append(f"G01 U[{self.Lr} * #520] F{self.F};")
                gcode.append(f"G00 W[{self.CT} * #521 * -1] F{self.F};")
                gcode.append(f"G00 U[{self.Lr} * #520 * -1] F{self.F};")
                gcode.append("M30;")  # End of program

        return "\n".join(gcode)