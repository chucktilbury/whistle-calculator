from tkinter import messagebox

class DataStore:
    '''
    This is a simple class to facilitate communicating the data between
    the GUI and the calculator. It contains the state of the progam as
    it pertains to what the calculator needs to function. This object can
    be passed around providing a consistent way to access the data it
    contains.
    '''

    def __init__(self):

        self.disp_frac = True   # True if the holes are displayed in fractions
        self.units = False      # True if the units are mm and false if it's inch
        self.title = "Default Whistle"
        self.inside_dia = 0.5
        self.wall_thickness = 0.15
        self.number_holes = 6
        self.bell_note_select = 62
        self.embouchure_area = 1.2
        self.bell_freq = 587.33
        self.intervals = [2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2]

        self.note_table = [
            {"note":"C0",      "frequency":16.35},   # index = 0
            {"note":"C#0/Db0", "frequency":17.32},   # index = 1
            {"note":"D0",      "frequency":18.35},   # index = 2
            {"note":"D#0/Eb0", "frequency":19.45},   # index = 3
            {"note":"E0",      "frequency":20.60},   # index = 4
            {"note":"F0",      "frequency":21.83},   # index = 5
            {"note":"F#0/Gb0", "frequency":23.12},   # index = 6
            {"note":"G0",      "frequency":24.50},   # index = 7
            {"note":"G#0/Ab0", "frequency":25.96},   # index = 8
            {"note":"A0",      "frequency":27.50},   # index = 9
            {"note":"A#0/Bb0", "frequency":29.14},   # index = 10
            {"note":"B0",      "frequency":30.87},   # index = 11
            {"note":"C1",      "frequency":32.70},   # index = 12
            {"note":"C#1/Db1", "frequency":34.65},   # index = 13
            {"note":"D1",      "frequency":36.71},   # index = 14
            {"note":"D#1/Eb1", "frequency":38.89},   # index = 15
            {"note":"E1",      "frequency":41.20},   # index = 16
            {"note":"F1",      "frequency":43.65},   # index = 17
            {"note":"F#1/Gb1", "frequency":46.25},   # index = 18
            {"note":"G1",      "frequency":49.00},   # index = 19
            {"note":"G#1/Ab1", "frequency":51.91},   # index = 20
            {"note":"A1",      "frequency":55.00},   # index = 21
            {"note":"A#1/Bb1", "frequency":58.27},   # index = 22
            {"note":"B1",      "frequency":61.74},   # index = 23
            {"note":"C2",      "frequency":65.41},   # index = 24
            {"note":"C#2/Db2", "frequency":69.30},   # index = 25
            {"note":"D2",      "frequency":73.42},   # index = 26
            {"note":"D#2/Eb2", "frequency":77.78},   # index = 27
            {"note":"E2",      "frequency":82.41},   # index = 28
            {"note":"F2",      "frequency":87.31},   # index = 29
            {"note":"F#2/Gb2", "frequency":92.50},   # index = 30
            {"note":"G2",      "frequency":98.00},   # index = 31
            {"note":"G#2/Ab2", "frequency":103.83},  # index = 32
            {"note":"A2",      "frequency":110.00},  # index = 33
            {"note":"A#2/Bb2", "frequency":116.54},  # index = 34
            {"note":"B2",      "frequency":123.47},  # index = 35
            {"note":"C3",      "frequency":130.81},  # index = 36
            {"note":"C#3/Db3", "frequency":138.59},  # index = 37
            {"note":"D3",      "frequency":146.83},  # index = 38
            {"note":"D#3/Eb3", "frequency":155.56},  # index = 39
            {"note":"E3",      "frequency":164.81},  # index = 40
            {"note":"F3",      "frequency":174.61},  # index = 41
            {"note":"F#3/Gb3", "frequency":185.00},  # index = 42
            {"note":"G3",      "frequency":196.00},  # index = 43
            {"note":"G#3/Ab3", "frequency":207.65},  # index = 44
            {"note":"A3",      "frequency":220.00},  # index = 45
            {"note":"A#3/Bb3", "frequency":233.08},  # index = 46
            {"note":"B3",      "frequency":246.94},  # index = 47
            {"note":"C4",      "frequency":261.63},  # index = 48
            {"note":"C#4/Db4", "frequency":277.18},  # index = 49
            {"note":"D4",      "frequency":293.66},  # index = 50
            {"note":"D#4/Eb4", "frequency":311.13},  # index = 51
            {"note":"E4",      "frequency":329.63},  # index = 52
            {"note":"F4",      "frequency":349.23},  # index = 53
            {"note":"F#4/Gb4", "frequency":369.99},  # index = 54
            {"note":"G4",      "frequency":392.00},  # index = 55
            {"note":"G#4/Ab4", "frequency":415.30},  # index = 56
            {"note":"A4",      "frequency":440.00},  # index = 57
            {"note":"A#4/Bb4", "frequency":466.16},  # index = 58
            {"note":"B4",      "frequency":493.88},  # index = 59
            {"note":"C5",      "frequency":523.25},  # index = 60
            {"note":"C#5/Db5", "frequency":554.37},  # index = 61
            {"note":"D5",      "frequency":587.33},  # index = 62 (Default)
            {"note":"D#5/Eb5", "frequency":622.25},  # index = 63
            {"note":"E5",      "frequency":659.25},  # index = 64
            {"note":"F5",      "frequency":698.46},  # index = 65
            {"note":"F#5/Gb5", "frequency":739.99},  # index = 66
            {"note":"G5",      "frequency":783.99},  # index = 67
            {"note":"G#5/Ab5", "frequency":830.61},  # index = 68
            {"note":"A5",      "frequency":880.00},  # index = 69
            {"note":"A#5/Bb5", "frequency":932.33},  # index = 70
            {"note":"B5",      "frequency":987.77},  # index = 71
            {"note":"C6",      "frequency":1046.50}, # index = 72
            {"note":"C#6/Db6", "frequency":1108.73}, # index = 73
            {"note":"D6",      "frequency":1174.66}, # index = 74
            {"note":"D#6/Eb6", "frequency":1244.51}, # index = 75
            {"note":"E6",      "frequency":1318.51}, # index = 76
            {"note":"F6",      "frequency":1396.91}, # index = 77
            {"note":"F#6/Gb6", "frequency":1479.98}, # index = 78
            {"note":"G6",      "frequency":1567.98}, # index = 79
            {"note":"G#6/Ab6", "frequency":1661.22}, # index = 80
            {"note":"A6",      "frequency":1760.00}, # index = 81
            {"note":"A#6/Bb6", "frequency":1864.66}, # index = 82
            {"note":"B6",      "frequency":1975.53}, # index = 83
            {"note":"C7",      "frequency":2093.00}, # index = 84
            {"note":"C#7/Db7", "frequency":2217.46}, # index = 85
            {"note":"D7",      "frequency":2349.32}, # index = 86
            {"note":"D#7/Eb7", "frequency":2489.02}, # index = 87
            {"note":"E7",      "frequency":2637.02}, # index = 88
            {"note":"F7",      "frequency":2793.83}, # index = 89
            {"note":"F#7/Gb7", "frequency":2959.96}, # index = 90
            {"note":"G7",      "frequency":3135.96}, # index = 91
            {"note":"G#7/Ab7", "frequency":3322.44}, # index = 92
            {"note":"A7",      "frequency":3520.00}, # index = 93
            {"note":"A#7/Bb7", "frequency":3729.31}, # index = 94
            {"note":"B7",      "frequency":3951.07}, # index = 95
            {"note":"C8",      "frequency":4186.01}, # index = 96
            {"note":"C#8/Db8", "frequency":4434.92}, # index = 97
            {"note":"D8",      "frequency":4698.63}, # index = 98
            {"note":"D#8/Eb8", "frequency":4978.03}, # index = 99
            {"note":"E8",      "frequency":5274.04}, # index = 100
            {"note":"F8",      "frequency":5587.65}, # index = 101
            {"note":"F#8/Gb8", "frequency":5919.91}, # index = 102
            {"note":"G8",      "frequency":6271.93}, # index = 103
            {"note":"G#8/Ab8", "frequency":6644.88}, # index = 104
            {"note":"A8",      "frequency":7040.00}, # index = 105
            {"note":"A#8/Bb8", "frequency":7458.62}, # index = 106
            {"note":"B8",      "frequency":7902.13}  # index = 107
        ]

        # create an array of dictionaries to hold the values for each line
        self.line_store = [{'index':k, 'name':'', 'interval':0, 'note':'', 'freq':0.0, 'hole':0.25, 'location':0.0, 'diff':0.0, 'cutoff':0.0} for k in range(12)]
        self.bellNoteArray = []
        for num in range(len(self.note_table)):
                self.bellNoteArray.append("%s (%s Hz)"%(self.note_table[num]["note"], str(self.note_table[num]["frequency"])))

    def get_data(self):
        return {
            'disp_frac':self.disp_frac,
            'units':self.units,
            'title':self.title,
            'inside_dia':self.inside_dia,
            'wall_thickness':self.wall_thickness,
            'number_holes':self.number_holes,
            'bell_selection':self.bell_note_select,
            'emb_area':self.embouchure_area,
            'bell_freq':self.bell_freq,
            'line_store':self.line_store
        }

    def set_data(self, data):
        self.disp_frac = data['disp_frac']
        self.units = data['units']
        self.title = data['title']
        self.inside_dia = data['inside_dia']
        self.wall_thickness = data['wall_thickness']
        self.number_holes = data['number_holes']
        self.bell_note_select = data['bell_selection']
        self.embouchure_area = data['emb_area']
        self.bell_freq = data['bell_freq']
        self.line_store = data['line_store']

    def get_disp_frac(self):
        return self.disp_frac
    def get_units(self):
        return self.units
    def get_title(self):
        return self.title
    def get_inside_dia(self):
        return self.inside_dia
    def get_wall_thickness(self):
        return self.wall_thickness
    def get_number_holes(self):
        return self.number_holes
    def get_bell_selection(self):
        return self.bell_note_select
    def get_emb_area(self):
        return self.embouchure_area
    def get_bell_freq(self):
        return self.bell_freq
    def get_line_data(self):
        return self.line_data

    def set_disp_frac(self, data):
        if type(data) != type(True):
            messagebox.showerror("Error", "set_disp_frac: expected type %s but got type %s"%(type(True), type(data)))
            return
        self.disp_frac = data
    def set_units(self, data):
        if type(data) != type(True):
            messagebox.showerror("Error", "set_units: expected type %s but got type %s"%(type(True), type(data)))
            return
        self.units = data
    def set_title(self, data):
        if type(data) != type(""):
            messagebox.showerror("Error", "set_title: expected type %s but got type %s"%(type(""), type(data)))
            return
        self.title = data
    def set_inside_dia(self, data):
        if type(data) != type(0.0):
            messagebox.showerror("Error", "set_title: expected type %s but got type %s"%(type(0.0), type(data)))
            return
        self.inside_dia = data
    def set_wall_thickness(self, data):
        if type(data) != type(0.0):
            messagebox.showerror("Error", "set_wall_thickness: expected type %s but got type %s"%(type(0.0), type(data)))
            return
        self.wall_thickness = data
    def set_number_holes(self, data):
        if type(data) != type(0.0):
            messagebox.showerror("Error", "set_number_holes: expected type %s but got type %s"%(type(0.0), type(data)))
            return
        self.number_holes = data
    def set_bell_selection(self, data):
        if type(data) != type(""):
            messagebox.showerror("Error", "set_bell_selection: expected type %s but got type %s"%(type(True), type(data)))
            return
        self.bell_note_select = data
    def set_emb_area(self, data):
        if type(data) != type(0):
            messagebox.showerror("Error", "set_emb_area: expected type %s but got type %s"%(type(0), type(data)))
            return
        self.embouchure_area = data
    def set_bell_freq(self, data):
        if type(data) != type(0.0):
            messagebox.showerror("Error", "set_bell_freq: expected type %s but got type %s"%(type(0.0), type(data)))
            return
        self.bell_freq = data
    def set_line_data(self, data):
        if type(data) != type(0.0):
            messagebox.showerror("Error", "set_line_data: expected type %s but got type %s"%(type(0.0), type(data)))
            return
        self.line_data = data

    def get_line(self, index):
        return self.line_store[index]

    def set_line(self, index, line):
        self.line_store[index] = line