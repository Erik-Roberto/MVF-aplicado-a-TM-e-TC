import numpy as np

import discretizacao.interfaces as inter
import discretizacao.geometrias as geo
from discretizacao.condicoes import Condicoes
import discretizacao.propriedades as prop


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
        self.valores = np.array([phi_0], dtype = float)
        self.phi_2 = 1
        self.tipo_celula = tipo_celula
        self.pos = pos
        self.coord = coordenadas
        self.condicoes = condicoes
        self.tipo_problema = tipo_problema
        self.geometria = geometria


    def __str__(self):
        text = f'\tnorte: {self.norte}\n'
        text += f'\tsul: {self.sul}\n'
        text += f'\tinterior: {self.interior}\n'
        text += f'\texterior: {self.exterior}\n'
        return text


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
        a0, b0 = self.calc_a0()
        a_p = a0 + self.norte.calc_a() + self.sul.calc_a() + self.exterior.calc_a() + self.interior.calc_a()
        b = b0 + self.norte.calc_b() + self.sul.calc_b() + self.exterior.calc_b() + self.interior.calc_b()
        return (a_norte, a_interior, a_p, a_exterior, a_sul, b)


    def calc_a0(self):
        a0 = 1/self.malha.dt
        b = self.valores[-1]/self.malha.dt
        return a0, b


    def update_valores(self, phi):
        self.valores = np.append(self.valores, phi)


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
            self.geo = geo.Cartesiano(dx, dy)
        else:
            raise ValueError("Geometria inválida.")


    def definir_tipo(self):
        linha = self.coord[0]
        coluna = self.coord[1]
        if self.tipo_celula == 1:
            # Vértice superior esquerdo
            self.tipo_celula_1(coluna, linha)

        elif self.tipo_celula == 2:
            # Vertice superior direito
            self.tipo_celula_2(coluna, linha)

        elif self.tipo_celula == 3:
            # Vertice inferior esquerdo
            self.tipo_celula_3(coluna, linha)

        elif self.tipo_celula == 4:
            # Vertice inferior direito
            self.tipo_celula_4(coluna, linha)

        elif self.tipo_celula == 5:
            # Aresta superior
            self.tipo_celula_5(coluna)

        elif self.tipo_celula == 6:
            # Aresta inferior
            self.tipo_celula_6(coluna)

        elif self.tipo_celula == 7:
            # Aresta direita
            self.tipo_celula_7(linha)

        elif self.tipo_celula == 8:
            # Aresta esquerda
            self.tipo_celula_8(linha)

        elif self.tipo_celula == 9:
            # Volume interno
            self.tipo_celula_9()

        else:
            raise ValueError("Tipo de célula não válido.")


    def tipo_celula_1(self, coluna, linha):
        # Vértice superior esquerdo
        condicao_norte = self.condicoes.get_condicao(coluna, "superior")
        norte = self.case_condicoes.get(condicao_norte[0])
        valor_cc_norte = condicao_norte[1]
        
        condicao_interior = self.condicoes.get_condicao(linha, "interior")
        interior = self.case_condicoes.get(condicao_interior[0])
        valor_cc_interior = condicao_interior[1]

        self.norte = norte(valor_cc_norte, self, self.geo.ds2,
                             self.geo.area_superior, tipo = 'saida')
        self.sul = self.sul_std()
        self.exterior = self.exterior_std()
        self.interior = interior(valor_cc_interior, self, self.geo.ds1,
                                     self.geo.area_interna, tipo = 'entrada')

    def tipo_celula_2(self, coluna, linha):
        # Vertice superior direito
        condicao_norte = self.condicoes.get_condicao(coluna, "superior")
        norte = self.case_condicoes.get(condicao_norte[0])
        valor_cc_norte = condicao_norte[1]
        
        condicao_exterior = self.condicoes.get_condicao(linha, "exterior")
        exterior = self.case_condicoes.get(condicao_exterior[0])
        valor_cc_exterior = condicao_exterior[1]

        self.norte = norte(valor_cc_norte, self, self.geo.ds2,
                             self.geo.area_superior, tipo = 'saida')
        self.sul = self.sul_std()
        self.exterior = exterior(valor_cc_exterior, self, self.geo.ds1,
                                 self.geo.area_externa,  tipo = 'saida')
        self.interior = self.interior_std()


    def tipo_celula_3(self, coluna, linha):
        # Vertice inferior esquerdo
        condicao_sul = self.condicoes.get_condicao(coluna, "inferior")
        sul = self.case_condicoes.get(condicao_sul[0])
        valor_cc_sul = condicao_sul[1]

        condicao_interior = self.condicoes.get_condicao(linha, "interior")
        interior = self.case_condicoes.get(condicao_interior[0])
        valor_cc_interior = condicao_interior[1]

        self.norte = self.norte_std()
        self.sul = sul(valor_cc_sul, self, self.geo.ds2,
                         self.geo.area_inferior,  tipo = 'entrada')
        self.exterior = self.exterior_std()
        self.interior = interior(valor_cc_interior, self, self.geo.ds1,
                                 self.geo.area_interna, tipo = 'entrada')
        

    def tipo_celula_4(self, coluna, linha):
        # Vertice inferior direito
        condicao_sul = self.condicoes.get_condicao(coluna, "inferior")
        sul = self.case_condicoes.get(condicao_sul[0])
        valor_cc_sul = condicao_sul[1]

        condicao_exterior = self.condicoes.get_condicao(linha, "exterior")
        exterior = self.case_condicoes.get(condicao_exterior[0])
        valor_cc_exterior = condicao_exterior[1]

        self.norte = self.norte_std()
        self.sul = sul(valor_cc_sul, self, self.geo.ds2,
                         self.geo.area_inferior, tipo = 'entrada')
        self.exterior = exterior(valor_cc_exterior, self, self.geo.ds1,
                                 self.geo.area_externa, tipo = 'saida')
        self.interior = self.interior_std()


    def tipo_celula_5(self, coluna):
        # Aresta superior
        condicao_norte = self.condicoes.get_condicao(coluna, "superior")
        norte = self.case_condicoes.get(condicao_norte[0])
        valor_cc_norte = condicao_norte[1]

        self.norte = norte(valor_cc_norte, self, self.geo.ds2,
                             self.geo.area_superior,  tipo = 'saida')
        self.sul = self.sul_std()
        self.exterior = self.exterior_std()
        self.interior = self.interior_std()


    def tipo_celula_6(self, coluna):
        # Aresta inferior
        condicao_sul = self.condicoes.get_condicao(coluna, "inferior")
        sul = self.case_condicoes.get(condicao_sul[0])
        valor_cc_sul = condicao_sul[1]

        self.norte = self.norte_std()
        self.sul = sul(valor_cc_sul, self, self.geo.ds2,
                         self.geo.area_inferior,  tipo = 'entrada')
        self.exterior = self.exterior_std()
        self.interior = self.interior_std()


    def tipo_celula_7(self, linha):
        # Aresta direita
        condicao_exterior = self.condicoes.get_condicao(linha, "exterior")
        exterior = self.case_condicoes.get(condicao_exterior[0])
        valor_cc_exterior = condicao_exterior[1]

        self.norte = self.norte_std()
        self.sul = self.sul_std()
        self.exterior = exterior(valor_cc_exterior, self, self.geo.ds1,
                                 self.geo.area_externa,  tipo = 'saida')
        self.interior = self.interior_std()


    def tipo_celula_8(self, linha):
         # Aresta esquerda
        condicao_interior = self.condicoes.get_condicao(linha, "interior")
        interior = self.case_condicoes.get(condicao_interior[0])
        valor_cc_interior = condicao_interior[1]

        self.norte = self.norte_std()
        self.sul = self.sul_std()
        self.exterior = self.exterior_std()
        self.interior = interior(valor_cc_interior, self, self.geo.ds1,
                                 self.geo.area_interna,  tipo = 'entrada')


    def tipo_celula_9(self):
        # Volume interno
        self.norte = self.norte_std()
        self.sul = self.sul_std()
        self.exterior = self.exterior_std()
        self.interior = self.interior_std()


    def norte_std(self):
        return inter.InterfaceDifusiva(self, self.geo.ds2, self.geo.area_superior)


    def sul_std(self):
        return inter.InterfaceDifusiva(self, self.geo.ds2, self.geo.area_inferior)


    def exterior_std(self):
        return inter.InterfaceDifusiva(self, self.geo.ds1, self.geo.area_externa)


    def interior_std(self):
        return inter.InterfaceDifusiva(self, self.geo.ds1, self.geo.area_interna)


    def calc_gama1(self):
        return self.propriedades.gama1(self.phi_2, self.valores[-1])


    def calc_gama2(self):
        return self.propriedades.gama2(self.phi_2, self.valores[-1])