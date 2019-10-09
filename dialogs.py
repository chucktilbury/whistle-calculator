from tkinter import messagebox as mbox
from tkinter import ttk
import tkinter
import math
from utility import Logger, debugger
from data_store import DataStore

help_text = """
Tilbury Woodwinds Company Whistle Calculator
Chuck Tilbury (c) 2019

This software is open source under the MIT and BSD licenses.

-------------------------------------------
General use.
-------------------------------------------
This program is used to place the tone holes on a simple flute or tin whistle.

When the program starts, a file called \"default.wis\" is created. This has
all of the dettings for the calculator set to reasonable values. If the
change these values and then simply save, the settings will be saved to
the default file and they will be present the next time you use the program.
To prevent this from happening, you can "save as" a different filename. All
of the current settings are saved to that file.

When entering the values it's important to make the values as accurate as you
can. Even though you can only see 4 decimal places, there is no limit on the
internal storage of a number.

Steps to create a basic whistle design.
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
9. When you have the design the way you want it, you can export it to a text
   file for printing under the \"File\" menu.

When you set the values, look at the "Hole Diff" and the "Cutoff Freq" columns.

The diff column tells you how far apart the hols will be, center-to-center.
For most people, the maximum will be about an inch (25.4 mm) and the minimum
will be around half an inch (12.7 mm). In any case, if the difference is such
that the holes overlap, you will need to drill them on different sides of the
tube.

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

-------------------------------------------
Reset to default settings
-------------------------------------------
The default setting are what may be considered to be generic. To reset the
settings for new instruments, simply delete the file \"default.wis\". A new
default file will be created when the program starts up.

"""

# see: https://effbot.org/tkinterbook/tkinter-dialog-windows.htm
class BaseDialog(tkinter.Toplevel):
    '''
    This class provides common services to simple data dialogs.
    '''

    def __init__(self, parent):# , title = None):

        #init the logger
        self.logger = Logger(self, level=Logger.DEBUG)
        self.logger.debug("start constructor")

        tkinter.Toplevel.__init__(self, parent)
        self.transient(parent)

        self.parent = parent

        self.result = None
        # get a copy of the data_store for the children
        self.data_store = DataStore.get_instance()

        body = tkinter.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

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

        box.grid()

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


###############################################################################
# Does not use BaseDialog
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
        self.tx.config(state='disabled')

        self.logger.debug("leave constructer")

###############################################################################
class TestDialog(BaseDialog):
    '''
    This implements a minimum dialog using the Base Dialog class.
    '''

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

###############################################################################
# Emb can be round, rectangle, oblong.
# Calculate the area and put it in the data_store.
class EmbouchureDialog(BaseDialog):
    '''
    Adjust the embouchure parameters.
    '''

    @debugger
    def body(self, master):

        self.changed = False
        self.selection = self.data_store.get_emb_type()
        self.width = self.data_store.get_emb_width()
        self.height = self.data_store.get_emb_length()
        self.diameter = self.data_store.get_emb_diameter()
        self.area = self.data_store.get_embouchure_area()

        ROUND_EMB = '''
            #define round_fipple_width 75
            #define round_fipple_height 56
            static unsigned char round_fipple_bits[] = {
            0x00, 0x00, 0x00, 0x80, 0xff, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x78, 0x00, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0e,
            0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00,
            0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x01, 0x00, 0x00, 0x30, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00,
            0x18, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x00,
            0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00,
            0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x30,
            0x00, 0x00, 0x00, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00,
            0x00, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x40,
            0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x80, 0x01, 0x00, 0x00, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x01, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00,
            0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x08,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x78, 0x08, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x88, 0x0c, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x06, 0x00, 0x88, 0x04, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00,
            0x04, 0x00, 0x88, 0x04, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00,
            0x88, 0x04, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x88, 0x04,
            0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x08, 0x00, 0x78, 0x24, 0x00, 0x00,
            0x40, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x34, 0x00, 0x00, 0x40, 0x00,
            0x00, 0x00, 0x0b, 0x00, 0xe0, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0x01, 0x00, 0x34, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x0b, 0x00,
            0x00, 0x24, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x0d, 0x00, 0x00, 0x04,
            0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x04, 0x00, 0x00,
            0x40, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x04, 0x00, 0x00, 0x40, 0x00,
            0x00, 0x00, 0x04, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x06, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00,
            0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x18,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x10, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x01, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80,
            0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00,
            0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x00, 0xc0,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00,
            0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x18,
            0x00, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00,
            0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00,
            0x10, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x70, 0x00,
            0x00, 0x00, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x00,
            0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x03, 0x00, 0x00, 0x38, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0xe0, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00 };
            '''

        OVAL_EMB = '''
            #define oval_fipple_width 75
            #define oval_fipple_height 56
            static unsigned char oval_fipple_bits[] = {
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x24, 0x00, 0x11, 0x80, 0x04, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x34, 0x00, 0x15, 0x80, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfc,
            0x7f, 0xd5, 0xff, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x34, 0x00, 0x0a,
            0x80, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x24, 0x00, 0x0a, 0x80, 0x04,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04,
            0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00,
            0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00,
            0xff, 0x1f, 0xe0, 0xff, 0xff, 0xff, 0xff, 0x7f, 0x00, 0x00, 0x10, 0x00,
            0x38, 0x04, 0x00, 0x00, 0x00, 0x84, 0x03, 0x00, 0x38, 0x00, 0x06, 0x04,
            0x00, 0x00, 0x00, 0x04, 0x0c, 0x00, 0x7c, 0x00, 0x01, 0x04, 0x00, 0x00,
            0x00, 0x04, 0x10, 0x00, 0x10, 0x80, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04,
            0x20, 0x00, 0x10, 0x40, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x40, 0x00,
            0x10, 0x20, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x80, 0x00, 0x10, 0x10,
            0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x01, 0x10, 0x08, 0x00, 0x04,
            0x00, 0x00, 0x00, 0x04, 0x00, 0x01, 0x10, 0x08, 0x00, 0x04, 0x00, 0x00,
            0x00, 0x04, 0x00, 0x02, 0x10, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x02, 0x10, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04,
            0x10, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x48, 0x04,
            0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x04, 0x48, 0x02, 0x00, 0x04,
            0x00, 0x00, 0x00, 0x04, 0x00, 0x04, 0x78, 0x02, 0x00, 0x04, 0x00, 0x00,
            0x00, 0x04, 0x00, 0x04, 0x48, 0x02, 0x80, 0x3f, 0x00, 0x00, 0x80, 0x3f,
            0x00, 0x04, 0x48, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x04,
            0x10, 0x02, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x04, 0x10, 0x04,
            0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x04, 0x10, 0x04, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x10, 0x04, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x04, 0x10, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x02, 0x10, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02,
            0x10, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x10, 0x10,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x10, 0x20, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x10, 0x40, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x40, 0x00, 0x10, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x20, 0x00, 0x7c, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00,
            0x38, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x10, 0x00,
            0x18, 0x00, 0x00, 0x00, 0x00, 0x80, 0x03, 0x00, 0xff, 0x1f, 0xe0, 0xff,
            0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
        '''

        RECT_EMB = '''
            #define rect_fipple_width 75
            #define rect_fipple_height 56
            static unsigned char rect_fipple_bits[] = {
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x08, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00,
            0x00, 0x00, 0x12, 0x00, 0x00, 0x11, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00,
            0x1a, 0x00, 0x00, 0x15, 0x00, 0x00, 0x0b, 0x00, 0x00, 0x00, 0xfe, 0xff,
            0x7f, 0xd5, 0xff, 0xff, 0x0f, 0x00, 0x00, 0x00, 0x1a, 0x00, 0x00, 0x0a,
            0x00, 0x00, 0x0b, 0x00, 0x00, 0x00, 0x12, 0x00, 0x00, 0x0a, 0x00, 0x00,
            0x09, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00,
            0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00,
            0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x02, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0xff, 0x1f, 0xfe, 0xff, 0xff, 0xff, 0xff, 0xff, 0x0f, 0x00, 0x10, 0x00,
            0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x38, 0x00, 0x02, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x7c, 0x00, 0x02, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x08, 0x00, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x08, 0x00, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00,
            0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x00,
            0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x00, 0x02, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x08, 0x00, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x08, 0x00, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00,
            0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x48, 0x00,
            0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x48, 0x00, 0x02, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x78, 0x00, 0x02, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x08, 0x00, 0x48, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x08, 0x00, 0x48, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00,
            0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x00,
            0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x00, 0x02, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x08, 0x00, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x08, 0x00, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00,
            0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x00,
            0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x00, 0x02, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x08, 0x00, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x08, 0x00, 0x7c, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00,
            0x38, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x00,
            0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0xff, 0x1f, 0xfe, 0xff,
            0xff, 0xff, 0xff, 0xff, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
        '''

        self.title('Embouchure')

        self.bitmap_round = tkinter.BitmapImage(data=ROUND_EMB)
        self.b1 = tkinter.Label(master, image=self.bitmap_round)
        self.b1.config(width=75, height=56)

        self.bitmap_oval = tkinter.BitmapImage(data=OVAL_EMB)
        self.b2 = tkinter.Label(master, image=self.bitmap_oval)
        self.b2.config(width=75, height=56)

        self.bitmap_rect = tkinter.BitmapImage(data=RECT_EMB)
        self.b3 = tkinter.Label(master, image=self.bitmap_rect)
        self.b3.config(width=75, height=56)

        tkinter.Label(master, text="Type:").grid(row=0, column=1, pady=4, padx=4)
        self.combo = ttk.Combobox(master, state="readonly", values=["Rectangle", "Oval", "Round"])
        self.combo.bind("<<ComboboxSelected>>", self.typeCallback)
        self.combo.grid(row=0, column=2, pady=4, padx=4)

        tkinter.Label(master, text='Width:').grid(row=2, column=1, padx=4, pady=4, sticky=tkinter.E)
        self.widthEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.calculate)
        self.widthEntry.grid(row=2, column=2, padx=4, pady=4)
        self.widthEntry.bind('<Return>', self.validate_width)
        self.widthEntry.bind('<Tab>', self.validate_width)

        tkinter.Label(master, text='Height:').grid(row=3, column=1, padx=4, pady=4, sticky=tkinter.E)
        self.heightEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.calculate)
        self.heightEntry.grid(row=3, column=2, padx=4, pady=4)
        self.heightEntry.bind('<Return>', self.validate_height)
        self.heightEntry.bind('<Tab>', self.validate_height)

        tkinter.Label(master, text='Diameter:').grid(row=4, column=1, padx=4, pady=4, sticky=tkinter.E)
        self.diameterEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.calculate)
        self.diameterEntry.grid(row=4, column=2, padx=4, pady=4)
        self.diameterEntry.bind('<Return>', self.validate_diameter)
        self.diameterEntry.bind('<Tab>', self.validate_diameter)

        tkinter.Label(master, text='Area:').grid(row=5, column=1, padx=4, pady=4, sticky=tkinter.E)
        self.areaEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.calculate)
        self.areaEntry.grid(row=5, column=2, padx=4, pady=4)

        self.combo.current(self.selection)
        self.diameterEntry.insert(0, "%0.4f"%(self.diameter))
        self.heightEntry.insert(0, "%0.4f"%(self.height))
        self.widthEntry.insert(0, "%0.4f"%(self.width))
        self.areaEntry.insert(0, "%0.4f"%(self.area))
        self.areaEntry.config(state='readonly')

        self.setup_controls()
        return self.combo

    @debugger
    def validate_diameter(self, event=None):
        try:
            s = self.diameterEntry.get()
            val = float(s)
            if val != self.diameter: #self.data_store.get_emb_diameter():
                self.diameter = val
                self.changed = True
                self.calculate()
        except ValueError:
            self.logger.error("Cannot convert diameter field to float: \"%s\""%(s))
            mbox.showerror("ERROR", "Cannot convert diameter into a float: \"%s\""%(s))
            self.diameterEntry.delete(0, tkinter.END)
            self.diameterEntry.insert(0, "%0.4f"%(self.diameter))
            return False
        return True

    @debugger
    def validate_height(self, event=None):
        try:
            s = self.heightEntry.get()
            val = float(s)
            if val != self.height: #self.data_store.get_emb_length():
                self.height = val
                self.changed = True
                self.calculate()
        except ValueError:
            self.logger.error("Cannot convert height field to float: \"%s\""%(s))
            mbox.showerror("ERROR", "Cannot convert height into a float: \"%s\""%(s))
            self.heightEntry.delete(0, tkinter.END)
            self.heightEntry.insert(0, "%0.4f"%(self.height))
            return False
        return True

    @debugger
    def validate_width(self, event=None):
        try:
            s = self.widthEntry.get()
            val = float(s)
            if val != self.width: #self.data_store.get_emb_width():
                self.width = val
                self.changed = True
                self.calculate()
        except ValueError:
            self.logger.error("Cannot convert width field to float: \"%s\""%(s))
            mbox.showerror("ERROR", "Cannot convert width into a float: \"%s\""%(s))
            self.widthEntry.delete(0, tkinter.END)
            self.widthEntry.insert(0, "%0.4f"%(self.width))
            return False
        return True

    @debugger
    def validate(self):
        if self.validate_diameter() == False:
            return False
        if self.validate_height() == False:
            return False
        if self.validate_width() == False:
            return False
        return True

    @debugger
    def calculate(self):
        if self.validate():
            if self.selection == 0:
                # calculate area for rectangle
                self.area = self.width * self.height
            elif self.selection == 1:
                # calculate area for oval
                self.area = (self.width * self.height) + (math.pi * math.pow(self.height/2, 2))
            else:
                # calculate area for round
                self.area = math.pi * math.pow(self.diameter/2, 2)

            self.logger.debug("set the area to %f"%(self.area))
            self.areaEntry.config(state='normal')
            self.areaEntry.delete(0, tkinter.END)
            self.areaEntry.insert(0, "%0.4f"%(self.area))
            self.areaEntry.config(state='readonly')

    @debugger
    def apply(self):
        self.calculate()
        if self.changed:
            self.data_store.set_change_flag()
            self.data_store.set_embouchure_area(self.area)
            self.data_store.set_emb_type(self.selection)
            self.data_store.set_emb_width(self.width)
            self.data_store.set_emb_length(self.height)
            self.data_store.set_emb_diameter(self.diameter)

    @debugger
    def setup_controls(self):
        self.b1.grid_forget()
        self.b2.grid_forget()
        self.b3.grid_forget()

        if self.selection == 0:
            self.b3.grid(row=0, column=0, rowspan=4, pady=4, padx=4)
            self.diameterEntry.config(state='disable')
            self.heightEntry.config(state='normal')
            self.widthEntry.config(state='normal')
        elif self.selection == 1:
            self.b2.grid(row=0, column=0, rowspan=4, pady=4, padx=4)
            self.diameterEntry.config(state='disable')
            self.heightEntry.config(state='normal')
            self.widthEntry.config(state='normal')
        else:
            self.b1.grid(row=0, column=0, rowspan=4, pady=4, padx=4)
            self.diameterEntry.config(state='normal')
            self.heightEntry.config(state='disable')
            self.widthEntry.config(state='disable')
        #self.data_store.set_emb_type(val)
        self.calculate()

    @debugger
    def typeCallback(self, event):
        val = self.combo.current()
        if self.selection != val:
            self.selection = val
            self.setup_controls()
            self.changed = True



###############################################################################
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
        self.title('Configuration')

        # local copies of datastore items
        self.calc_method = 0
        self.max_in = 0.0
        self.min_in = 0.0
        self.inc_in = 0.0
        self.max_mm = 0.0
        self.min_mm = 0.0
        self.inc_mm = 0.0
        self.vsound_in = 0.0
        self.vsound_mm = 0.0
        self.chim = 0.0
        self.temp = 0.0
        self.embo = 0.0
        #self.humidity = 0.0
        self.change_flag = False

        tkinter.Label(master, text='Calculation Method:').grid(row=0, column=0, padx=4, pady=4, sticky=tkinter.E)
        self.calcCombo = ttk.Combobox(master, state="readonly", values=["Quadratic", "Iterative"], width=8)
        self.calcCombo.bind("<<ComboboxSelected>>", self.comboCallback)
        self.calcCombo.grid(row=0, column=1, pady=4, padx=4)

        ##################

        tkinter.Label(master, text='Max hole inch:').grid(row=1, column=0, padx=4, pady=4, sticky=tkinter.E)
        self.holeMaxInchEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.validate_max_in, width=10)
        self.holeMaxInchEntry.grid(row=1, column=1, padx=4, pady=4)
        self.holeMaxInchEntry.bind('<Return>', self.validate_max_in)
        self.holeMaxInchEntry.bind('<Tab>', self.validate_max_in)

        tkinter.Label(master, text='Min hole inch:').grid(row=2, column=0, padx=4, pady=4, sticky=tkinter.E)
        self.holeMinInchEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.validate_min_in, width=10)
        self.holeMinInchEntry.grid(row=2, column=1, padx=4, pady=4)
        self.holeMinInchEntry.bind('<Return>', self.validate_min_in)
        self.holeMinInchEntry.bind('<Tab>', self.validate_min_in)

        tkinter.Label(master, text='Hole increment inch:').grid(row=3, column=0, padx=4, pady=4, sticky=tkinter.E)
        self.holeIncInchEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.validate_inc_in, width=10)
        self.holeIncInchEntry.grid(row=3, column=1, padx=4, pady=4)
        self.holeIncInchEntry.bind('<Return>', self.validate_inc_in)
        self.holeIncInchEntry.bind('<Tab>', self.validate_inc_in)

        #################

        tkinter.Label(master, text='Max hole mm:').grid(row=1, column=2, padx=4, pady=4, sticky=tkinter.E)
        self.holeMaxMMEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.validate_max_mm, width=10)
        self.holeMaxMMEntry.grid(row=1, column=3, padx=4, pady=4)
        self.holeMaxMMEntry.bind('<Return>', self.validate_max_mm)
        self.holeMaxMMEntry.bind('<Tab>', self.validate_max_mm)

        tkinter.Label(master, text='Min hole mm:').grid(row=2, column=2, padx=4, pady=4, sticky=tkinter.E)
        self.holeMinMMEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.validate_min_mm, width=10)
        self.holeMinMMEntry.grid(row=2, column=3, padx=4, pady=4)
        self.holeMinMMEntry.bind('<Return>', self.validate_min_mm)
        self.holeMinMMEntry.bind('<Tab>', self.validate_min_mm)

        tkinter.Label(master, text='Hole increment mm:').grid(row=3, column=2, padx=4, pady=4, sticky=tkinter.E)
        self.holeIncMMEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.validate_inc_mm, width=10)
        self.holeIncMMEntry.grid(row=3, column=3, padx=4, pady=4)
        self.holeIncMMEntry.bind('<Return>', self.validate_inc_mm)
        self.holeIncMMEntry.bind('<Tab>', self.validate_inc_mm)

        #################

        tkinter.Label(master, text='Chimney Constant:').grid(row=4, column=0, padx=4, pady=4, sticky=tkinter.E)
        self.chimEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.validate_chim, width=10)
        self.chimEntry.grid(row=4, column=1, padx=4, pady=4)
        self.chimEntry.bind('<Return>', self.validate_chim)
        self.chimEntry.bind('<Tab>', self.validate_chim)

        ####################

        tkinter.Label(master, text='End Correction:').grid(row=5, column=0, padx=4, pady=4, sticky=tkinter.E)
        self.emboEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.validate_embo, width=10)
        self.emboEntry.grid(row=5, column=1, padx=4, pady=4)
        self.emboEntry.bind('<Return>', self.validate_embo)
        self.emboEntry.bind('<Tab>', self.validate_embo)

        ####################

        self.units = self.data_store.get_units()
        if self.units:
            tkinter.Label(master, text='Temerature (C):').grid(row=6, column=0, padx=4, pady=4, sticky=tkinter.E)
        else:
            tkinter.Label(master, text='Temerature (F):').grid(row=6, column=0, padx=4, pady=4, sticky=tkinter.E)
        self.tempEntry = tkinter.Entry(master, validate="focusout", validatecommand=self.validate_temperature, width=10)
        self.tempEntry.grid(row=6, column=1, padx=4, pady=4)
        self.tempEntry.bind('<Return>', self.validate_temperature)
        self.tempEntry.bind('<Tab>', self.validate_temperature)

        tkinter.Label(master, text='Inch vsound:').grid(row=7, column=0, padx=4, pady=4, sticky=tkinter.E)
        self.inVsoundEntry = tkinter.Entry(master, width=10)
        self.inVsoundEntry.grid(row=7, column=1, padx=4, pady=4)

        tkinter.Label(master, text='Metric vsound:').grid(row=7, column=2, padx=4, pady=4, sticky=tkinter.E)
        self.mmVsoundEntry = tkinter.Entry(master, width=10)
        self.mmVsoundEntry.grid(row=7, column=3, padx=4, pady=4)

        # Give them the values from the data_store
        self.set_state()
        self.get_state()

        return  self.calcCombo

    @debugger
    def comboCallback(self, event):
        val = self.calcCombo.current()
        if val != self.calc_method:
            self.calc_method = val
            self.change_flag = True
            self.logger.debug("changed calc method to %s"%(val))


    @debugger
    def validate_embo(self, event=None):
        try:
            val = self.emboEntry.get()
            val = float(val) # save typing incase there is a convert error
            if val != self.embo:
                self.embo = val
                self.change_flag = True
        except ValueError:
            self.logger.error("Invalid floating point number in Embouchure Correction: %s"%(val))
            mbox.showerror("ERROR", "Invalid floating point number in Embouchure Correction: %s"%(val))
            self.emboEntry.delete(0, tkinter.END)
            self.emboEntry.insert(0, "%0.4f"%(self.embo))
            return False
        except:
            pass # ignore all other exceptions

        return True

    @debugger
    def validate_max_in(self, event=None):
        try:
            val = self.holeMaxInchEntry.get()
            val = float(val) # save typing incase there is a convert error
            if val != self.max_in:
                self.max_in = val
                self.change_flag = True
        except ValueError:
            self.logger.error("Invalid floating point number in Max IN: %s"%(val))
            mbox.showerror("ERROR", "Invalid floating point number in Max IN: %s"%(val))
            self.holeMaxInchEntry.delete(0, tkinter.END)
            self.holeMaxInchEntry.insert(0, "%0.4f"%(self.max_in))
            return False
        except:
            pass # ignore all other exceptions

        return True


    @debugger
    def validate_min_in(self, event=None):
        try:
            val = self.holeMinInchEntry.get()
            val = float(val) # save typing incase there is a convert error
            if val != self.min_in:
                self.min_in = val
                self.change_flag = True
        except ValueError:
            self.logger.error("Invalid floating point number in Min IN: %s"%(val))
            mbox.showerror("ERROR", "Invalid floating point number in Min IN: %s"%(val))
            self.holeMinInchEntry.delete(0, tkinter.END)
            self.holeMinInchEntry.insert(0, "%0.4f"%(self.min_in))
            return False
        except:
            pass # ignore all other exceptions

        return True

    @debugger
    def validate_inc_in(self, event=None):
        try:
            val = self.holeIncInchEntry.get()
            val = float(val) # save typing incase there is a convert error
            if val != self.inc_in:
                self.inc_in = val
                self.change_flag = True
        except ValueError:
            self.logger.error("Invalid floating point number in Increment IN: %s"%(val))
            mbox.showerror("ERROR", "Invalid floating point number in Increment IN: %s"%(val))
            self.holeIncInchEntry.delete(0, tkinter.END)
            self.holeIncInchEntry.insert(0, "%0.4f"%(self.inc_in))
            return False
        except:
            pass # ignore all other exceptions

        return True

    @debugger
    def validate_max_mm(self, event=None):
        try:
            val = self.holeMaxMMEntry.get()
            val = float(val) # save typing incase there is a convert error
            if val != self.max_mm:
                self.max_mm = val
                self.change_flag = True
        except ValueError:
            self.logger.error("Invalid floating point number in Max MM: %s"%(val))
            mbox.showerror("ERROR", "Invalid floating point number in Max MM: %s"%(val))
            self.holeMaxMMEntry.delete(0, tkinter.END)
            self.holeMaxMMEntry.insert(0, "%0.4f"%(self.max_mm))
            return False
        except:
            pass # ignore all other exceptions

        return True

    @debugger
    def validate_min_mm(self, event=None):
        try:
            val = self.holeMinMMEntry.get()
            val = float(val) # save typing incase there is a convert error
            if val != self.min_mm:
                self.min_mm = val
                self.change_flag = True
        except ValueError:
            self.logger.error("Invalid floating point number in Min MM: %s"%(val))
            mbox.showerror("ERROR", "Invalid floating point number in Min MM: %s"%(val))
            self.holeMinMMEntry.delete(0, tkinter.END)
            self.holeMinMMEntry.insert(0, "%0.4f"%(self.min_mm))
            return False
        except:
            pass # ignore all other exceptions

        return True

    @debugger
    def validate_inc_mm(self, event=None):
        try:
            val = self.holeIncMMEntry.get()
            val = float(val) # save typing incase there is a convert error
            if val != self.inc_mm:
                self.inc_mm = val
                self.change_flag = True
        except ValueError:
            self.logger.error("Invalid floating point number in Increment MM: %s"%(val))
            mbox.showerror("ERROR", "Invalid floating point number in Increment MM: %s"%(val))
            self.holeIncMMEntry.delete(0, tkinter.END)
            self.holeIncMMEntry.insert(0, "%0.4f"%(self.inc_mm))
            return False
        except:
            pass # ignore all other exceptions

        return True

    @debugger
    def validate_chim(self, event=None):
        try:
            val = self.chimEntry.get()
            val = float(val) # save typing incase there is a convert error
            if val != self.chim:
                self.chim = val
                self.change_flag = True
        except ValueError:
            self.logger.error("Invalid floating point number in Chimney Constant: %s"%(val))
            mbox.showerror("ERROR", "Invalid floating point number in Chimney Constant: %s"%(val))
            self.chimEntry.delete(0, tkinter.END)
            self.chimEntry.insert(0, "%0.4f"%(self.chim))
            return False
        except:
            pass # ignore all other exceptions

        return True

    @debugger
    def validate_temperature(self, event=None):
        try:
            val = self.tempEntry.get()
            val = float(val) # save typing incase there is a convert error
            if val != self.temp:
                self.temp = val
                self.change_flag = True
                self.calculate_sound()
        except ValueError:
            self.logger.error("Invalid floating point number in Temerature: %s"%(val))
            mbox.showerror("ERROR", "Invalid floating point number in Temerature: %s"%(val))
            self.tempEntry.delete(0, tkinter.END)
            self.tempEntry.insert(0, "%0.4f"%(self.temp))
            return False
        except:
            pass # ignore all other exceptions

        return True

    @debugger
    def validate(self):
        if not self.validate_chim():        return False
        if not self.validate_embo():        return False
        if not self.validate_max_in():      return False
        if not self.validate_min_in():      return False
        if not self.validate_inc_in():      return False
        if not self.validate_max_mm():      return False
        if not self.validate_min_mm():      return False
        if not self.validate_inc_mm():      return False
        if not self.validate_temperature(): return False
        return True

    @debugger
    def calculate_sound(self):
        if not self.units:
            T = (self.temp - 32) / 1.8 + 273.15
        else:
            T = self.temp +273.15
        self.vsound_mm = math.pow(401.66 * T, 0.5) * 1000 # mm per second
        self.vsound_in = self.vsound_mm / 25.4

        self.inVsoundEntry.config(state='normal')
        self.inVsoundEntry.delete(0, tkinter.END)
        self.inVsoundEntry.insert(0, "%0.2f"%(self.vsound_in))
        self.inVsoundEntry.config(state='readonly')

        self.mmVsoundEntry.config(state='normal')
        self.mmVsoundEntry.delete(0, tkinter.END)
        self.mmVsoundEntry.insert(0, "%0.2f"%(self.vsound_mm))
        self.mmVsoundEntry.config(state='readonly')

    @debugger
    def apply(self):
        if self.change_flag:
            self.get_state()
            self.data_store.set_calc_type(self.calc_method)
            self.data_store.set_hole_max_in(self.max_in)
            self.data_store.set_hole_min_in(self.min_in)
            self.data_store.set_hole_inc_in(self.inc_in)
            self.data_store.set_hole_max_mm(self.max_mm)
            self.data_store.set_hole_min_mm(self.min_mm)
            self.data_store.set_hole_inc_mm(self.inc_mm)
            self.data_store.set_chim_const(self.chim)
            self.data_store.set_temperature(self.temp)
            self.data_store.set_vsound_in(self.vsound_in)
            self.data_store.set_vsound_mm(self.vsound_mm)
            self.data_store.set_ecorr(self.embo)
            self.data_store.set_change_flag()
            self.logger.debug("State saved to data_store")

    @debugger
    def set_state(self):
        '''
        Set the state of all of the controls
        '''
        self.calcCombo.current(self.data_store.get_calc_type())

        self.emboEntry.delete(0, tkinter.END)
        self.emboEntry.insert(0, "%0.4f"%(self.data_store.get_ecorr()))

        self.holeMaxInchEntry.delete(0, tkinter.END)
        self.holeMaxInchEntry.insert(0, "%0.4f"%(self.data_store.get_hole_max_in()))

        self.holeMinInchEntry.delete(0, tkinter.END)
        self.holeMinInchEntry.insert(0, "%0.4f"%(self.data_store.get_hole_min_in()))

        self.holeIncInchEntry.delete(0, tkinter.END)
        self.holeIncInchEntry.insert(0, "%0.4f"%(self.data_store.get_hole_inc_in()))

        self.holeMaxMMEntry.delete(0, tkinter.END)
        self.holeMaxMMEntry.insert(0, "%0.4f"%(self.data_store.get_hole_max_mm()))

        self.holeMinMMEntry.delete(0, tkinter.END)
        self.holeMinMMEntry.insert(0, "%0.4f"%(self.data_store.get_hole_min_mm()))

        self.holeIncMMEntry.delete(0, tkinter.END)
        self.holeIncMMEntry.insert(0, "%0.4f"%(self.data_store.get_hole_inc_mm()))

        self.chimEntry.delete(0, tkinter.END)
        self.chimEntry.insert(0, "%0.4f"%(self.data_store.get_chim_const()))

        self.tempEntry.delete(0, tkinter.END)
        self.tempEntry.insert(0, "%0.2f"%(self.data_store.get_temperature()))

        self.inVsoundEntry.config(state='normal')
        self.inVsoundEntry.delete(0, tkinter.END)
        self.inVsoundEntry.insert(0, "%0.2f"%(self.data_store.get_vsound_in()))
        self.inVsoundEntry.config(state='readonly')

        self.mmVsoundEntry.config(state='normal')
        self.mmVsoundEntry.delete(0, tkinter.END)
        self.mmVsoundEntry.insert(0, "%0.2f"%(self.data_store.get_vsound_mm()))
        self.mmVsoundEntry.config(state='readonly')


    @debugger
    def get_state(self):
        '''
        Set the data_store information from the controls
        '''
        self.calc_method = int(self.calcCombo.current())
        self.max_in = float(self.holeMaxInchEntry.get())
        self.min_in = float(self.holeMinInchEntry.get())
        self.inc_in = float(self.holeIncInchEntry.get())
        self.max_mm = float(self.holeMaxMMEntry.get())
        self.min_mm = float(self.holeMinMMEntry.get())
        self.inc_mm = float(self.holeIncMMEntry.get())
        self.chim = float(self.chimEntry.get())
        self.temp = float(self.tempEntry.get())
        self.embo = float(self.emboEntry.get())
        # self.humidity = self.tempEntry.get()
        self.vsound_in = float(self.inVsoundEntry.get())
        self.vsound_mm = float(self.mmVsoundEntry.get())


###############################################################################
class NotesDialog(BaseDialog):
    '''
    Capture and store arbitrary notes.
    '''

    @debugger
    def body(self, master):
        self.title('Notes')
        self.tx = tkinter.Text(master, height=25, width=80)
        self.sb = tkinter.Scrollbar(master)
        self.sb.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.tx.pack(side=tkinter.LEFT)
        self.sb.config(command=self.tx.yview)
        self.tx.config(yscrollcommand=self.sb.set)
        self.notes = self.data_store.get_notes()
        self.tx.insert(tkinter.END, self.notes)

    @debugger
    def validate(self):
        self.notes = self.tx.get('1.0', tkinter.END)
        return True

    @debugger
    def apply(self):
        self.data_store.set_notes(self.notes)
