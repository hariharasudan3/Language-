import tkinter as tk
from tkinter import ttk
from threading import Thread
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import pyttsx3 

class TranslatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Language Translator")
        self.label_input_type = ttk.Label(self.master, text="Choose input type:")
        self.label_input_type.grid(row=0, column=0, padx=10, pady=10)
        self.input_type_var = tk.StringVar()
        self.input_type_var.set("text")
        self.radio_text = ttk.Radiobutton(self.master, text="Text", variable=self.input_type_var, value="text", command=self.update_prompt_label)
        self.radio_text.grid(row=0, column=1, padx=10, pady=10)
        self.radio_speech = ttk.Radiobutton(self.master, text="Speech", variable=self.input_type_var, value="speech", command=self.update_prompt_label)
        self.radio_speech.grid(row=0, column=2, padx=10, pady=10)
        self.label_input = ttk.Label(self.master, text="Enter text:")
        self.label_input.grid(row=1, column=0, padx=10, pady=10)
        self.input_text_var = tk.StringVar()
        self.entry_input = ttk.Entry(self.master, textvariable=self.input_text_var, width=30)
        self.entry_input.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        self.label_output_type = ttk.Label(self.master, text="Choose output type:")
        self.label_output_type.grid(row=2, column=0, padx=10, pady=10)
        self.output_type_var = tk.StringVar()
        self.output_type_var.set("voice")
        self.radio_voice = ttk.Radiobutton(self.master, text="Voice", variable=self.output_type_var, value="voice")
        self.radio_voice.grid(row=2, column=1, padx=10, pady=10)
        self.radio_text = ttk.Radiobutton(self.master, text="Text", variable=self.output_type_var, value="text")
        self.radio_text.grid(row=2, column=2, padx=10, pady=10)
        self.label_target_language = ttk.Label(self.master, text="Enter target language code:")
        self.label_target_language.grid(row=3, column=0, padx=10, pady=10)
        self.target_language_var = tk.StringVar()
        self.entry_target_language = ttk.Entry(self.master, textvariable=self.target_language_var, width=10)
        self.entry_target_language.grid(row=3, column=1, padx=10, pady=10)
        self.btn_translate = ttk.Button(self.master, text="Translate", command=self.translate_text)
        self.btn_translate.grid(row=4, column=0, columnspan=3, pady=10)
        self.label_result = ttk.Label(self.master, text="")
        self.label_result.grid(row=5, column=0, columnspan=3, pady=10)
        self.label_detected_language = ttk.Label(self.master, text="Detected Language: ")
        self.label_detected_language.grid(row=6, column=0, columnspan=3, pady=10)
        self.label_prompt = ttk.Label(self.master, text="")
        self.label_prompt.grid(row=7, column=0, columnspan=3, pady=10)

    def update_prompt_label(self):
        input_type = self.input_type_var.get()
        if input_type == 'speech':
            self.label_prompt.config(text="")
        else:
            self.label_prompt.config(text="")

    def get_user_input(self):
        user_input_type = self.input_type_var.get()
        if user_input_type == 'text':
            return self.input_text_var.get(), 'text'
        elif user_input_type == 'speech':
            return self.speech_to_text(), 'speech'
        else:
            print("Invalid input type. Please choose 'text' or 'speech'.")
            return None, None

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak something...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
            return None

    def text_to_speech_pyttsx3(self, text, lang='en'):
        try:
            engine = pyttsx3.init(driverName='sapi5')
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("pyttsx3 Text-to-speech error:", e)
            self.text_to_speech_gtts(text, lang)

    def text_to_speech_gtts(self, text, lang='en'):
        try:
            tts = gTTS(text=text, lang=lang, slow=True)
            tts.save("output.mp3")
            os.system("start output.mp3")
        except Exception as e:
            print("gTTS Text-to-speech error:", e)

    def play_audio_parallel(self, text):
        print("Your audio is playing")
        Thread(target=self.text_to_speech_pyttsx3, args=(text,)).start()

    def translate_text(self):
        input_text, input_type = self.get_user_input()
        if input_text is None or input_type is None:
            return
        print("Input:", input_text)

        try:
            translator = Translator()
            detected_language = translator.detect(input_text).lang
            self.label_detected_language.config(text=f"Detected Language: {LANGUAGES[detected_language].capitalize()}")
            target_language = self.entry_target_language.get()
            translation = translator.translate(input_text, dest=target_language)
            translated_text = translation.text
            if self.output_type_var.get() == 'voice':
                self.label_prompt.config(text="")
                self.play_audio_parallel(translated_text)
                self.label_result.config(text="Your audio is playing")
            else:
                self.label_prompt.config(text="")
                self.label_result.config(text=f"Translated Text: {translated_text}")
        except Exception as e:
            self.label_result.config(text=f"Translation error: {e}")
            print("Translation error:", e)
    
    def list_language_codes(self):
        print("Supported languages and their codes:")
        languages = ["en", "es", "fr", "de", "it", "ja", "ko", "zh-CN"]
        for language in languages:
            print(f"{language}: {self.translate_text('Hello', language)}")

def main():
    root = tk.Tk()
    icon_path = 'C:\\Users\HEMANTH KUMAR\\OneDrive\\Desktop\\Edits\\somesh lop\\icon.ico'
    if os.path.exists(icon_path):
        root.iconbitmap(default=icon_path)
    else:
        print("Icon file not found:", icon_path)
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
