// inputs
var maxHoleCount = 12;              // Number of flute finger holes
var holeCount = 7;                  // Number of flute finger holes
var fhDs = new Array(maxHoleCount+1); // finger hole diameters
var actEmbD;                        // physical embouchure hole diameter
var adjEmbD;                        // embouchure hole diameter, adusted for lip cover
var borD;                           // inside diameter of tube
var walW;                           // wall thickness of tube
var fhFs = new Array(maxHoleCount+1); // finger hole note frequencies
var endF;                           // all-holes-closed end-of-flute frequency

// raw results (distances from "beginning of air column" which is actually undefined)
var endX;                           // effective location of end of flute
var fhXs = new Array(maxHoleCount+1); // location of finger holes
var embX;                           // location of embouchure

var inMm = 25.4;                    // inches to mm
var sVMmS = 345000.0;                 // velocity of sound in mm/s
var unitMult = 1.0;                 // units multiplier (1 = mm)
var decPl = 1;                      // units decimal places
var firstLoad = true;

// effective wall thickness, i.e. height of air column at open finger holes;
// air column extends out past end of hole 3/4 of the hole diameter
function effWalW(holeNum) {
  return walW + 0.75 * fhDs[holeNum];
}

// Closed hole for tone hole n.  The length of the vibrating air column is
// effectively increased by each closed tone hole which exists above the
// first open tone hole. Corrections must be added for each such closed tone
// tone hole to endCorr, openFH1Corr, and openFHCorr.
function closedFHCorr(holeNum) {
  var fhBorRatio = fhDs[holeNum] / borD;
  return 0.25 * walW * fhBorRatio * fhBorRatio;
}

// Calculates the distance from physical open end of flute to effective end of
// vibrating air column.  The vibrating air column ends beyond the end of the
// flute and endCorr is always positive. NOTE: Closed hole corrections must be added to
// this value!
function endCorr() {
  return 0.30665 * borD;
}

// Calculates the effective distance from the first ("single") tone hole to
// the end of the vibrating air column when only that hole is open.
// NOTE: closed hole corrections must be added to this value!
function openFH1Corr() {
  var borFh1Ratio = borD / fhDs[1];
  return  (endX - fhXs[1]) * borFh1Ratio * borFh1Ratio;
}

// Calculates the effective distance from the second and subsequent tone holes
// to the end of the vibrating air column when all holes below are open.
// NOTE: closed hole corrections must be added to this value!
// NOTE: the value of this correction is invalid if the frequency of the note
// played is above the cutoff frequency cutoffForHole.
function openFHCorr(n) {
  var borFhRatio = borD / fhDs[n];
  var fhXsDiff = fhXs[n-1] - fhXs[n];
  return 0.25 * fhXsDiff
    * (Math.sqrt(1 +  4 * borFhRatio * borFhRatio * effWalW(n) / fhXsDiff) -  1);
}

// embCorr = distance from theoretical start of air column to center of embouchure hole;
// the air column effectively extends beyond the blow hole center by this distance.
// (the cork face should be about 1 to 1.5 embouchure diameters from emb. center)
//embCorr := borEmbRatio*borEmbRatio*(walW+0.75*adjEmbD); // per spreadsheet
//embCorr := borEmbRatio*borEmbRatio*(borD/2 + walW + 0.6133*adjEmbD/2); // an alternative
//embCorr := 10.84*borEmbRatio*borEmbRatio*walW*adjEmbD/(borD + 2*walW); // kosel's empirical fit
function embCorr() {
  var borEmbRatio = borD / adjEmbD;
  //return borEmbRatio * borEmbRatio * (walW + 0.75 * adjEmbD); // per spreadsheet
  return borEmbRatio * borEmbRatio * (borD / 2 + walW + 0.6133 * adjEmbD / 2); // an alternative
  //return borEmbRatio * borEmbRatio * (walW + 1.7 * adjEmbD); // http://www.phy.mtu.edu/~suits/fingers.html
  //return 10.84 * borEmbRatio * borEmbRatio * walW * adjEmbD / (borD + 2 * walW); // kosel's empirical fit
}

// Calculates the cutoff frequency above which the open hole correction
// is not valid.  Instrument should be designed so that all second register
// notes are well below this frequency.
function cutoffForHole(n) {
  if (n == 1)
    fhXsDiff = endX - fhXs[1];
  else
    fhXsDiff = fhXs[n-1] - fhXs[n];
  return 0.5 * sVMmS * fhDs[n] / (Math.PI * borD * Math.sqrt(effWalW(n) * fhXsDiff));
}

// This procedure finds the locations of end of flute, all finger holes, and emb. hole
// This involves use
// of quadratic solutions of the Benade equations obtained by "simple but tedious algebraic
// manipulation".
function findLocations2() {
  var i;
  var L;
  var holeNum;
  var a,b,c;

// find end location...
  endX = sVMmS * 0.5 / endF;  // uncorrected location
  endX = endX - endCorr();  // subtract end correction
  for (i=1; i<=holeCount; i++)
    endX = endX - closedFHCorr(i);  // subtract closed hole corrections

// find first finger hole location
  var halfWl = sVMmS * 0.5 / fhFs[1];
  for (i=2; i<=holeCount; i++)
    halfWl -= closedFHCorr(i);  // subtract closed hole corrections
  var fhBorRatio = fhDs[1] / borD;
  var a = fhBorRatio * fhBorRatio;
  var b = -(endX + halfWl) * a;
  var c = endX * halfWl * a + effWalW(1) * (halfWl - endX);
  fhXs[1] = (-b - Math.sqrt((b * b) - 4 * a * c) ) / (2 * a);

// find subsequent finger hole locations
  if (holeCount >= 2) {
    for (holeNum = 2; holeNum <= holeCount; holeNum++) {
      halfWl = 0.5 * sVMmS / fhFs[holeNum];
      if (holeNum < holeCount)
        for (i = holeNum; i <= holeCount; i++)
          halfWl -= closedFHCorr(i);
      a = 2;
      var borFhRatio = borD / fhDs[holeNum];
      var holeCalc = effWalW(holeNum) * borFhRatio * borFhRatio;
      b = -fhXs[holeNum - 1] - 3 * halfWl + holeCalc;
      c = fhXs[holeNum - 1] * (halfWl - holeCalc) + (halfWl * halfWl);
      fhXs[holeNum] = (-b - Math.sqrt((b * b) - 4 * a * c)) / (2 * a);
    }
  }

// set embouchure hole location
  embX = embCorr();
}

