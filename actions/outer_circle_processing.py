import Levenshtein
import pypinyin
import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from typing import List, Dict, Any
from component.neo4j_service import Neo4jService  # 引入服务

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def to_pinyin(text: str) -> str:
    if not text:  # 检查是否为空或 None
        logger.warning("输入的文本为空，返回空字符串。")
        return ""  # 返回空字符串或其他适当的默认值
    # 将中文字符转换为拼音，拼音之间用空格分隔
    pinyin_list = pypinyin.lazy_pinyin(text)
    logger.info(f"将文本 '{text}' 转换为拼音 '{''.join(pinyin_list)}'")
    return ''.join(pinyin_list)  # 拼音拼接成字符串


def calculate_similarity(input_str: str, reference_str: str) -> float:
    # 将输入字符串和参考字符串转换为拼音
    input_pinyin = to_pinyin(input_str)
    reference_pinyin = to_pinyin(reference_str)

    # 计算拼音之间的 Levenshtein 距离
    distance = Levenshtein.distance(input_pinyin, reference_pinyin)

    # 计算相似度，值为 1 - 距离/最大长度（用于归一化）
    max_len = max(len(input_pinyin), len(reference_pinyin))
    similarity = 1 - distance / max_len if max_len > 0 else 0  # 避免除以零

    logger.info(f"输入拼音: '{input_pinyin}', 参考拼音: '{reference_pinyin}', "
                f"Levenshtein 距离: {distance}, 相似度: {similarity:.2f}")

    return similarity



class ActionRequestOuterCircleProcessing(Action):
    def name(self) -> str:
        return "action_request_outer_circle_processing"

    def __init__(self):
        self.neo4j_service = Neo4jService.get_instance()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        user_input_process = tracker.get_slot("process_type")  # 从插槽获取用户输入
        logger.info(f"获取到用户输入的工艺类型: {user_input_process}")

        # 查询所有工艺类型
        all_processes = self.neo4j_service.query_all_processes()
        logger.info(f"从数据库查询到的所有工艺: {all_processes}")

        # 如果用户输入为空，则提供所有工艺的按钮供选择
        if not user_input_process:
            buttons = [{"title": process, "payload": f"/select_process{{process_type:'{process}'}}"} for process in all_processes]
            dispatcher.utter_message(
                text="请从以下列表中选择工艺类型：",
                buttons=buttons
            )
            logger.info("用户输入为空，已发送工艺选择按钮。")
            return []

        # 如果用户输入不为空，但未找到匹配工艺，则计算相似度
        process_found = False
        similarities = []  # 用于存储相似度信息
        for process in all_processes:
            similarity = calculate_similarity(user_input_process, process)
            similarities.append((process, similarity))  # 存储工艺和对应的相似度
            logger.info(f"工艺: '{process}' 与用户输入的相似度: {similarity:.2f}")  # 打印每个工艺的相似度

            if similarity > 0.8:
                user_input_process = process
                process_found = True
                logger.info(f"找到相似工艺: {user_input_process}")
                break

        if not process_found:
            # 提示用户重新输入，并提供所有工艺的按钮选择
            buttons = [{"title": process, "payload": f"/select_process{{process_type:'{process}'}}"} for process in all_processes]
            dispatcher.utter_message(
                text=f"抱歉，未找到工艺类型 '{user_input_process}'，请从以下列表中选择工艺类型：",
                buttons=buttons
            )
            logger.warning(f"未找到与用户输入相似的工艺: '{user_input_process}'")
            return []

        # 更新插槽
        return [SlotSet("process_type", user_input_process)]