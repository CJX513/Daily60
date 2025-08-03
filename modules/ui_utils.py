def get_emotion_emoji(emotion: str) -> str:
    mapping = {
        "快乐": "😄",
        "平静": "😌",
        "焦虑": "😰",
        "悲伤": "😢",
        "愤怒": "😠",
    }
    return mapping.get(emotion, "📝")
