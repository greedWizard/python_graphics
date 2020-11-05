import tkinter as tk
import math
import numpy as np


class Drawer:
    WIDTH = 800
    HEIGHT = 800
    STEP = 12
    dF = math.pi/6
    dR = 60
    X0 = 30
    Y0 = 30
    LENGTH = 300
    CIR_COUT = 6
    INDENT = 30
    a = 1
    m = 2
    DASH = 360
    RULER = False
    step = 1
    COORDINATES = False

    def _convert_coordinates(self, x, y):
        new_x = self.start_x + x
        new_y = self.start_y + y
        return new_x, new_y

    def _draw_figure(self):
        start = 2 * math.pi

        for i in np.arange(0, int(self.DASH), self.step):
            f = start/self.DASH*i
            p = self.a * math.pow(abs(math.cos(self.m*f)), 1/self.m)

            x = p*math.cos(f)*self.dR*self.scale
            y = p*math.sin(f)*self.dR*self.scale

            x, y = self._convert_coordinates(x, y)
            
            self.canvas.create_line(x, y, x+1, y, fill='green', width=4)


    def _draw_coordinates(self):
        self.start_x = self.HEIGHT/2 + self.X0
        self.start_y = self.WIDTH/2 + self.Y0

        if self.AXES.get():
            self.canvas.create_line(self.start_x, self.start_y, self.start_x+self.LENGTH+self.INDENT, self.start_y, arrow=tk.LAST, width=4)
            self.canvas.create_text(self.start_x+self.LENGTH+self.INDENT, self.start_y+10, text='p')

        for i in range(self.STEP):
            x0 = self.start_x + (self.LENGTH+self.INDENT)*math.cos(self.dF*i)
            y0 = self.start_y + (self.LENGTH+self.INDENT)*math.sin(self.dF*i)

            x1 = self.start_x - (self.LENGTH-self.INDENT)*math.cos(self.dF*i)
            y1 = self.start_y - (self.LENGTH-self.INDENT)*math.sin(self.dF*i)

            if i % 2 == 0:
                fill='blue'
            else:
                fill='black'
            
            if self.RULER.get():
                self.canvas.create_line(x0, y0, x1, y1, fill=fill)
            if self.COORDINATES.get():
                self.canvas.create_text(x0, y0, text=f'{(360-30*i)%360}{chr(176)}')

        for i in range(self.CIR_COUT):
            if i % 2 == 0:
                color='red'
            else:
                color='gray'                                

            x0 = self.start_x + i*self.dR - self.LENGTH
            y0 = self.start_y + i*self.dR - self.LENGTH

            x1 = self.start_x + self.LENGTH - i*self.dR
            y1 = self.start_y + self.LENGTH - i*self.dR

            try:
                right_coordinate = i/self.scale
                left_coordinate = (self.CIR_COUT-i-1)/self.scale
            except ZeroDivisionError:
                pass

            if self.AXES.get():
                pass
            
            if self.RULER.get() or self.COORDINATES.get():
                if self.RULER.get():
                    self.canvas.create_oval(x0, y0, x1, y1, outline=color)
                if self.COORDINATES.get():
                    if left_coordinate != 0:
                        self.canvas.create_text(x0-self.INDENT/3, self.HEIGHT/2+self.INDENT/2, text='{0:.1f}'.format(abs(left_coordinate)))
                    if right_coordinate != 0:
                        self.canvas.create_text(x0+self.INDENT/3+self.LENGTH, self.HEIGHT/2+self.INDENT/2, text='{0:.1f}'.format(right_coordinate))

            

    def redraw(self):
        self.canvas.delete('all')
        self._draw_coordinates()
        self._draw_figure()

    def change_scale(self, event):
        try:
            self.scale = float(self.entry_scale.get())
        except ValueError:
            pass
        self.redraw()

    def change_step(self, event):
        try:
            self.step = float(self.entry_step.get())
        except ValueError:
            pass
        self.redraw()

    def change_a(self, event):
        try:
            self.a = float(self.entry_a.get())
        except ValueError:
            pass
        self.redraw()
    
    def change_m(self, event):
        try:
            self.m = float(self.entry_m.get())
        except ValueError:
            pass
        self.redraw()

    def __init__(self):
        self.tkinter = tk.Tk()

        self.scale = 1

        top_frame = tk.Frame(self.tkinter)
        bottom_frame = tk.Frame(self.tkinter)
        top_frame.pack(side=tk.TOP)
        bottom_frame.pack(side=tk.BOTTOM)

        label_scale = tk.Label(top_frame, text='scale')
        label_scale.pack(side=tk.LEFT)

        self.entry_scale = tk.Entry(top_frame, width=5)
        self.entry_scale.insert(0, self.scale)
        self.entry_scale.bind('<KeyRelease>', self.change_scale)
        self.entry_scale.pack(side=tk.LEFT)

        label_step = tk.Label(top_frame, text='step')
        label_step.pack(side=tk.LEFT)

        self.entry_step = tk.Entry(top_frame, width=5)
        self.entry_step.insert(0, self.scale)
        self.entry_step.bind('<KeyRelease>', self.change_step)
        self.entry_step.pack(side=tk.LEFT)

        label_a = tk.Label(top_frame, text='a')
        label_a.pack(side=tk.LEFT)

        self.entry_a = tk.Entry(top_frame, width=5)
        self.entry_a.insert(0, self.a)
        self.entry_a.bind('<KeyRelease>', self.change_a)
        self.entry_a.pack(side=tk.LEFT)

        label_m = tk.Label(top_frame, text='m')
        label_m.pack(side=tk.LEFT)

        self.entry_m = tk.Entry(top_frame, width=5)
        self.entry_m.insert(0, self.m)
        self.entry_m.bind('<KeyRelease>', self.change_m)
        self.entry_m.pack(side=tk.LEFT)

        label_ruler = tk.Label(top_frame, text='ruler')
        label_ruler.pack(side=tk.LEFT)

        self.RULER = tk.IntVar()
        self.ruler_box = tk.Checkbutton(top_frame, variable=self.RULER, command=self.redraw)
        self.ruler_box.pack(side=tk.LEFT)

        label_coordinates = tk.Label(top_frame, text='coordinates')
        label_coordinates.pack(side=tk.LEFT)

        self.COORDINATES = tk.IntVar()
        self.coordinates_box = tk.Checkbutton(top_frame, variable=self.COORDINATES, command=self.redraw)
        self.coordinates_box.pack(side=tk.LEFT)

        label_axes = tk.Label(top_frame, text='axes')
        label_axes.pack(side=tk.LEFT)

        self.AXES = tk.IntVar()
        self.axes_box = tk.Checkbutton(top_frame, variable=self.AXES, command=self.redraw)
        self.axes_box.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(bottom_frame, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack(side=tk.LEFT)

    def start(self):
        self.redraw()
        self.tkinter.mainloop()


d = Drawer()
d.start()
