"""
TASK 1: Language Translation Tool
-----------------------------------
A simple GUI application that lets users enter text, select source & target
languages, and get the translated text back instantly.

Features implemented:
✔ User interface (Tkinter)
✔ Uses a free translation engine (Google Translate, via deep-translator)
✔ Sends text to the API and gets translated response
✔ Displays translated text clearly on screen
✔ Optional: Copy button + Text-to-Speech button

HOW TO RUN:
    1. Install dependencies:
         pip install -r requirements.txt
    2. Run the app:
         python translator_app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

try:
    from deep_translator import GoogleTranslator
except ImportError:
    raise ImportError(
        "deep-translator is not installed. Run: pip install deep-translator"
    )

# Optional text-to-speech (works offline)
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


# ---------------------------------------------------------------------------
# Language list (code : friendly name) - a practical subset of Google Translate
# ---------------------------------------------------------------------------
LANGUAGES = {
    "auto": "Detect Language",
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh-CN": "Chinese (Simplified)",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "bn": "Bengali",
    "gu": "Gujarati",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu",
    "tr": "Turkish",
    "nl": "Dutch",
}

NAME_TO_CODE = {v: k for k, v in LANGUAGES.items()}


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Language Translator")
        self.root.geometry("720x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6fa")

        self.tts_engine = pyttsx3.init() if TTS_AVAILABLE else None

        self._build_ui()

    # ---------------------------------------------------------------
    def _build_ui(self):
        title = tk.Label(
            self.root, text="🌐 Language Translation Tool",
            font=("Segoe UI", 18, "bold"), bg="#f4f6fa", fg="#1a1a2e"
        )
        title.pack(pady=(15, 10))

        # ---- Language selection row ----
        lang_frame = tk.Frame(self.root, bg="#f4f6fa")
        lang_frame.pack(pady=5)

        tk.Label(lang_frame, text="From:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=0, column=0, padx=5)
        self.src_lang = ttk.Combobox(lang_frame, values=list(LANGUAGES.values()), width=20, state="readonly")
        self.src_lang.set("Detect Language")
        self.src_lang.grid(row=0, column=1, padx=5)

        swap_btn = tk.Button(lang_frame, text="⇄", font=("Segoe UI", 12, "bold"),
                              command=self.swap_languages, bg="#4361ee", fg="white",
                              relief="flat", width=3)
        swap_btn.grid(row=0, column=2, padx=10)

        tk.Label(lang_frame, text="To:", font=("Segoe UI", 11), bg="#f4f6fa").grid(row=0, column=3, padx=5)
        self.tgt_lang = ttk.Combobox(lang_frame, values=[v for k, v in LANGUAGES.items() if k != "auto"],
                                      width=20, state="readonly")
        self.tgt_lang.set("Hindi")
        self.tgt_lang.grid(row=0, column=4, padx=5)

        # ---- Input text box ----
        tk.Label(self.root, text="Enter text:", font=("Segoe UI", 11, "bold"),
                 bg="#f4f6fa", fg="#1a1a2e").pack(anchor="w", padx=30, pady=(15, 0))
        self.input_text = tk.Text(self.root, height=6, width=78, font=("Segoe UI", 11), wrap="word")
        self.input_text.pack(padx=30, pady=5)

        # ---- Action buttons ----
        btn_frame = tk.Frame(self.root, bg="#f4f6fa")
        btn_frame.pack(pady=8)

        self.translate_btn = tk.Button(
            btn_frame, text="Translate ➜", font=("Segoe UI", 11, "bold"),
            bg="#2a9d8f", fg="white", relief="flat", padx=20, pady=6,
            command=self.translate_text_thread
        )
        self.translate_btn.grid(row=0, column=0, padx=10)

        clear_btn = tk.Button(
            btn_frame, text="Clear", font=("Segoe UI", 11),
            bg="#e63946", fg="white", relief="flat", padx=20, pady=6,
            command=self.clear_all
        )
        clear_btn.grid(row=0, column=1, padx=10)

        # ---- Output text box ----
        tk.Label(self.root, text="Translated text:", font=("Segoe UI", 11, "bold"),
                 bg="#f4f6fa", fg="#1a1a2e").pack(anchor="w", padx=30, pady=(10, 0))
        self.output_text = tk.Text(self.root, height=6, width=78, font=("Segoe UI", 11),
                                    wrap="word", bg="#eef1f8")
        self.output_text.pack(padx=30, pady=5)

        # ---- Copy / Speak buttons ----
        extra_frame = tk.Frame(self.root, bg="#f4f6fa")
        extra_frame.pack(pady=8)

        copy_btn = tk.Button(
            extra_frame, text="📋 Copy Translation", font=("Segoe UI", 10),
            bg="#4361ee", fg="white", relief="flat", padx=15, pady=5,
            command=self.copy_translation
        )
        copy_btn.grid(row=0, column=0, padx=10)

        speak_btn = tk.Button(
            extra_frame, text="🔊 Speak", font=("Segoe UI", 10),
            bg="#f77f00", fg="white", relief="flat", padx=15, pady=5,
            command=self.speak_translation
        )
        speak_btn.grid(row=0, column=1, padx=10)

        self.status_label = tk.Label(self.root, text="", font=("Segoe UI", 9, "italic"),
                                      bg="#f4f6fa", fg="#555")
        self.status_label.pack(pady=(5, 0))

    # ---------------------------------------------------------------
    def swap_languages(self):
        src = self.src_lang.get()
        tgt = self.tgt_lang.get()
        if src != "Detect Language":
            self.tgt_lang.set(src)
        self.src_lang.set(tgt)

    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.status_label.config(text="")

    def translate_text_thread(self):
        """Run translation in a separate thread so UI doesn't freeze."""
        threading.Thread(target=self.translate_text, daemon=True).start()

    def translate_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input required", "Please enter some text to translate.")
            return

        src_name = self.src_lang.get()
        tgt_name = self.tgt_lang.get()
        src_code = NAME_TO_CODE.get(src_name, "auto")
        tgt_code = NAME_TO_CODE.get(tgt_name, "en")

        self.status_label.config(text="Translating...")
        self.translate_btn.config(state="disabled")

        try:
            translated = GoogleTranslator(source=src_code, target=tgt_code).translate(text)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated)
            self.status_label.config(text="✅ Translation complete.")
        except Exception as e:
            messagebox.showerror("Translation Error", f"Something went wrong:\n{e}")
            self.status_label.config(text="❌ Translation failed.")
        finally:
            self.translate_btn.config(state="normal")

    def copy_translation(self):
        translated = self.output_text.get("1.0", tk.END).strip()
        if translated:
            self.root.clipboard_clear()
            self.root.clipboard_append(translated)
            self.status_label.config(text="📋 Copied to clipboard.")
        else:
            messagebox.showinfo("Nothing to copy", "Translate some text first.")

    def speak_translation(self):
        translated = self.output_text.get("1.0", tk.END).strip()
        if not translated:
            messagebox.showinfo("Nothing to speak", "Translate some text first.")
            return
        if not TTS_AVAILABLE:
            messagebox.showinfo(
                "TTS not available",
                "Install pyttsx3 for text-to-speech: pip install pyttsx3"
            )
            return

        def _speak():
            self.tts_engine.say(translated)
            self.tts_engine.runAndWait()

        threading.Thread(target=_speak, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
