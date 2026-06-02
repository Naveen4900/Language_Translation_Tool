# 🌐 Language Translation Tool

> **CodeAlpha Internship — Artificial Intelligence Track | Task 1**

A modern, feature-rich desktop translation application built with Python. Supports 18+ languages with real-time translation, automatic language detection, text-to-speech playback, and a clean dark-mode UI.

---

## 📸 Features

- 🌍 **18+ Languages** — English, Spanish, French, German, Arabic, Hindi, Japanese, Chinese, and more
- 🔍 **Auto Language Detection** — Automatically identifies the input language using `langdetect`
- ⚡ **Async Translation** — Non-blocking translation using `ThreadPoolExecutor` for smooth UI
- 🔊 **Text-to-Speech** — Plays translated text aloud via `gTTS` + `pygame`
- 📋 **Copy to Clipboard** — One-click copy of translated output
- ⌨️ **Keyboard Shortcut** — `Ctrl+Enter` to trigger translation instantly
- 🎨 **Modern Dark UI** — Built with `customtkinter` for a polished look

---

## 🗂 Project Structure

```
CodeAlpha_LanguageTranslationTool/
├── app.py                  # Main entry point, UI logic
├── translator/
│   ├── __init__.py
│   ├── engine.py           # Translation engine, language detection, async wrapper
│   └── tts.py              # Text-to-speech module (non-blocking)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🛠 Tech Stack

| Library | Purpose |
|---|---|
| `customtkinter` | Modern dark-mode desktop UI |
| `deep-translator` | Google Translate API wrapper (free, no API key) |
| `langdetect` | Automatic source language detection |
| `gTTS` | Google Text-to-Speech |
| `pygame` | Audio playback for TTS output |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- macOS / Windows / Linux

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/CodeAlpha_LanguageTranslationTool.git
cd CodeAlpha_LanguageTranslationTool

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python3 app.py
```

---

## 🌐 Supported Languages

| Language | Code | Language | Code |
|---|---|---|---|
| Auto Detect | auto | Arabic | ar |
| English | en | Hindi | hi |
| Spanish | es | Korean | ko |
| French | fr | Dutch | nl |
| German | de | Turkish | tr |
| Italian | it | Polish | pl |
| Portuguese | pt | Swedish | sv |
| Russian | ru | Urdu | ur |
| Japanese | ja | Chinese (Simplified) | zh-CN |

---

## 💡 Usage

1. Enter text in the **Input Text** box
2. Select **Source Language** (or leave as Auto Detect)
3. Select **Target Language**
4. Click **Translate** or press `Ctrl+Enter`
5. Use **Copy** to copy the result, **Speak** to hear it, or **Clear** to reset

---

## 📁 Architecture Overview

```
app.py  (UI Layer)
    │
    ├──▶  translator/engine.py   (Business Logic)
    │         ├── GoogleTranslator  →  deep-translator
    │         ├── detect_language   →  langdetect
    │         └── translate_async   →  ThreadPoolExecutor
    │
    └──▶  translator/tts.py     (Audio Layer)
              └── speak()  →  gTTS + pygame (daemon thread)
```

---

## ⚙️ How It Works

1. User input is passed to `translate_async()` in `engine.py`
2. Translation runs on a background thread — UI stays responsive
3. On completion, the callback updates the output box via `root.after()` (thread-safe)
4. If source is set to Auto Detect, `langdetect` identifies the language before the API call
5. TTS runs in a separate daemon thread to avoid blocking the main loop

---

## 🐛 Known Issues

- TTS is unavailable for `Auto Detect` as target — a valid target language must be selected
- `langdetect` may misidentify very short input strings (< 5 words)
- Requires an active internet connection for translation and TTS

---

## 📄 License

This project was developed as part of the **CodeAlpha AI Internship Program**.  
Free to use for educational purposes.

---

## 🙌 Acknowledgements

- [deep-translator](https://github.com/nidhaloff/deep-translator)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [gTTS](https://github.com/pndurette/gTTS)
- [CodeAlpha](https://www.codealpha.tech) — Internship Program