# gcode_generator.py

from abc import ABC, abstractmethod

from sub_process.ChamferProcess import Chamfer1Process, Chamfer2Process, Chamfer3Process, Chamfer4Process
from sub_process.ConeFaceProcess import ConeFace1Process, ConeFace2Process, ConeFace3Process, ConeFace4Process
from sub_process.EndFaceProcess import EndFace1Process, EndFace2Process, EndFace3Process
from sub_process.InnerHoleProcess import InnerHole1Process, InnerHole2Process, InnerHole3Process, InnerHole4Process, \
    InnerHole5Process
from sub_process.OuterCircleProcess import OuterCircle1Process, OuterCircle2Process, OuterCircle3Process
from sub_process.ScrewThreadProcess import ScrewThread1Process, ScrewThread2Process, ScrewThread3Process, \
    ScrewThread4Process



# 工厂

def get_process_instance(sub_process_type: str, **kwargs):
    """
    根据工艺类型创建相应的工艺实例。
    """

    # 创建并返回工艺实例
    if sub_process_type == "外圆":
        return OuterCircle1Process(sub_process_type, **kwargs)
    elif sub_process_type == "外圆弧":
        return OuterCircle2Process(sub_process_type, **kwargs)
    elif sub_process_type == "外锥面":
        return OuterCircle3Process(sub_process_type, **kwargs)

    elif sub_process_type == "端面":
        return EndFace1Process(sub_process_type, **kwargs)
    elif sub_process_type == "切槽":
        return EndFace2Process(sub_process_type, **kwargs)
    elif sub_process_type == "内端面":
        return EndFace3Process(sub_process_type, **kwargs)
    elif sub_process_type == "中心孔":
        return InnerHole1Process(sub_process_type, **kwargs)
    elif sub_process_type == "内锥面":
        return InnerHole2Process(sub_process_type, **kwargs)
    elif sub_process_type == "内槽":
        return InnerHole3Process(sub_process_type, **kwargs)
    elif sub_process_type == "内弧":
        return InnerHole4Process(sub_process_type, **kwargs)
    elif sub_process_type == "内圆":
        return InnerHole5Process(sub_process_type, **kwargs)
    elif sub_process_type == "外反锥面":
        return ConeFace1Process(sub_process_type, **kwargs)
    elif sub_process_type == "内反锥面":
        return ConeFace2Process(sub_process_type, **kwargs)
    elif sub_process_type == "外正锥面":
        return ConeFace3Process(sub_process_type, **kwargs)
    elif sub_process_type == "内正锥面":
        return ConeFace4Process(sub_process_type, **kwargs)
    elif sub_process_type == "外直螺纹":
        return ScrewThread1Process(sub_process_type, **kwargs)
    elif sub_process_type == "外锥（管）螺纹":
        return ScrewThread2Process(sub_process_type, **kwargs)
    elif sub_process_type == "内直螺纹":
        return ScrewThread3Process(sub_process_type, **kwargs)
    elif sub_process_type == "内锥（管）螺纹":
        return ScrewThread4Process(sub_process_type, **kwargs)
    elif sub_process_type == "外圆角倒角":
        return Chamfer1Process(sub_process_type, **kwargs)
    elif sub_process_type == "外倒角":
        return Chamfer2Process(sub_process_type, **kwargs)
    elif sub_process_type == "内圆角倒角":
        return Chamfer3Process(sub_process_type, **kwargs)
    elif sub_process_type == "内倒角":
        return Chamfer4Process(sub_process_type, **kwargs)
    else:
        raise ValueError(f"暂不支持加工工艺: {sub_process_type}")
