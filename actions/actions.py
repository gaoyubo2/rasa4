# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from rasa.shared.exceptions import RasaException
# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from rasa_sdk import Action

from neo4j import GraphDatabase


class ActionQueryNeo4j(Action):
    def name(self):
        return "action_query_neo4j"

    async def run(self, dispatcher, tracker, domain):
        try:
            # 连接 Neo4j 数据库
            uri = "bolt://localhost:7687"
            driver = GraphDatabase.driver(uri, auth=("neo4j", "gyb20010204"))
            session = driver.session()

            # 执行查询
            query = "MATCH (n) RETURN n LIMIT 5"
            result = session.run(query)

            # 处理查询结果
            records = [record["n"] for record in result]
            if not records:
                dispatcher.utter_message(text="未找到任何记录。")
            else:
                for record in records:
                    dispatcher.utter_message(text=str(record))

            session.close()

        except Exception as e:
            dispatcher.utter_message(text=f"查询失败: {str(e)}")
            raise RasaException("Neo4j 查询失败") from e


