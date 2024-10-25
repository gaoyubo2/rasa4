from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
import logging
from markdownify import markdownify as md
from component.neo4j_service import Neo4jService

logger = logging.getLogger(__name__)


class ActionConfirmProcessing(Action):
    def name(self) -> str:
        return "action_request_sub_processing"

    def __init__(self):
        self.neo4j_service = Neo4jService.get_instance()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        # 获取插槽值
        sub_process_type = tracker.get_slot("sub_process_type")
        process_type = tracker.get_slot("process_type")
        logger.info(f"获取到的父工艺: {process_type}, 子工艺: {sub_process_type}")

        # 如果子工艺不为空，直接返回加工成功信息
        if sub_process_type:
            # 执行G代码生成动作
            return [FollowupAction("action_generate_gcode")]  # 调用 G 代码生成动作

        # 子工艺为空，父工艺为空
        if not process_type:
            dispatcher.utter_message("请您先选择工艺类型")
            dispatcher.utter_message(md("您可以这样向我提问: <br/>我想加工一个外圆工艺<br/>\
                                                  我需要外圆工艺的加工<br/>\
                                                  能帮我做一个外圆工艺吗<br/>\
                                                    "))
            return []

        # 当父工艺存在时，查询相关的子工艺
        sub_processes = self.neo4j_service.query_process(process_type)
        logger.info(f"为父工艺 '{process_type}' 查询到的子工艺: {sub_processes}")

        # 提供子工艺按钮供用户选择
        buttons = [{"title": sub_process, "payload": f'/request_gcode{{"sub_process_type": "{sub_process}"}}'} for sub_process in sub_processes]
        dispatcher.utter_message(
            text=f"已选择父工艺 '{process_type}'，请选择相关的子工艺：",
            buttons=buttons
        )
        logger.info("已发送子工艺选择按钮。")

        return []
