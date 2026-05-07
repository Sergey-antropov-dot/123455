import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

HISTORY_FILE = "history.json"
MIN_LEN = 6
MAX_LEN = 32

# Символы для генерации пароля
DIGITS = "0123456789"
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPECIALS = "!@#$%^&*()-_=+,.<>/?"

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("500x400")

        self.length = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_specials = tk.BooleanVar(value=True)

        self.history = []

        self._build_gui()
        self.load_history()

    def _build_gui(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        # Параметры генерации
        label_len = ttk.Label(frm, text="Длина пароля:")
        label_len.grid(row=0, column=0, sticky=tk.W)
        slider = ttk.Scale(frm, from_=MIN_LEN, to=MAX_LEN, orient="horizontal", variable=self.length)
        slider.grid(row=0, column=1, columnspan=3, sticky=tk.EW)
        label_len_val = ttk.Label(frm, textvariable=self.length)
        label_len_val.grid(row=0, column=4)

        chk_digits = ttk.Checkbutton(frm, text="Цифры", variable=self.use_digits)
        chk_digits.grid(row=1, column=1, sticky=tk.W)
        chk_letters = ttk.Checkbutton(frm, text="Буквы", variable=self.use_letters)
        chk_letters.grid(row=1, column=2, sticky=tk.W)
        chk_specials = ttk.Checkbutton(frm, text="Спецсимволы", variable=self.use_specials)
        chk_specials.grid(row=1, column=3, sticky=tk.W)

        # Кнопка генерации
        btn_gen = ttk.Button(frm, text="Сгенерировать пароль", command=self.generate_password)
        btn_gen.grid(row=2, column=1, columnspan=3, pady=10)

        # Поле для вывода нового пароля
        self.generated_pw = tk.StringVar()
        lbl_pw = ttk.Label(frm, text="Пароль:")
        lbl_pw.grid(row=3, column=0, sticky=tk.W)
        entry_pw = ttk.Entry(frm, textvariable=self.generated_pw, width=30)
        entry_pw.grid(row=3, column=1, columnspan=3, sticky=tk.EW)

        # Таблица истории
        self.tree = ttk.Treeview(frm, columns=('pw', 'len', 'chars'), show='headings')
        self.tree.heading('pw', text='Пароль')
        self.tree.heading('len', text='Длина')
        self.tree.heading('chars', text='Типы символов')
        self.tree.grid(row=4, column=0, columnspan=5, sticky=tk.NSEW)
        frm.rowconfigure(4, weight=1)

        # Кнопки сохранения/загрузки
        btn_save = ttk.Button(frm, text="Сохранить историю", command=self.save_history)
        btn_save.grid(row=5, column=1)
        btn_load = ttk.Button(frm, text="Загрузить историю", command=self.load_history)
        btn_load.grid(row=5, column=2)

    def generate_password(self):
        length = int(self.length.get())
        if not (MIN_LEN <= length <= MAX_LEN):
            messagebox.showerror("Ошибка", f"Длина пароля должна быть от {MIN_LEN} до {MAX_LEN}.")
            return

        chars = ""
        char_types = []
        if self.use_digits.get():
            chars += DIGITS
            char_types.append("Цифры")
        if self.use_letters.get():
            chars += LETTERS
            char_types.append("Буквы")
        if self.use_specials.get():
            chars += SPECIALS
            char_types.append("Спецсимволы")

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        self.generated_pw.set(password)
        self._add_to_history(password, length, ",".join(char_types))

    def _add_to_history(self, password, length, chars):
        self.history.append({"password": password, "length": length, "chars": chars})
        self.tree.insert('', tk.END, values=(password, length, chars))

    def save_history(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успешно", "История сохранена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def load_history(self):
        self.tree.delete(*self.tree.get_children())
        self.history.clear()
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                for item in self.history:
                    self.tree.insert('', tk.END, values=(item['password'], item['length'], item['chars']))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
