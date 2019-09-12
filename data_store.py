import sys
from tkinter import messagebox
from logger import Logger
from exception import AppError, AppFatalError, AppWarning

class DataStore:
    '''
    This is a simple class to facilitate communicating the data between
    the GUI and the calculator. It contains the state of the progam as
    it pertains to what the calculator needs to function. This object can
    be passed around providing a consistent way to access the data it
    contains.
    '''

    # TODO: 
    #  1. Read the default state from a configuration file.
    #  2. Add methods to save and restore the default state.
    #  3. Add methods to save and restore the current state as a "saved file".
    def __init__(self):

        self.logger = Logger(self.__class__.__name__, Logger.DEBUG)
        self.logger.debug(sys._getframe().f_code.co_name)
        
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
        #self.line_store = [{'index':k, 'name':'', 'interval':0, 'note':'', 'freq':0.0, 'hole':0.25, 'location':0.0, 'diff':0.0, 'cutoff':0.0} for k in range(12)]
        self.line_store = []
        self.bellNoteArray = []
        for num in range(len(self.note_table)):
                self.bellNoteArray.append("%s (%s Hz)"%(self.note_table[num]["note"], str(self.note_table[num]["frequency"])))


    # get by data structure
    def get_state(self):
        self.logger.debug(sys._getframe().f_code.co_name)
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

    # set by data structure
    def set_state(self, data):
        self.logger.debug(sys._getframe().f_code.co_name)

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

    # get and set the line data structure
    def get_line(self, index):
        return self.line_store[index]

    def set_line(self, index, line):
        self.logger.debug(sys._getframe().f_code.co_name)
        self.line_store.insert(index, line)

    def del_line(self, index):
        self.logger.debug(sys._getframe().f_code.co_name)
        self.logger.debug("destroy line number %d"%(index))
        return self.line_store.pop(index)

    def get_line_store(self):
        '''
        Simply return the line store for direct manipulation.
        '''
        return self.line_store

    # Utilities
    def validate_type(self, var, t):
        '''
        Validate the type of the srguement. If it cannot be converted, then the program cannot continue.
        This is considered a developer error. The exceptions here only happen if the input validation 
        from the GUI has failed.
        '''
        self.logger.debug(sys._getframe().f_code.co_name)
        if type(var) != t:
            if t is float:
                try:
                    tmp = float(var)
                    return tmp
                except ValueError:
                    raise AppFatalError("expected type %s but got type %s"%(str(t), str(type(var))), "validate_type")
                except:
                    raise AppFatalError("float type error.", "validate_type")

            elif t is int:
                try:
                    tmp = int(var)
                    return tmp
                except ValueError:
                    raise AppFatalError("expected type %s but got type %s"%(str(t), str(type(var))), "validate_type")
                except:
                    raise AppFatalError("int type error.", "validate_type")

            elif t is bool:
                try:
                    tmp = bool(var)
                    return tmp
                except ValueError:
                    raise AppFatalError("expected type %s but got type %s"%(str(t), str(type(var))), "validate_type")
                except:
                    raise AppFatalError("bool type error.", "validate_type")

            elif t is str:
                # anything can be converted to a str()
                return str(var)
            else:
                raise AppFatalError("attempt to validate an unexpected type %s as type %s."%(str(type(var)), str(t)), "validate_type")
        else:
            return var

    '''
    # individual getters
    def get_disp_frac(self):
        self.logger.debug("get_disp_frac(): %s"%(str(self.disp_frac)))
        return self.disp_frac
    
    def get_units(self):
        self.logger.debug("get_units(): %s"%(str(self.units)))
        return self.units

    def get_title(self):
        self.logger.debug("get_title(): %s"%(str(self.title)))
        return self.title

    def get_inside_dia(self):
        self.logger.debug("get_inside_dia(): %s"%(str(self.inside_dia)))
        return self.inside_dia

    def get_wall_thickness(self):
        self.logger.debug("get_wall_thickness(): %s"%(str(self.wall_thickness)))
        return self.wall_thickness

    def get_number_holes(self):
        self.logger.debug("get_number_holes(): %s"%(str(self.number_holes)))
        return self.number_holes

    def get_bell_selection(self):
        self.logger.debug("get_bell_selection(): %s"%(str(self.bell_note_select)))
        return self.bell_note_select

    def get_emb_area(self):
        self.logger.debug("get_disp_frac(): %s"%(str(self.disp_frac)))
        return self.embouchure_area

    def get_bell_freq(self):
        self.logger.debug("get_emb_area(): %s"%(str(self.bell_freq)))
        return self.bell_freq

#    def get_line_data(self):
#        self.logger.debug("DataStore.get_line_data(): %s"%(str(self.line_data)))
#        return self.line_data

    # individual setters
    def set_disp_frac(self, data):
        self.disp_frac = self.validate_type(data, bool)
        self.logger.debug("set_disp_frac(): %s"%(str(self.disp_frac)))

    def set_units(self, data):
        self.units = self.validate_type(data, bool)
        self.logger.debug("set_units(): %s"%(str(self.units)))

    def set_title(self, data):
        self.title = self.validate_type(data, str)
        self.logger.debug("set_title(): %s"%(str(self.title)))

    def set_inside_dia(self, data):
        self.inside_dia = self.validate_type(data, float)
        self.logger.debug("set_inside_dia(): %s"%(str(self.inside_dia)))

    def set_wall_thickness(self, data):
        self.wall_thickness = self.validate_type(data, float)
        self.logger.debug("set_wall_thickness(): %s"%(str(self.wall_thickness)))

    def set_number_holes(self, data):
        self.number_holes = self.validate_type(data, int)
        self.logger.debug("set_number_holes(): %s"%(str(self.number_holes)))

    def set_bell_selection(self, data):
        self.bell_note_select = self.validate_type(data, int)
        self.logger.debug("set_bell_selection(): %s"%(str(self.bell_note_select)))

    def set_emb_area(self, data):
        self.embouchure_area = self.validate_type(data, float)
        self.logger.debug("set_emb_area(): %s"%(str(self.embouchure_area)))

    def set_bell_freq(self, data):
        self.bell_freq = self.validate_type(data, float)
        self.logger.debug("set_bell_freq(): %s"%(str(self.bell_freq)))

    # Line getters and setters. These are so that the class using the line 
    # only needs to know about the data_store object and not about the line
    # object.


#    def set_line_data(self, data):
#        if type(data) != type(0.0):
#            messagebox.showerror("Error", "set_line_data: expected type %s but got type %s"%(type(0.0), type(data)))
#            return
#        self.line_data = data

    '''
