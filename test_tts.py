import pyttsx3

# Initialize the engine
engine = pyttsx3.init()

# Set a simple property (optional, but good practice)
engine.setProperty('rate', 150) 

# Say the text
engine.say("Hello, if you can hear me, the voice engine is working!")

# Wait for the speech to finish
engine.runAndWait()