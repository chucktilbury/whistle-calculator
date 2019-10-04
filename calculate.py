import math, sys
import traceback

from data_store import DataStore
#from configuration import Configuration
from utility import Logger, debugger, register_event, raise_event

# Speed of Sound = 345 m/s = 1130 ft/s = 770 miles/hr

class Calculator:

    # TODO:
    #   1. Add formulas 
    #   2. Connect the formulas to the data store
    def __init__(self):
        # constant data
        self.logger = Logger(self, Logger.INFO)
        self.logger.debug("enter constructor")
        #self.configuration = Configuration.get_instance()
        self.data = DataStore.get_instance()
        self.logger.debug("end constructor")
        register_event("CALCULATE_EVENT", self.do_calc)

        # TODO: make temperature a configurable variable
        self.isound = 13584.0
        self.msound = self.isound * 25.4

        # TODO: make these accessible from configuration??
        self.max_loop = 12
        self.max_delta = 0.0001


    @debugger
    def update(self):
        '''
        Make all calculations based on the current state.
        '''
        pass

    @debugger
    def do_calc(self):
        self.data.clear_hole_data()
        if self.data.get_calc_type() == 0:
            self.quadratic()
            #self.iterative()
        else:
            self.iterative()
        raise_event("UPDATE_LINES_EVENT")

    @debugger
    def closedCorrection(self, index):
        b = self.data.get_inside_dia()
        holeSize = self.data.get_hole_size(index)
        p = (holeSize / b) * (holeSize / b)
        retv = (self.data.get_wall_thickness() * p) / 4.0
        return retv


    @debugger
    def effectiveThickness(self, index):
        return self.data.get_wall_thickness() + (self.data.get_chim_const() * self.data.get_hole_size(index))


    @debugger
    def embouchureCorrection(self):
        #embarea = windowlen * windowwid; embarea *= 6.4516;
        embArea = (self.data.get_emb_width() * self.data.get_emb_length() * 2 * math.pi)
        embRadius = math.sqrt(embArea / math.pi)

        # embdist = 3.14159265F * Embcorr * Cfg.borecent * Cfg.borecent / embarea * (Cfg.thickcent
        # + 1.5F * (double) sqrt( (double) (embarea / 3.14159265F)));
        embDist = ((math.pi * self.data.get_inside_dia() * self.data.get_inside_dia() * self.data.get_ecorr()) / embArea)
        ccc = ((self.data.get_wall_thickness() + 1.5 * embRadius))
        embDist = embDist * ccc
        return embDist


    @debugger
    def holeSpacing(self, index):
        holeSpacing = 0.0
        if (index == 0):
            holeSpacing = self.data.get_end_location() - self.data.get_hole_location(index)
        else:
            holeSpacing = self.data.get_hole_location(index-1) - self.data.get_hole_location(index)
        
        return holeSpacing


    @debugger
    def endCorrection(self):
        return 0.6133 * self.data.get_inside_dia() / 2  # original flutomat


    @debugger
    #def firstHoleDistance(self, index):
    def firstHoleDistance(self):
        # // Cfg.open[1] = Cfg.height[1] /
        # // ((double) pow((double) (Cfg.diacent[1]/Cfg.borecent), 2.0) +
        # // Cfg.height[1] * (1.0F / Cfg.hs[1]));
        # final double bore = hole.whistle.bore;
        pow = ((self.data.get_hole_size(0) / self.data.get_inside_dia()) * 
                    (self.data.get_hole_size(0) / self.data.get_inside_dia()))
        holeSp = self.holeSpacing(0)
        e = self.effectiveThickness(0)
        q = e * (1.0 / holeSp)
        r = pow + q
        openCorrection = e / r
        return openCorrection


    @debugger
    def subsequentHoleDistance(self, index):
        # // Cfg.open[n] = Cfg.hs[n] * 0.5F *
        # // ( (double) sqrt((double) 1.0F + 4.0F * Cfg.height[n] / Cfg.hs[n] *
        # // (double) pow((double) (Cfg.borecent / Cfg.diacent[n]), 2.0)) - 1.0F);
        # final double bore = hole.whistle.bore;

        a = self.data.get_inside_dia() / self.data.get_hole_size(index)
        b = a * a
        holeSp = self.holeSpacing(index)
        c = 4.0 * self.effectiveThickness(index) / holeSp * b
        d = math.sqrt(1.0 + c)
        openCorrection = holeSp * 0.5 * (d - 1.0)
        return openCorrection


    @debugger
    def cutoffFrequency(self, index):
        dist = self.data.get_hole_location(index-1) - self.data.get_hole_location(index)
        sqrtTerm = math.sqrt(self.effectiveThickness(index) * dist)
        ratio = self.vsound() / (2 * math.pi)
        ratio = ratio * (self.data.get_hole_size(index) / self.data.get_inside_dia())
        ratio = ratio / sqrtTerm
        return ratio

    @debugger 
    def vsound(self):
        if self.data.get_units():
            return self.msound
        else:
            return self.isound

    @debugger
    def iterative(self):
        # Calculate position of end hole
        xEnd = self.vsound() / (2 * self.data.get_bell_freq())
        xEnd = xEnd - self.endCorrection()
        for i in range(self.data.get_number_holes()):
            xEnd = xEnd - self.closedCorrection(i)
        self.data.set_end_location(xEnd)

        # find first finger hole location
        nominalPosition = self.vsound() / (2 * self.data.get_hole_freq(0))
        self.data.set_hole_location(0, 0.0)
        delta = 10.0

        for i in range(self.max_loop):
            oldPosition = self.data.get_hole_location(0)
            self.data.set_hole_location(0, nominalPosition - self.firstHoleDistance())
            self.data.print_data()

            for h in range(1, self.data.get_number_holes()):
                loc = self.data.get_hole_location(0) 
                loc -= self.closedCorrection(h)
                self.data.set_hole_location(0, loc) 

            delta = math.fabs(self.data.get_hole_location(0) - oldPosition)
            if delta < self.max_delta:
                break

        # set subsequent finger hole locations
        for holeNum in range(1, self.data.get_number_holes()):
            # final Hole hole = whistle.hole[holeNum]
            nominalPosition = self.vsound() / (2 * self.data.get_hole_freq(holeNum))
            self.data.set_hole_location(holeNum, 0.0)
            delta = 10.0
            for i in range(self.max_loop):
                oldPosition = self.data.get_hole_location(holeNum)
                self.data.set_hole_location(holeNum, nominalPosition - self.subsequentHoleDistance(holeNum))
                for h in range(holeNum+1, self.data.get_number_holes()):
                    loc = self.data.get_hole_location(holeNum)
                    loc -= self.closedCorrection(h)
                    self.data.set_hole_location(holeNum, loc)

                delta = math.fabs(self.data.get_hole_location(holeNum) - oldPosition)

        self.embouchureCorrection()
        for holeNum in range(self.data.get_number_holes()):
            self.data.set_hole_cutoff(holeNum, self.cutoffFrequency(holeNum))
            self.data.set_hole_rcutoff(holeNum, self.data.get_hole_cutoff(holeNum) / self.data.get_hole_freq(holeNum))
            self.data.set_hole_xloc(holeNum, self.data.get_end_location() - self.data.get_hole_location(holeNum))
            if holeNum == 0:
                self.data.set_hole_diff(0, self.data.get_end_location() - self.data.get_hole_location(holeNum))
            else:
                self.data.set_hole_diff(0, self.data.get_hole_location(holeNum-1) - self.data.get_hole_location(holeNum))


    @debugger
    def quadratic(self):
            # Calculate position of end hole
        xEnd = self.vsound() / (2 * self.data.get_bell_freq())
        xEnd = xEnd - self.endCorrection()

        for i in range(self.data.get_number_holes()):
            xEnd -= self.closedCorrection(i)
        self.data.set_end_location(xEnd)

        # Calculate the position of the first tone hole
        length = self.vsound() / (2 * self.data.get_hole_freq(0))
        for i in range(1, self.data.get_number_holes()):
            length = length - self.closedCorrection(i)

        try:
            h = self.data.get_hole_size(0)
            a =  h / self.data.get_inside_dia()
            a = a * a
            b = -(xEnd + length) * a
            c = (xEnd * length) * a
            c += self.effectiveThickness(0) * (length - xEnd)
            v = (b * b) - (4.0 * a * c)
            self.data.set_hole_location(0, (-b - math.sqrt(math.fabs(v))) / ((2 * a)))

            # find subsequent finger hole locations
            for holeNum in range(1, self.data.get_number_holes()):
                length = self.vsound() / (2.0 * self.data.get_hole_freq(holeNum))
                for i in range(holeNum + 1, self.data.get_number_holes()):
                    length = length - self.closedCorrection(i)

                a = 2.0
                ratio = self.data.get_inside_dia() / self.data.get_hole_size(holeNum)
                ratio = ratio * ratio * self.effectiveThickness(holeNum)

                prevHole = self.data.get_hole_location(holeNum - 1)

                b = -prevHole - (3.0 * length)
                b = b + ratio
                c = length - ratio
                c = c * prevHole
                c = c + length * length
                v = (b * b) - (4 * a * c)
                self.data.set_hole_location(holeNum, (-b - math.sqrt(math.fabs(v))) / ((2 * a)))
        except ValueError as e:
            self.logger.error("%s: a = %f, b = %f, c = %f, v = %f"%(str(e), a, b, c, v))


        self.embouchureCorrection()
        for holeNum in range(self.data.get_number_holes()):
            self.data.set_hole_cutoff(holeNum, self.cutoffFrequency(holeNum))
            self.data.set_hole_rcutoff(holeNum, self.data.get_hole_cutoff(holeNum) / self.data.get_hole_freq(holeNum))
            self.data.set_hole_xloc(holeNum, self.data.get_end_location() - self.data.get_hole_location(holeNum))
            if holeNum == 0:
                self.data.set_hole_diff(0, self.data.get_end_location() - self.data.get_hole_location(holeNum))
            else:
                self.data.set_hole_diff(holeNum, self.data.get_hole_location(holeNum-1) - self.data.get_hole_location(holeNum))

