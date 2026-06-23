# VelaBridge AI Demo
# 功能：字幕简化、快捷回复推荐、沟通摘要生成
# 当前版本为 MVP 模拟版，后续可替换为 GPT / Codex / openvela AI Agent 调用

from datetime import datetime


def simplify_caption(text: str) -> str:
    """将复杂句子简化成更适合字幕显示的短句。"""
    rules = {
        "你需要先去教务处提交申请表，然后再到学院办公室盖章。": "先去教务处交表。\n再去学院办公室盖章。",
        "你好，请问你要去图书馆还是实训楼？": "你要去图书馆，还是实训楼？",
        "请你下午三点到信息楼一楼大厅集合。": "下午三点。\n信息楼一楼大厅集合。"
    }
    return rules.get(text, text)


def recommend_reply(scene: str) -> str:
    """根据场景推荐快捷回复。"""
    replies = {
        "问路": "请帮我确认当前位置，谢谢。",
        "课堂": "请说慢一点，谢谢。",
        "求助": "你好，我需要帮助，请帮我确认当前位置。",
        "窗口服务": "我听不清，请看我的屏幕。"
    }
    return replies.get(scene, "请说慢一点，谢谢。")


def generate_summary(events: list) -> str:
    """根据事件日志生成沟通摘要。"""
    summary = "本次沟通摘要：\n"
    for index, event in enumerate(events, start=1):
        summary += f"{index}. {event}\n"
    return summary


def create_log(event_type: str, content: str, mode: str = "normal") -> dict:
    """生成设备日志。"""
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event_type,
        "content": content,
        "mode": mode
    }


if __name__ == "__main__":
    print("=== VelaBridge AI Demo ===")

    original_text = "你需要先去教务处提交申请表，然后再到学院办公室盖章。"
    simplified_text = simplify_caption(original_text)

    print("\n原始语音识别文本：")
    print(original_text)

    print("\nAI 简化字幕：")
    print(simplified_text)

    reply = recommend_reply("问路")
    print("\n快捷回复推荐：")
    print(reply)

    logs = [
        "对方说明办事流程",
        "系统生成简化字幕",
        "用户选择快捷回复：请帮我确认当前位置",
        "设备触发语音播报和震动提醒"
    ]

    summary = generate_summary(logs)
    print("\n" + summary)

    log = create_log("quick_reply", reply, "blind_mode")
    print("\n设备日志：")
    print(log)
