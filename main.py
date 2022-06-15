import colorama

from discretizacao import Frame, Malha
import config as conf
import toolbox as tb


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(f"{matrix[i][j]:.3f}", end = 5*" ")
        print()


def progress_bar(progress, total):
    color = colorama.Fore.GREEN
    percent = 100 * (progress / total)
    bar = "█"*int(percent) + "-"*(100 - int(percent))
    if percent == 100:
        print(color + f"\r|{bar}| {percent: .2f}%", end="\n")
    else:
        print(color + f"\r|{bar}| {percent: .2f}%", end="\r")
    

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
  
    frame = Frame(conf.
    n_s1, conf.n_s2)
    malha.setup(frame = frame)
    

    colorama.init()
    for _ in range(conf.n_t):
        malha.gerar_sistema_linear()
        #Solve by modified TMDA 
        resp_tdma = tb.solve_linear_system(malha.coeficientes, malha.vetor_independente, malha.phi, malha.ns1)
        malha.atualizar_celulas(resp_tdma)
        progress_bar(_, conf.n_t-1)
    colorama.Style.RESET_ALL

    #Plotando animação
    hm = tb.Heatmap(malha)
    hm.call_animation()


if __name__ == "__main__":
    main()