// VelaBridge MVP hardware interaction pseudocode
// This file is for openvela / embedded implementation planning.
// It does not depend on external libraries and is not intended to compile directly.

#define BUTTON_A 1
#define BUTTON_B 2
#define BUTTON_C 3

#define PRESS_NONE 0
#define PRESS_SHORT 1
#define PRESS_LONG 2

#define MODE_NORMAL 0
#define MODE_BLIND 1
#define MODE_EMERGENCY 2

static int current_mode = MODE_NORMAL;
static const char *current_caption = "请说慢一点，谢谢";
static const char *quick_reply = "请说慢一点，谢谢";

void init_display(void)
{
    // TODO: Initialize OLED / LCD driver on openvela.
}

void init_buttons(void)
{
    // TODO: Configure button GPIO and debounce logic.
}

void init_vibrator(void)
{
    // TODO: Configure vibration motor GPIO or PWM output.
}

void init_speaker(void)
{
    // TODO: Initialize speaker, amplifier, or audio playback module.
}

void display_text(const char *text)
{
    // TODO: Clear screen and draw text.
    // MVP target: show short captions and fixed reply text.
}

void vibrate(int duration_ms)
{
    // TODO: Turn motor on, wait duration_ms, then turn motor off.
}

void speak_text(const char *text)
{
    // TODO: Play fixed voice clip or call text-to-speech module.
}

void save_log(const char *event_type, const char *content, const char *mode)
{
    // TODO: Append one text log item to local storage.
    // MVP privacy rule: save confirmed text events, not raw audio.
}

void enter_blind_mode(void)
{
    current_mode = MODE_BLIND;
    vibrate(120);
    speak_text("已进入盲人模式。按A重听字幕，按B播报快捷回复，长按C紧急求助。");
    save_log("enter_blind_mode", "用户长按C进入盲人模式", "blind");
}

void trigger_emergency_help(void)
{
    int i;

    current_mode = MODE_EMERGENCY;

    for (i = 0; i < 5; i++) {
        vibrate(300);
        // TODO: Add a short delay between vibration pulses.
    }

    speak_text("你好，我需要帮助，请帮我确认当前位置");
    save_log("emergency_help", "触发紧急求助", "emergency");
}

void handle_button_short_press(int button_id)
{
    if (current_mode == MODE_BLIND) {
        if (button_id == BUTTON_A) {
            speak_text(current_caption);
            save_log("blind_replay_caption", current_caption, "blind");
        } else if (button_id == BUTTON_B) {
            speak_text(quick_reply);
            save_log("blind_quick_reply", quick_reply, "blind");
        } else if (button_id == BUTTON_C) {
            speak_text("我需要帮助");
            save_log("blind_help_voice", "我需要帮助", "blind");
        }
        return;
    }

    if (button_id == BUTTON_A) {
        display_text("请说慢一点，谢谢");
        save_log("quick_reply_display", "请说慢一点，谢谢", "normal");
    } else if (button_id == BUTTON_B) {
        vibrate(120);
        save_log("vibration_alert", "短震一次", "normal");
    } else if (button_id == BUTTON_C) {
        speak_text("我需要帮助");
        save_log("help_voice", "我需要帮助", "normal");
    }
}

void handle_button_long_press(int button_id)
{
    if (button_id != BUTTON_C) {
        return;
    }

    if (current_mode == MODE_BLIND) {
        trigger_emergency_help();
    } else {
        enter_blind_mode();
    }
}

int read_button_id(void)
{
    // TODO: Return BUTTON_A, BUTTON_B, BUTTON_C, or 0 when no button is pressed.
    return 0;
}

int read_press_type(void)
{
    // TODO: Return PRESS_SHORT or PRESS_LONG after debounce and long-press detection.
    return PRESS_NONE;
}

void main_loop(void)
{
    while (1) {
        int button_id = read_button_id();
        int press_type = read_press_type();

        if (press_type == PRESS_SHORT) {
            handle_button_short_press(button_id);
        } else if (press_type == PRESS_LONG) {
            handle_button_long_press(button_id);
        }

        // TODO: Sleep briefly to reduce CPU usage in the polling loop.
    }
}

int main(void)
{
    init_display();
    init_buttons();
    init_vibrator();
    init_speaker();

    display_text("VelaBridge MVP");
    save_log("boot", "VelaBridge MVP started", "normal");

    main_loop();
    return 0;
}
