"""
Лабораторна робота №8  –  Варіант 9/10
Тема: Бот підтримки дій при ПОЖЕЖІ У ГРОМАДСЬКИХ МІСЦЯХ
Три LLM вільного доступу: Google Gemini, Groq/LLaMA-3.1, Cohere/Command-R
Аудіоформат: Google STT (вхід) + gTTS (вихід)
"""

import sys
from audio_handler import AudioHandler
from llm_handler import LLMHandler

WELCOME = (
    "Вітаю! Я бот-помічник для дій при пожежі у громадських місцях. "
    "Задавайте питання голосом. "
    "Для завершення роботи скажіть «вихід» або «стоп»."
)

GOODBYE = "До побачення! Бережіть себе та оточуючих!"

EXIT_WORDS = {"вихід", "стоп", "вийти", "завершити", "exit", "stop", "quit"}

RETRY_MSG = "Вибачте, не вдалося розпізнати мову. Будь ласка, спробуйте ще раз."

THINKING_MSG = "Обробляю ваше запитання, зачекайте будь ласка."


def is_exit(text: str) -> bool:
    return any(word in text.lower() for word in EXIT_WORDS)


def print_separator(title: str = "") -> None:
    line = "=" * 60
    if title:
        print(f"\n{line}")
        print(f"  {title}")
        print(line)
    else:
        print(line)


def main() -> None:
    print_separator("БОТ: ПОЖЕЖА У ГРОМАДСЬКИХ МІСЦЯХ")
    print("  LLM: Gemini · Groq/LLaMA-3.1 · Cohere/Command-R")
    print("  Аудіо: Google STT + gTTS (українська)")
    print_separator()

    audio = AudioHandler()
    llm = LLMHandler()

    audio.speak(WELCOME)

    while True:
        print("\n" + "-" * 40)
        audio.speak("Задайте ваше питання.")

        question = audio.listen()

        if not question:
            audio.speak(RETRY_MSG)
            continue

        if is_exit(question):
            audio.speak(GOODBYE)
            print_separator()
            sys.exit(0)

        audio.speak(THINKING_MSG)

        # --- Query all three LLMs ---
        responses = llm.get_all_responses(question)

        # --- Display individual responses ---
        print_separator("ВІДПОВІДІ LLM")
        for name, resp in responses.items():
            print(f"\n[{name}]\n{resp}")

        # --- Aggregate ---
        print_separator("УЗАГАЛЬНЕНА ВІДПОВІДЬ")
        final = llm.aggregate(question, responses)
        print(final)

        # --- Speak final answer ---
        audio.speak(final)


if __name__ == "__main__":
    main()
