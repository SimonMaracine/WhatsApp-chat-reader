import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from data import read_chat_file, Message, retrieve_data, is_chat
from plotting import day, week
from about import About
from choose_timeline import ChooseTimeline


class MainApplication(tk.Frame):

    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.root = root
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.root.option_add("*tearOff", False)
        self.root.title("WhatsApp Chat Reader")

        men_file = tk.Menu(self)
        men_file.add_command(label="Open Chat", command=self.open_chat)

        men_help = tk.Menu(self)
        men_help.add_command(label="About", command=self.about)

        men_main = tk.Menu(self)
        men_main.add_cascade(label="File", menu=men_file)
        men_main.add_cascade(label="Help", menu=men_help)
        self.root.configure(menu=men_main)

        # Main frames
        frm_people = tk.Frame(self, relief="ridge", bd=3)
        frm_people.grid(row=0, column=0, padx=(0, 5), sticky="nsew")

        frm_right_side = tk.Frame(self)
        frm_right_side.grid(row=0, column=1, sticky="nsew")
        frm_right_side.columnconfigure(0, weight=1)
        frm_right_side.rowconfigure(0, weight=1)
        frm_right_side.rowconfigure(1, weight=1)
        frm_right_side.rowconfigure(2, weight=1)

        # Left side
        bar_people = tk.Scrollbar(frm_people, orient="vertical")
        bar_people.pack(side="right", fill="y")

        self.cvs_people = tk.Canvas(frm_people, width=370, borderwidth=0, yscrollcommand=bar_people.set)
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
        tk.Label(frm_oldest_newest, textvariable=self.var_oldest, font="Times, 13").grid(row=0, column=0)
        self.var_newest = tk.StringVar(frm_oldest_newest, "Newest: n/a")
        tk.Label(frm_oldest_newest, textvariable=self.var_newest, font="Times, 13").grid(row=1, column=0)

        self.var_days = tk.StringVar(frm_oldest_newest, "0 days")
        tk.Label(frm_oldest_newest, textvariable=self.var_days, font="Times, 13").grid(row=2, column=0)

        frm_buttons = tk.Frame(frm_right_side)
        frm_buttons.grid(row=2, column=0)
        tk.Button(frm_buttons, text="Timeline", command=self.timeline, font="Times, 13") \
            .grid(row=0, column=0, columnspan=2, pady=(0, 8))
        tk.Button(frm_buttons, text="Week", command=self.week, font="Times, 13").grid(row=1, column=0, padx=(0, 8))
        tk.Button(frm_buttons, text="Day", command=self.day, font="Times, 13").grid(row=1, column=1)

        self.messages: list[Message] = []
        self.days = 0  # Needed by timeline; it's the total number of days from the first to the lst message

    def frame_configure(self):
        self.cvs_people.configure(scrollregion=self.cvs_people.bbox("all"))

    def open_chat(self):
        file_path = filedialog.askopenfilename(parent=self.root)  # Returns nothing on cancel or exit

        if not file_path:
            return

        try:
            if not is_chat(file_path):
                print("This is not a chat file", file=sys.stderr)
                messagebox.showerror("Invalid Chat", "This is not a chat file.", parent=self.root)
                return
        except OSError:
            messagebox.showerror("Some Error", "There is an error opening this file.", parent=self.root)
            return

        try:
            self.messages = read_chat_file(file_path)
        except OSError:
            messagebox.showerror("Some Error", "There is an error opening this file.", parent=self.root)
            return
        except RuntimeError:
            messagebox.showerror("File Error", "The chat file is corrupted.", parent=self.root)
            return

        self.reset_UI()

        data = retrieve_data(self.messages)

        self.days = (data.newest_message.date() - data.oldest_message.date()).days

        people = 0
        for person, count in data.people.items():
            tk.Label(self.frm_canvas_frame, text=f"{person}", font="Times, 14") \
                .grid(row=people, column=0, padx=(0, 20), pady=(0, 10))

            text = f"{count} messages" if count > 1 else "1 message"
            tk.Label(self.frm_canvas_frame, text=text, font="Times, 14") \
                .grid(row=people, column=1, pady=(0, 10))

            people += 1

        self.var_total_messages.set(f"{data.total_messages} total messages")
        self.var_oldest.set(f"Oldest: {str(data.oldest_message)[0:-3]}")
        self.var_newest.set(f"Newest: {str(data.newest_message)[0:-3]}")
        self.var_days.set(f"{self.days} days")

    def reset_UI(self):
        for widget in self.frm_canvas_frame.winfo_children():
            widget.destroy()

        self.var_total_messages.set("0 total messages")
        self.var_oldest.set("Oldest: n/a")
        self.var_newest.set("Newest: n/a")
        self.var_days.set("0 days")

    def timeline(self):
        if not self.messages:
            print("Please open a chat", file=sys.stderr)
            messagebox.showerror("No Chat Opened", "Please open a chat.", parent=self.root)
            return

        top_level = tk.Toplevel()
        ChooseTimeline(top_level, self.messages, self.days)

    def week(self):
        if not self.messages:
            print("Please open a chat", file=sys.stderr)
            messagebox.showerror("No Chat Opened", "Please open a chat.", parent=self.root)
            return

        week(self.messages)

    def day(self):
        if not self.messages:
            print("Please open a chat", file=sys.stderr)
            messagebox.showerror("No Chat Opened", "Please open a chat.", parent=self.root)
            return

        day(self.messages)

    @staticmethod
    def about():
        top_level = tk.Toplevel()
        About(top_level)


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
