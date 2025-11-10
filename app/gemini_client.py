import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.0"))

# Configure client
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize model
client = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config={
        "temperature": TEMPERATURE,
    },
)
