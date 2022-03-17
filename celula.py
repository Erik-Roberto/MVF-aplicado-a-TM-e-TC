import numpy as np

import interfaces as inter
import geometrias as geo
from condicoes import Condicoes
import propriedades as prop

class Celula:
    case_condicoes = {
        Condicoes.Tipo_1: inter.InterfaceCCTipo1,
        Condicoes.Tipo_2: inter.InterfaceCCTipo2,
        Condicoes.Tipo_3: inter.InterfaceCCTipo3,
    }

    def __init__(self, malha, phi_0, tipo_celula, geometria, tipo_problema,
                 pos, coordenadas, condicoes):
        """
        malha (objeto Malha): Malha que conterá as células
        phi_0 (float): Valor inicial de phi
        tipo_celula (int): Define se a célula está em borda, aresta ou interior do domínio
        tipo (int): Tipo da celula de acordo com a discretização (1-9)
        geometria (str): Geometria do problema (cilindrico ou cartesiano)
        tipo_problema (str): Define se o problema é de T.C ou T.M.
        pos (tuple): Posição do centro da célula
        coordenadas (tuple): Coordenadas da célula na malha
        condicoes (dict): Dicionário especificando as CC em contato com a célula
                         exemplo - {'norte': (Condicoes.Tipo_1, phi_f)}
        """
        self.malha = malha
        self.valores = [phi_0]
        self.tipo_celula = tipo_celula
        self.pos = pos
        self.coord = coordenadas
        self.condicoes = condicoes
        self.tipo_problema = tipo_problema
        self.geometria = geometria

    def setup(self):
        """ Inicializa as estruturas da célula
        """
        self.definir_propriedades()
        self.definir_geometria()
        self.definir_tipo()


    def calc_coefs(self):
        self.gama2 = self.calc_gama2()
        self.gama1 = self.calc_gama1()
        a_norte = self.norte.calc_anb()
        a_sul = self.sul.calc_anb()
        a_exterior = self.exterior.calc_anb()
        a_interior = self.interior.calc_anb()
        a_p = self.norte.calc_a() + self.sul.calc_a() + self.exterior.calc_a() + self.interior.calc_a()
        b = self.norte.calc_b() + self.sul.calc_b() + self.exterior.calc_b() + self.interior.calc_b()
        return (a_norte, a_sul, a_exterior, a_interior, a_p, b)


    def definir_propriedades(self):
        if self.tipo_problema.lower() == 'massa':
            self.propriedades = prop.PropMassa()
        elif self.tipo_problema.lower() == 'temperatura':
            self.propriedades = prop.PropTemperatura()
        else:
            raise ValueError("Tipo de probema inválido.")


    def definir_geometria(self):
        if self.geometria.lower() == 'cilindrico':
            dr = self.malha.ds1
            dz = self.malha.ds2
            r_ext = self.pos[0] + dr/2
            r_int = self.pos[0] - dr/2
            self.geo = geo.Cilindrico(dz, dr, r_ext, r_int)
        elif self.geometria.lower() == 'cartesiano':
            dx = self.malha.ds1
            dy = self.malha.ds2
            dz = self.malha.ds3
            self.geo = geo.Cartesiano(dx, dy, dz)
        else:
            raise ValueError("Geometria inválida.")


    def definir_tipo(self):
        linha = self.coord[0]
        coluna = self.coord[1]
        if self.tipo_celula == 1:
            # Vértice superior esquerdo
            condicao_norte = self.condicoes.get_condicao(coluna, "superior")
            norte = self.case_condicoes.get(condicao_norte[0])
            valor_cc_norte = condicao_norte[1]
            
            condicao_interior = self.condicoes.get_condicao(linha, "interior")
            interior = self.case_condicoes.get(condicao_interior[0])
            valor_cc_interior = condicao_interior[1]

            self.norte = norte(self, self.geo.ds2, self.geo.area_superior,
                                valor_cc_norte, tipo = 'saida')
            self.sul = self.sul_std()
            self.exterior = self.exterior_std()
            self.interior = interior(self, self.geo.ds1, self.geo.area_interna, 
                                     valor_cc_interior, tipo = 'entrada')
        elif self.tipo_celula == 2:
            # Vertice superior direito
            condicao_norte = self.condicoes.get_condicao(coluna, "superior")
            norte = self.case_condicoes.get(condicao_norte[0])
            valor_cc_norte = condicao_norte[1]
            
            condicao_exterior = self.condicoes.get_condicao(linha, "exterior")
            exterior = self.case_condicoes.get(condicao_exterior[0])
            valor_cc_exterior = condicao_exterior[1]

            self.norte = norte(self, self.geo.ds2, self.geo.area_superior,
                                valor_cc_norte, tipo = 'saida')
            self.sul = self.sul_std()
            self.exterior = exterior(self, self.geo.ds1, self.geo.area_externa,
                                     valor_cc_exterior, tipo = 'saida')
            self.interior = self.interior_std()
        elif self.tipo_celula == 3:
            # Vertice inferior esquerdo
            condicao_sul = self.condicoes.get_condicao(coluna, "inferior")
            sul = self.case_condicoes.get(condicao_sul[0])
            valor_cc_sul = condicao_sul[1]

            condicao_interior = self.condicoes.get_condicao(linha, "interior")
            interior = self.case_condicoes.get(condicao_interior[0])
            valor_cc_interior = condicao_interior[1]

            self.norte = self.norte_std()
            self.sul = sul(self, self.geo.ds2, self.geo.area_inferior,
                            valor_cc_sul, tipo = 'entrada')
            self.exterior = self.exterior_std()
            self.interior = interior(self, self.geo.ds1, self.geo.area_interna,
                                     valor_cc_interior, tipo = 'entrada')
        elif self.tipo_celula == 4:
            # Vertice inferior direito
            condicao_sul = self.condicoes.get_condicao(coluna, "inferior")
            sul = self.case_condicoes.get(condicao_sul[0])
            valor_cc_sul = condicao_sul[1]

            condicao_exterior = self.condicoes.get_condicao(linha, "exterior")
            exterior = self.case_condicoes.get(condicao_exterior[0])
            valor_cc_exterior = condicao_exterior[1]

            self.norte = self.norte_std()
            self.sul = sul(self, self.geo.ds2, self.geo.area_inferior,
                            valor_cc_sul, tipo = 'entrada')
            self.exterior = exterior(self, self.geo.ds1, self.geo.area_externa,
                                     valor_cc_exterior, tipo = 'saida')
            self.interior = self.interior_std()
        elif self.tipo_celula == 5:
            # Aresta superior
            condicao_norte = self.condicoes.get_condicao(coluna, "superior")
            norte = self.case_condicoes.get(condicao_norte[0])
            valor_cc_norte = condicao_norte[1]

            self.norte = norte(self, self.geo.ds2, self.geo.area_superior,
                                 valor_cc_norte, tipo = 'saida')
            self.sul = self.sul_std()
            self.exterior = self.exterior_std()
            self.interior = self.interior_std()
        elif self.tipo_celula == 6:
            # Aresta inferior
            condicao_sul = self.condicoes.get_condicao(coluna, "inferior")
            sul = self.case_condicoes.get(condicao_sul[0])
            valor_cc_sul = condicao_sul[1]

            self.norte = self.norte_std()
            self.sul = sul(self, self.geo.ds2, self.geo.area_inferior,
                             valor_cc_sul, tipo = 'entrada')
            self.exterior = self.exterior_std()
            self.interior = self.interior_std()
        elif self.tipo_celula == 7:
            # Aresta direita
            condicao_exterior = self.condicoes.get_condicao(linha, "exterior")
            exterior = self.case_condicoes.get(condicao_exterior[0])
            valor_cc_exterior = condicao_exterior[1]

            self.norte = self.norte_std()
            self.sul = self.sul_std()
            self.exterior = exterior(self, self.geo.ds1, self.geo.area_externa,
                                     valor_cc_exterior, tipo = 'saida')
            self.interior = self.interior_std()
        elif self.tipo_celula == 8:
            # Aresta esquerda
            condicao_interior = self.condicoes.get_condicao(linha, "interior")
            interior = self.case_condicoes.get(condicao_interior[0])
            valor_cc_interior = condicao_interior[1]

            self.norte = self.norte_std()
            self.sul = self.sul_std()
            self.exterior = self.exterior_std()
            self.interior = interior(self, self.geo.ds1, self.geo.area_interna,
                                     valor_cc_interior, tipo = 'entrada')
        elif self.tipo_celula == 9:
            # Volume interno
            self.norte = self.norte_std()
            self.sul = self.sul_std()
            self.exterior = self.exterior_std()
            self.interior = self.interior_std()
        else:
            raise ValueError("Tipo de célula não válido.")


    def norte_std(self):
        return inter.InterfaceDifusiva(self, self.geo.ds2, self.geo.area_superior)


    def sul_std(self):
        return inter.InterfaceDifusiva(self, self.geo.ds2, self.geo.area_inferior)


    def exterior_std(self):
        return inter.InterfaceDifusiva(self, self.geo.ds1, self.geo.area_externa)


    def interior_std(self):
        return inter.InterfaceDifusiva(self, self.geo.ds1, self.geo.area_interna)


    def calc_gama1(self):
        return self.propriedades.gama1()


    def calc_gama2(self):
        return self.propriedades.gama2()