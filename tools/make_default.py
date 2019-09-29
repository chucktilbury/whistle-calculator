import pickle
import time

default_values = {
    'date_created':0.0,
    'date_modified':0.0,

    # upper section values
    'disp_frac': True,   # True if the holes are displayed in fractions
    'units': False,      # True if the units are mm and false if it's inch
    'title': "Default Whistle",
    'inside_dia': 0.5,
    'wall_thickness': 0.15,
    'number_holes': 6,
    'bell_note_select': 62,
    'bell_freq': 587.33,
    'embouchure_area': 1.2,

    'intervals': [2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2],
    'notes': ['E', 'F#', 'G', 'A', 'B', 'C#', '', '', '', '', '', ''],
    'freqs': [659.26, 739.99, 783.99, 880.0, 987.77, 1108.73, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'locations': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'diffs': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'cutoffs': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'hole_sizes': [1/4, 11/32, 1/4, 9/32, 9/32, 1/4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],

    # applies to all the holes
    'hole_in_inc': 1/64,
    'hole_in_max': 1/2,
    'hole_in_min': 3/16,
    'hole_mm_inc': 0.5,
    'hole_mm_max': 12.5,
    'hole_mm_min': 2.5,
}

default_values['date_created'] = time.time()
default_values['date_modified'] = time.time()

with open('default.wis', 'wb') as fp:
    pickle.dump(default_values, fp, protocol=pickle.HIGHEST_PROTOCOL)