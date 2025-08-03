import streamlit as st
import os
import json
from datetime import datetime
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.ui_utils import get_emotion_emoji
from modules.structure_analyzer import analyze_text

st.sidebar.page_link("app.py", label="📥 记录日记")
st.sidebar.page_link("pages/view_calendar.py", label="📆 日历总览")

# ✅ 关键修正：从 session_state 中获取日期
target_date = st.session_state.get("target_date")

if not target_date:
    st.error("未指定日期，无法查看日记。")
    if st.button("返回日历"):
        st.switch_page("pages/view_calendar.py")
    st.stop()

records_file = "data/records.json"
if not os.path.exists(records_file):
    st.error("数据文件不存在。")
    st.stop()

with open(records_file, "r", encoding="utf-8") as f:
    records = json.load(f)

record = next((r for r in records if r["datetime"].startswith(target_date)), None)

if record:
    st.title(f"📝 {target_date} 的日记")
    
    with st.container(border=True):
        st.subheader("情绪分析与总结")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**心情：** {record['emotion']} {get_emotion_emoji(record['emotion'])}")
        with col2:
            st.markdown(f"**类型：** {record['type']}")
        st.markdown(f"**一句话总结：** {record['summary']}")
        st.audio(record["audio_path"])

    st.markdown("---")
    st.subheader("日记正文")
    edited_text = st.text_area("识别文本", record["text"], height=200, key="edit_text")

    with st.container(border=True):
        st.subheader("来自 AI 的鼓励")
        st.markdown(f"**{record['encouragement']}**")
    
    col1, col2 = st.columns(2)
    if col1.button("💾 保存修改"):
        for r in records:
            if r["datetime"].startswith(target_date):
                r["text"] = edited_text
                analysis = analyze_text(edited_text)
                r.update(analysis)
                break
        
        with open(records_file, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        st.success("🎉 日记已成功修改！")
        st.rerun()
    
    if col2.button("🗑️ 删除日记"):
        records_to_keep = [r for r in records if not r["datetime"].startswith(target_date)]
        with open(records_file, "w", encoding="utf-8") as f:
            json.dump(records_to_keep, f, ensure_ascii=False, indent=2)
        st.success("🗑️ 日记已删除！正在返回日历...")
        del st.session_state["target_date"] # 成功删除后移除状态
        st.switch_page("pages/view_calendar.py")

else:
    st.warning(f"未找到 {target_date} 的记录。")
    if st.button("创建新日记"):
        st.switch_page("app.py")