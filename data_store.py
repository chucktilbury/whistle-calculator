import sys, pickle, pprint
from tkinter import messagebox
from utility import Logger, debugger
from exception import AppError, AppFatalError, AppWarning
#from configuration import Configuration


class DataStore:
    '''
    This is a simple class to facilitate communicating the data between
    the GUI and the calculator. It contains the state of the progam as
    it pertains to what the calculator needs to function. This object can
    be passed around providing a consistent way to access the data it
    contains.

    This is a singleton class. To get the instance call get_instance()
    '''
    __instance = None

    @staticmethod
    def get_instance():
        '''
        This static method is used to get the singleton object for this class.
        '''
        if DataStore.__instance == None:
            DataStore()
        return DataStore.__instance

    def __init__(self):

        # gate the accress to __init__()
        if DataStore.__instance != None:
            raise Exception("DataStore class is a singleton. Use get_instance() instead.")
        else:
            DataStore.__instance = self

        # Continue with init exactly once.
        self.logger = Logger(self, Logger.INFO)
        self.logger.debug("enter constructor")

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

        # default values
        self.internal_data = {}
        self.load('default.wis')

        # self.intervals = [2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2]

        self.bellNoteArray = []
        for num in range(len(self.note_table)):
                self.bellNoteArray.append("%s (%s Hz)"%(self.note_table[num]["note"], str(self.note_table[num]["frequency"])))

        self.logger.debug("leave constructor")

    # # get by data structure
    # @debugger
    # def get_state(self):
    #     return self.internal_data

    # # set by data structure
    # @debugger
    # def set_state(self, data):
    #     self.internal_data = data

    # # get and set the line data structure
    # @debugger
    # def get_line(self, index):
    #     return self.internal_data['hole_values'][index]

    # @debugger
    # def set_line(self, index, line):
    #     #self.internal_data['hole_values'].insert(index, line)
    #     self.internal_data['hole_values'][index] = line

    # @debugger
    # def del_line(self, index):
    #     self.logger.debug("destroy line number %d"%(index))
    #     return self.internal_data['hole_values'].pop(index)

    # @debugger
    # def get_line_store(self):
    #     '''
    #     Simply return the line store for direct manipulation.
    #     '''
    #     return self.internal_data['hole_values']

    # file IO
    @debugger
    def load(self, fname=None):
        with open(fname, 'rb') as fh:
            self.internal_data = pickle.load(fh)

    @debugger
    def save(self, fname=None):
        with open(fname, "wb") as fh:
            pickle.dump(self.internal_data, fh, protocol=pickle.HIGHEST_PROTOCOL)

    # getters and setters
    @debugger
    def get_file_name(self):
        return self.internal_data['file_name']

    @debugger
    def set_file_name(self, name):
        self.internal_data['file_name'] = self.validate_type(name, str)

    @debugger
    def get_disp_frac(self):
        return self.internal_data['disp_frac']

    @debugger
    def get_units(self):
        return self.internal_data['units']

    @debugger
    def get_title(self):
        return self.internal_data['title']

    @debugger
    def get_inside_dia(self):
        return self.internal_data['inside_dia']

    @debugger
    def get_wall_thickness(self):
        return self.internal_data['wall_thickness']

    @debugger
    def get_number_holes(self):
        return self.internal_data['number_holes']

    @debugger
    def get_bell_note_select(self):
        return self.internal_data['bell_note_select']

    @debugger
    def get_bell_freq(self):
        return self.internal_data['bell_freq']

    @debugger
    def get_embouchure_area(self):
        return self.internal_data['embouchure_area']

    @debugger
    def set_disp_frac(self, val):
        self.internal_data['disp_frac'] = self.validate_type(val, bool)

    @debugger
    def set_units(self, val):
        self.internal_data['units'] = self.validate_type(val, bool)

    @debugger
    def set_title(self, val):
        self.internal_data['title'] = self.validate_type(val, str)

    @debugger
    def set_inside_dia(self, val):
        self.internal_data['inside_dia'] = self.validate_type(val, float)

    @debugger
    def set_wall_thickness(self, val):
        self.internal_data['wall_thickness'] = self.validate_type(val, float)

    @debugger
    def set_number_holes(self, val):
        #self.logger.push_level(Logger.DEBUG)
        #self.logger.debug("setting holes to %d"%(val))
        self.internal_data['number_holes'] = self.validate_type(val, int)
        #self.logger.pop_level()

    @debugger
    def set_bell_note_select(self, val):
        self.internal_data['bell_note_select'] = self.validate_type(val, int)

    @debugger
    def set_bell_freq(self, val):
        self.internal_data['bell_freq'] = self.validate_type(val, float)
        self.internal_data['freqs'][0] = self.validate_type(val, float)

    @debugger
    def set_embouchure_area(self, val):
        self.internal_data['embouchure_area'] = self.validate_type(val, float)

    @debugger
    def get_emb_length(self):
        return self.internal_data['emb_length']

    @debugger
    def get_emb_width(self):
        return self.internal_data['emb_width']

    @debugger
    def set_emb_length(self, val):
        self.internal_data['emb_length'] = self.validate_type(val, float)

    @debugger
    def set_emb_width(self, val):
        self.internal_data['emb_width'] = self.validate_type(val, float)

    def get_ecorr(self):
        return self.internal_data['ecorr']

    def get_chim_const(self):
        return self.internal_data['chim_const']

    def set_ecorr(self, val):
        self.internal_data['ecorr'] = self.validate_type(val, float)

    def set_chim_const(self, val):
        self.internal_data['chim_const'] = self.validate_type(val, float)

    @debugger
    def get_hole_inc(self):
        if self.internal_data['units']:
            return self.internal_data['hole_mm_inc']
        else:
            return self.internal_data['hole_in_inc']
    
    @debugger
    def get_hole_max(self):
        if self.internal_data['units']:
            return self.internal_data['hole_mm_max']
        else:
            return self.internal_data['hole_in_max']
    
    @debugger
    def get_hole_min(self):
        if self.internal_data['units']:
            return self.internal_data['hole_mm_min']
        else:
            return self.internal_data['hole_in_min']
    
    @debugger
    def set_hole_inc(self, val):
        if self.internal_data['units']:
            self.internal_data['hole_mm_inc'] = self.validate_type(val, float)
        else:
            self.internal_data['hole_in_inc'] = self.validate_type(val, float)
    
    @debugger
    def set_hole_max(self, val):
        if self.internal_data['units']:
            self.internal_data['hole_mm_max'] = self.validate_type(val, float)
        else:
            self.internal_data['hole_in_max'] = self.validate_type(val, float)
    
    @debugger
    def set_hole_min(self, val):
        if self.internal_data['units']:
            self.internal_data['hole_mm_min'] = self.validate_type(val, float)
        else:
            self.internal_data['hole_in_min'] = self.validate_type(val, float)
    
    @debugger
    def get_hole_size(self, index):
        return self.internal_data['hole_sizes'][index+1]

    @debugger
    def get_hole_interval(self, index):
        return self.internal_data['intervals'][index+1]

    @debugger
    def get_hole_note(self, index):
        return self.internal_data['notes'][index+1]

    @debugger
    def get_hole_freq(self, index):
        return self.internal_data['freqs'][index+1]

    @debugger
    def get_hole_location(self, index):
        return self.internal_data['locations'][index+1]

    @debugger
    def get_end_location(self):
        return self.internal_data['locations'][0]

    @debugger
    def set_end_location(self, val):
        self.internal_data['locations'][0] = self.validate_type(val, float)

    @debugger
    def get_hole_diff(self, index):
        return self.internal_data['diffs'][index+1]

    @debugger
    def get_hole_cutoff(self, index):
        return self.internal_data['cutoffs'][index+1]

    @debugger
    def get_hole_rcutoff(self, index):
        return self.internal_data['rcutoffs'][index+1]

    @debugger
    def get_hole_xloc(self, index):
        return self.internal_data['xlocs'][index+1]

    @debugger
    def get_calc_type(self):
        return self.internal_data['calc_type']
    
    ######################################################################

    @debugger
    def set_calc_type(self, val):
        self.internal_data['calc_type'] = self.validate_type(val, int)

    @debugger
    def set_hole_rcutoff(self, index, val):
        self.internal_data['rcutoffs'][index+1] = self.validate_type(val, float)

    @debugger
    def set_hole_xloc(self, index, val):
        self.internal_data['xlocs'][index+1] = self.validate_type(val, float)

    @debugger
    def set_hole_size(self, index, val):
        self.internal_data['hole_sizes'][index+1] = self.validate_type(val, float)

    @debugger
    def set_hole_interval(self, index, val):
        self.internal_data['intervals'][index+1] = self.validate_type(val, int)

    @debugger
    def set_hole_note(self, index, val):
        self.internal_data['notes'][index+1] = self.validate_type(val, str)

    @debugger
    def set_hole_freq(self, index, val):
        self.internal_data['freqs'][index+1] = self.validate_type(val, float)

    @debugger
    def set_hole_location(self, index, val):
        self.internal_data['locations'][index+1] = self.validate_type(val, float)

    @debugger
    def set_hole_diff(self, index, val):
        self.internal_data['diffs'][index+1] = self.validate_type(val, float)

    @debugger
    def set_hole_cutoff(self, index, val):
        self.internal_data['cutoffs'][index+1] = self.validate_type(val, float)

    @debugger
    def clear_hole_data(self):
        for x in range(12):
            #self.set_hole_size(x, 0.0)
            #self.set_hole_note(x, '')
            #self.set_hole_freq(x, 0.0)
            self.set_hole_location(x, 0.0)
            self.set_hole_diff(x, 0.0)
            self.set_hole_cutoff(x, 0.0)
            self.set_hole_rcutoff(x, 0.0)
            self.set_hole_xloc(x, 0.0)

    # Utilities
    @debugger
    def validate_type(self, var, t):
        '''
        Validate the type of the srguement. If it cannot be converted, then the program cannot continue.
        This is considered a developer error. The exceptions here only happen if the input validation 
        from the GUI has failed.
        '''
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

    def print_data(self):
        pprint.pprint(self.internal_data)

