import streamlit as st
import calendar
from datetime import date
import json
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from modules.ui_utils import get_emotion_emoji

st.sidebar.page_link("app.py", label="📥 记录日记")
st.sidebar.page_link("pages/view_calendar.py", label="📆 日历总览")

st.set_page_config(page_title="日历视图 - 每日60s", layout="wide")
st.title("📆 每日60s - 日历视图")

records_file = "data/records.json"
if not os.path.exists(records_file):
    st.warning("暂无记录，请先在主页面上传日记语音。")
    st.stop()

with open(records_file, "r", encoding="utf-8") as f:
    records = json.load(f)

date_map = {}
for record in records:
    record_date = record["datetime"][:10]
    date_map[record_date] = record

today = date.today()
year = st.selectbox("选择年份", range(today.year - 5, today.year + 5), index=5)
month = st.selectbox("选择月份", range(1, 13), index=today.month - 1)

st.subheader(f"{year} 年 {month} 月")

cal = calendar.Calendar()
month_days = cal.monthdayscalendar(year, month)

cols_names = ["一", "二", "三", "四", "五", "六", "日"]
cols_head = st.columns(7)
for i, name in enumerate(cols_names):
    cols_head[i].markdown(f"**{name}**")

for week in month_days:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            cols[i].markdown(" ")
            continue

        this_date = date(year, month, day).isoformat()
        record = date_map.get(this_date)
        
        display_text = f"{day}"
        if record:
            emoji = get_emotion_emoji(record["emotion"])
            type_tag = record["type"]
            display_text = f"{day} {emoji}\n{type_tag}"
            target_page = "pages/view_diary_with_edit.py"
        else:
            display_text = f"{day}"
            target_page = "app.py"

        with cols[i]:
            if st.button(display_text, key=f"btn_{this_date}"):
                # ✅ 关键修正：使用 session_state 来传递日期
                st.session_state["target_date"] = this_date
                st.switch_page(target_page)