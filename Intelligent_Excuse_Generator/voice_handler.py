# voice_handler.py — Text-to-speech and audio playback using gTTS and pygame

import os
import tempfile
import pygame
from gtts import gTTS


# Supported languages for TTS
LANGUAGES = {
    "English":    {"code": "en"},
    "Spanish":    {"code": "es"},
    "French":     {"code": "fr"},
    "German":     {"code": "de"},
    "Italian":    {"code": "it"},
    "Portuguese": {"code": "pt"},
    "Russian":    {"code": "ru"},
    "Japanese":   {"code": "ja"},
    "Chinese":    {"code": "zh-CN"},
    "Arabic":     {"code": "ar"},
    "Hindi":      {"code": "hi"},
}


class VoiceHandler:
    """
    Handles text-to-speech generation and audio playback.
    """

    def __init__(self):
        self.current_audio_file = None
        self._init_audio()

    def _init_audio(self):
        """Initialize pygame audio mixer."""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        except Exception as e:
            print(f"[VoiceHandler] Audio init error: {e}")

    def speak(self, text: str, language: str = "English"):
        """
        Convert text to speech and play it.

        Args:
            text (str): The text to speak.
            language (str): Language name key (from LANGUAGES dict).
        """
        lang_code = LANGUAGES.get(language, {}).get("code", "en")

        try:
            self.stop()  # Stop any currently playing audio
            tts = gTTS(text=text, lang=lang_code)

            # Save to temp file
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            self.current_audio_file = tmp.name
            tmp.close()

            tts.save(self.current_audio_file)
            pygame.mixer.music.load(self.current_audio_file)
            pygame.mixer.music.play()

        except Exception as e:
            print(f"[VoiceHandler] TTS error: {e}")

    def stop(self):
        """Stop audio playback and clean up temp file."""
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception:
            pass

        if self.current_audio_file and os.path.exists(self.current_audio_file):
            try:
                os.remove(self.current_audio_file)
            except Exception:
                pass
            self.current_audio_file = None

    def is_playing(self) -> bool:
        """Return True if audio is currently playing."""
        try:
            return pygame.mixer.music.get_busy()
        except Exception:
            return False

    def get_available_languages(self) -> list:
        """Return list of supported language names."""
        return list(LANGUAGES.keys())
