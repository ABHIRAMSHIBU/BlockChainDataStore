import pickle
import sys
print(pickle.loads(open(sys.argv[1],"rb").read()))
