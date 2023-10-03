import sys;
sys.path.append("..");

from main import *;

coordinate = graph_evolve();
for each in coordinate:
    print(each);