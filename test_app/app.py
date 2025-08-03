import streamlit as st

st.set_page_config(page_title="主页")

st.sidebar.page_link("app.py", label="主页")
st.sidebar.page_link("pages/calendar_page.py", label="日历页面")

# 获取并处理查询参数
query = st.query_params
target_date = query.get("date")

# --- 关键修改：这里是加载和显示日记的逻辑 ---
if "record" not in st.session_state:
    st.session_state.record = {}
    
if target_date and target_date in st.session_state.record:
    # 如果有日期参数且对应记录存在，则显示日记内容
    record = st.session_state.record[target_date]
    st.title(f"📝 {target_date} 的日记")
    st.write(f"情绪: {record['emotion']}")
    st.write(f"类型: {record['type']}")
    st.write("---")
    st.write("这里可以显示更多日记详情")
    st.stop()
elif target_date and target_date not in st.session_state.record:
    # 如果有日期参数但记录不存在
    st.warning(f"未找到 {target_date} 的记录。")
    st.stop()

# --- 如果没有日期参数，则显示上传日记的正常流程 ---
st.title("主页")
st.write("这是主页，你可以通过侧边栏导航到日历页面。")

# 这里是生成测试记录的代码，可以用于测试跳转功能
if st.button("生成一个测试记录"):
    st.session_state.record["2025-08-03"] = {"emotion": "😀", "type": "工作"}
    st.session_state.record["2025-08-10"] = {"emotion": "😊", "type": "生活"}
    st.success("测试记录已生成！请前往日历页面查看。")