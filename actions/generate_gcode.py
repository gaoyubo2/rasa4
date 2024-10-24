import logging
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

logger = logging.getLogger(__name__)
def generate_gcode(F, Hr, deltaT, L):
    # 生成 G 代码的函数逻辑
    gcode = []
    gcode.append(f"G71 U{deltaT:.6f} R{deltaT / 2:.6f} F{F:.6f};")
    gcode.append("G71 P80 Q120 U#610 W#611 J1 K1;")
    gcode.append(f"N80 G00 U[{L:.6f} * -1];")
    gcode.append(f"G01 W[{Hr:.6f} * -1];")
    gcode.append("G01 U20.000000;")
    gcode.append("N120;")
    gcode.append("M30;")
    return "\n".join(gcode)


class ActionGenerateGCode(Action):

    def name(self) -> Text:
        return "action_generate_gcode"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            F = float(tracker.get_slot('F')) if tracker.get_slot('F') is not None else 0.0
            Hr = float(tracker.get_slot('Hr')) if tracker.get_slot('Hr') is not None else 0.0
            deltaT = float(tracker.get_slot('deltaT')) if tracker.get_slot('deltaT') is not None else 0.0
            L = float(tracker.get_slot('L')) if tracker.get_slot('L') is not None else 0.0

            logger.info(f"收到的值 - F: {F}, Hr: {Hr}, deltaT: {deltaT}, L: {L}")

            gcode = generate_gcode(F, Hr, deltaT, L)

            dispatcher.utter_message(text=f"生成的 G 代码:\n{gcode}")
        except Exception as e:
            dispatcher.utter_message(text=f"生成 G 代码时出错: {str(e)}")

            # 清空槽
            return [
                SlotSet('F', None),
                SlotSet('Hr', None),
                SlotSet('deltaT', None),
                SlotSet('L', None)
            ]

