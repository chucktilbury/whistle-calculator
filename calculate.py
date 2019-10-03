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
        self.logger = Logger(self, Logger.DEBUG)
        self.logger.debug("enter constructor")
        #self.configuration = Configuration.get_instance()
        self.data = DataStore.get_instance()
        self.logger.debug("end constructor")
        register_event("CALCULATE_EVENT", self.do_calc)

        # TODO: make temperature a configurable variable
        self.isound = 13584.0
        self.msound = self.isound * 25.4

        # reset these for each calc
        self.xend = 0.0
        self.xemb = 0.0


    @debugger
    def update(self):
        '''
        Make all calculations based on the current state.
        '''
        pass

    @debugger
    def do_calc(self):
        self.iterative()
        raise_event("UPDATE_LINES_EVENT")

    @debugger
    def eff_wall(self, n):
        '''
        effective wall thickness, i.e. height of air column at open finger holes
        air column extends out past end of hole 3/4 of the hole diameter
        '''
        # TODO: make the 0.75 configurable
        a = self.data.get_wall_thickness()
        b = 0.75 * self.data.get_hole_size(n)
        retv= a+b
        return retv

    # @debugger
    # def emb_correction(self):
	# 	# return (Bore/Demb)*(Bore/Demb)*10.84*wall*Demb/(1.0*Bore + 2*wall);
    #     # TODO: Fix this
    #     Demb = (0.375 + 0.175) / 2
    #     r = (self.data.get_inside_dia() / Demb) * (self.data.get_inside_dia() / Demb)
    #     r = r * (10.84 * self.data.get_wall_thickness() * Demb)
    #     r = r / (self.data.get_inside_dia() + (2 * self.data.get_wall_thickness()))
    #     return r

    @debugger
    def closed_correction(self, n):
        '''
        Closed hole for tone hole n.  The length of the vibrating air column is
        effectively increased by each closed tone hole which exists above the
        first open tone hole. Corrections must be added for each such closed tone
        tone hole to C_end, C_s, and C_o.
        '''
        x = math.pow((self.data.get_hole_size(n) / self.data.get_inside_dia()), 2.0)
        retv = 0.25 * self.data.get_wall_thickness() * x
        return retv

    @debugger
    def end_correction(self):
        '''
        Calculates the distance from physical open end of flute to effective
        end of vibrating air column.  The vibrating air column ends beyond the
        end of the flute and C_end is always positive. NOTE: Closed hole
        corrections must be added to this value!
        '''
        # TODO: make the 0.6133 configurable
        #retv = 0.6133 * self.data.get_inside_dia() / 2
        retv = 0.30665 * self.data.get_inside_dia()
        return retv


    @debugger
    def first_correction(self):
        '''
        Calculates the effective distance from the first ("single") tone hole to
        the end of the vibrating air column when only that hole is open.
        NOTE: closed hole corrections must be added to this value!
        '''
        a = math.pow(self.data.get_hole_size(0) / self.data.get_inside_dia(), 2.0)
        b = self.eff_wall(0) / (self.xend - self.data.get_hole_size(0))
        retv = self.eff_wall(0) / a + b
        return retv

    @debugger
    def open_correction(self, n):
        '''
        Calculates the effective distance from the second and subsequent tone holes
        to the end of the vibrating air column when all holes below are open.
        NOTE: closed hole corrections must be added to this value!
        NOTE: the value of this correction is invalid if the frequency of the note
        played is above the cutoff frequency f_c. get_hole_location
        '''
        self.logger.debug(">>>>>>>>>>>>>>>>>> hole number: %d"%(n))
        self.logger.debug("hole location: %f"%(self.data.get_hole_location(n)))
        try:
            hl = self.data.get_hole_location(n-1) - self.data.get_hole_location(n)
            a = hl / 2.0
            b = self.eff_wall(n) / hl
            c = math.pow(self.data.get_inside_dia() / self.data.get_hole_size(n), 2)
            retv = a * (math.sqrt(1.0 + 4.0 * b * c) - 1)
        except Exception as ex:
            print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))
            raise

        return retv

    @debugger
    def emb_correction(self):
        '''
        C_emb = distance from theoretical start of air column to center of embouchure hole;
        the air column effectively extends beyond the blow hole center by this distance.
        (the cork face should be about 1 to 1.5 embouchure diameters from emb. center)
           C_emb := (Bore/Demb)*(Bore/Demb)*(wall+0.75*Demb); // per spreadsheet
           C_emb := (Bore/Demb)*(Bore/Demb)*(Bore/2 + wall + 0.6133*Demb/2); // an alternative
           C_emb := (Bore/Demb)*(Bore/Demb)*10.84*wall*Demb/(Bore + 2*wall); // kosel's empirical fit
        '''
        # TODO: Make these methods selectable in configuration
        # TODO: make these constants configurable
        a = math.pow(self.data.get_inside_dia() / self.data.get_embouchure_area(), 2)
        b = 1.0 * self.data.get_inside_dia() + 2.0 * self.data.get_wall_thickness()
        return (a * 10.84 * self.data.get_wall_thickness() * self.data.get_embouchure_area() / b )

    @debugger
    def cutoff(self, n):
        '''
        Calculates the cutoff frequency above which the open hole correction
        is not valid.  Instrument should be designed so that all second register
        notes are well below this frequency.
        '''
        if n == 0:
            hl = self.xend - self.data.get_hole_location(n)
        else:
            hl = self.data.get_hole_location(n-1) - self.data.get_hole_location(n)

        if self.data.get_units():
            vsound = self.msound
        else:
            vsound = self.isound

        a = self.data.get_hole_size(n) / self.data.get_inside_dia()
        # TODO: make these formulas selectable from configuration
        # formula 1
        retv = vsound / 2.0 / math.pi * a / math.sqrt(self.eff_wall(n) * hl)
        # formula 2
        #retv = vsound / (2.0 * math.pi) * a * (1.0 / math.sqrt(self.eff_wall(n) * hl))

        return retv

    @debugger 
    def vsound(self):
        if self.data.get_units():
            return self.msound
        else:
            return self.isound

    def iterative(self):
        pass

    def quadratic(self):
        pass

    # @debugger
    # def FindLocations(self):
    #     '''
    #     This procedure finds the locations of end of flute, all finger holes, and
    #     emb. hole using the Benade equations above in an interative manner.
    #     '''

    #     #var i, X, oldX, holeNum;

    #     # find end location...
    #     self.logger.debug("End correction and closed holes to end")
    #     self.xend = self.vsound() * 0.5 / self.data.get_bell_freq()  # uncorrected location
    #     self.xend = self.xend - self.end_correction()    # subtract end correction
    #     # subtract closed hole corrections
    #     for n in range(self.data.get_number_holes()):
    #         self.xend = self.xend - self.closed_correction(n)

    #     # find first finger hole location
    #     self.logger.debug("First hole location")
    #     X = self.vsound() * 0.5 / self.data.get_hole_freq(0)
    #     self.data.set_hole_location(0, 0)
    #     while True:
    #         oldX = self.data.get_hole_location(0)
    #         self.data.set_hole_location(0, X - self.first_correction())
    #         for n in range(1, self.data.get_number_holes()):
    #             self.data.set_hole_location(0, self.data.get_hole_location(0) - self.closed_correction(n))
    #         if math.fabs(self.data.get_hole_location(0) - oldX) < 0.0001:
    #             break

    #     # set subsequent finger hole locations
    #     self.logger.debug("other hole corrections")
    #     for holeNum in range(1, self.data.get_number_holes()):
    #         self.logger.debug("hole number: %d"%(holeNum))
    #         X = self.vsound() * 0.5 / self.data.get_hole_freq(holeNum)
    #         self.data.set_hole_location(holeNum, 0)
    #         while True:
    #             oldX = self.data.get_hole_location(holeNum)
    #             self.data.set_hole_location(holeNum, X - self.open_correction(holeNum))
    #             if holeNum <= self.data.get_number_holes():
    #                 for n in range(holeNum+1, self.data.get_number_holes()):
    #                     self.data.set_hole_location(holeNum, self.data.get_hole_location(holeNum) - self.closed_correction(n))

    #             if math.fabs(self.data.get_hole_location(0) - oldX) < 0.0001:
    #                 break

    #     # set embouchure hole location
    #     self.xemb = self.emb_correction()
    #     for n in range(self.data.get_number_holes()):
    #         self.data.set_hole_cutoff(n, self.cutoff(n))


# // This is a non-iterative procedure equivalent to the above procedure.  It involves use
# // of quadratic solutions of the Benade equations obtained by "simple but tedious algebraic
# // manipulation".
# def FindLocations2()
# {
#     var i;
#     var L;
#     var holeNum;
#     var a,b,c;


#     // find end location...
#     xend = vsound * 0.5 / base_freq;  // uncorrected location
#     xend = xend - end_correction();  // subtract end correction
#     for(i = 1; i <= num_holes; i++)
#         xend = xend - closed_correction(i);  // subtract closed hole corrections
#     //alert("Xend="+Xend)

#     // find first finger hole location
#     L = vsound * 0.5 / frequencies[1];
#     for(i = 2; i <= num_holes; i++)
#         L = L - closed_correction(i);  // subtract closed hole corrections
#     a = (hole_dias[1]/bore_dia)*(hole_dias[1]/bore_dia);
#     b = -(xend + L)*(hole_dias[1]/bore_dia)*(hole_dias[1]/bore_dia);
#     c = xend * L * (hole_dias[1]/bore_dia)*(hole_dias[1]/bore_dia) + eff_wall(1)*(L-xend);
#     //alert("eff_wall(1)="+eff_wall(1))
#     //alert("hole_dias[1]="+hole_dias[1]+"frequencies[1]="+frequencies[1]+" a="+a+" b="+b+" c="+c+" L="+L)
#     hole_locs[1] = ( -b - Math.sqrt((b*b) - 4*a*c) ) / (2*a);

#     // find subsequent finger hole locations
#     if(num_holes >= 2)
# 	for(holeNum=2;holeNum<=num_holes;holeNum++)
# 		{
# 		L = vsound * 0.5 / frequencies[holeNum];
# 		if (holeNum < num_holes)for(i=holeNum;i<=num_holes;i++) L = L - closed_correction(i);
# 		a = 2;
# 		b = - hole_locs[holeNum-1] - 3*L + eff_wall(holeNum)*(bore_dia/hole_dias[holeNum])*(bore_dia/hole_dias[holeNum]);
# 		c = hole_locs[holeNum-1]*(L - eff_wall(holeNum)*(bore_dia/hole_dias[holeNum])*(bore_dia/hole_dias[holeNum])) + (L*L);
# 		hole_locs[holeNum] = ( -b - Math.sqrt((b*b) - 4*a*c) ) / (2*a);
# 		}

#     // set embouchure hole location
#     xemb = emb_correction();
#     for(var i = 1; i <= num_holes; i++)
#         cutoff_freqs[i] = cutoff(i);
# }
