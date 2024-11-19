import logging
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from rasa_sdk.types import DomainDict
import actions.action_generate_gcode

from rasa_sdk import Tracker
import logging

from component.config_loader import load_process_params_config, get_required_params


class GCodeForm(FormAction):
    def name(self) -> str:
        return "gcode_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> list:
        logging.info("轮询所需参数中...")

        # 加载配置文件
        config = load_process_params_config()
        if not config:
            logging.error("无法加载工艺参数配置")
            return []

        # 获取子工艺类型
        sub_process_type = tracker.get_slot("sub_process_type")

        # 获取工艺类型的所需参数
        required_params = get_required_params(sub_process_type, config)

        if not required_params:
            logging.error(f"未找到子工艺类型 {sub_process_type} 的所需参数")
        return required_params

    def slot_mappings(self) -> dict:
        # 定义如何映射每个插槽的填充规则
        return {
            "Cn": self.from_text(),  # 通过文本输入填充
            "L": self.from_text(),
            "Tr": self.from_text(),
            "Cr": self.from_text(),
            "F": self.from_text(),
            "A": self.from_text(),
            "xDir": self.from_text(),
            "zDir": self.from_text(),
            "G71G73": self.from_text(),
            "R": self.from_text(),
            "G2G3": self.from_text(),
            "PHi1": self.from_text(),
            "Lr": self.from_text(),
            "CT": self.from_text(),
            "W": self.from_text(),
            "Tw": self.from_text(),
            "sub_process_type": self.from_text(),  # 通过文本输入填充
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> list:
        logging.info("参数预处理完毕")
        # 调用生成 G 代码的 action
        action = actions.action_generate_gcode.ActionGenerateGcode()
        action.run(dispatcher, tracker, domain)

        # 返回空列表，表示表单提交完成
        return []
