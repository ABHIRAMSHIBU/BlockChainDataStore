import pickle
import sys
from pprint import pprint
pprint(pickle.loads(open(sys.argv[1],"rb").read()))
