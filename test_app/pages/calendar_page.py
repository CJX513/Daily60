import streamlit as st
import calendar as cal
import datetime

st.set_page_config(page_title="日历", layout="wide")

st.title("日历视图")

def get_emotion_emoji(emotion):
    emojis = {
        "平静": "😌",
        "积极": "😊",
        "消极": "😔",
        "工作": "👨‍💻"
    }
    return emojis.get(emotion, "😐")

# 获取测试记录
if "record" not in st.session_state:
    st.session_state.record = {}
date_map = st.session_state.record

today = datetime.date.today()
year = st.selectbox("选择年份", range(today.year - 5, today.year + 5), index=5)
month = st.selectbox("选择月份", range(1, 13), index=today.month - 1)

st.subheader(f"{year} 年 {month} 月")

cal = cal.Calendar()
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

        this_date = datetime.date(year, month, day).isoformat()
        
        record = date_map.get(this_date)
        
        display_text = f"{day}"
        if record:
            emoji = get_emotion_emoji(record["emotion"])
            type_tag = record["type"]
            display_text = f"{day} {emoji}\n{type_tag}"

        if cols[i].button(display_text, key=f"btn_{this_date}"):
            # 关键修改：设置查询参数并跳转
            st.query_params["date"] = this_date
            st.switch_page("app.py")