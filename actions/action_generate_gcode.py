import logging
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import os

from component.config_loader import load_process_params_config, get_required_params
from component.gcode_generator import get_process_instance

logger = logging.getLogger(__name__)


class ActionGenerateGcode(Action):
    def name(self) -> str:
        return "action_generate_gcode"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        # 加载工艺类型参数配置
        config = load_process_params_config()
        if not config:
            dispatcher.utter_message(text="配置文件加载失败，请稍后再试。")
            return []

        # 获取所选的工艺类型
        sub_process_type = tracker.get_slot("sub_process_type")

        if not sub_process_type:
            dispatcher.utter_message(text="请先选择一个子工艺类型。")
            return []

        # 获取工艺类型所需的参数
        required_params = get_required_params(sub_process_type, config)
        logger.info(f"验证插槽阶段，子工艺类型: {sub_process_type}")
        logger.info(f"验证插槽阶段，需要的参数: {required_params}")

        # 检查是否所有必要的参数都有值
        missing_params = [param for param in required_params if tracker.get_slot(param) is None]

        if missing_params:
            # 如果有缺失的参数，提醒用户补充
            dispatcher.utter_message(text=f"请提供以下缺失的参数: {', '.join(missing_params)}")
            return [SlotSet("process_type", None)]  # 清空槽位，要求用户补充数据

        # 创建工艺实例并生成 G 代码
        try:
            process_instance = get_process_instance(sub_process_type,
                                                    **{param: tracker.get_slot(param) for param in required_params})
            gcode = process_instance.generate_gcode()
            # 发送生成的 G 代码给用户
            dispatcher.utter_message(text=f"生成的 {sub_process_type} G 代码:\n{gcode}")
        except ValueError as e:
            dispatcher.utter_message(text=f"错误: {e}")
            return [SlotSet("process_type", None)]  # 如果出错，清空槽位，要求用户重新输入

        return []
