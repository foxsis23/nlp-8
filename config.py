import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")

# Audio settings
LANGUAGE_CODE = "uk-UA"   # for Google STT
TTS_LANGUAGE = "uk"       # for gTTS

# LLM model names
GEMINI_MODEL = "gemini-2.5-flash-lite"
GROQ_MODEL = "llama-3.1-8b-instant"
COHERE_MODEL = "command-r-plus-08-2024"

SYSTEM_PROMPT = """Ти є спеціалізованим помічником із дій у кризових ситуаціях при пожежах у громадських місцях.
Твоя роль — надавати чіткі, точні та покрокові інструкції з безпеки українською мовою.
Правила відповіді:
- Будь спокійним, впевненим та зрозумілим.
- Давай практичні, дієві поради.
- Відповідай лише зв'язними реченнями (без маркованих списків з символами "-", "*", "•").
- Максимум 4-5 речень на відповідь.
- Пріоритет: збереження життя та безпечна евакуація."""
