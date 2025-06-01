import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables (make sure your .env file is in the correct directory)
load_dotenv()

# Configure the Gemini API key
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please set it.")
genai.configure(api_key=GEMINI_API_KEY)

# List available models
try:
    for m in genai.list_models():
        # Filter for generative models (as opposed to embedding models, etc.)
        if "generateContent" in m.supported_generation_methods:
            print(f"Model Name: {m.name}")
            print(f"  Description: {m.description}")
            print(f"  Version: {m.version}")
            print(f"  Supported Methods: {m.supported_generation_methods}")
            print("-" * 30)
except Exception as e:
    print(f"An error occurred while listing models: {e}")
    print("Please ensure your GEMINI_API_KEY is correct and you have network access.")