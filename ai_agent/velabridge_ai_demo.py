# -*- coding: utf-8 -*-
"""VelaBridge AI MVP demo.

This script intentionally avoids third-party dependencies so it can run in a
basic Python 3 environment during the hardware competition demo.
"""

from datetime import datetime, timezone, timedelta
import json


CHINA_TZ = timezone(timedelta(hours=8))


def simplify_caption(text: str) -> str:
    """Simplify a long sentence into a short caption for small screens."""
    if not text:
        return "未识别到有效内容。"

    if "说慢" in text and "字幕" in text:
        return "请说慢一点，我需要看字幕。"
    if "帮助" in text or "求助" in text:
        return "我需要帮助。"
    if "听不清" in text or "没听清" in text:
        return "我没有听清，请再说一遍。"

    replacements = {
        "麻烦您": "请",
        "能不能": "",
        "是否可以": "",
        "尽可能": "",
        "稍微": "",
        "因为": "原因是",
        "所以": "因此",
        "如果": "若",
    }

    simplified = text.strip()
    for old, new in replacements.items():
        simplified = simplified.replace(old, new)

    separators = ["。", "，", ",", "；", ";", "！", "？"]
    for sep in separators:
        simplified = simplified.replace(sep, " ")

    words = [part for part in simplified.split() if part]
    caption = " ".join(words)
    while "请请" in caption:
        caption = caption.replace("请请", "请")

    max_length = 28
    if len(caption) > max_length:
        caption = caption[:max_length - 1] + "…"

    return caption or "请重复一遍。"


def recommend_reply(scene: str) -> str:
    """Recommend a quick reply according to a simple scene keyword."""
    scene_text = scene.strip().lower()
    reply_map = {
        "课堂": "请老师再重复一遍，谢谢。",
        "class": "请老师再重复一遍，谢谢。",
        "医院": "我听不清，请写下来或说慢一点。",
        "hospital": "我听不清，请写下来或说慢一点。",
        "窗口": "请说慢一点，谢谢。",
        "service": "请说慢一点，谢谢。",
        "问路": "请告诉我方向，我会跟着语音提示走。",
        "travel": "请告诉我方向，我会跟着语音提示走。",
        "求助": "我需要帮助，请帮我联系工作人员。",
        "help": "我需要帮助，请帮我联系工作人员。",
    }

    for keyword, reply in reply_map.items():
        if keyword in scene_text:
            return reply

    return "请说慢一点，谢谢。"


def generate_summary(events: list) -> str:
    """Generate a short communication summary from device event logs."""
    if not events:
        return "本次沟通暂无有效事件。"

    event_count = len(events)
    modes = sorted({event.get("mode", "normal") for event in events})
    event_types = [event.get("event_type", "unknown") for event in events]

    important_contents = [
        event.get("content", "")
        for event in events
        if event.get("event_type") in {"caption", "quick_reply", "emergency_help", "ai_summary"}
    ]
    important_contents = [item for item in important_contents if item]

    summary = (
        f"本次沟通共记录 {event_count} 条事件，"
        f"涉及模式：{'、'.join(modes)}。"
        f"主要事件包括：{'、'.join(event_types)}。"
    )

    if important_contents:
        summary += f"关键内容：{important_contents[-1]}"

    return summary


def create_log(event_type: str, content: str, mode: str = "normal") -> dict:
    """Create a device log entry with a China timezone timestamp."""
    return {
        "timestamp": datetime.now(CHINA_TZ).isoformat(timespec="seconds"),
        "event_type": event_type,
        "content": content,
        "mode": mode,
    }


def main() -> None:
    """Run a complete MVP demo flow."""
    source_text = "麻烦您能不能稍微说慢一点，因为我需要看字幕理解您刚才说的内容。"
    scene = "窗口服务"

    caption = simplify_caption(source_text)
    reply = recommend_reply(scene)

    logs = [
        create_log("caption", caption),
        create_log("quick_reply", reply),
        create_log("vibration", "短震 1 次：快捷回复已触发"),
        create_log("blind_mode_enter", "进入盲人模式，播报语音菜单", mode="blind"),
        create_log("emergency_help", "我需要帮助", mode="emergency"),
    ]

    summary = generate_summary(logs)
    logs.append(create_log("ai_summary", summary))

    print("=== VelaBridge AI Demo ===")
    print(f"原始文本：{source_text}")
    print(f"AI 简化字幕：{caption}")
    print(f"推荐快捷回复：{reply}")
    print(f"沟通摘要：{summary}")
    print("设备日志：")
    print(json.dumps(logs, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
