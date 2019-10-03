import math
import sys

vsound = 13584.0
nholes = 6
bore = 0.5
wall = 0.015

holes = [0.0, 1/4, 11/32, 1/4, 9/32, 9/32, 1/4]
# first entry is the bell freq
hfreqs = [587.33, 659.26, 739.99, 783.99, 880.0, 987.77, 1108.73]

bhlocs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
hlocs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
diffs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
cutoffs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
rcutoffs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# this value changes the output quite a bit...
# it moves the holes about 0.06 toward the bell
# this may be useful as a tuning tweak mechanism
chimney = 0.75  # 0.62133

ecorr = 0.25
windL = 0.175
windW = 0.375


def closedCorrection(index):
    b = bore
    holeSize = holes[index]
    p = (holeSize / b) * (holeSize / b)
    retv = (wall * p) / 4.0
    return retv


def effectiveThickness(index):
    return wall + (chimney * holes[index])


def embouchureCorrection():
    #embarea = windowlen * windowwid; embarea *= 6.4516;
    embArea = (windW * windL * 2 * math.pi)
    embRadius = math.sqrt(embArea / math.pi)

    # embdist = 3.14159265F * Embcorr * Cfg.borecent * Cfg.borecent / embarea * (Cfg.thickcent
    # + 1.5F * (double) sqrt( (double) (embarea / 3.14159265F)));
    embDist = ((math.pi * bore * bore * ecorr) / embArea)
    ccc = ((wall + 1.5 * embRadius))
    embDist = embDist * ccc
    sys.stdout.write("emb corretion = %f\n" % (embDist))
    return embDist


def holeSpacing(index):
    holeSpacing = 0.0
    if (index > 0):
        holeSpacing = hlocs[index-1] - hlocs[index]
    return holeSpacing


def endCorrection():
    return 0.6133 * bore / 2  # original flutomat


def firstHoleDistance(index):
    # // Cfg.open[1] = Cfg.height[1] /
    # // ((double) pow((double) (Cfg.diacent[1]/Cfg.borecent), 2.0) +
    # // Cfg.height[1] * (1.0F / Cfg.hs[1]));
    # final double bore = hole.whistle.bore;
    pow = (holes[index] / bore) * (holes[index] / bore)
    holeSp = holeSpacing(index)
    e = effectiveThickness(index)
    q = e * (1 / holeSp)
    r = pow + q
    openCorrection = e / r
    return openCorrection


def subsequentHoleDistance(index):
    # // Cfg.open[n] = Cfg.hs[n] * 0.5F *
    # // ( (double) sqrt((double) 1.0F + 4.0F * Cfg.height[n] / Cfg.hs[n] *
    # // (double) pow((double) (Cfg.borecent / Cfg.diacent[n]), 2.0)) - 1.0F);
    # final double bore = hole.whistle.bore;

    a = bore / holes[index]
    b = a * a
    holeSp = holeSpacing(index)
    c = 4.0 * effectiveThickness(index) / holeSp * b
    d = math.sqrt(1.0 + c)
    openCorrection = holeSp * 0.5 * (d - 1.0)
    return openCorrection


def cutoffFrequency(index):
    dist = hlocs[index-1] - hlocs[index]
    sqrtTerm = math.sqrt(effectiveThickness(index) * dist)
    ratio = vsound / (2 * math.pi)
    ratio = ratio * (holes[index] / bore)
    ratio = ratio / sqrtTerm
    return ratio


MAX_DELTA = 0.0001
MAX_LOOP = 12


def calculateIterative():
    # Calculate position of end hole
    xEnd = vsound / (2 * hfreqs[0])
    xEnd = xEnd - endCorrection()
    for i in range(1, len(holes)):
        xEnd = xEnd - closedCorrection(i)
    hlocs[0] = xEnd

    # find first finger hole location
    nominalPosition = vsound / (2 * hfreqs[1])
    hlocs[1] = 0.0
    delta = 10.0

    for i in range(MAX_LOOP):
        oldPosition = hlocs[1]
        hlocs[1] = nominalPosition - firstHoleDistance(1)

        for h in range(2, len(hlocs)):
            hlocs[1] -= closedCorrection(h)

        delta = math.fabs(hlocs[1] - oldPosition)
        if delta < MAX_DELTA:
            break

    # set subsequent finger hole locations
    for holeNum in range(2, len(hlocs)):
        # final Hole hole = whistle.hole[holeNum]
        nominalPosition = vsound / (2 * hfreqs[holeNum])
        hlocs[holeNum] = 0.0
        delta = 10.0
        for i in range(MAX_LOOP):
            oldPosition = hlocs[holeNum]
            hlocs[holeNum] = nominalPosition - subsequentHoleDistance(holeNum)
            for h in range(holeNum+1, len(hlocs)):
                hlocs[holeNum] -= closedCorrection(h)

            delta = math.fabs(hlocs[holeNum] - oldPosition)

    embouchureCorrection()
    for holeNum in range(1, len(hlocs)):
        cutoffs[holeNum] = cutoffFrequency(holeNum)
        rcutoffs[holeNum] = cutoffs[holeNum] / hfreqs[holeNum]
        bhlocs[holeNum] = hlocs[0] - hlocs[holeNum]


def calculateQuadratic():
        # Calculate position of end hole
    xEnd = vsound / (2 * hfreqs[0])
    xEnd = xEnd - endCorrection()

    for i in range(1, len(holes)):
        xEnd -= closedCorrection(i)
    hlocs[0] = xEnd

    # Calculate the position of the first tone hole
    length = vsound / (2 * hfreqs[1])
    for i in range(2, len(holes)):
        length = length - closedCorrection(i)

    a = holes[1] / bore
    a = a * a
    b = -(xEnd + length) * a
    c = (xEnd * length) * a
    c += effectiveThickness(1) * (length - xEnd)
    hlocs[1] = (-b - math.sqrt((b * b) - (4 * a * c))) / ((2 * a))

    # find subsequent finger hole locations
    for holeNum in range(2, len(holes)):
        length = vsound / (2.0 * hfreqs[holeNum])
        for i in range(holeNum + 1, len(holes)):
            length = length - closedCorrection(i)

        a = 2
        ratio = bore / holes[holeNum]
        ratio = ratio * ratio * effectiveThickness(holeNum)

        prevHole = hlocs[holeNum - 1]

        b = -prevHole - (3.0 * length)
        b = b + ratio
        c = length - ratio
        c = c * prevHole
        c = c + length * length
        hlocs[holeNum] = (-b - math.sqrt((b * b) - (4 * a * c))) / ((2 * a))

    embouchureCorrection()
    for holeNum in range(1, len(holes)):
        cutoffs[holeNum] = cutoffFrequency(holeNum)
        rcutoffs[holeNum] = cutoffs[holeNum] / hfreqs[holeNum]
        bhlocs[holeNum] = hlocs[0] - hlocs[holeNum]


calculateQuadratic()
print("first run")
print("\tbhlocs: \t", bhlocs)
print("\thlocs:  \t", hlocs)
print("\tcutoffs:\t", cutoffs)
print("\trcutoffs:\t", rcutoffs)


bhlocs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
hlocs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
diffs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
cutoffs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
rcutoffs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

calculateIterative()
print("second run")
print("\tbhlocs: \t", bhlocs)
print("\thlocs:  \t", hlocs)
print("\tcutoffs:\t", cutoffs)
print("\trcutoffs:\t", rcutoffs)
