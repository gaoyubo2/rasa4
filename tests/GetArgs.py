from sklearn.metrics import precision_score, recall_score, f1_score

# 定义模型的预测结果
models = {
    "DIET": {"TP": 80, "FP": 15, "FN": 10, "TN": 5},
    "DIET (BERT)": {"TP": 81, "FP": 14, "FN": 9, "TN": 5},
    "DIET (DistilBERT)": {"TP": 85, "FP": 12, "FN": 7, "TN": 5},
    "BiLSTM-CRF": {"TP": 78, "FP": 17, "FN": 12, "TN": 5},
    "LSTM-DIET": {"TP": 82, "FP": 14, "FN": 9, "TN": 5},
    "CMT-BERT": {"TP": 97, "FP": 3, "FN": 1, "TN": 5},
}

# 定义计算指标的函数
def calculate_metrics(TP, FP, FN, TN):
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

# 计算每个模型的指标并输出
for model, metrics in models.items():
    TP, FP, FN, TN = metrics["TP"], metrics["FP"], metrics["FN"], metrics["TN"]
    precision, recall, f1 = calculate_metrics(TP, FP, FN, TN)
    print(f"{model}:")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall: {recall:.3f}")
    print(f"  F1-Score: {f1:.3f}")
    print()

