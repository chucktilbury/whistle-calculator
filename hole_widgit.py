from tkinter import messagebox
import tkinter
import sys, math

class HoleSizeWidgit(tkinter.Frame):

    def __init__(self, parent, default=""):
        '''
        This is a specialized widget to track the hole diameter. It is capable
        of tracking the state of the GUI and displaying the diameter as a
        fraction, a decimal inch, or a metric measurement. Which version is
        displayed is controlled by the DataStore object that is given when this
        object is created. When the mode is changed from inch to mm, for example,
        the maxval, minval, and increment is automatically switched to metric
        equivalent values.
        '''
        tkinter.Frame.__init__(self, parent)

        BITMAP_UP = """
            #define up_width 9
            #define up_height 5
            static unsigned char up_bits[] = {
                0x10, 0x00, 0x38, 0x00, 0x7c, 0x00, 0xfe, 0x00, 0xff, 0x01 };
            """

        BITMAP_DOWN = """
            #define down_width 9
            #define down_height 5
            static unsigned char down_bits[] = {
                0xff, 0x01, 0xfe, 0x00, 0x7c, 0x00, 0x38, 0x00, 0x10, 0x00 };
        """

        self.increment = 0.0
        self.maxval = 0.0
        self.minval = 0.0
        self.internal_value = 0.0
        self.fract = True # display as fractions if true
        self.mm_in = False # calculate as mm if true

        self.entry = tkinter.Entry(self, width=25-18)
        self.entry.insert(0, default)

        self.entry.grid(row=0, column=1, rowspan=2)

        self.bitmap_up = tkinter.BitmapImage(data=BITMAP_UP, foreground="black", background="white")
        self.b1 = tkinter.Button(self, text="up", image=self.bitmap_up, command=self.incr_command)
        self.b1.grid(row=0, column=2)
        self.b1.config(width=9, height=5)

        self.bitmap_down = tkinter.BitmapImage(data=BITMAP_DOWN)
        self.b2 = tkinter.Button(self, image=self.bitmap_down, command=self.decr_command)
        self.b2.grid(row=1, column=2)
        self.b2.config(width=9, height=5)


    def get(self):
        return self.internal_value

    def set_frac(self, value):
        if type(value) != type(True):
            messagebox.showerror("Internal Error", "Set Frac\nInvalid value passed to hole size widget.\nCannot continue.")
            sys.exit()
        self.fract = value # only changes the display, not the actual value
        self.update_val()

    def set_units(self, value):
        #print("set the scale to ", value)
        if type(value) != type(True):
            messagebox.showerror("Internal Error", "Set Scale\nInvalid value passed to hole size widget.\nCannot continue.")
            sys.exit()
        if self.mm_in != value:
            if self.mm_in:
                self.internal_value = self.internal_value / 0.03937008
            else:
                self.internal_value = self.internal_value * 0.03937008
        self.mm_in = value # change the actual value
        self.update_val()

    def set_minval(self, value):
        #print("min value set to", value)
        try:
            self.minval = float(value)
            self.update_val()
        except:
            messagebox.showerror("Internal Error", "Min Value\nCannot convert value \"%s\" to\na floating point number.\nCannot continue."%(str(value)))
            sys.exit()

    def set_maxval(self, value):
        #print("max value set to", value)
        try:
            self.maxval = float(value)
            self.update_val()
        except:
            messagebox.showerror("Internal Error", "Max Value\nCannot convert value \"%s\" to\na floating point number.\nCannot continue."%(str(value)))
            sys.exit()

    def set_startval(self, value):
        try:
            self.internal_value = float(value)
            self.update_val()
        except:
            messagebox.showerror("Internal Error", "Start Value\nCannot convert value \"%s\" to\na floating point number.\nCannot continue."%(str(value)))
            sys.exit()

    def update_val(self):
        #print("updating value to", self.internal_value)
        self.entry.delete(0, tkinter.END)
        if self.mm_in or (not self.mm_in and not self.fract):
            print("here1", self.fract, self.mm_in)
            self.entry.insert(0, "%0.3f"%(self.internal_value))
        else:
            print("here2", self.fract, self.mm_in)
            self.entry.insert(0, "%s"%(self.reduce()))

    def set_incval(self, value):
        #print("increment value set to", value)
        try:
            self.increment = float(value)
        except:
            messagebox.showerror("Internal Error", "Set Increment Value\nCannot convert value \"%s\" to\na floating point number.\nCannot continue."%(str(value)))

    # event handlers
    def incr_command(self):
        #print("increment value")
        self.internal_value = self.internal_value + self.increment
        if self.internal_value > self.maxval:
            self.internal_value = self.maxval
        self.update_val()

    def decr_command(self):
        #print("decrement value")
        self.internal_value = self.internal_value - self.increment
        if self.internal_value < self.minval:
            self.internal_value = self.minval
        self.update_val()

    # Utility methods
    def reduce(self):
        '''
        Reduce the internal value to a fraction and return it as a string.
        '''
        w = int(self.internal_value / (1/64))
        f = 64
        while w % 2 == 0:
            w = w / 2
            f = f / 2

            if f == 0:
                messagebox.showerror("ERROR", "Cannot convert internal value (%0.3f) to a fraction."%(self.internal_value))
                return None
        # This can yield stupid values if w or f go below zero
        return str(int(w))+"/"+str(int(f))

    def fractof(self, frac):
        '''
        Convert the string given as a fraction into a float. Return the value.
        '''
        a = frac.split('/')
        return float(a[0]) / float(a[1])

    def rnd(self, num, factor):
        '''
        Find the closest multiple of factor for num.
        '''
        a = math.ceil(num/factor)*factor
        b = math.floor(num/factor)*factor
        if abs(num - a) < abs(num - b):
            return a
        else:
            return b
