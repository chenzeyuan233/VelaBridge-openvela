# VelaBridge-openvela

## 项目名称

VelaBridge：基于 openvela 的多模态无障碍 AI 沟通与伴行终端

## 项目简介

VelaBridge 是一款面向听障、视障和语言表达困难人群的可穿戴 AI 硬件设备。

设备通过 openvela 实现屏幕显示、按键交互、语音播报、震动提醒、日志保存和 AI Agent 调用，帮助用户在校园、课堂、窗口服务、医院、交通出行等场景中完成无障碍沟通。

## 核心功能

1. 实时字幕：将语音内容转换为文字显示。
2. 快捷回复：通过按键触发常用语音播报。
3. 盲人模式：通过语音菜单、触感按键和震动反馈完成无屏操作。
4. 震动提醒：用不同震动模式提示状态和紧急信息。
5. 一键求助：长按按键触发求助播报和日志记录。
6. AI 摘要：生成沟通过程摘要和事件记录。

## 项目目录

```text
VelaBridge-openvela/
├── docs/              项目文档
├── hardware/          硬件清单、接线图
├── firmware/          openvela 端代码
├── ai_agent/          AI Agent、提示词、后端脚本
├── demo/              演示脚本、测试数据
├── logs/              设备日志样例
├── ai_coding_logs/    AI Coding 原始日志
└── README.md
