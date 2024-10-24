from typing import Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionConfirmProcessing(Action):
    def name(self) -> str:
        return "action_confirm_processing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        selected_sub_process = tracker.get_slot("sub_process")
        dispatcher.utter_message(text=f"加工成功：'{selected_sub_process}' 子工艺。")
        return []
