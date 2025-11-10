# NoovaX/core/productivity.py
import os
import sqlite3
import datetime
from core.voice_engine import speak

DB_PATH = os.path.join("data", "tasks.db")

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_description TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS custom_commands (
            trigger_phrase TEXT PRIMARY KEY,
            action_code TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# --- ADD / LIST / CLEAR TASKS ---
def add_task(description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_description) VALUES (?)", (description,))
    conn.commit()
    conn.close()
    speak(f"Task added: {description}")
    return True


def list_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_description, status FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        speak("You have no pending tasks.")
        return False
    speak(f"You have {len(rows)} tasks.")
    for task in rows:
        print(f"{task[0]} - {task[1]} [{task[2]}]")
        speak(task[1])
    return True


def clear_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
    speak("All tasks cleared successfully.")
    return True


# --- FOCUS TIMER (SIMPLE) ---
def start_pomodoro(minutes=25):
    speak(f"Starting focus timer for {minutes} minutes.")
    speak("Focus session complete! Time for a short break.")
    return True


# --- CUSTOM COMMAND SYSTEM ---
def teach_command(trigger, action_code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO custom_commands (trigger_phrase, action_code) VALUES (?, ?)",
        (trigger.lower(), action_code),
    )
    conn.commit()
    conn.close()
    speak(f"Learned new command: '{trigger}' will now execute your action.")
    return True


def execute_custom_command(trigger):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT action_code FROM custom_commands WHERE trigger_phrase = ?",
        (trigger.lower(),),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        os.system(row[0])
        speak(f"Executing your custom command: {trigger}")
        return True
    return False
