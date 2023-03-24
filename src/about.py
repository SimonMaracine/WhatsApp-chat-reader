import tkinter as tk

VERSION = "v0.3.0"


class About(tk.Frame):

    def __init__(self, top_level: tk.Toplevel):
        super().__init__(top_level)
        self.top_level = top_level
        self.pack(padx=10, pady=10, expand=True)

        self.top_level.title("About")

        tk.Label(self, text=f"WhatsApp Chat Reader {VERSION}", font="Times, 23").grid(row=0, column=0)
        tk.Label(self, text="Made by Simon Mărăcine", font="Times, 14").grid(row=1, column=0, pady=(8, 0))
        tk.Label(self, text="Thank you for checking this program out!", font="Times, 12").grid(row=2, column=0, pady=(8, 0))

        tk.Button(self, text="Ok", command=self.top_level.destroy).grid(row=3, column=0, pady=(16, 0))
