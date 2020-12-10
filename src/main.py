import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from data import read_chat_file, Message, retrieve_data, is_chat


class MainApplication(tk.Frame):

    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.root = root
        self.pack(fill="both", expand=True, padx=30, pady=30)

        self.root.option_add("*tearOff", False)
        self.root.title("WhatsApp Chat Reader")

        men_file = tk.Menu(self)
        men_file.add_command(label="Open Chat", command=self.open_chat)

        men_help = tk.Menu(self)
        men_help.add_command(label="About", command=None)

        men_main = tk.Menu(self)
        men_main.add_cascade(label="File", menu=men_file)
        men_main.add_cascade(label="Help", menu=men_help)
        self.root.configure(menu=men_main)

        # Main frames
        frm_people = tk.Frame(self, relief="ridge", bd=3)
        frm_people.grid(row=0, column=0)

        frm_right_side = tk.Frame(self)
        frm_right_side.grid(row=0, column=1)

        # Left side
        bar_people = tk.Scrollbar(frm_people, orient="vertical")
        bar_people.pack(side="right", fill="y")

        self.cvs_people = tk.Canvas(frm_people, width=300, borderwidth=0, yscrollcommand=bar_people.set)
        self.cvs_people.pack(side="left", fill="both", expand=True)
        bar_people.configure(command=self.cvs_people.yview)

        self.frm_canvas_frame = tk.Frame(frm_people)
        self.cvs_people.create_window((0, 0), window=self.frm_canvas_frame, anchor="nw")
        self.frm_canvas_frame.bind("<Configure>", lambda event: self.frame_configure())

        # Right side
        tk.Label(frm_right_side, text="0 total messages", font="Times, 28").grid(row=0, column=0)


        self.messages: list[Message] = []

        # self.messages = read_chat_file("../chats/WhatsApp Chat with +40 758 628 378.txt")

    def frame_configure(self):
        self.cvs_people.configure(scrollregion=self.cvs_people.bbox("all"))

    def open_chat(self):
        file_path = filedialog.askopenfilename(parent=self.root)  # Returns nothing on cancel or exit

        if not file_path:
            return

        if not is_chat(file_path):
            print("This file is not a chat file", file=sys.stderr)
            messagebox.showerror("Invalid Chat", "This file is not a chat file.", parent=self.root)
            return

        self.messages = read_chat_file(file_path)

        self.reset_UI()

        some_data = retrieve_data(self.messages)

        people = 0
        for person, count in some_data.people.items():
            tk.Label(self.frm_canvas_frame, text=f"{person}").grid(row=people, column=0, padx=(0, 30))
            tk.Label(self.frm_canvas_frame, text=f"{count} messages").grid(row=people, column=1)
            people += 1



    def reset_UI(self):
        pass


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
