import tkinter as tk
from tkinter import ttk
from google_trans_new import google_translator

class GlobalSpeakTranslatorApp:
    def __init__(self, root):
        """Initializes the main application window and its widgets."""
        self.root = root
        self.root.title("GlobalSpeak Translator")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Create the main frame to hold all widgets
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a translator instance
        self.translator = google_translator()

        # Input Section
        input_label = ttk.Label(main_frame, text="Enter text to translate:", font=("Helvetica", 12))
        input_label.pack(pady=(0, 5))

        self.input_text = tk.Text(main_frame, height=5, width=60, font=("Helvetica", 10), wrap="word")
        self.input_text.pack()

        # Language Selection Section
        lang_frame = ttk.Frame(main_frame, padding="10 0")
        lang_frame.pack(pady=10)

        lang_label = ttk.Label(lang_frame, text="Select target language:", font=("Helvetica", 10))
        lang_label.pack(side=tk.LEFT, padx=(0, 5))
         
        # Dictionary of supported languages
        self.languages = {
            'Spanish': 'es', 'French': 'fr', 'German': 'de', 'Japanese': 'ja', 
            'Chinese (Simplified)': 'zh-cn', 'Italian': 'it', 'Portuguese': 'pt', 
            'Russian': 'ru', 'Arabic': 'ar', 'Hindi': 'hi'
        }
        
        self.lang_var = tk.StringVar()
        self.lang_combobox = ttk.Combobox(lang_frame, textvariable=self.lang_var, state="readonly")
        self.lang_combobox['values'] = list(self.languages.keys())
        self.lang_combobox.current(0)  # Set default language to the first one
        self.lang_combobox.pack(side=tk.LEFT)

        # Translate Button
        translate_button = ttk.Button(main_frame, text="Translate", command=self.translate_text)
        translate_button.pack(pady=10)

        # Output Section
        output_label = ttk.Label(main_frame, text="Translated text:", font=("Helvetica", 12))
        output_label.pack(pady=(0, 5))

        self.output_text = tk.Text(main_frame, height=5, width=60, font=("Helvetica", 10), wrap="word")
        self.output_text.pack()

    def translate_text(self):
        """Fetches the text from the input, translates it, and displays the result."""
        text_to_translate = self.input_text.get("1.0", tk.END).strip()
        target_lang_name = self.lang_var.get()
        target_lang_code = self.languages.get(target_lang_name, 'en')

        if not text_to_translate:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Please enter some text to translate.")
            return

        try:
            translated = self.translator.translate(text_to_translate, lang_tgt=target_lang_code)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated)
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"An error occurred: {e}")

if __name__ == "__main__":
    # Create the main application instance and run the main loop
    root = tk.Tk()
    app = GlobalSpeakTranslatorApp(root)
    root.mainloop()
