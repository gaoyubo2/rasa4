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

    elif sub_process_type == "END_FACE_ONE":
        return EndFace1Process(sub_process_type, **kwargs)
    elif sub_process_type == "END_FACE_TWO":
        return EndFace2Process(sub_process_type, **kwargs)
    elif sub_process_type == "END_FACE_THREE":
        return EndFace3Process(sub_process_type, **kwargs)
    elif sub_process_type == "INNER_HOLE_ONE":
        return InnerHole1Process(sub_process_type, **kwargs)
    elif sub_process_type == "INNER_HOLE_TWO":
        return InnerHole2Process(sub_process_type, **kwargs)
    elif sub_process_type == "INNER_HOLE_THREE":
        return InnerHole3Process(sub_process_type, **kwargs)
    elif sub_process_type == "INNER_HOLE_FOUR":
        return InnerHole4Process(sub_process_type, **kwargs)
    elif sub_process_type == "INNER_HOLE_FIVE":
        return InnerHole5Process(sub_process_type, **kwargs)
    elif sub_process_type == "CONE_FACE_ONE":
        return ConeFace1Process(sub_process_type, **kwargs)
    elif sub_process_type == "CONE_FACE_TWO":
        return ConeFace2Process(sub_process_type, **kwargs)
    elif sub_process_type == "CONE_FACE_THREE":
        return ConeFace3Process(sub_process_type, **kwargs)
    elif sub_process_type == "CONE_FACE_FOUR":
        return ConeFace4Process(sub_process_type, **kwargs)
    elif sub_process_type == "SCREW_THREAD_ONE":
        return ScrewThread1Process(sub_process_type, **kwargs)
    elif sub_process_type == "SCREW_THREAD_TWO":
        return ScrewThread2Process(sub_process_type, **kwargs)
    elif sub_process_type == "SCREW_THREAD_THREE":
        return ScrewThread3Process(sub_process_type, **kwargs)
    elif sub_process_type == "SCREW_THREAD_FOUR":
        return ScrewThread4Process(sub_process_type, **kwargs)
    elif sub_process_type == "CHAMFER_ONE":
        return Chamfer1Process(sub_process_type, **kwargs)
    elif sub_process_type == "CHAMFER_TWO":
        return Chamfer2Process(sub_process_type, **kwargs)
    elif sub_process_type == "CHAMFER_THREE":
        return Chamfer3Process(sub_process_type, **kwargs)
    elif sub_process_type == "CHAMFER_FOUR":
        return Chamfer4Process(sub_process_type, **kwargs)
    else:
        raise ValueError(f"Unknown process type: {sub_process_type}")
