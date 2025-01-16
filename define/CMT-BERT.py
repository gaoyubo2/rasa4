from rasa.nlu.components import Component
from transformers import BertTokenizer, BertForSequenceClassification
import torch

from component.neo4j_service import Neo4jService


class CMTBertIntentClassifier(Component):
    """ CMT-BERT 任务分类器 """
    def __init__(self, component_config=None):
        super().__init__(component_config)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=6)
        self.neo4j_service = Neo4jService.get_instance()
    def process(self, message, **kwargs):
        """ 使用BERT进行任务分类 """
        text = message.text
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.nn.functional.softmax(logits, dim=-1)
            predicted_class = torch.argmax(probs, dim=-1).item()
        intent = self._get_intent_from_class(predicted_class)
        message.set("intent", {"name": intent, "confidence": float(probs[0][predicted_class])})

    def _get_intent_from_class(self, predicted_class):
        process_types = self.neo4j_service.query_all_processes()
        if 0 <= predicted_class < len(process_types):
            return process_types[predicted_class]
        else:
            return "未知工艺类型"


class CMTBertEntityExtractor(Component):
    """ CMT-BERT 实体提取器 """

    def __init__(self, component_config=None):
        super().__init__(component_config)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        # 使用 BertForTokenClassification 进行实体提取
        self.model = BertForTokenClassification.from_pretrained('bert-base-uncased', num_labels=3)  # 假设有3个实体

    def process(self, message, **kwargs):
        text = message.text
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_entities = torch.argmax(logits, dim=-1).squeeze().tolist()  # 获取每个词的标签

        # 示例：将实体提取结果设置为message的实体
        entities = []
        for idx, label in enumerate(predicted_entities):
            if label == 1:  # 例如 label 1 代表 "diameter"
                entities.append({"entity": "diameter", "value": "50mm"})
        message.set("entities", entities)