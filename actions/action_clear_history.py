from typing import List, Dict, Text, Any
from rasa_sdk import Action
from rasa_sdk.events import AllSlotsReset, Restarted


class ActionClearHistory(Action):

    def name(self) -> Text:
        return "action_clear_history"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="已清除所有历史记录和插槽。")
        return [AllSlotsReset(), Restarted()]  # 清空所有插槽并重置会话
