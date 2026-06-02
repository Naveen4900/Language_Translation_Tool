import customtkinter as ctk
from tkinter import messagebox
from translator.engine import LANGUAGES, detect_language, translate_async
from translator.tts import speak

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

LANG_NAMES = list(LANGUAGES.keys())
LANG_CODES = LANGUAGES


class TranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Language Translation Tool — CodeAlpha")
        self.geometry("860x620")
        self.resizable(True, True)
        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(self, text="🌐 Language Translation Tool",
                     font=ctk.CTkFont(size=22, weight="bold")).grid(
                     row=0, column=0, pady=(20, 2))
        ctk.CTkLabel(self, text="CodeAlpha Internship · Powered by Google Translate",
                     font=ctk.CTkFont(size=11), text_color="gray").grid(row=1, column=0)

        # Language bar
        lang_bar = ctk.CTkFrame(self, fg_color="transparent")
        lang_bar.grid(row=2, column=0, pady=14)

        self.src_var = ctk.StringVar(value="Auto Detect")
        self.tgt_var = ctk.StringVar(value="Spanish")
        self.detected_var = ctk.StringVar(value="")

        ctk.CTkLabel(lang_bar, text="From:").grid(row=0, column=0, padx=6)
        self.src_menu = ctk.CTkComboBox(lang_bar, values=LANG_NAMES,
                                         variable=self.src_var, width=190,
                                         state="readonly")
        self.src_menu.grid(row=0, column=1, padx=6)

        ctk.CTkLabel(lang_bar, text="→",
                     font=ctk.CTkFont(size=18)).grid(row=0, column=2, padx=8)

        ctk.CTkLabel(lang_bar, text="To:").grid(row=0, column=3, padx=6)
        self.tgt_menu = ctk.CTkComboBox(lang_bar, values=LANG_NAMES,
                                         variable=self.tgt_var, width=190,
                                         state="readonly")
        self.tgt_menu.grid(row=0, column=4, padx=6)

        self.detected_lbl = ctk.CTkLabel(lang_bar, textvariable=self.detected_var,
                                          text_color="#888", font=ctk.CTkFont(size=11))
        self.detected_lbl.grid(row=1, column=0, columnspan=5, pady=(4, 0))

        # Input
        ctk.CTkLabel(self, text="Input Text",
                     font=ctk.CTkFont(weight="bold")).grid(
                     row=3, column=0, sticky="w", padx=44)
        self.input_box = ctk.CTkTextbox(self, height=160,
                                         font=ctk.CTkFont(size=13))
        self.input_box.grid(row=4, column=0, sticky="ew", padx=40, pady=(2, 8))

        # Buttons
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.grid(row=5, column=0, pady=4)

        ctk.CTkButton(btn_row, text="Translate ↵", command=self._on_translate,
                      width=130).grid(row=0, column=0, padx=8)
        ctk.CTkButton(btn_row, text="📋 Copy", command=self._copy,
                      width=100, fg_color="#444").grid(row=0, column=1, padx=8)
        ctk.CTkButton(btn_row, text="🔊 Speak", command=self._speak,
                      width=100, fg_color="#444").grid(row=0, column=2, padx=8)
        ctk.CTkButton(btn_row, text="🗑 Clear", command=self._clear,
                      width=100, fg_color="#333").grid(row=0, column=3, padx=8)

        # Output
        ctk.CTkLabel(self, text="Translation",
                     font=ctk.CTkFont(weight="bold")).grid(
                     row=6, column=0, sticky="w", padx=44)
        self.output_box = ctk.CTkTextbox(self, height=160,
                                          font=ctk.CTkFont(size=13),
                                          state="disabled",
                                          text_color="#7fffb0")
        self.output_box.grid(row=7, column=0, sticky="ew", padx=40, pady=(2, 20))

        # Bind Ctrl+Enter
        self.bind("<Control-Return>", lambda _: self._on_translate())

    # ── Handlers ──────────────────────────────────────────────────────────
    def _on_translate(self):
        text = self.input_box.get("1.0", "end").strip()
        src  = LANG_CODES[self.src_var.get()]
        tgt  = LANG_CODES[self.tgt_var.get()]

        if not text:
            messagebox.showwarning("Empty Input", "Please enter text to translate.")
            return
        if tgt == "auto":
            messagebox.showwarning("Invalid Target", "Choose a valid target language.")
            return

        # Show detected language while translating
        if src == "auto":
            detected = detect_language(text)
            self.detected_var.set(f"Detected: {detected}")

        self._set_output("⏳ Translating...")

        def callback(future):
            try:
                result = future.result()
                self.after(0, self._set_output, result)
            except Exception as e:
                self.after(0, messagebox.showerror, "Error", str(e))

        translate_async(text, src, tgt, callback)

    def _set_output(self, text: str):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", text)
        self.output_box.configure(state="disabled")

    def _copy(self):
        text = self.output_box.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)

    def _speak(self):
        text = self.output_box.get("1.0", "end").strip()
        if text:
            lang = LANG_CODES[self.tgt_var.get()]
            if lang != "auto":
                speak(text, lang)

    def _clear(self):
        self.input_box.delete("1.0", "end")
        self._set_output("")
        self.detected_var.set("")


if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
