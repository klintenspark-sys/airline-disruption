import os
from dotenv import load_dotenv
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OLLAMA_HOST = "http://localhost:11434"