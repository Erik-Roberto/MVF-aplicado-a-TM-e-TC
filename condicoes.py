"""
Define as condições do problema
"""
from enum import Enum

class Condicoes(Enum):
    Interior = 0
    Tipo_1 = 1
    Tipo_2 = 2
    Tipo_3 = 3

cc_temperatura = {
    'Superior': (Condicoes.Tipo_1, 100), 
    'Inferior': (Condicoes.Tipo_1, 100), 
    'Direita':  (Condicoes.Tipo_1, 100), 
    'Esquerda': (Condicoes.Tipo_1, 100)
}

cc_concentracao = {
    'Superior': (Condicoes.Tipo_1, 100), 
    'Inferior': (Condicoes.Tipo_1, 100), 
    'Direita':  (Condicoes.Tipo_1, 100), 
    'Esquerda': (Condicoes.Tipo_1, 100)
}
