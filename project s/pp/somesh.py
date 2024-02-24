from translate import Translator

def translate_text(input_text, target_language):
    # Initialize Translator
    translator = Translator(to_lang=target_language)

    # Translate input text to target language
    translated_text = translator.translate(input_text)

    return translated_text

def list_language_codes():
    print("Supported languages and their codes:")
    # You can explore supported languages using the translate library
    # However, note that it may not have the exact same set as googletrans
    translator = Translator()
    languages = translator.detect_langs('')  # Detect language to get a list of supported languages
    for lang in languages:
        print(f"{lang.lang}: {lang.lang}")

def translate_prompt():
    while True:
        # Prompt the user to see the language codes or not
        show_language_codes = input("Do you want to see the list of supported languages and their codes? (yes/no): ")
        if show_language_codes.lower() == 'yes':
            list_language_codes()

        # Get input text from user
        input_text = input("\nEnter text to translate (or type 'exit' to quit): ")
        if input_text.lower() == 'exit':
            break

        print("Input: ", input_text)

        # Prompt the user to specify the target language for translation
        target_language = input("Enter target language code (e.g., fr for French): ")

        # Translate input text
        translated_text = translate_text(input_text, target_language)
        print("Translated: ", translated_text)

def main():
    # Call the translate_prompt function to start the translation process
    translate_prompt()

if __name__ == "__main__":
    main()
