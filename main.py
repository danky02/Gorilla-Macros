import utilities.gui as gui
import keyboard
from utilities.actions import *
import utilities.core as core
import utilities.listener as listener

def run():
    with freeze_clipboard():
        try:
            # copy selection
            _text = get_selected_text()

            # run gui => get method
            _method = gui.app_run(core.get_available_methods())

            #     replace
            _refactor_fn = core.get_refactor_fn(_method or '')
            if _refactor_fn:
                replace_selected_text(_refactor_fn(_text))

        except Exception as exc:
            print(f"Gorilla is angry, reason: {exc}")


# TODO separate thread
listener.listener_thread(run)
