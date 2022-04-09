import numpy as np
import matplotlib.pyplot as plt

from malha import Malha
from frame import Frame
import config as conf
import toolbox as tb


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(f"{matrix[i][j]:.3f}", end = 5*" ")
        print()


def foo_temporaria_para_atualizar_phi_das_celulas(malha, valores):
    for i, lista in enumerate(malha.malha):
        for j, celula in enumerate(lista):
            celula.update_valores(valores[i*malha.ns2 + j])


def foo_temporaria_para_pegar_a_matriz_de_valores(malha, index):
    valores = np.zeros(shape = (malha.ns1, malha.ns2))
    for i, lista in enumerate(malha.malha):
        for j, celula in enumerate(lista):
            valores[i][j] = celula.valores[index]
    return valores


def foo_temporaria_para_plotar_a_matriz_de_valores(malha):
    plt.imshow(malha , cmap = 'autumn' , interpolation = 'nearest' )
  
    plt.title( "2-D Heat Map" )
    plt.show()



def main():
    dominio = [
        (0, conf.dimensao1),
        (0, conf.dimensao2),
        (conf.tempo_inicial, conf.tempo_simulacao)
    ]
    discretizacao = [
        conf.n_s1,
        conf.n_s2,
        conf.n_t
    ]
    malha = Malha(
        dominio = dominio,
        divisoes = discretizacao,
        tipo_problema = conf.tipo_problema,
        phi_0 = conf.temperatura_ini,
        geometria = conf.geometria
        )
  
    frame = Frame(conf.n_s1, conf.n_s2)
    malha.setup(frame = frame)
    
    
    for _ in range(conf.n_t):

        malha.gerar_sistema_linear()
    
        #Solve by modified TMDA 
        resp_tdma = tb.solve_linear_system(malha.coeficientes, malha.vetor_independente, malha.phi, malha.ns1)


        foo_temporaria_para_atualizar_phi_das_celulas(malha, resp_tdma)
        print(_)

    valores = foo_temporaria_para_pegar_a_matriz_de_valores(malha, conf.n_t)

    foo_temporaria_para_plotar_a_matriz_de_valores(valores)
    # for i in range(len(valores)):
    #     for j in range(len(valores[i])):
    #         print(f"{valores[i][j]:.3f}", end = 5*" ")
    #     print()



if __name__ == "__main__":
    main()