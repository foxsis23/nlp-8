from google import genai
from google.genai import types
from groq import Groq
import cohere

from config import (
    GEMINI_API_KEY, GROQ_API_KEY, COHERE_API_KEY,
    GEMINI_MODEL, GROQ_MODEL, COHERE_MODEL,
    SYSTEM_PROMPT,
)


class LLMHandler:
    """
    Wrapper for three free-tier LLMs:
      1. Google Gemini  (gemini-1.5-flash)    via google-genai
      2. Groq / LLaMA-3.1-8B                 via groq
      3. Cohere / Command-R                   via cohere
    """

    def __init__(self):
        self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.cohere_client = cohere.ClientV2(api_key=COHERE_API_KEY)

    # ------------------------------------------------------------------ #
    #  Individual LLM queries                                              #
    # ------------------------------------------------------------------ #

    def ask_gemini(self, question: str) -> str:
        try:
            response = self.gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=question,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    max_output_tokens=350,
                    temperature=0.4,
                ),
            )
            return response.text.strip()
        except Exception as e:
            return f"[Gemini недоступний: {e}]"

    def ask_groq(self, question: str) -> str:
        try:
            response = self.groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question},
                ],
                max_tokens=350,
                temperature=0.4,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[Groq недоступний: {e}]"

    def ask_cohere(self, question: str) -> str:
        try:
            response = self.cohere_client.chat(
                model=COHERE_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question},
                ],
            )
            return response.message.content[0].text.strip()
        except Exception as e:
            return f"[Cohere недоступний: {e}]"

    # ------------------------------------------------------------------ #
    #  Aggregation                                                         #
    # ------------------------------------------------------------------ #

    def get_all_responses(self, question: str) -> dict:
        """Query all three LLMs and return a dict of their answers."""
        print("\n  Запит до Gemini...")
        r1 = self.ask_gemini(question)
        print("  Запит до Groq / LLaMA-3.1...")
        r2 = self.ask_groq(question)
        print("  Запит до Cohere / Command-R...")
        r3 = self.ask_cohere(question)
        return {
            "Gemini": r1,
            "Groq (LLaMA-3.1)": r2,
            "Cohere (Command-R)": r3,
        }

    def aggregate(self, question: str, responses: dict) -> str:
        """
        Use Gemini to synthesise the three responses into one coherent answer
        optimised for audio playback (no bullet symbols, clear sentences).
        """
        valid = {
            name: resp
            for name, resp in responses.items()
            if not resp.startswith("[")
        }

        if not valid:
            return (
                "На жаль, усі три моделі тимчасово недоступні. "
                "Негайно телефонуйте 101 або 112."
            )

        if len(valid) == 1:
            return next(iter(valid.values()))

        prompt = (
            f'Нижче наведено три відповіді різних ШІ-моделей на питання: "{question}"\n\n'
            f'--- Gemini ---\n{responses.get("Gemini", "недоступно")}\n\n'
            f'--- Groq / LLaMA-3.1 ---\n{responses.get("Groq (LLaMA-3.1)", "недоступно")}\n\n'
            f'--- Cohere / Command-R ---\n{responses.get("Cohere (Command-R)", "недоступно")}\n\n'
            "Завдання: узагальни ці відповіді в одну чітку відповідь українською мовою.\n"
            "Вимоги:\n"
            "- Лише зв'язні речення (без маркованих списків).\n"
            "- Максимум 5 речень.\n"
            "- Фрази мають звучати природно при аудіовідтворенні.\n"
            "- Пріоритет: безпека та збереження життя."
        )

        try:
            synthesis = self.gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(max_output_tokens=400),
            )
            return synthesis.text.strip()
        except Exception:
            return max(valid.values(), key=len)
