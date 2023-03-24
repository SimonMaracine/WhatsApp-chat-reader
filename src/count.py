import tkinter as tk
from tkinter import messagebox

from data import Message, get_number_of_times_character_appears, get_number_of_times_text_appears


class Count(tk.Frame):
    RESULT = "Number of times: "

    def __init__(self, top_level: tk.Toplevel, messages: list[Message]):
        super().__init__(top_level)
        self.top_level = top_level
        self.pack(padx=10, pady=10, expand=True)

        self.messages = messages

        self.top_level.title("Count")

        tk.Label(self, text="Text to find").grid(row=0, column=0)

        self.ent_text = tk.Entry(self)
        self.ent_text.grid(row=0, column=1)

        self.var_result = tk.StringVar(self, value=Count.RESULT)
        tk.Label(self, textvariable=self.var_result).grid(row=1, column=0)

        tk.Button(self, text="Apply", command=self.apply).grid(row=1, column=1)

    def apply(self):
        text = self.ent_text.get()

        if text:
            self.var_result.set(Count.RESULT + str(get_number_of_times_text_appears(self.messages, text)))
        else:
            messagebox.showerror("No Text", "Please provide text to search.", parent=self.top_level)
