import sys;
sys.path.append("..");

from main import *;

str1 = "-0b110";
str2 = "00101";
print("String = " + str(int(str1+str2, 2)));

teste = Cromossomo(5, 2);

population = create_population();
avaliar(population);

for each in population:
    print(each);

print("------------ SELEÇÃO");
selecao = selecionar(population, "ROLETA");
for each in selecao:
    print(each);

print("------------ CROSS-OVER");
cross_reprod = crossover(selecao[0], selecao[1])
for each in cross_reprod:
    print(each);

print("---------------- Mutação");
for each in cross_reprod:
    print(mutate(each));