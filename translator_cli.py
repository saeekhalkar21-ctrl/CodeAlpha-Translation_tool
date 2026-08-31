"""
TASK 1 (CLI VERSION): Language Translation Tool
-------------------------------------------------
A terminal-based version of the translator - useful if you don't have a
graphical display (e.g., running on a server) or just prefer the command line.

HOW TO RUN:
    pip install -r requirements.txt
    python translator_cli.py
"""

from deep_translator import GoogleTranslator, GoogleTranslator as GT

COMMON_LANGUAGES = {
    "1": ("en", "English"),
    "2": ("hi", "Hindi"),
    "3": ("mr", "Marathi"),
    "4": ("es", "Spanish"),
    "5": ("fr", "French"),
    "6": ("de", "German"),
    "7": ("zh-CN", "Chinese (Simplified)"),
    "8": ("ja", "Japanese"),
    "9": ("ar", "Arabic"),
    "10": ("ru", "Russian"),
}


def print_menu():
    print("\nAvailable target languages:")
    for key, (code, name) in COMMON_LANGUAGES.items():
        print(f"  {key}. {name} ({code})")


def main():
    print("=" * 55)
    print("   🌐  LANGUAGE TRANSLATION TOOL (CLI)")
    print("=" * 55)

    while True:
        text = input("\nEnter text to translate (or 'quit' to exit): ").strip()
        if text.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not text:
            print("Please enter some text.")
            continue

        print_menu()
        choice = input("Choose target language number: ").strip()
        target_code, target_name = COMMON_LANGUAGES.get(choice, ("hi", "Hindi"))

        try:
            result = GoogleTranslator(source="auto", target=target_code).translate(text)
            print(f"\n➡  Translated to {target_name}: {result}")
        except Exception as e:
            print(f"❌ Error while translating: {e}")


if __name__ == "__main__":
    main()
