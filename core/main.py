# NoovaX/core/main.py

import datetime
import subprocess
import time
from core.voice_engine import speak, listen_for_command 
import os # Ensure os is imported for potential subprocess use

# --- PHASE 2: NEW IMPORTS ---
# Ensure these files and functions exist in your 'core/' directory.
from core.automation import (open_application, take_screenshot, 
                             system_info, create_folder) 
from core.productivity import (init_db, add_task, start_pomodoro, 
                               teach_command, execute_custom_command,
                               list_tasks, clear_tasks) 

# --- PHASE 3: AI IMPORT (CRITICAL FIX) ---
from core.coding_ai import get_ai_response # <--- THIS LINE IS NOW UNCOMMENTED AND ACTIVE

# --- STARTUP ---
# Initialize the database at the start of the program
init_db() 


def handle_basic_commands(text):
    """Executes basic commands based on user text input."""
    
    if not text:
        return None 
    
    # 1. Check for Custom Commands FIRST (Teach Command Feature)
    if execute_custom_command(text):
        return True

    # --- Teach Command Logic ---
    if "teach command" in text or "create shortcut" in text:
        speak("What is the short phrase you want to use to trigger the command?")
        trigger = listen_for_command()
        speak("What OS command should I run?")
        action = listen_for_command()
        
        if trigger and action:
            return teach_command(trigger, action)
        else:
            speak("Command teaching canceled because I didn't get both parts.")
            return True


    # --- Productivity Commands ---
    
    if "add task" in text or "create task" in text:
        try:
            description = text.split("task", 1)[1].strip()
            if not description:
                 speak("What is the description of the task?")
                 description = listen_for_command()
            
            if description:
                return add_task(description)
        except IndexError:
             speak("I didn't catch the task description.")
             return True
             
    if "start pomodoro" in text or "start focus" in text:
        return start_pomodoro()
    
    # --- NEW: Task Listing/Clearing ---
    if "show my tasks" in text or "list tasks" in text:
        return list_tasks()

    if "clear tasks" in text:
        return clear_tasks()
    
    
    # --- System Automation Commands ---
    
    # Generalize the 'open' command check
    if "open" in text and ("chrome" in text or "vscode" in text or "spotify" in text or "notion" in text):
        app_name = text.split("open", 1)[1].strip()
        return open_application(app_name)

    if "take a screenshot" in text or "capture my screen" in text:
        return take_screenshot()

    # --- NEW: File Management ---
    if "create folder" in text:
        name = text.split("create folder", 1)[1].strip() or "new_folder"
        return create_folder(name)

    # --- NEW: System Info ---
    # IMPROVEMENT: Adding 'systematic status' and 'status' to catch common misrecognitions
    if "system status" in text or "battery" in text or "pc health" in text or "systematic status" in text or "status" in text:
        return system_info()
    
    
    # --- Phase 1 Commands (Existing) ---
    
    # Time command
    if "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
        return True

    # Open Visual Studio Code (kept as specific fallback)
    if "open visual studio code" in text or "open code" in text:
        try:
            subprocess.Popen(["code"])
            speak("Opening Visual Studio Code now.")
        except FileNotFoundError:
            speak("Sorry, I couldn't find the Visual Studio Code executable.")
        return True

    # Exit command
    if "exit" in text or "goodbye" in text or "stop listening" in text:
        speak("Goodbye Nova. I’ll be here when you need me.")
        return "EXIT"

    # --- General Intelligence Fallback (Phase 3) ---
    # If no hardcoded command matched, send it to the AI.
    speak("I'm accessing my knowledge core...")
    ai_answer = get_ai_response(text)
    
    if "Sorry, my AI brain is currently offline" in ai_answer:
         # If AI failed, fall back to the original hardcoded message
         return False 
    else:
         # --- If no command matched, use AI Brain ---
        ai_answer = get_ai_response(text)
        speak(ai_answer)
        return True



def main_loop():
    """Main continuous listening and response loop."""
    speak("Hello Nova, I am Pipoo. I'm listening for your commands.")

    while True:
        user_input = listen_for_command()

        if user_input:
            result = handle_basic_commands(user_input)

            if result == "EXIT":
                break
            elif result is False:
                # This only fires now if the AI failed to connect/respond.
                speak("I'm not trained for that command yet.") 
        
        time.sleep(0.5)


if __name__ == "__main__":
    main_loop()