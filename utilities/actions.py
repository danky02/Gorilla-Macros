import pyperclip
import pyautogui


from contextlib import contextmanager

@contextmanager
def freeze_clipboard():
    # store original clipboard
    snapshot = pyperclip.paste()
    try:
        yield
    finally:
        # restore original clipboard
        pyperclip.copy(snapshot)


def get_selected_text() -> str:
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()


def replace_selected_text(text:str):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
