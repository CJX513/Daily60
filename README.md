## 第一周（语音转文字）

-  搭建初始目录结构
-  搭建 Streamlit 页面
-  实现音频上传 / 播放
-  Whisper-small 实现语音转文字（本地）
-  展示识别结果
-  保存音频 + 转写内容（本地 JSON）

```
daily60s/
├── app.py                  # Streamlit 主应用入口
├── requirements.txt        # 依赖包列表
├── /data/
│   └── records.json        # 存储转写结果
│   └── uploads/            # 存储上传音频文件
├── /modules/
│   └── speech_to_text.py   # Whisper模型封装
├── README.md
```

## 第二周（ai识别）

+ 接入原始语音转文字结果

+ 自动生成：

	+ 类型标签（事件 / TODO / 思考 / 情绪反思）

	+ 情绪类别（快乐 / 平静 / 焦虑 / 悲伤 / 愤怒）

	+ 一句话总结（简洁表达主旨）

	+ 鼓励语（情绪驱动型反馈）

```
daily60s/
├── modules/
│   ├── speech_to_text.py
│   └── structure_analyzer.py  ← 🆕 新模块：结构化分析器
```

## 第三周（）

+ 实现结构化卡片（情绪表情+色块+总结+鼓励）
+ 创建“日历视图”页面（view_calendar.py）
+ 将记录按日期汇总，生成日历数据结构 
+ 每天的情绪用图标代表，点击可弹出总结
+ 提取 emoji / 色块逻辑为 ui_utils.py 模块

```
daily60s/
├── app.py                # 首页（上传+分析）
├── view_calendar.py      # 🆕 日历视图
├── modules/
│   ├── speech_to_text.py
│   ├── structure_analyzer.py
│   └── ui_utils.py       # 🆕 emoji映射 / 色块渲染函数等
├── data/
│   ├── records.json
│   └── uploads/
```

