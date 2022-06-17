

from discretizacao import Frame, Malha, Condicoes
import config as conf
import toolbox as tb


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(f"{matrix[i][j]:.3f}", end = 5*" ")
        print()




def frame_opcional(ns1, ns2):
    frame = Frame(ns1, ns2)
    borda_exterior = [
        {"pos":(0, 0.05/3), "tipo":Condicoes.Tipo_2, "valor": 1000},
        {"pos":(0.05/3, 2*0.05/3), "tipo":Condicoes.Tipo_2, "valor": 0},
        {"pos":(2*0.05/3, 0.05), "tipo":Condicoes.Tipo_2, "valor": 1000},
        ]

    borda_superior = [{"pos": (0, 0.075), "tipo": Condicoes.Tipo_2, "valor": 0}]
    borda_inferior = [{"pos": (0, 0.075), "tipo": Condicoes.Tipo_2, "valor": 0}]

    frame.definir_borda_exterior(borda_exterior)
    frame.definir_borda_superior(borda_superior)
    frame.definir_borda_inferior(borda_inferior)

    return frame

def caso_um():
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
  
    # frame = Frame(conf.
    # n_s1, conf.n_s2)
    frame = frame_opcional(conf.n_s1, conf.n_s2)
    malha.setup(frame = frame)
    

    eng = tb.Engine(malha)

    eng.calculate()

    #Plotando animação
    hm = tb.Heatmap(malha)
    hm.call_animation()


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

    malha_temperatura = Malha(
        dominio = dominio,
        divisoes = discretizacao,
        tipo_problema = "temperatura",
        phi_0 = conf.temperatura_ini,
        geometria = conf.geometria
        )
    
    malha_massa = Malha(
        dominio = dominio,
        divisoes = discretizacao,
        tipo_problema = "massa",
        phi_0 = conf.c_ini,
        geometria = conf.geometria
        )

    # Temperatura    
    frame_temperatura = Frame(conf.n_s1, conf.n_s2)
    borda_superior = [{"pos": (0, 0.075), "tipo": Condicoes.Tipo_1, "valor": 350}]
    borda_inferior = [{"pos": (0, 0.075), "tipo": Condicoes.Tipo_1, "valor": 273}]
    
    frame_temperatura.definir_borda_superior(borda_superior)
    frame_temperatura.definir_borda_inferior(borda_inferior)
    malha_temperatura.setup(frame = frame_temperatura)

    #Massa
    frame_massa = Frame(conf.n_s1, conf.n_s2)
    borda_superior = [{"pos": (0, 0.075), "tipo": Condicoes.Tipo_1, "valor": 5000}]
    borda_inferior = [{"pos": (0, 0.075), "tipo": Condicoes.Tipo_1, "valor": 1000}]
    
    frame_massa.definir_borda_superior(borda_superior)
    frame_massa.definir_borda_inferior(borda_inferior)
    malha_massa.setup(frame = frame_massa)
    

    eng = tb.Engine(grid_mass=malha_massa, grid_temperature=malha_temperatura)

    eng.solve_coupled()
    

    #Plotando animação
    hm = tb.Heatmap(malha_temperatura)
    hm.call_animation()


if __name__ == "__main__":
    main()