import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from data import read_chat_file, Message, retrieve_data, is_chat


class MainApplication(tk.Frame):

    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.root = root
        self.pack(fill="both", expand=True, padx=20, pady=20)

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
        frm_people.grid(row=0, column=0, padx=(0, 5))

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
        self.var_total_messages = tk.StringVar(frm_right_side, "0 total messages")
        tk.Label(frm_right_side, textvariable=self.var_total_messages, font="Times, 28", wrap=220) \
            .grid(row=0, column=0, pady=(0, 20))

        frm_oldest_newest = tk.Frame(frm_right_side)
        frm_oldest_newest.grid(row=1, column=0, pady=(0, 20))
        self.var_oldest = tk.StringVar(frm_oldest_newest, "Oldest: n/a")
        tk.Label(frm_oldest_newest, textvariable=self.var_oldest, font="Times, 12").grid(row=0, column=0)
        self.var_newest = tk.StringVar(frm_oldest_newest, "Newest: n/a")
        tk.Label(frm_oldest_newest, textvariable=self.var_newest, font="Times, 12").grid(row=1, column=0)

        frm_buttons = tk.Frame(frm_right_side)
        frm_buttons.grid(row=2, column=0)
        tk.Button(frm_buttons, text="Timeline", command=None, font="Times, 12").grid(row=0, column=0, pady=(0, 8))
        tk.Button(frm_buttons, text="Day", command=None, font="Times, 12").grid(row=1, column=0)

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
            tk.Label(self.frm_canvas_frame, text=f"{person}", font="Times, 12") \
                .grid(row=people, column=0, padx=(0, 20), pady=(0, 10))
            tk.Label(self.frm_canvas_frame, text=f"{count} messages", font="Times, 12") \
                .grid(row=people, column=1, pady=(0, 10))
            people += 1

        self.var_total_messages.set(f"{some_data.total_messages} total messages")
        self.var_oldest.set(f"Oldest: {str(some_data.oldest_message)[0:-3]}")
        self.var_newest.set(f"Newest: {str(some_data.newest_message)[0:-3]}")

    def reset_UI(self):
        pass


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
