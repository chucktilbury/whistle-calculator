import pickle
import sys
import pprint

if len(sys.argv) < 2:
    print("need file name")
    sys.exit()

with open(sys.argv[1], "rb") as fh:
    data = pickle.load(fh)
    pprint.pprint(data)
