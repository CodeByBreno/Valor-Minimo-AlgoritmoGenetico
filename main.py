# Valor Mínimo de uma Função através de um Algoritmo Genético
# Desafio 2 para Disciplina de Inteligência Artificial - 2023.1
# Feito por: Breno Gabriel de Souza Coelho | Turma 2019.2
# Apresentado em ......

import random;

INTERVALO = [-10, 10];
TAM_MAX_POPULACAO = 8;
TAXA_MUTACAO = 0.15;
TAXA_CROSSOVER_MIN = 0.6;
TAXA_CROSSOVER_MAX = 0.6;
MAX_GERACOES = 100;
PRECISION = 100;

def funct_objetivo(x):
    return x**2 - 3*x + 4;

def binario(x):
    bin1 = bin(x);

    append = 0;
    if bin1[0] == '-':
        append = 1;
    
    start = bin1[0:2+append]; 
    new_bin = bin1[2+append:];

    while (len(new_bin) != 10):
        new_bin = "0" + new_bin;

    return start + new_bin;

class Cromossomo():
    def __init__(self, genot, nota=0):
        self.genotipo = genot;
        self.fenotipo = binario(int(genot*PRECISION)); # Como o número pode ter vírgulas, vc vai ter que modificar isso aqui
        self.nota = nota;
        self.value = round(funct_objetivo(self.genotipo),2);
    
    def __str__(self):
        return ("Cromossomo G=" + str(self.genotipo) + " Bin=" + str(self.fenotipo) + " N=" + str(self.nota) + " V=" + str(round(self.value, 2)));

    def avaliar(self): 
        # Nesse caso, o teste de aptidão pode ser a própria função objetivo
        self.nota = round(100/funct_objetivo(self.genotipo), 2);

def evolve():
    populacao = create_population();
    avaliar(populacao);
    
    for i in range(0, MAX_GERACOES):
        geradores = selecionar(populacao, "TORNEIO");
        populacao = [];
        
        while len(populacao) < TAM_MAX_POPULACAO:
            novos_individuos = crossover(geradores[0], geradores[1]);

            for indiv in novos_individuos:
                populacao.append(mutate(indiv));

        avaliar(populacao);

    return melhorEscolha(populacao);

def graph_evolve():
    coordinates = [];
    populacao = create_population();
    avaliar(populacao);
    
    for i in range(0, MAX_GERACOES):
        geradores = selecionar(populacao, "ROLETA");
        populacao = [];
        
        while len(populacao) < TAM_MAX_POPULACAO:
            novos_individuos = crossover(geradores[0], geradores[1]);

            for indiv in novos_individuos:
                populacao.append(mutate(indiv));

        avaliar(populacao);
        best = melhorEscolha(populacao);
        coordinates.append((best.genotipo, best.value));
    return coordinates;

def evolve_DEBUG():
    populacao = create_population();
    avaliar(populacao);

    print("================================================================================================");
    print("População Inicial")
    for each in populacao:
        print (each);
    
    for i in range(0, MAX_GERACOES):
        geradores = selecionar(populacao, "ROLETA");

        print("\nSELECIONADOS PARA REPRODUÇÃO: ");
        for each in geradores:
            print(each);
        
        populacao = [];
        
        while len(populacao) < TAM_MAX_POPULACAO:
            novos_individuos = crossover(geradores[0], geradores[1]);

            print("\nRESULTADO DO CROSSOVER:");
            for each in novos_individuos:
                print(each);
            
            for indiv in novos_individuos:
                populacao.append(mutate(indiv));
            
            print("\nRESULTADO DA MUTACAO:");
            for each in populacao:
                print(each)

        avaliar(populacao);
        print("========================")
        print("Geração " + str(i));
        for each in populacao:
            print(each);

    return melhorEscolha(populacao);

def melhorEscolha(populacao) -> 'Cromossomo':
    best = populacao[0];
    for each in populacao:
        if each.nota > best.nota:
            best = each;
    return best;

def apresentar_melhorEscolha(best : 'Cromossomo'):
    print("O melhor valor de 'x' encontrado é x = " + str(best.genotipo));
    print("O valor da função para esse 'x' é y = " + str(best.value));

def create_population() -> list['Cromossomo']:
    first_population = [];
    for i in range(0, TAM_MAX_POPULACAO):
        rand = random.randint(-10*PRECISION, 10*PRECISION);
        children = Cromossomo(round(rand/PRECISION,2));
        first_population.append(children);
    
    return first_population;

def avaliar(populacao: list['Cromossomo']) -> None:
    for each in populacao:
        each.avaliar();

def selecionar(populacao : list['Cromossomo'], metodo : str) -> tuple['Cromossomo']:
    if metodo == 'TORNEIO':
        selecionados = torneio_selecao(populacao);

    elif metodo == 'ROLETA':
        selecionados = roleta_selecao(populacao);

    return selecionados;

def torneio_selecao(populacao: list['Cromossomo']) -> tuple['Cromossomo']:
    ganhadores = [];
    while len(ganhadores) != 2:
        while len(populacao) != 0:
            g1 = random.choice(populacao);
            populacao.remove(g1);
            g2 = random.choice(populacao);
            populacao.remove(g2);
            if (g1.nota >= g2.nota):
                ganhadores.append(g1);
            else:
                ganhadores.append(g2);

        for each in ganhadores: 
            populacao.append(each);
    
    return ganhadores;

def roleta_selecao(populacao: list['Cromossomo']) -> tuple['Cromossomo']:
    selecionados = [];
    # Sorteia dois números aleatórios e escolhe 2 filhos de acordo com o valor desses números
    # a chance de escolha de cada, baseada na probabilidade relativa à sua aptidão
    removed = 0;
    while len(populacao) != 2:
        base = 0;
        total = 0;

        # Calcula o total da base de escolha
        for each in populacao:
            total += int(each.nota*PRECISION);
        
        rand = random.randint(0, int(total));
        print("Sorteio=" + str(rand) + " TOTAL=" + str(total));
        for i in range(0, TAM_MAX_POPULACAO - removed):
            print("INTERVALO " + str(i) + " = [" + str(base) + ", " + str(int(populacao[i].nota*PRECISION + base)) + "]");
            if (rand < int(populacao[i].nota*PRECISION + base) and rand > base):
                selecionados.append(populacao.pop(i));
                removed += 1;
                break;
            base += int(populacao[i].nota*PRECISION);
    
    return selecionados;
    
def crossover(g1 : 'Cromossomo', g2 : 'Cromossomo') -> tuple['Cromossomo']:
    bin1 = g1.fenotipo;
    bin2 = g2.fenotipo;
    c1 = c2 = 0;

    # Se houver um '-' no número, ele será considerado adequadamente no corte
    if bin1[0] == '-':
        c1 = 1;
    if bin2[0] == '-':
        c2 = 1;

    rand = random.randint(int(TAXA_CROSSOVER_MIN*100),int(TAXA_CROSSOVER_MAX*100))//10;
    bin1_part1 = bin1[0:rand+2+c1];
    bin1_part2 = bin1[rand+2+c1:];
    bin2_part1 = bin2[0:rand+2+c2];
    bin2_part2 = bin2[rand+2+c2:];
    #debug_crossover(g1, g2, rand, bin1_part1, bin1_part2, bin2_part1, bin2_part2);
    r1 = Cromossomo(int(bin1_part1+bin2_part2, 2)/PRECISION);
    r2 = Cromossomo(int(bin2_part1+bin1_part2, 2)/PRECISION);

    return (r1, r2);

def mutate(g1 : 'Cromossomo') -> 'Cromossomo':
    bin1 = '';

    if g1.fenotipo[0] == '-':
        bin1 = "-0b";
        base = 3;
    else:
        bin1 = "0b";
        base = 2;
    
    for i in range(base, len(g1.fenotipo)):
        rand = random.randint(0, 100);
        if rand < TAXA_MUTACAO*100:
            bin1 = bin1 + inverter_bit(g1.fenotipo[i]);
        else:
            bin1 = bin1 + g1.fenotipo[i];

    r1 = Cromossomo(int(bin1, 2)/PRECISION);
    return r1;

def debug_crossover(g1, g2, rand, bin1_part1, bin1_part2, bin2_part1, bin2_part2):
    print(g1);
    print(g2);
    print(rand);
    print(bin1_part1);
    print(bin1_part2);
    print(bin2_part1);
    print(bin2_part2);
    print(int(bin1_part1+bin2_part2,2));
    print(int(bin2_part1+bin1_part2,2));

def inverter_bit(bit):
    if bit == "0":
        return "1";
    else:
        return "0";