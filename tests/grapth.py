import matplotlib.pyplot as plt

# 数据
models = ['DIET', 'DIET(BERT)', 'DIET(DistilBERT)', 'BiLSTM-CRF', 'LSTM-DIET', '本文模型']
f1_scores = [0.934, 0.929, 0.933, 0.904, 0.949, 0.956]

# 创建柱状图
plt.figure(figsize=(10,6))
bars = plt.bar(models, f1_scores, color='skyblue')

# 显示每个柱子上的值
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.001, round(yval, 3), ha='center', va='bottom', fontsize=10)

# 添加标题和标签
plt.title('实际F1值对比', fontsize=14)
plt.xlabel('模型', fontsize=12)
plt.ylabel('F1值', fontsize=12)

# 显示图形
plt.show()
