import yaml
import random
from collections import defaultdict

# =========================
# 1. 读取原始 YAML
# =========================
input_file = "cnc_nlu_final.yaml"

with open(input_file, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# =========================
# 2. 解析所有 intent → examples
# =========================
intent_samples = defaultdict(list)

for block in data["nlu"]:
    intent = block["intent"]
    examples_text = block["examples"]

    lines = [
        l.strip()[2:]  # 去掉 "- "
        for l in examples_text.split("\n")
        if l.strip().startswith("- ")
    ]

    intent_samples[intent].extend(lines)

# =========================
# 3. 按 intent 内部打乱
# =========================
random.seed(42)

for intent in intent_samples:
    random.shuffle(intent_samples[intent])

# =========================
# 4. 8:1:1 划分函数
# =========================
def split_list(lst):
    n = len(lst)
    n_train = int(n * 0.8)
    n_val = int(n * 0.1)

    train = lst[:n_train]
    val = lst[n_train:n_train + n_val]
    test = lst[n_train + n_val:]

    return train, val, test

# =========================
# 5. 合并各 intent 到 train/val/test
# =========================
train_data = defaultdict(list)
val_data = defaultdict(list)
test_data = defaultdict(list)

for intent, samples in intent_samples.items():
    train, val, test = split_list(samples)

    train_data[intent].extend(train)
    val_data[intent].extend(val)
    test_data[intent].extend(test)

# =========================
# 6. YAML 构建函数
# =========================
def build_yaml(data_dict):
    nlu = []

    for intent, samples in data_dict.items():
        if not samples:
            continue

        nlu.append({
            "intent": intent,
            "examples": "|\n" + "\n".join(["- " + s for s in samples])
        })

    return {"version": "3.1", "nlu": nlu}

train_yaml = build_yaml(train_data)
val_yaml = build_yaml(val_data)
test_yaml = build_yaml(test_data)

# =========================
# 7. 保存
# =========================
with open("train.yml", "w", encoding="utf-8") as f:
    yaml.dump(train_yaml, f, allow_unicode=True, sort_keys=False)

with open("val.yml", "w", encoding="utf-8") as f:
    yaml.dump(val_yaml, f, allow_unicode=True, sort_keys=False)

with open("test.yml", "w", encoding="utf-8") as f:
    yaml.dump(test_yaml, f, allow_unicode=True, sort_keys=False)

# =========================
# 8. 统计输出
# =========================
print("===== 数据集划分完成 =====")
for intent in intent_samples:
    print(intent,
          "train:", len(train_data[intent]),
          "val:", len(val_data[intent]),
          "test:", len(test_data[intent]))