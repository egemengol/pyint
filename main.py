import tkinter as tk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
from enum import Enum


im_names = [
    "rect",
    "circ",
    "line",
    "draw",
    "undo",
    "color",
]


class Radio(Enum):
    NULL = 0
    RECT = 1
    CIRCLE = 2
    LINE = 3
    DRAW = 4


class Paint:
    def __init__(self, im_names):
        self.last_item = None
        self.setup_grid()
        self.setup_toolbar(im_names)
        self.setup_canvas()
    
    def setup_grid(self):
        self.window = tk.Tk()
        self.window.title("Pyint")

        self.window.rowconfigure(0, weight=0)
        self.window.rowconfigure(1, weight=0, minsize=400)
        self.window.columnconfigure(0, minsize=60, weight=0)
        self.window.columnconfigure(1, minsize=200, weight=1)

        info = tk.Label(
            self.window,
            text="Done with Python and Tkinter from scratch by Egemen Göl.")
        info.grid(row=0, column=0, columnspan=2)

    def setup_toolbar(self, im_names):
        self.radio_val = tk.IntVar()
        self.slider_val = tk.IntVar()
        self.is_undo = tk.BooleanVar()
        self.color = "#000"

        toolbar = tk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1,
        )
        toolbar.grid(row=1, column=0, sticky="ns", padx=1, pady=1)

        # only self because of GC
        self.ims = [
            ImageTk.PhotoImage(file=f"static/{f}.png")
            for f in im_names
        ]

        
        for i, im in enumerate(self.ims[:-2], 1):
            rdio = tk.Radiobutton(
                image=im,
                master=toolbar,
                indicatoron=False,
                relief=tk.RAISED,
                value=i,
                variable=self.radio_val,
            )
            rdio.pack(padx=4, pady=4)

        self.btn_undo = tk.Button(
            image=self.ims[-2],
            master=toolbar,
            relief=tk.RAISED,
            state=tk.DISABLED,
            command=self.handle_undo
        )
        self.btn_undo.pack(padx=4, pady=4)


        btn_color = tk.Button(
            image=self.ims[-1],
            master=toolbar,
            relief=tk.RAISED,
            command=self.handle_color,
        )
        btn_color.pack(padx=4, pady=4)

        
        slider = tk.Scale(
            master=toolbar,
            relief=tk.RAISED,
            from_=12,
            to=1,
            orient=tk.VERTICAL,
            variable=self.slider_val,
        )
        slider.pack(padx=4, pady=4)
    
    def setup_canvas(self):
        self.canvas = tk.Canvas(master=self.window, width=600, height=600, bg="white")
        self.canvas.grid(row=1, column=1, sticky="nw")

        self.canvas.bind("<Button-1>", self.handle_press)
        self.canvas.bind("<ButtonRelease-1>", self.handle_release)
        self.canvas.bind("<B1-Motion>", self.handle_drag)

    def mainloop(self):
        self.window.mainloop()

    def handle_press(self, event):
        self.pressed_x = event.x
        self.pressed_y = event.y
        self.last_item = None
    
    def handle_release(self, event):
        if not Radio(self.radio_val.get()) == Radio.DRAW:
            self.btn_undo.config(state=tk.NORMAL)

    def handle_drag(self, event):
        if not Radio(self.radio_val.get()) == Radio.DRAW:
            self.canvas.delete(self.last_item)
        self.last_item = self.draw(event.x, event.y)
        

    def draw(self, x, y): # -> itemid
        radio = Radio(self.radio_val.get())
        if radio == Radio.LINE:
            return self.canvas.create_line(
                self.pressed_x,
                self.pressed_y,
                x, y,
                width=self.slider_val.get(),
                fill=self.color,
            )
        elif radio == Radio.RECT:
            return self.canvas.create_rectangle(
                self.pressed_x,
                self.pressed_y,
                x, y,
                width=self.slider_val.get(),
                outline=self.color,
            )
        elif radio == Radio.CIRCLE:
            return self.canvas.create_oval(
                self.pressed_x,
                self.pressed_y,
                x, y,
                width=self.slider_val.get(),
                outline=self.color,
            )
        elif radio == Radio.DRAW:
            self.btn_undo.config(state=tk.DISABLED)
            width = self.slider_val.get() // 2
            return self.canvas.create_oval(
                x - width,
                y - width,
                x + width,
                y + width,
                fill=self.color,
                outline=self.color,
            )
    
    def handle_undo(self):
        self.canvas.delete(self.last_item)
        self.btn_undo.config(state=tk.DISABLED)

    def handle_color(self):
        self.color = askcolor(
            self.color,
            title="Please choose a color",
        )[1]



if __name__ == "__main__":
    paint = Paint(im_names)
    paint.mainloop()