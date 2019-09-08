from tkinter import ttk
from tkinter import messagebox
import tkinter
import sys, os

#from calc import Calculator
#from line_widgit import LineWidgit
from data_store import DataStore
from lower_frame import LowerFrame
from upper_frame import UpperFrame

class MainFrame(tkinter.Frame):
    '''
    This is the main frame that "contains" the other frames.
    '''
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)

        self.general_params = tkinter.LabelFrame(self.master, text="General Parameters")
        self.general_params.pack()
        self.output_params = tkinter.LabelFrame(self.master, text="Output Parameters")
        self.output_params.pack(fill="both", expand="yes")

        # set up some default values
        self.current_file_name = os.path.join(os.getcwd(), "untitled.wis")
        self.data = DataStore()
        #self.calc = Calculator(self.data)
        self.upper_frame = UpperFrame(self.general_params, self.data)
        self.lower_frame = LowerFrame(self.output_params, self.data)
        #self.title = "default whistle"

        menu = tkinter.Menu(self.master, tearoff=0)
        self.master.config(menu=menu)
        self.master.geometry("750x450")

        fileMenu = tkinter.Menu(menu, tearoff=0)
        fileMenu.add_command(label="Load", command=self.loadCommand)
        fileMenu.add_command(label="Save", command=self.saveCommand)
        fileMenu.add_command(label="Save As", command=self.saveasCommand)
        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=self.close_window)
        menu.add_cascade(label="File", menu=fileMenu)

        editMenu = tkinter.Menu(menu, tearoff=0)
        editMenu.add_command(label="Help", command=self.helpCommand)
        editMenu.add_command(label="About", command=self.aboutCommand)
        menu.add_cascade(label="Help", menu=editMenu)

        tkinter.Label(self.master, text="Tilbury Woodwinds Whistle Calculator",
                    font=("Helvetica", 14)).pack()

        self.upper_frame.create_frame()
        self.lower_frame.create_frame()

    def close_window(self):
        print("closing window")
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.master.destroy()

    def loadCommand(self):
        f = tkinter.filedialog.askopenfilename(initialfile=self.current_file_name, filetypes=(("Whistle Files","*.wis"), ("all files", "*.*")))
        print("loading file = " + f)

    def saveCommand(self):
        d = tkinter.filedialog.askdirectory(initialdir=os.getcwd(), mustexist=True)
        p = os.path.join(d, self.current_file_name)
        print("saving file = " + p )
        #f = open(p, 'w')
        #f.close()

    def saveasCommand(self):
        f = tkinter.filedialog.asksaveasfilename(initialfile=self.current_file_name, filetypes=(("Whistle Files","*.wis"), ("all files", "*.*")))
        print("file save as = " + f)

    def helpCommand(self):
        print("help command")
        #print("display format: "+ self.displayFormatOpt.get())
        #print("measure units: "+ self.measureUnitsOpt.get())
        #print("bellnote: %s (%d)"%(str(self.bellNoteEntry.get()), self.bellNoteEntry.current()))

    def aboutCommand(self):
        messagebox.showinfo(
            "About", "Tilbury Woodwinds Company\nWhistle Calculator\nChuck Tilbury (c) 2019")
