import tkinter as tk
from tkinter import font
import time

class AlphaTypeClean:
    def __init__(self, root):
        self.root = root
        self.root.title("AlphaType - Typing Speed Test")
        self.root.configure(bg="#1E1E2F")
        self.root.state('zoomed')
        self.root.minsize(900, 500)

        # Fonts & Colors
        self.title_font = font.Font(family="Segoe UI", size=48, weight="bold")
        self.sentence_font = font.Font(family="Consolas", size=28)
        self.counter_font = font.Font(family="Segoe UI", size=24, weight="bold")
        self.button_font = font.Font(family="Segoe UI", size=16, weight="bold")

        self.bg_color = "#1E1E2F"
        self.text_color = "#FFFFFF"
        self.accent_color = "#00CFFF"
        self.error_color = "#FF6B6B"

        # Sentences to type
        self.sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "Typing fast improves your productivity every day.",
            "Practice makes perfect, so keep typing and learning.",
            "Python programming is fun and rewarding.",
            "Stay focused and keep improving your typing speed."
        ]
        self.sentence_index = 0
        self.current_sentence = self.sentences[self.sentence_index]
        self.total_chars = len(self.current_sentence)

        self.test_started = False
        self.start_time = 0
        self.correct_chars = 0

        self.setup_ui()
        self.update_counter()

    def setup_ui(self):
        self.title_label = tk.Label(self.root, text="AlphaType", font=self.title_font,
                                    fg=self.accent_color, bg=self.bg_color)
        self.title_label.pack(pady=40)

        self.sentence_label = tk.Label(self.root, text=self.current_sentence, font=self.sentence_font,
                                       fg=self.text_color, bg=self.bg_color, wraplength=self.root.winfo_screenwidth() - 150,
                                       justify="center")
        self.sentence_label.pack(pady=30)

        self.text_entry = tk.Text(self.root, height=4, font=("Consolas", 26), wrap="word",
                                  bg="#2D2D44", fg=self.text_color, insertbackground=self.accent_color,
                                  bd=2, relief="solid")
        self.text_entry.pack(padx=100, fill="x")
        self.text_entry.bind("<KeyRelease>", self.on_key_release)

        self.counter_label = tk.Label(self.root, text="WPM: 0", font=self.counter_font,
                                      fg=self.accent_color, bg=self.bg_color)
        self.counter_label.pack(pady=25)

        self.progress_container = tk.Frame(self.root, bg="#333353", height=20, width=600)
        self.progress_container.pack(pady=10)
        self.progress_container.pack_propagate(0)

        self.progress_bar = tk.Frame(self.progress_container, bg=self.accent_color, width=0, height=20)
        self.progress_bar.pack(side="left")

        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=30)

        self.restart_btn = tk.Button(self.button_frame, text="Restart", font=self.button_font,
                                     bg=self.accent_color, fg=self.bg_color, width=12, command=self.restart_test,
                                     activebackground="#00A5CC", activeforeground=self.bg_color, relief="flat")
        self.restart_btn.grid(row=0, column=0, padx=30)

        self.leave_btn = tk.Button(self.button_frame, text="Leave", font=self.button_font,
                                   bg=self.error_color, fg=self.bg_color, width=12, command=self.confirm_leave,
                                   activebackground="#FF4C4C", activeforeground=self.bg_color, relief="flat")
        self.leave_btn.grid(row=0, column=1, padx=30)

    def on_key_release(self, event):
        if not self.test_started:
            self.test_started = True
            self.start_time = time.time()

        typed_text = self.text_entry.get("1.0", "end-1c")

        # Count correct chars
        self.correct_chars = 0
        for i, c in enumerate(typed_text):
            if i < len(self.current_sentence) and c == self.current_sentence[i]:
                self.correct_chars += 1
            else:
                break  # Stop at first error to prevent premature advancement

        progress_percent = min(len(typed_text) / self.total_chars, 1.0)
        new_width = int(600 * progress_percent)
        self.progress_bar.config(width=new_width)

        # Check if entire sentence is typed correctly
        if typed_text == self.current_sentence:
            self.test_started = False
            self.next_sentence()

    def next_sentence(self):
        self.sentence_index += 1
        if self.sentence_index >= len(self.sentences):
            self.sentence_index = 0  # Loop to start or can show completion message
        self.current_sentence = self.sentences[self.sentence_index]
        self.total_chars = len(self.current_sentence)
        self.sentence_label.config(text=self.current_sentence)
        self.text_entry.delete("1.0", "end")
        self.correct_chars = 0
        self.start_time = 0
        self.counter_label.config(text="WPM: 0")
        self.progress_bar.config(width=0)

    def update_counter(self):
        if self.test_started:
            elapsed_time = time.time() - self.start_time
            words_typed = self.correct_chars / 5
            wpm = int(words_typed / (elapsed_time / 60)) if elapsed_time > 0 else 0
            self.counter_label.config(text=f"WPM: {wpm}")
        else:
            self.counter_label.config(text="WPM: 0")
        self.root.after(500, self.update_counter)

    def restart_test(self):
        self.test_started = False
        self.sentence_index = 0
        self.current_sentence = self.sentences[self.sentence_index]
        self.total_chars = len(self.current_sentence)
        self.sentence_label.config(text=self.current_sentence)
        self.text_entry.delete("1.0", "end")
        self.counter_label.config(text="WPM: 0")
        self.progress_bar.config(width=0)
        self.correct_chars = 0
        self.start_time = 0

    def confirm_leave(self):
        # Overlay dims main window
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.6)
        self.overlay.configure(bg="black")
        self.overlay.focus_set()

        # Popup window on top
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Confirm Exit")
        self.popup.configure(bg=self.bg_color)
        self.popup.geometry("450x200+{}+{}".format(
            int(self.root.winfo_screenwidth() / 2 - 225),
            int(self.root.winfo_screenheight() / 2 - 100)))
        self.popup.transient(self.root)
        self.popup.grab_set()

        msg = tk.Label(self.popup, text="Are you sure you want to leave?", font=("Segoe UI", 18, "bold"),
                       fg=self.accent_color, bg=self.bg_color)
        msg.pack(pady=30)

        btn_frame = tk.Frame(self.popup, bg=self.bg_color)
        btn_frame.pack(pady=10)

        yes_btn = tk.Button(btn_frame, text="Yes", font=("Segoe UI", 14, "bold"),
                            bg=self.error_color, fg=self.bg_color, width=12, command=self.exit_app,
                            relief="flat", activebackground="#FF4C4C")
        yes_btn.grid(row=0, column=0, padx=20)

        no_btn = tk.Button(btn_frame, text="No", font=("Segoe UI", 14, "bold"),
                           bg=self.accent_color, fg=self.bg_color, width=12, command=self.close_popup,
                           relief="flat", activebackground="#00A5CC")
        no_btn.grid(row=0, column=1, padx=20)

        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)

    def close_popup(self):
        self.popup.destroy()
        self.overlay.destroy()

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlphaTypeClean(root)
    root.mainloop()
