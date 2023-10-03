import matplotlib.pyplot as plt;
from main import *;

def hexadecimal(value):
    hex1 = hex(value);
    if len(hex1) == 3:
        return "0" + hex1[2:];
    else:
        return hex1[2:];

SAMPLING_SIZE = 100;
DX = round((INTERVALO[1] - INTERVALO[0])/SAMPLING_SIZE, 2);

abcissas = [];
ordenadas = [];

for i in range(0, SAMPLING_SIZE+1):
    x = INTERVALO[0] + i*DX;
    abcissas.append(x);
    ordenadas.append(round(funct_objetivo(x), 2));

plt.plot(abcissas, ordenadas);
plt.xlabel("x");
plt.ylabel("F(x)");
plt.title("Desafio 02 - Valor Mínimo com AG");

coordinates = graph_evolve();
c = 255/MAX_GERACOES;
tone = 0;
for point in coordinates:
    tone += c; 
    hex_color = hexadecimal(int(tone));
    gradient = "#00" + hex_color + hex_color;
    print(gradient);

    plt.scatter(point[0], point[1], color=gradient);

plt.show();