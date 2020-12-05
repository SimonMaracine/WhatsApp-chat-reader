import tkinter as tk

from data import read_chat_file, Message


class MainApplication(tk.Frame):

    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.root = root
        self.pack(fill="both", expand=True, padx=30, pady=30)

        self.root.option_add("*tearOff", False)
        self.root.title("WhatsApp Chat Reader")

        men_file = tk.Menu(self)
        men_file.add_command(label="Open Chat", command=None)

        men_help = tk.Menu(self)
        men_help.add_command(label="About", command=None)

        men_main = tk.Menu(self)
        men_main.add_cascade(label="File", menu=men_file)
        men_main.add_cascade(label="Help", menu=men_help)

        # Main frames
        frm_people = tk.Frame(self, relief="ridge", bd=3)
        frm_people.grid(row=0, column=0)

        frm_right_side = tk.Frame(self)
        frm_right_side.grid(row=0, column=1)

        tk.Label(frm_people, text="Simon - 100 messages").pack()

        self.messages: list[Message] = []

        read_chat_file("../chats/WhatsApp Chat with +40 758 628 378.txt", self.messages)


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
