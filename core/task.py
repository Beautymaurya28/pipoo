import json
import time
from datetime import datetime
from core.voice_engine import speak

TASK_FILE = "data/tasks.json"

def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(task_name):
    tasks = load_tasks()
    tasks.append({"task": task_name, "time": str(datetime.now())})
    save_tasks(tasks)
    speak(f"Added task {task_name}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        speak("You have no pending tasks.")
        return
    speak(f"You have {len(tasks)} tasks.")
    for t in tasks:
        speak(t["task"])

def clear_tasks():
    save_tasks([])
    speak("All tasks cleared.")

def pomodoro_timer(minutes=25):
    speak(f"Starting focus timer for {minutes} minutes.")
    time.sleep(minutes * 60)
    speak("Time’s up! Take a break.")
