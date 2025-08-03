import whisper
from opencc import OpenCC

model = whisper.load_model("small")
cc = OpenCC('t2s')  # 繁体转简体

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    simplified_text = cc.convert(result["text"])
    return simplified_text
