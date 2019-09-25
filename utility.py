
import sys, math, time
from exception import AppError


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

    def __init__(self, name, level=DEBUG, stream=STDOUT):

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

        if stream == self.STDERR:
            self.stream = sys.stderr
        else:
            self.stream = sys.stdout

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

logger = Logger("Utility", Logger.DEBUG)

# Utility methods
def reduce(val):
    '''
    Reduce the internal value to a fraction and return it as a string.
    '''
    logger.debug(sys._getframe().f_code.co_name)

    w = int(val / (1/64))
    f = 64
    while w % 2 == 0:
        w = w / 2
        f = f / 2

        if f == 0:
            logger.error("inch value = %0.3f"%(val))
            raise AppError("reduce", "Cannot convert internal value (%0.3f) to a fraction."%(val))

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
        raise AppError("fractof", "Cannot convert value to a fraction: \"%s\""%(frac), e)

def rnd(num, factor):
    '''
    Find the closest multiple of factor for num.
    '''
    logger.debug(sys._getframe().f_code.co_name)
    a = math.ceil(num/factor)*factor
    b = math.floor(num/factor)*factor
    if abs(num - a) < abs(num - b):
        return a
    else:
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
    logger.debug(sys._getframe().f_code.co_name)
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
    '''
    def wrapper(*args, **kwargs):
        args[0].logger.debugger(func.__name__, "-- enter")
        retv = func(*args, **kwargs)
        args[0].logger.debugger(func.__name__, "-- leave")
        return retv
    return wrapper

