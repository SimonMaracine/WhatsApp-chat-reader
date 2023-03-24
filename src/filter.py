import tkinter as tk
from tkinter import messagebox

from data import Message, get_all_messages_from_person, write_messages_to_file


class Filter(tk.Frame):

    def __init__(self, top_level: tk.Toplevel, messages: list[Message]):
        super().__init__(top_level)
        self.top_level = top_level
        self.pack(padx=10, pady=10, expand=True)

        self.messages = messages

        self.top_level.title("Filter")

        tk.Label(self, text="Person name").grid(row=0, column=0)

        self.ent_text = tk.Entry(self)
        self.ent_text.grid(row=0, column=1)

        tk.Button(self, text="Apply", command=self.apply).grid(row=1, column=0, columnspan=2)

    def apply(self):
        text = self.ent_text.get()

        if text:
            write_messages_to_file(f"messages_of_{text}.txt", get_all_messages_from_person(self.messages, text))
        else:
            messagebox.showerror("No Text", "Please provide text to search.", parent=self.top_level)
