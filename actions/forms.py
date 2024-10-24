from typing import Any, Text, Dict, List
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ValidateGCodeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_gcode_form"

    def validate_F(
            self, value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:
        if isinstance(value, float) and value > 0:
            return {"F": value}
        else:
            dispatcher.utter_message(text="F 的值应该是一个大于 0 的数字。")
            return {"F": None}

    # 可以对 Hr、deltaT 和 L 进行类似的验证
