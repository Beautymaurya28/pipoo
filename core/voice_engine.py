# NoovaX/core/voice_engine.py

import speech_recognition as sr
import pyttsx3
import time
import json
import os

# --- CONFIGURATION LOADER ---

# Define the relative path to the config file
CONFIG_PATH = os.path.join('data', 'config.json')

def load_config():
    """Loads configuration settings from data/config.json."""
    # Check if running from the root directory
    if not os.path.exists(CONFIG_PATH):
        # Check if the script is being run directly from the 'core' folder
        alt_path = os.path.join('..', 'data', 'config.json')
        if os.path.exists(alt_path):
            config_file = alt_path
        else:
            print(f"Warning: Configuration file not found at {CONFIG_PATH}. Using defaults.")
            return {"stt_language_code": "en-US", "tts_rate": 160}
    else:
        config_file = CONFIG_PATH

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}. Using defaults.")
        return {"stt_language_code": "en-US", "tts_rate": 160}

# Load configuration settings
config = load_config()
TTS_RATE = config.get("tts_rate", 160)
STT_LANG = config.get("stt_language_code", "en-US")

# --- INITIALIZATION ---
r = sr.Recognizer()


def speak(text):
    """Converts text to speech and speaks it out using a temporary engine."""
    
    # 1. Terminal Response
    print(f"Assistant: {text}")

    # 2. Initialize engine inside the function (helps prevent pyttsx3 freezing)
    try:
        temp_engine = pyttsx3.init()
        
        # Use the configurable, more human-like TTS rate (e.g., 160 WPM)
        temp_engine.setProperty('rate', TTS_RATE) 
        temp_engine.setProperty('volume', 0.9)
        
        # 3. Voice Response
        temp_engine.say(text)
        
        # 4. Execution (Must be called to hear the audio)
        temp_engine.runAndWait()
        
    except Exception as e:
        print(f"ERROR: pyttsx3 failed to speak. Check system drivers or try an older version: {e}")
        
    finally:
        # Clean up the engine object
        if 'temp_engine' in locals():
            # Explicitly stop/clean up the engine if possible (though often handled by runAndWait)
            pass


def listen_for_command():
    """
    Listens for audio input from the user and converts it to text,
    using the language code specified in config.json.
    """
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print(f"\nListening ({STT_LANG})...") # Indicate the current listening language
        
        audio = None
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("No speech detected after timeout.")
            return ""
        
        if audio:
            print("Processing...")

    recognized_text = ""
    try:
        # CRITICAL: Use the configurable language code (STT_LANG)
        recognized_text = r.recognize_google(audio, language=STT_LANG).lower()
        print(f"User said: {recognized_text}")
    
    except sr.UnknownValueError:
        # User spoke, but Google STT couldn't parse it
        pass
    except sr.RequestError:
        # Network issue or service down
        print("Speech service request failed. Check internet connection.")

    return recognized_text