
import sys, math

from logger import Logger
from exception import AppError

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

