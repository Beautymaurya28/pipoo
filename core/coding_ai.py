# NoovaX/core/coding_ai.py

from core.voice_engine import speak
from ollama import Client # NEW
import os

# --- Configuration ---
# CHANGE THIS to the model you pulled (e.g., 'mistral', 'llama3')
MODEL_NAME = 'phi3:mini' 
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", 'http://localhost:11434')

# Initialize the Ollama Client
try:
    ollama_client = Client(host=OLLAMA_HOST)
    # Test connection by listing models (will fail if server is down)
    ollama_client.list() 
    OLLAMA_STATUS = True
except Exception:
    OLLAMA_STATUS = False
    # Use print instead of speak() here to avoid recursive voice calls on startup failure
    print("AI Warning: Local Ollama server connection failed. AI functions disabled.")


def get_ai_response(prompt, context=""):
    """
    Sends a question to the local LLM and returns the response.
    This is the core function for general intelligence.
    """
    if not OLLAMA_STATUS:
        return "Sorry, my AI brain is currently offline. Please run the Ollama server and verify the model name."

    # Construct the prompt with a clear system instruction (this gives the AI personality)
    full_prompt = (
        f"You are an offline, helpful, and concise desktop companion named Pipoo. "
        f"Keep your answers short and friendly. \nUser Query: {prompt}"
    )

    try:
        # Generate the response
        response = ollama_client.generate(
            model=MODEL_NAME, 
            prompt=full_prompt, 
            stream=False # Waits for the complete answer
        )
        
        # Return the clean text response
        return response['response'].strip()
    
    except Exception as e:
        print(f"Ollama communication error: {e}")
        return "I had trouble generating a response from my knowledge core."

# The main.py will now use get_ai_response for any non-hardcoded command.