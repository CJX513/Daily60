import streamlit as st
import os
import json
from datetime import datetime
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.speech_to_text import transcribe_audio
from modules.structure_analyzer import analyze_text
from modules.ui_utils import get_emotion_emoji

st.sidebar.page_link("app.py", label="📥 记录日记")
st.sidebar.page_link("pages/view_calendar.py", label="📆 日历总览")

# ✅ 关键修正：从 session_state 中获取日期
target_date_from_calendar = st.session_state.get("target_date")
if target_date_from_calendar:
    st.subheader(f"正在为 {target_date_from_calendar} 创建新日记")
    # ✅ 获取后立即从 session_state 中移除，避免后续刷新时仍存在
    del st.session_state["target_date"]
    current_date = target_date_from_calendar
else:
    current_date = datetime.now().isoformat()[:10]

st.title("每日60s - AI语音日记")

uploaded_file = st.file_uploader("上传语音文件（.wav/.mp3）", type=["wav", "mp3"])

if uploaded_file:
    with st.spinner("正在处理您的日记..."):
        os.makedirs("data/uploads", exist_ok=True)
        audio_path = f"data/uploads/{uploaded_file.name}"
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.read())

        text = transcribe_audio(audio_path)
        analysis = analyze_text(text)
        
        record_datetime = f"{current_date}T{datetime.now().time().isoformat()}"
        
        record = {
            "datetime": record_datetime,
            "audio_path": audio_path,
            "text": text,
            **analysis
        }
        
        os.makedirs("data", exist_ok=True)
        records_file = "data/records.json"
        records = []
        if os.path.exists(records_file):
            with open(records_file, "r", encoding="utf-8") as f:
                records = json.load(f)
        
        found = False
        for i, r in enumerate(records):
            if r["datetime"].startswith(current_date):
                records[i] = record
                found = True
                break
        if not found:
            records.append(record)
        
        with open(records_file, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    st.success("🎉 日记已保存！正在跳转到日记详情页...")
    st.session_state["target_date"] = current_date # 传递新日记日期
    st.switch_page("pages/view_diary_with_edit.py")