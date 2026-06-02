from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
from concurrent.futures import ThreadPoolExecutor

LANGUAGES: dict[str, str] = {
    "Auto Detect":        "auto",
    "English":            "en",
    "Spanish":            "es",
    "French":             "fr",
    "German":             "de",
    "Italian":            "it",
    "Portuguese":         "pt",
    "Russian":            "ru",
    "Japanese":           "ja",
     "Chinese (Simplified)": "zh-CN",
    "Arabic":             "ar",
    "Hindi":              "hi",
    "Korean":             "ko",
    "Dutch":              "nl",
    "Turkish":            "tr",
    "Polish":             "pl",
    "Swedish":            "sv",
    "Urdu":               "ur",
}

LANG_CODE_TO_NAME = {v: k for k, v in LANGUAGES.items()}
_executor = ThreadPoolExecutor(max_workers=2)


def translate(text: str, source: str, target: str) -> str:
    if not text.strip():
        raise ValueError("Input text is empty.")
    if target == "auto":
        raise ValueError("Target language cannot be Auto Detect.")
    return GoogleTranslator(source=source, target=target).translate(text)


def detect_language(text: str) -> str:
    try:
        code = detect(text)
        return LANG_CODE_TO_NAME.get(code, code.upper())
    except LangDetectException:
        return "Unknown"


def translate_async(text, source, target, callback):
    future = _executor.submit(translate, text, source, target)
    future.add_done_callback(lambda f: callback(f))
    return future
