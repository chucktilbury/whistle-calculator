
import sys, math, time, pprint, pickle
import traceback
from tkinter import messagebox as mbox
#from exception import AppError

class Logger(object):
    '''
    Logger class produces messages on the text console. Used mostly for
    debugging. Supports individual class debugging and debug levels.
    '''

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    MESSAGE = 4
    STDERR = 0
    STDOUT = 1

    def __init__(self, name, level=DEBUG):

        self.dbg = 0
        self.inf = 1
        self.warn = 2
        self.err = 3
        self.mess = 4
        self.stderr = 0
        self.stdout = 1

        if type(name) == str:
            self.name = name
        else:
            self.name = name.__class__.__name__
        self.level = []
        self.level.insert(0, level)

        #if stream == self.STDERR:
        self.stream = sys.stderr
        #else:
        #self.stream = sys.stdout

    def fmt(self, args, lev):
        t = time.strftime("[%Y%m%d %H:%M:%S]")
        return "%s %s: %s: %s\n"%(t, lev, self.name, args)

    def debug(self, args, frame_num = 1):
        if self.level[0] <= self.dbg:
            s1 = sys._getframe(frame_num).f_code.co_name
            t = time.strftime("[%Y%m%d %H:%M:%S]")
            self.stream.write("%s %s: %s.%s(): %s\n"%(t, "DEBUG", self.name, s1, args))

    def info(self, args):
        if self.level[0] <= self.inf:
            self.stream.write(self.fmt(args, 'INFO'))

    def warning(self, args):
        if self.level[0] <= self.warn:
            self.stream.write(self.fmt(args, 'WARNING'))

    def error(self, args):
        if self.level[0] <= self.err:
            self.stream.write(self.fmt(args, 'ERROR'))

    def msg(self, args):
        if self.level[0] <= self.mess:
            self.stream.write(self.fmt(args, 'MSG'))

    def fatal(self, args):
        self.stream.write(self.fmt(args, 'FATAL ERROR'))
        self.stream.write("System cannot continue\n\n")
        sys.exit(1)

    def push_level(self, level):
        self.level.insert(0, level)

    def pop_level(self):
        if len(self.level) > 1:
            self.level.remove(0)

    def set_level(self, level):
        self.level[0] = level

    def debugger(self, name, args):
        if self.level[0] <= self.dbg:
            t = time.strftime("[%Y%m%d %H:%M:%S]")
            self.stream.write("%s %s: %s.%s(): %s\n"%(t, "DEBUG", self.name, name, args))

logger = Logger("Utility", Logger.INFO)

# Utility methods
def mm_to_in(val, round=False):
    '''
    Simply convert the value given from MM to inches and round to the increment
    '''
    logger.debug(sys._getframe().f_code.co_name)
    from data_store import DataStore as ds # avoid a circular dependency
    data = ds.get_instance()
    if round:
        return rnd(val/25.4, data.internal_data['hole_in_inc'])
    else:
        return val/25.4

def in_to_mm(val, round=False):
    '''
    Simply convert the value given from inches to MM and round to the increment
    '''
    logger.debug(sys._getframe().f_code.co_name)
    from data_store import DataStore as ds # avoid a circular dependency
    data = ds.get_instance()
    if round:
        return rnd(val*25.4, data.internal_data['hole_mm_inc'])
    else:
        return val*25.4

def reduce(val):
    '''
    Reduce the internal value to a fraction and return it as a string.
    '''
    logger.debug(sys._getframe().f_code.co_name)
    if val == 0.0:
        return '--'

    w = int(val / (1/64))
    f = 64
    while w % 2 == 0:
        w = w / 2
        f = f / 2

        if f == 0:
            logger.error("inch value = %0.3f"%(val))
            mbox.showerror("ERROR", "Cannot convert internal value (%0.3f) to a fraction."%(val))

    # This can yield stupid values if w or f go below zero
    s = str(int(w))+"/"+str(int(f))
    logger.debug("reduce: %s: %s"%(str(val), s))
    return s

def fractof(frac):
    '''
    Convert the string given as a fraction into a float. Return the value.
    '''
    logger.debug(sys._getframe().f_code.co_name)
    logger.debug("convert string \"%s\""%(frac))
    if len(frac) == 0:
        return 0.0

    a = frac.split('/')
    try:
        return float(a[0]) / float(a[1])
    except ValueError as e:
        mbox.showerror("ERROR", "Cannot convert value to a fraction: \"%s\": %s"%(frac, str(e)))

def rnd(num, factor):
    '''
    Find the closest multiple of factor for num.
    '''
    if factor == 0.0:
        logger.debug("tring to factor zero")
        return num

    logger.debug("%s: num= %f, factor= %f"%(sys._getframe().f_code.co_name, num, factor))
    a = math.ceil(num/factor)*factor
    b = math.floor(num/factor)*factor
    logger.debug("a = %f, b = %f"%(a, b))
    # take the closest one
    if abs(num - a) > abs(num - b):
        logger.debug("return: %f"%(a))
        return a
    else:
        logger.debug("return: %f"%(b))
        return b

'''
The reason that the event handler exists is that the tkinter event
handler does not have a mechanism to send events to anything but a widget
and then there is no way to send the same event to multiple widgits.

The problem that this one solves is that there are a couple of controls in
the main window that need to cause everything else in the window to update.
One example of this is when the units are changed from inch to metric.
Every widgit that carries a measurement of some kind needs to be updated and
some of them are harder to change than others, so they all need their own
method to do that.

This event handler is very dumb. When a event is invoked, every handler
that has registered for the event is invoked in the order that it was
registered. This is done synchronously. It is perfectly okay for one event
handler to to raise another event, however, there is no checking to see
if there is a circular event chain. Event chains should be short. It is
unwise to depend on the order that they are run.

If an event is raised with arguments, but the handler does not have the
positional args, then an exception will be raised at runtime. Every
handler is called with the same arguments from the call to raise_event()

This is implemented as functions to make it unnessessary to pass around
an event object to every class that will use it.
'''

__event_list__ = {}
def register_event(name, callback):
    '''
    Store the event in the internal storage.
    '''
    logger.debug("%s: %s: %s.%s"%(
                sys._getframe().f_code.co_name,
                name,
                callback.__self__.__class__.__name__,
                callback.__name__))

    if not name in __event_list__:
        __event_list__[name] = []
    __event_list__[name].append(callback)


def raise_event(name, *args):
    '''
    Call all of the callbacks that have been registered.
    '''
    logger.debug("%s: %s"%(sys._getframe().f_code.co_name, name))
    if name in __event_list__:
        for cb in __event_list__[name]:
            if len(args) != 0:
                cb(*args)
            else:
                cb()
    logger.debug("%s: %s"%(sys._getframe().f_code.co_name, "returning"))

def dump_events():
    for item in __event_list__:
        print("%s:"%item)
        for cb in __event_list__[item]:
            print("\t%s.%s"%(cb.__self__.__class__.__name__, cb.__name__))

def make_default():
    '''
    This function creates the default whistle specification.

    Do not mess with this unless you know what you are doing. You will also
    have to change the data_store to utilize any changes.
    '''
    default_values = {
        'date_created':0.0,
        'date_modified':0.0,
        'file_name': "default.wis",

        # upper section values
        'disp_frac': True,   # True if the holes are displayed in fractions
        'units': False,      # True if the units are mm and false if it's inch
        'calc_type': 0,      # 0 = quadratic, 1 = iterative
        'title': "Default Whistle",
        'inside_dia': 0.5,
        'wall_thickness': 0.015,
        'number_holes': 6,
        'bell_note_select': 62,
        'bell_freq': 587.33,
        'vsound_in': 13584.0,
        'vsound_mm': 13584.0 * 25.4,
        'temperature': 72.0,
        #'humidity': 50,

        # embouchure data, considered configuration
        'embouchure_area': 0.0656,
        'emb_length': 0.175,
        'emb_width': 0.375,
        'emb_diameter': 0.0,
        'emb_type': 0, # 0 = rectangle, 1 = oval, 2 = round
        'ecorr':0.6133,
        'chim_const': 0.75,
        'length': 10.5,

        # holes data
        'intervals': [0, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2],
        'notes': ['', 'E', 'F#', 'G', 'A', 'B', 'C#', '', '', '', '', '', ''],
        'freqs': [587.33, 659.26, 739.99, 783.99, 880.0, 987.77, 1108.73, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'locations': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'xlocs': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'diffs': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'cutoffs': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'rcutoffs': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'hole_sizes': [0.0, 1/4, 11/32, 1/4, 9/32, 9/32, 1/4, 1/4, 1/4, 1/4, 1/4, 1/4, 1/4],

        # applies to all the holes
        'hole_in_inc': 1/64,
        'hole_in_max': 1/2,
        'hole_in_min': 3/16,
        'hole_mm_inc': 0.5,
        'hole_mm_max': 12.5,
        'hole_mm_min': 2.5,
        'version': 1.0,
        'text_notes': 'put your notes here',
        'max_delta': 0.0001
    }

    default_values['date_created'] = time.time()
    default_values['date_modified'] = time.time()

    with open('default.wis', 'wb') as fp:
        pickle.dump(default_values, fp, protocol=pickle.HIGHEST_PROTOCOL)

def base_decorator(decorator):
    '''This decorator can be used to turn simple functions
    into well-behaved decorators, so long as the decorators
    are fairly simple. If a decorator expects a function and
    returns a function (no descriptors), and if it doesn't
    modify function attributes or docstring, then it is
    eligible to use this. Simply apply @simple_decorator to
    your decorator and it will automatically preserve the
    docstring and function attributes of functions to which
    it is applied.'''
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    # Now a few lines needed to make simple_decorator itself
    # be a well-behaved decorator.
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator

# debug decorator
@base_decorator
def debugger(func):
    '''
    Debugger decorator places messages in the debug output when the class
    method is entered and when it is exited. It cannot be used with functions
    and it depends on the class having a "logger" member. When the logging
    level is below DEBUG this function does nothing.

    This can only wrap a method in a class that has a logger.
    '''
    def wrapper(*args, **kwargs):
        try:
            args[0].logger.debugger(func.__name__, "-- enter")
            retv = func(*args, **kwargs)
            args[0].logger.debugger(func.__name__, "-- returning: %s"%(str(retv)))
            return retv
        except Exception as ex:
            print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))

    return wrapper

