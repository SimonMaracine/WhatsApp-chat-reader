import tkinter as tk

from plotting import timeline
from data import Message, TimelineMode, TimelinePart


class ChooseTimeline(tk.Frame):

    def __init__(self, top_level: tk.Toplevel, messages: list[Message]):
        super().__init__(top_level)
        self.top_level = top_level
        self.messages = messages
        self.pack(padx=10, pady=10, expand=True)

        self.top_level.title("Select Timeline")

        frm_mode = tk.Frame(self)
        frm_mode.grid(row=0, column=0, pady=(0, 30))
        frm_buttons = tk.Frame(self)
        frm_buttons.grid(row=1, column=0)

        self.var_mode = tk.BooleanVar(self, True)
        tk.Radiobutton(frm_mode, text="Bar", variable=self.var_mode, value=True).grid(row=0, column=0)
        tk.Radiobutton(frm_mode, text="Plot", variable=self.var_mode, value=False).grid(row=1, column=0)

        tk.Label(frm_mode, text='Note that the performance of the graph type "bar" may be lower.', wraplength=200) \
            .grid(row=0, column=1, rowspan=2, padx=(30, 0))

        tk.Button(frm_buttons, text="Whole", command=self.whole).grid(row=0, column=0, columnspan=4, sticky="ew")
        tk.Button(frm_buttons, text="Half 1", command=self.half1).grid(row=1, column=0, columnspan=2, sticky="ew")
        tk.Button(frm_buttons, text="Half 2", command=self.half2).grid(row=1, column=2, columnspan=2, sticky="ew")
        tk.Button(frm_buttons, text="Quarter 1", command=self.quarter1).grid(row=2, column=0)
        tk.Button(frm_buttons, text="Quarter 2", command=self.quarter2).grid(row=2, column=1)
        tk.Button(frm_buttons, text="Quarter 3", command=self.quarter3).grid(row=2, column=2)
        tk.Button(frm_buttons, text="Quarter 4", command=self.quarter4).grid(row=2, column=3)

    def whole(self):
        timeline(self.messages, self.var_mode.get(), TimelineMode.WHOLE)

    def half1(self):
        timeline(self.messages, self.var_mode.get(), TimelineMode.HALF, TimelinePart.FIRST)

    def half2(self):
        timeline(self.messages, self.var_mode.get(), TimelineMode.HALF, TimelinePart.SECOND)

    def quarter1(self):
        timeline(self.messages, self.var_mode.get(), TimelineMode.QUARTER, TimelinePart.FIRST)

    def quarter2(self):
        timeline(self.messages, self.var_mode.get(), TimelineMode.QUARTER, TimelinePart.SECOND)

    def quarter3(self):
        timeline(self.messages, self.var_mode.get(), TimelineMode.QUARTER, TimelinePart.THIRD)

    def quarter4(self):
        timeline(self.messages, self.var_mode.get(), TimelineMode.QUARTER, TimelinePart.FOURTH)
