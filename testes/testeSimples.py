import sys;
sys.path.append("..");

from main import *;

print("------------- Teste Geral");
best = evolve_DEBUG();
apresentar_melhorEscolha(best);