# Task 1: Language Translation Tool

A functional, ready-to-run translation application with two interfaces:

- **`translator_app.py`** — full graphical desktop app (Tkinter) with language
  dropdowns, translate button, copy-to-clipboard, and text-to-speech.
- **`translator_cli.py`** — lightweight terminal version (no GUI required).

## ✅ Features Implemented
- User interface to enter text and select source & target languages
- Uses Google Translate engine (via the free `deep-translator` library — no API key needed)
- Sends text and receives translated response
- Displays translated text clearly on screen
- Optional: Copy button + Text-to-Speech button

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the GUI version
python translator_app.py

# --- OR ---

# 2. Run the terminal version
python translator_cli.py
```

## 📁 Files
| File | Purpose |
|---|---|
| `translator_app.py` | GUI application (Tkinter) |
| `translator_cli.py` | Command-line version |
| `requirements.txt` | Python dependencies |

## Notes
- Internet connection is required (Google Translate is a web-based engine).
- If you'd rather use an official API key (Google Cloud Translate API or Microsoft
  Translator), swap out the `GoogleTranslator` call in `translator_app.py`
  with your authenticated client — the rest of the UI logic stays the same.
- Text-to-speech (`pyttsx3`) works fully offline once installed.
