import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
import pygame

from config import LANGUAGE_CODE, TTS_LANGUAGE


class AudioHandler:
    """Handles speech-to-text input and text-to-speech output."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        pygame.mixer.init()

    def listen(self, timeout: int = 10, phrase_limit: int = 30) -> str:
        """
        Record audio from microphone and return transcribed text.
        Returns empty string on failure.
        """
        try:
            with sr.Microphone() as source:
                print("  [Мікрофон активний — говоріть...]")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit
                )

            text = self.recognizer.recognize_google(audio, language=LANGUAGE_CODE)
            print(f"  [Розпізнано]: {text}")
            return text

        except sr.WaitTimeoutError:
            print("  [Час очікування вичерпано]")
            return ""
        except sr.UnknownValueError:
            print("  [Мова не розпізнана]")
            return ""
        except sr.RequestError as e:
            print(f"  [Помилка STT]: {e}")
            return ""

    def speak(self, text: str) -> None:
        """Convert text to Ukrainian speech and play it."""
        if not text.strip():
            return

        print(f"\n  [БОТ]: {text}\n")

        try:
            tts = gTTS(text=text, lang=TTS_LANGUAGE, slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp_path = tmp.name
                tts.save(tmp_path)

            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()

        except Exception as e:
            print(f"  [Помилка TTS]: {e}")
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
