from tkinter import messagebox as mbox
import tkinter
from utility import Logger, debugger
from data_store import DataStore

help_text = """
Tilbury Woodwinds Company Whistle Calculator
Chuck Tilbury (c) 2019

This software is open source under the MIT and BSD licenses.

-------------------------------------------
General use.
-------------------------------------------
You can use it to place the tone holes on a simple flute or tin whistle. The
steps to do that are very simple. When entering the values it's important to
make the values as accurate as you can. 

1. Set the inside diameter of the bore of the instrument.
2. Set the wall thickness of the tube.
3. Set the number of holes that you want. Note that a simple flute or whistle 
   has 6 holes and a recorder has 8 holes.
4. Select the bell note. The bell note is the lowest note that the instrument
   is capable of making.
5. Select the unis of measure. 
6. If you have selected inches, then you can display the hole sizes as a 
   decimal number or as a fraction. Using fractions helps with selecting a 
   drill for the holes.
7. Select the intervals. The default is for a major scale, but you can really
   use any intervals that will allow you to physically make and play the 
   instrument. 
8. Select each hole size. The small up and down arrows beside the number 
   allows you to increment or decrement the holesize. The metric and inch 
   increments are separate configuration options set using the 
   "Other Parameters" button. 

When you set the values, look at the "Hole Diff" and the "Cutoff Freq" columns. 

The diff column tells you how far apart the hols will be, cent-to-center. For 
most people, the maximum will be about an inch (25.4 mm) and the minimum will 
be around half an inch (12.7 mm). In any case, if the difference is such that 
the holes overlap, you will need to drill them on different sides of the tube.

The cutoff column gives the highest calculated frequency that the hole can 
make. That should normally be greater than 2x what is shown in the frequency 
column. If the cutoff value is too low, then the instrument will not play in
the upper octave.

The hole location is where to drill the hole as measured from the bell end 
of the instrument. The bell end is the end that you do not blow into. If you 
are using inches, and you are laying out the whistle with a tape measure, then
you will want to convert the decimal values to fractional values yourself.

-------------------------------------------
Saving a file
-------------------------------------------
Save a whistle specification using the file menu and the save option. Note 
that when the program starts up, it will load a file called "default.wis" 
from the current directory. If you save a file with that name, then that 
will be what the program loads when it starts up. The file that you save
must have the ".wis" ending for you to be able to load it again. The file
that is saved is binary and it is not intended to be edited directly. A
file can be saved anywhere in the file system, but you must remember where
to load it again.

-------------------------------------------
Loading a file
-------------------------------------------
To load a file, you use the file menu and the load option. Select the file
that you want to use. You can keep the files anywhere in the file system.


"""

# see: https://effbot.org/tkinterbook/tkinter-dialog-windows.htm
class BaseDialog(tkinter.Toplevel):
    '''
    This class provides common services to simple data dialogs. 
    '''

    def __init__(self, parent, title = None):

        #init the logger
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("start constructor")

        tkinter.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None
        # get a copy of the data_store for the children
        self.data_store = DataStore.get_instance()

        body = tkinter.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        #self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
        #                            parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)
        self.logger.debug("leave constructor")

    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        return self

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = tkinter.Frame(self)

        w = tkinter.Button(box, text="OK", width=10, command=self.ok, default=tkinter.ACTIVE)
        w.pack(side=tkinter.LEFT, padx=5, pady=5)
        w = tkinter.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tkinter.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics
    @debugger
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    @debugger
    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks
    def validate(self):
        return True # override

    def apply(self):
        pass # override


class helpDialog:

    def __init__(self, parent):
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("enter constructer")

        self.top = tkinter.Toplevel(parent)
        self.tx = tkinter.Text(self.top, height=25, width=80)
        self.sb = tkinter.Scrollbar(self.top)
        self.sb.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.tx.pack(side=tkinter.LEFT)
        self.sb.config(command=self.tx.yview)
        self.tx.config(yscrollcommand=self.sb.set)
        self.tx.insert(tkinter.END, help_text)
        
        self.logger.debug("leave constructer")

class TestDialog(BaseDialog):

    @debugger
    def body(self, master):

        tkinter.Label(master, text="First:").grid(row=0)
        tkinter.Label(master, text="Second:").grid(row=1)

        self.e1 = tkinter.Entry(master)
        self.e2 = tkinter.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    @debugger
    def validate(self):
        try:
            self.first = int(self.e1.get())
            self.second = int(self.e2.get())
        except ValueError as e:
            self.logger.error("Cannot convert values to ints: (%s, %s)"%(self.e1.get(), self.e2.get()))
            mbox.showerror("ERROR", "Cannot convert value to an int\n(%s, %s)"%(self.e1.get(), self.e2.get()))
            return False
        except Exception as e:
            self.logger.error("Unexpected exception while validating dialog: %s"%(str(e)))
            mbox.showerror("UNKNOWN ERROR", "Cannot convert value to an int\n(%s, %s)"%(self.e1.get(), self.e2.get()))
            return False
        return True
        

    @debugger
    def apply(self):
        print(self.first, self.second) # or something

# Emb can be round, rectangle, oblong. 
# Calculate the area and put it in the data_store.
class EmbouchureDialog(BaseDialog):
    '''
    Adjust the embouchure parameters.
    '''

    @debugger
    def body(self, master):
        pass

    @debugger
    def validate(self):
        return True

    @debugger
    def apply(self):
        pass

# inc, min, and max hole sizes in mm and in
# chimney constant (default = 0.75)
# speed of sound in mm and in by temperature and humidity
# use quadratic or iterative calculations
class ConstDialog(BaseDialog):
    '''
    Adjust the system constants.
    '''

    @debugger
    def body(self, master):
        pass

    @debugger
    def validate(self):
        return True

    @debugger
    def apply(self):
        pass
    