from gtts import gTTS
import pygame
import tempfile
import os
import threading


def speak(text: str, lang: str) -> None:
    """Non-blocking TTS playback."""
    def _play():
        try:
            tts = gTTS(text=text, lang=lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                path = f.name
            tts.save(path)
            pygame.mixer.init()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.unlink(path)
        except Exception as e:
            print(f"[TTS Error] {e}")

    threading.Thread(target=_play, daemon=True).start()
