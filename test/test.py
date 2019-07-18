import pickle
import os

baseDir = os.path.dirname(os.getcwd())
with open(os.path.join(baseDir, 'processedData', 'Trees.pkl'), 'rb') as Objwrite:
    Trees = pickle.load(Objwrite)
    tree = Trees[0]
    print(tree.host)
    print(tree.domain)
    print(tree.edges)
    print(tree.time2StrDict)