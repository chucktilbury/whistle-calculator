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

    # values for each line
    'hole_values': [
        {
            'interval': 2,
            'note': 'E',
            'freq': 659.26,
            'hole_size': 1/4,
            'location': 0.0,
            'diff': 0.0,
            'cutoff':0.0},
        {
            'interval': 2,
            'note': 'F#',
            'freq': 739.99,
            'hole_size': 11/32,
            'location': 0.0,
            'diff': 0.0,
            'cutoff':0.0},
        {
            'interval': 1,
            'note': 'G',
            'freq': 783.99,
            'hole_size': 1/4,
            'location': 0.0,
            'diff': 0.0,
            'cutoff':0.0},
        {
            'interval': 2,
            'note': 'A',
            'freq': 880.0,
            'hole_size': 9/32,
            'location': 0.0,
            'diff': 0.0,
            'cutoff':0.0},
        {
            'interval': 2,
            'note': 'B',
            'freq': 987.77,
            'hole_size': 9/32,
            'location': 0.0,
            'diff': 0.0,
            'cutoff':0.0},
        {
            'interval': 2,
            'note': 'C#',
            'freq': 1108.73,
            'hole_size': 1/4,
            'location': 0.0,
            'diff': 0.0,
            'cutoff':0.0},
    ],

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