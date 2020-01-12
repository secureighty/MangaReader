import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import random


def clear_image_array(array):
    for i in array:
        i.destroy()


class Viewer:
    def __init__(self, dictionary, timer=None):
        self.n = 0
        self.dict = dictionary
        self.image_array = []
        self.app = tk.Tk()
        self.clear_array = []
        self.timer = timer

    def start(self):
        self.app.bind("<Key>", self.key)
        self.app.attributes("-fullscreen", True)
        self.app["bg"] = "Black"
        self.fill_image_array()
        self.app.update()
        self.display_image_pair()
        if self.timer is not None:
            self.swap_color()
        self.app.mainloop()

    def fill_image_array(self):
        for i in self.dict:
            print(i)
            if i is None:
                self.image_array += [None]
            else:
                load = Image.open(i)
                self.image_array += [load]

    def display_image(self, load, panel_number=0):
        '''
        display image on screen
        :param load: preloaded PIL image
        :param panel_number: is panel first(1), second(2), or a double(0)?
        '''
        # get info on widths and heights
        width, height = load.size
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()

        # logic for how to resize and place an image

        # logic for resizing
        if panel_number != 0:
            # if this panel is a side panel, scale per half the screen. else, scale per the whole screen
            window_width = window_width / 2
        if width / window_width > height / window_height:
            new_width = window_width
            new_height = new_width / width * height
        else:
            new_height = window_height
            new_width = new_height / height * width

        # logic for placing
        if panel_number == 1:
            xpos = window_width
        elif panel_number == 2:
            xpos = window_width - new_width
        elif panel_number == 0:
            xpos = window_width / 2 - new_width / 2
        else:
            print("invalid panel number")
            exit()
        load = load.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.app, image=render)
        img.image = render
        img.place(x=xpos, y=0)
        return img

    def jump_callback(self, page_number):
        try:
            page_number = int(page_number.get())
            if page_number % 2 == 0 and page_number != 0:
                self.n = page_number
            else:
                self.n = page_number - 1
            clear_image_array(self.clear_array)
            self.display_image_pair()
        except ValueError:
            print("NaN")

    def query_jump(self):
        popup = tk.Label(self.app, anchor="center")
        jump_text = tk.Label(popup, text="Jump to what page?")
        self.clear_array += [popup]
        jump_text.pack()
        input_text = tk.StringVar()
        entry = ttk.Entry(popup, textvariable=input_text)
        entry.bind("<Return>", lambda event: self.jump_callback(page_number=input_text))
        entry.pack()
        entry.focus_set()
        popup.pack()

    def display_image_pair(self):
        n = self.n
        m = n + 1
        try:
            if self.image_array[n] is None and self.image_array[m] is None:
                pass
            elif self.image_array[n] is None:
                self.clear_array += [self.display_image(self.image_array[m], 0)]
            elif self.image_array[m] is None:
                self.clear_array += [self.display_image(self.image_array[n], 0)]
            else:
                self.clear_array += [self.display_image(self.image_array[n], 1)]
                self.clear_array += [self.display_image(self.image_array[m], 2)]
        except (KeyError, IndexError):
            pass

    def swap_color(self):
        hex_number = "#%0.6x" % random.randint(0, 16777215)
        self.app.configure(background=hex_number)
        self.app.after(self.timer, self.swap_color)

    def key(self, event):
        kp = event.keysym
        print(kp)
        if kp == "Escape":
            self.key_quit()
        elif kp == "a" or kp == "s" or kp == "Left" or kp == "Down":
            self.key_forward()
        elif kp == "d" or kp == "w" or kp == "Right" or kp == "Up":
            self.key_back()
        elif kp == "q" or kp == "comma":
            self.key_forward_adjust()
        elif kp == "e" or kp == "period":
            self.key_back_adjust()
        elif kp == "j":
            self.key_jump()

    def key_forward(self, event=None):
        clear_array = self.clear_array
        self.clear_array = []
        if self.n <= len(self.dict) - 3:
            self.n += 2
        self.display_image_pair()
        clear_image_array(clear_array)

    def key_forward_adjust(self, event=None):
        clear_array = self.clear_array
        self.clear_array = []
        if self.n <= len(self.dict) - 1:
            self.n += 1
        self.display_image_pair()
        clear_image_array(clear_array)

    def key_back(self, event=None):
        clear_array = self.clear_array
        self.clear_array = []
        if self.n >= 2:
            self.n -= 2
        self.display_image_pair()
        clear_image_array(clear_array)

    def key_back_adjust(self, event=None):
        clear_array = self.clear_array
        self.clear_array = []
        if self.n >= 1:
            self.n -= 1
        self.display_image_pair()
        clear_image_array(clear_array)

    def key_jump(self, event=None):
        self.query_jump()

    def key_quit(self, event=None):
        self.app.destroy()
