# NoovaX/core/automation.py
import os
import subprocess
import pyautogui
import psutil
import time
from core.voice_engine import speak

# --- APP CONTROL ---
def open_application(app_name):
    app_name = app_name.lower().strip()
    app_map = {
        "chrome": "chrome",
        "browser": "chrome",
        "vscode": "code",
        "visual studio code": "code",
        "notion": "notion",
        "spotify": "spotify",
        "calculator": "calc",
        "notepad": "notepad"
    }

    command = app_map.get(app_name)
    if not command:
        speak(f"I don't have a command configured for {app_name}.")
        return False

    try:
        subprocess.Popen([command])
        speak(f"Opening {app_name} now.")
        return True
    except FileNotFoundError:
        speak(f"Couldn't find {app_name}. Please check if it's installed.")
        return False


# --- CREATE FOLDER ---
def create_folder(name):
    """Creates a new folder in current directory or inside data/folders."""
    try:
        base_dir = os.path.join("data", "folders")
        os.makedirs(base_dir, exist_ok=True)
        folder_path = os.path.join(base_dir, name)
        os.makedirs(folder_path, exist_ok=True)
        speak(f"Folder named {name} created successfully.")
        return True
    except Exception as e:
        speak(f"Couldn't create folder: {e}")
        return False


# --- SYSTEM INFO ---
def system_info():
    """Reports system CPU, RAM, and battery percentage."""
    try:
        battery = psutil.sensors_battery()
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        report = f"Battery {battery.percent if battery else 0}% | CPU {cpu}% | Memory {mem}%"
        speak(report)
        return report
    except Exception as e:
        speak(f"Failed to get system info: {e}")
        return False


# --- SCREENSHOT ---
def take_screenshot():
    try:
        save_dir = os.path.join("data", "images")
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.join(save_dir, f"screenshot_{int(time.time())}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        
        speak("Screenshot captured successfully.")
        return True
    except Exception as e:
        speak(f"Failed to take screenshot: {e}")
        return False
