import random
import yaml

# =========================
# 1. 工艺体系
# =========================
PROCESS_CONFIG = {
    "外圆": {
        "types": ["外圆", "外圆弧", "外锥面", "外圆面"],
        "slots": ["Cn", "L", "F", "A", "Tr"]
    },
    "内孔": {
        "types": ["内圆", "内锥面", "内槽", "中心孔", "内弧"],
        "slots": ["Cn", "L", "F", "A", "deltaT", "BT"]
    },
    "端面": {
        "types": ["端面", "切槽", "内端面"],
        "slots": ["Cn", "Lr", "CT", "F", "W", "Tw", "Tr"]
    },
    "锥面": {
        "types": ["外正锥面", "外反锥面", "内正锥面", "内反锥面"],
        "slots": ["Cn", "L", "F", "A", "xDir", "zDir", "Tr"]
    },
    "螺纹": {
        "types": ["外直螺纹", "外锥螺纹", "内直螺纹", "内锥螺纹"],
        "slots": ["L", "Tr", "Tp", "Cn", "multi_head", "tailLength"]
    },
    "倒角": {
        "types": ["外倒角", "内倒角", "外圆角倒角", "内圆角倒角"],
        "slots": ["R", "A", "F", "Cn", "PHi1"]
    }
}

# =========================
# 2. 参数生成
# =========================
def gen_value(slot):
    if slot == "Cn":
        return random.randint(5, 30)
    if slot in ["L", "Lr", "tailLength"]:
        return round(random.uniform(20, 150), 2)
    if slot == "F":
        return random.randint(80, 200)
    if slot == "A":
        return random.randint(10, 90)
    if slot in ["Tr", "R"]:
        return round(random.uniform(0.5, 6), 2)
    if slot == "deltaT":
        return round(random.uniform(0.1, 2.5), 2)
    if slot in ["W", "Tw"]:
        return round(random.uniform(1, 12), 2)
    if slot == "CT":
        return round(random.uniform(0.5, 5), 2)
    if slot == "Tp":
        return random.randint(1, 8)
    if slot in ["xDir", "zDir"]:
        return random.choice(["+1", "-1"])
    if slot == "multi_head":
        return random.randint(1, 5)
    if slot == "PHi1":
        return random.randint(10, 70)
    if slot == "BT":
        return round(random.uniform(0.5, 3), 2)
    return random.randint(1, 100)

# =========================
# 3. 表达增强
# =========================
PREFIXES = ["我想", "我要", "帮我", "请帮我", "需要", "我打算", "我计划", ""]

VERBS = ["加工", "做一个", "生成", "创建", "设计", "编写", "搞一个"]

CONNECTORS = ["一个", "该", "", "这个"]

NOISE = ["速度快一点", "差不多就行", "精度高一点", "随便给个参数", "不用太精确"]

def format_slot(slot, val):
    style = random.choice([1, 2, 3])
    if style == 1:
        return f"{slot}[{val}]({slot})"
    if style == 2:
        return f"{slot}是[{val}]({slot})"
    return f"[{val}]({slot})"

# =========================
# 4. 工业句子生成
# =========================
def gen_processing():
    group = random.choice(list(PROCESS_CONFIG.keys()))
    process = random.choice(PROCESS_CONFIG[group]["types"])
    slots = PROCESS_CONFIG[group]["slots"]

    s = f"{random.choice(PREFIXES)}{random.choice(VERBS)}{random.choice(CONNECTORS)}[{process}](process_type)"

    parts = []
    for i in slots:
        if random.random() < 0.25:
            continue
        parts.append(format_slot(i, gen_value(i)))

    random.shuffle(parts)
    if parts:
        s += "，" + "，".join(parts)

    if random.random() < 0.2:
        s += "，" + random.choice(NOISE)

    return s

# =========================
# 5. G-code intent（增强）
# =========================
def gen_gcode():
    templates = [
        "我想生成G代码",
        "帮我生成一个G代码",
        "生成数控加工程序",
        "创建CNC程序",
        "请给我G代码",
        "帮我写加工程序",
        "生成机床代码",
        "我要一个G-code程序",
        "做一个加工代码",
        "生成G71/G72程序"
    ]
    return random.choice(templates)

# =========================
# 6. sub process（增强）
# =========================
def gen_sub():
    p = random.choice(sum([v["types"] for v in PROCESS_CONFIG.values()], []))
    templates = [
        f"我想加工[{p}](sub_process_type)子工艺",
        f"帮我做[{p}](sub_process_type)的G代码",
        f"[{p}](sub_process_type)怎么加工",
        f"车一个[{p}](sub_process_type)",
        f"生成[{p}](sub_process_type)工艺",
        f"我要[{p}](sub_process_type)加工方案",
        f"[{p}](sub_process_type)程序怎么写"
    ]
    return random.choice(templates)

# =========================
# 7. neo4j（增强）
# =========================
def gen_neo4j():
    return random.choice([
        "从Neo4j查询CNC数据",
        "查G71相关加工记录",
        "查询外圆加工工艺数据",
        "有没有螺纹加工信息",
        "查找所有G代码案例",
        "获取加工参数数据库",
        "查工艺知识图谱",
        "查询刀具路径信息"
    ])

# =========================
# 8. 通用 intent
# =========================
def simple(lst): return ["- " + i for i in lst]

# =========================
# 9. 生成数据
# =========================
processing = set()
while len(processing) < 1200:
    processing.add(gen_processing())
processing = list(processing)

# =========================
# 10. YAML 构建
# =========================
nlu = [
    {"intent": "greet", "examples": "\n".join(simple(
        ["hello","hi","hey","你好","在吗","早上好","工程系统在吗"]
    ))},

    {"intent": "goodbye", "examples": "\n".join(simple(
        ["bye","goodbye","再见","退出","结束","关闭系统"]
    ))},

    {"intent": "affirm", "examples": "\n".join(simple(
        ["yes","ok","好的","可以","确认","对","行"]
    ))},

    {"intent": "deny", "examples": "\n".join(simple(
        ["no","不","不是","取消","错误","n"]
    ))},

    {"intent": "mood_great", "examples": "\n".join(simple(
        ["great","perfect","good","不错","很好","满意"]
    ))},

    {"intent": "mood_unhappy", "examples": "\n".join(simple(
        ["bad","sad","不满意","出错了","有问题","失败"]
    ))},

    {"intent": "bot_challenge", "examples": "\n".join(simple(
        ["are you a bot?","你是机器人吗","human?","你是谁"]
    ))},

    {"intent": "inquire_neo4j", "examples": "|\n" + "\n".join(["- "+gen_neo4j() for _ in range(200)])},

    {"intent": "request_gcode", "examples": "|\n" + "\n".join(["- "+gen_gcode() for _ in range(200)])},

    {"intent": "request_sub_processing", "examples": "|\n" + "\n".join(["- "+gen_sub() for _ in range(200)])},

    {"intent": "request_processing", "examples": "|\n" + "\n".join(["- "+e for e in processing])}
]

yaml_data = {"version": "3.1", "nlu": nlu}

# =========================
# 11. 保存
# =========================
with open("cnc_nlu_final.yaml", "w", encoding="utf-8") as f:
    yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

print("完成，总 processing:", len(processing))