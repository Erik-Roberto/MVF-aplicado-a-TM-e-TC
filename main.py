from malha import Malha
from frame import Frame
import config as conf



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
    print(malha)

if __name__ == "__main__":
    main()