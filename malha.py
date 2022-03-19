from matplotlib.pyplot import text
import numpy as np

from celula import Celula
from condicoes import Condicoes
from frame import Frame 


class Malha:
    def __init__(self, dominio, divisoes, tipo_problema, phi_0, geometria):
        """ 
        dominio (lista): Pares de valores contendo as dimensões de cada direção
        (ultima posição para o tempo)
        Cilindro:      raio       z       tempo
                     [(0,100), (0,200), (0, 1800)]
        Cartesiano:      x        y       tempo
        divisoes (lista): Número de volumes em cada direção.
        Exemplo - [100, 200, 1800] (ultm. p/ o tempo)
        tipo_problema (str): Define se o problema é de T.M. ou T.C.
        phi_0 (float): Valor inicial da propriedade
        geometria (str): Geometria do problema (cilindrico ou cartesiano)
        """
        self.ns1 = divisoes[0] # R / x
        self.ns2 = divisoes[1] # z / y
        self.nt = divisoes[2]
        self.dominio = dominio
        self.phi_0 = phi_0
        self.geometria = geometria
        self.tipo_problema = tipo_problema
        self.malha = []


    def __str__(self):
        text = ""
        for lista in self.malha:
            for celula in lista:
                text += f"celula {celula.coord}: {celula.__str__()}"    
        return text


    def setup(self, frame = None):
        self.discretizar_dominio()
        self.definir_cc(frame)
        self.gerar_malha()


    def switcher(self, i, j):
        if i == 0:
            if j == 0: # Vértice superior esquerdo
                tipo = 1
            elif j == (self.ns1 - 1): # Vértice superior direito
                tipo = 2
            else: # Aresta superior
                tipo = 5
        elif i == (self.ns2 - 1):
            if j == 0: # Vértice inferior esquerdo
                tipo = 3
            elif j == (self.ns1 - 1): # Vértice inferior direito
                tipo = 4
            else: # Aresta inferior
                tipo = 6
        else:
            if j == 0: # Aresta esquerda
                tipo = 8
            elif j == (self.ns1 - 1): # Aresta direita
                tipo = 7
            else: # Volumes internos
                tipo = 9
        return tipo

        
    def definir_cc(self, frame):
        if not frame:
            frame = Frame(self.ns1, self.ns2)
        self.condicoes = frame


    def gerar_malha(self):
        for i in range(self.ns2): # linhas
            self.malha.append([])
            for j in range(self.ns1): #colunas
                tipo = self.switcher(i, j)
                pos1 = (self.s1[j+1] + self.s1[j])
                pos2 = (self.s2[i+1] + self.s2[i])
                celula = Celula(self,
                                self.phi_0,
                                tipo,
                                self.geometria,
                                self.tipo_problema,
                                (pos1, pos2),
                                (i, j),
                                self.condicoes)
                celula.setup()
                self.malha[i].append(celula)
            

    def discretizar_dominio(self):
        self.ds1 = (self.dominio[0][1] - self.dominio[0][0])/self.ns1
        self.ds2 = (self.dominio[1][1] - self.dominio[1][0])/self.ns2
        self.dt = (self.dominio[2][1] - self.dominio[2][0])/self.nt

        self.s1 = np.linspace(self.dominio[0][0],
                              self.dominio[0][1],
                              self.ns1 + 1)
        self.s2 = np.linspace(self.dominio[1][0],
                              self.dominio[1][1],
                              self.ns2 + 1)
        self.t = np.linspace(self.dominio[2][0],
                             self.dominio[2][1],
                             self.nt)

