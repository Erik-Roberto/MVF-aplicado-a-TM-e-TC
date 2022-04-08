import numpy as np

from malha import Malha
from frame import Frame
import config as conf
import toolbox as tb


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(f"{matrix[i][j]:.3f}", end = 5*" ")
        print()

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
    malha.gerar_sistema_linear()
    
    print("A")

    # #Solve by TMDA modified
    # resp_tmda = tb.solve_linear_system(malha.coeficientes, malha.vetor_independente, malha.phi, malha.ns1)
    
    # print_matrix(malha.coeficientes)

    # print(malha.vetor_independente)
    
    # for i in range(len(resp_np)):
    #     print(f"{resp_np[i]:.3f}", f"{resp_tmda[i]:.3f}")


if __name__ == "__main__":
    main()