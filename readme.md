🩵 PHASE 1: Base System Blueprint (The Foundation)
1. Folder Structure Setup
Start by creating the basic project structure. Use your terminal or file explorer to set this up:

NoovaX/
│
├── core/
│   ├── main.py               # Main entry point & command loop
│   ├── voice_engine.py       # Handles listening (Speech-to-Text) and replying (Text-to-Speech)
│
├── data/
│   ├── config.json           # User settings (wake word, name, voice rate)
│
└── requirements.txt          # List of necessary libraries
2. Libraries to Install
You'll need three core Python libraries for basic I/O (Input/Output).

Add the following to your requirements.txt file:

Plaintext

# Requirements for PHASE 1: Voice I/O and System Commands
SpeechRecognition
pyaudio
pyttsx3
Installation Instructions:

Navigate to the root NoovaX/ directory in your terminal.

Install the libraries using pip:

Bash

pip install -r requirements.txt
Note: pyaudio can sometimes be tricky to install on certain systems (especially Mac/Linux) as it relies on system-level components. If installation fails, search for system-specific instructions (e.g., brew install portaudio on macOS, or sudo apt-get install portaudio19-dev on Debian/Ubuntu, then retry pip install pyaudio)