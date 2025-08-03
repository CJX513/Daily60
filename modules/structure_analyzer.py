import random
from opencc import OpenCC

# 初始化简体转换器（备用）
cc = OpenCC('t2s')  # 繁转简

# 1️⃣ 类型标签推理
def infer_type(text: str) -> str:
    text = text.lower()
    if any(kw in text for kw in ["今天", "去了", "完成了", "参加", "约了", "吃了", "见了"]):
        return "事件"
    elif any(kw in text for kw in ["要做", "准备", "打算", "记得", "计划"]):
        return "TODO"
    elif any(kw in text for kw in ["我觉得", "意识到", "思考", "如果", "是不是"]):
        return "思考"
    elif any(kw in text for kw in ["难过", "开心", "焦虑", "崩溃", "感动"]):
        return "情绪反思"
    return "事件"

# 2️⃣ 情绪识别
def infer_emotion(text: str) -> str:
    emotion_keywords = {
        "快乐": ["开心", "愉快", "放松", "幸福", "满足"],
        "平静": ["平静", "还行", "一般", "没事", "淡然"],
        "焦虑": ["担心", "焦虑", "着急", "紧张", "不安"],
        "悲伤": ["难过", "低落", "沮丧", "无助", "委屈"],
        "愤怒": ["生气", "愤怒", "抓狂", "烦躁", "暴躁"]
    }

    text = text.lower()
    emotion_counts = {}

    for emotion, keywords in emotion_keywords.items():
        count = sum(kw in text for kw in keywords)
        if count > 0:
            emotion_counts[emotion] = count

    if emotion_counts:
        # 返回出现最多关键词的情绪
        return max(emotion_counts, key=emotion_counts.get)
    
    return "平静"  # 默认情绪


# 3️⃣ 一句话总结（简单方式，后续可接 LLM）
def summarize_text(text: str) -> str:
    text = text.strip()
    if len(text) <= 30:
        return text
    return text[:30] + "..."

# 4️⃣ 鼓励语生成（基于情绪）
def generate_encouragement(emotion: str) -> str:
    encouragement_dict = {
        "快乐": ["继续保持好心情！", "你今天真棒！"],
        "平静": ["平稳也是一种幸福。", "继续按节奏来，别急。"],
        "焦虑": ["深呼吸一下，一切会好起来的。", "慢慢来，别给自己太大压力。"],
        "悲伤": ["你并不孤单，抱抱你。", "允许自己难过一会，明天会更好。"],
        "愤怒": ["释放情绪是健康的，注意别伤到自己。", "写下来，有时会更清醒。"]
    }
    return random.choice(encouragement_dict.get(emotion, ["你值得被鼓励。"]))

# 5️⃣ 总整合函数：结构化分析（加载前4个模块）
def analyze_text(text: str) -> dict:
    _text = text.strip()
    _emotion = infer_emotion(_text)
    return {
        "raw_text": _text,
        "type": infer_type(_text),
        "emotion": _emotion,
        "summary": summarize_text(_text),
        "encouragement": generate_encouragement(_emotion)
    }
