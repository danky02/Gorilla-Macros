import keyboard


def listener_thread(hotkey_detected_fn):
    while True:
        keyboard.wait(    
            'ctrl+down',
            suppress=True,
            trigger_on_release=True
        )
        hotkey_detected_fn()